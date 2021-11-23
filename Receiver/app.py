import connexion
from connexion import NoContent
import json
import requests
import yaml
import logging
import logging.config
from flask import Response
import uuid
import datetime
import json
from pykafka import KafkaClient
from time import sleep
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"


MAX_EVENTS = 12
EVENT_FILE = 'events.json'

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml','r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

num_tries = 0
max_tries = int(app_config['events']['max_tries'])
while num_tries < max_tries:
    try:
        logger.info('Connecting to Kafka. Tries: {}'.format(max_tries))
        client = KafkaClient(hosts='{}:{}'.format(app_config['events']['hostname'],app_config['events']['port']))
        topic = client.topics[str.encode(app_config['events']['topic'])]
        producer = topic.get_sync_producer()
        num_tries = max_tries
    except:
        num_tries += 1
        logger.error("Could not connect to Kafka..")
        sleep(2.5)
# def get_cit_course(timestamp):
#     logger.info("Received cit class request {}".format(uuid.uuid4()))
#     request = requests.get(app_config['get_cit']['url']+"?timestamp="+json.dumps(timestamp))
#     logger.info("Returned event get_member response  {} with status {}".format(uuid.uuid4(),request.status_code))
#     return Response(response=request.content,status=200,headers={'Content-type': 'application/json'})


# def get_students(timestamp):
#     logger.info("Received student request {}".format(uuid.uuid4()))
#     request = requests.get(app_config['get_student']['url']+"?timestamp="+json.dumps(timestamp))
#     logger.info("Returned event get_groups response  {} with status {}".format(uuid.uuid4(),request.status_code))
#     return Response(response=request.content,status=200,headers={'Content-type': 'application/json'})


# def add_cit_course(body):
#     uniq_id = body['class_id']
#     logger.info("Received logger for CIT, getting unique id {}".format(uniq_id))
#     request = requests.post(app_config['post_cit']['url'], headers={"content-type":"application/json"}, data=json.dumps(body))
#     logger.info('Returned event {} request with a unique id of {}'.format(request.status_code, uniq_id))
#     return NoContent, request.status_code

def add_cit_course(body):
    logger.info(f"Received event add_cit_course request with a unique id of {body['class_id']}")
    #// response = requests.post(app_config['instore_sales']['url'], json=body)                 ##LAB5
    #// logger.info(f"Returned event instore_sales response(ID: {body['product_id']}) witt status {response.status_code}")
    #// return NoContent, response.status_code
    msg = { "type": "cit",   #event type #! DOUBLE CHECK IF IT NOT WORK
        "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body }  
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 200 #! You will need to hard-code your status code to 201 since you will no longer get it from the response of the requests.post call
# def add_student_info(body):
#     uniq_id = body['student_id']
#     logger.info("Received logger for student, getting unique id: {}".format(uniq_id))
#     request = requests.post(app_config['post_student']['url'], headers={"content-type":"application/json"}, data=json.dumps(body))
#     logger.info('Returned event {} request with a unique id of {}'.format(request.status_code, uniq_id))
#     return NoContent, request.status_code


def add_student_info(body):
    # headers = {"content-type":"application/json"}
    logger.info (f"Received event student info request with a unique id of {body['student_id']}")
    #// response = requests.post(app_config['online_sales']['url'], json=body,  headers=headers)    ##LAB5
    #// logger.info(f"Returned event online_sales response(ID: {body['product_id']}) witt status {response.status_code}")
    #// return NoContent, response.status_code
    msg = { "type": "student",   #event type
        "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body }  
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 200 #! You will need to hard-code your status code to 201 since you will no longer get it from the response of the requests.post call

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", 
            strict_validation=True, 
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)