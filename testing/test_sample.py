import pytest
import requests
import time


def test_server_health_check():
    #Check if the server is healthy or not
    url = "http://localhost:8080/"
    response = requests.get(url)
    assert response.status_code == 200

def test_polling_api():
    #check all functionalities of polling api
    url = "http://localhost:8080/upload-file/polling"
    file={'file': open('test.pdf','rb')}
    response = requests.post(url, files=file)
    assert response.status_code == 200
    assert response.json()["store_extract_task_id"] != None
    assert response.json()["delete_task_id"] != None
    store_extract_task_id = response.json()["store_extract_task_id"]
    delete_task_id = response.json()["delete_task_id"]
    #check if store and extract task is completed
    url = f"http://localhost:8080/polling-get-task/{store_extract_task_id}"
    time.sleep(5)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"
    assert response.json()["result"] != None
    #check if delete task is completed
    url = f"http://localhost:8080/polling-get-task/{delete_task_id}"
    time.sleep(5)
    response = requests.get(url)
    assert response.status_code == 200
    assert str(response.json())== "File deleted successfully"

def test_webhook_api():
    #check all functionalities of webhook api
    url = "http://localhost:8080/upload-file/webhook"
    file={'file': open('test.pdf','rb')}
    response = requests.post(url, files=file)
    assert response.status_code == 200
    assert response.json()["store_extract_task_id"] != None
    assert response.json()["delete_task_id"] != None
    store_extract_task_id = response.json()["store_extract_task_id"]
    delete_task_id = response.json()["delete_task_id"]
    #check if store and extract task is completed
    url = f"http://localhost:8080/polling-get-task/{store_extract_task_id}"
    time.sleep(5)
    response = requests.get(url)
    assert response.status_code == 200
    assert str(response.json())== "Task sent successfully"
    #check if delete task is completed
    url = f"http://localhost:8080/polling-get-task/{delete_task_id}"
    time.sleep(5)
    response = requests.get(url)
    assert response.status_code == 200
    assert str(response.json())== "File deleted successfully"
    #check if self-defined webhook works or not
    url = "http://localhost:8080/webhook-get-task/"
    response = requests.post(url, json={"status":"SUCCESS","result":"This is a test"})
    assert response.status_code == 200

