from fastapi import FastAPI,UploadFile,File,Form
from pydantic import BaseModel
from celery import Celery
from celery.result import AsyncResult
import os

simple_app=Celery('simple_worker' ,broker='amqp://admin:mypass@rabbit:5672',
                  backend='rpc://')

app = FastAPI()

class TaskResult(BaseModel):
    status:str
    result:str


@app.get("/")
def read_root():
    return {"Hello": "World"}


# FastAPI endpoint
@app.post("/upload-file/{output_type}")
async def upload_file(output_type : str , file: UploadFile = File(...)):
    try:
        # Check if the file is a PDF
        _, extension = os.path.splitext(file.filename)
        if extension.lower() != ".pdf":
            return {"error": "File is not a PDF"}
        
        # Get path and content
        file_path = f"uploaded_files/{file.filename}"
        file_content = await file.read()

        # Initiate tasks
        store_extract_result = simple_app.send_task('tasks.store_and_extract_text_from_pdf', kwargs={'file_path': file_path ,'file_content_bytes': file_content , 'output_type' : output_type })
        delete_result = simple_app.send_task('tasks.delete_file', kwargs={'file_path': file_path})

        return {"store_extract_task_id": store_extract_result.id , "delete_task_id": delete_result.id}
    except Exception as e:
        return {"error": str(e)}

# Polling endpoint
@app.get("/polling-get-task/{task_id}")
async def polling_get_task(task_id: str):
    task = AsyncResult(task_id, app=simple_app)
    if task.ready():
        return task.result
    else:
        return {"status": task.status}

# Webhook endpoint - This will be called by the worker when the task is completed    
@app.post("/webhook-get-task/")
async def webhook_get_result(task_result : TaskResult):
    print(task_result.status)
    print(task_result.result)
    return "Task recieved successfully"


    