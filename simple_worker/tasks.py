from celery import Celery
import PyPDF2
import os
import base64
import requests
import time

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

app = Celery('tasks',broker='amqp://admin:mypass@rabbit:5672',backend='rpc://')

#task to store and extract text data from pdf using PyPDF2
@app.task
def store_and_extract_text_from_pdf(file_path, file_content_bytes , output_type):


    # Store the PDF file
    file_content_bytes=base64.b64decode(file_content_bytes["__value__"])
    with open(file_path, 'wb') as f:
        f.write(file_content_bytes)

    # Extract text from the PDF file
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    pdf_file_obj.close()

    # Return the extracted text
    logger.info(output_type)
    output_result ={
            "status":"SUCCESS",
            "result":text
        }
    if (output_type == 'polling'):
        return output_result
    elif (output_type == 'webhook'):
        response = requests.post("http://host.docker.internal:8080/webhook-get-task/", json=output_result)
        return "Task sent successfully"
    else:
        response = requests.post("http://host.docker.internal:8080/webhook-get-task/", json=output_result)
        return output_result
    
#task to delete file from the server
@app.task
def delete_file(file_path):
    time.sleep(5)
    if os.path.exists(file_path):
        os.remove(file_path)
        return "File deleted successfully"
    else:
        return "The file does not exist"