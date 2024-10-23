# PDF Data Extraction Application

This application is designed to extract data from PDF files. It uses Docker for easy setup and execution.

## Prerequisites

You need Docker installed on your machine to run this application.

## Getting Started

After installing Docker, you can start the application using the following command in your terminal:

```bash
docker-compose up --build
```
command in your terminal. This will create a docker compose with 3 containers for :
1. The host application
2. RabbitMQ
3. Celery worker

## Explanation of the working:

The application has mainly 3 endpoints:
    1. To send the pdf file to the host application for extraction of data:
        URL: http://127.0.0.1:8080/upload-file/{output_type}
        arguments:
            - params: output_type (required) --> either webhook or polling
            - body(form-data): file (required) --> The file 
    
    2. POlling endpoint to check whether extraction is complete or not:
        URL: http://127.0.0.1:8080/polling-get-task/{task_id}
        arguments:
            - params: task_id (required) --> task_id of the task

    3. A webhook URL where the celery worker sends the extracted data after the extraction is complete (This can be customized in the future so that user can give their own webhook URL)
        URL: http://127.0.0.1:8080/webhook-get-task/
        arguments:
            - body(JSON) : result of the task in the structure {"status" : "<SUCCESS> or <FAILURE>" , result:       "Result text}

The application uses Celery as its background task Manager and Rabbit MQ as its broker.
RabbitMQ queues the tasks given to it by celery and returns them in order of their execution
Then celery worker executes thos background tasks one after another.

I have applied this concept to store and extract the data from the pdf and to delete the pdf later on.
There are mainly two tasks in celery worker :
    1. Store the pdf inside the server and extract the text from the pdf
    2. Delete the pdf from the server

## Testing

There is a directory call "testing" in which there are pytest test cases to test out the working of the system.
These test case can be tried from outside of the docker container using the following commands:

```bash
cd testing
pip install -r testing-requirements.txt
pytest test_sample.py
```

The test cases ar well commented in order to be understood better. These test cases test out the working of all components of the application and ensure there are no bugs.