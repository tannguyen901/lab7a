from datetime import datetime
import connexion
from connexion import NoContent

from flask import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from cit import Cit
from student import Student
import yaml
import logging
import logging.config
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from sqlalchemy import and_
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


logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

host = "tanlab6a.eastus.cloudapp.azure.com"
with open (app_conf_file, 'r') as f:
    app_config= yaml.safe_load(f.read())
    logger.info(f"Connecting to DB. Hostname {host}, Port: 3306")

with open(log_conf_file,'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(app_config['datastore']['user'], app_config['datastore']['password'], app_config['datastore']['hostname'],app_config['datastore']['port'], app_config['datastore']['db']))
# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_students(start_timestamp, end_timestamp):
    session = DB_SESSION()
    # timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    students = session.query(Student).filter(and_(Student.date_created >= start_timestamp_datetime,Student.date_created < end_timestamp_datetime))

    # students = session.query(Student).filter(Student.date_created >= timestamp_datetime)
    results_list = []
    for student in students:
        results_list.append(student.to_dict())
    session.close()
    logger.info("Query for student information after %s returns %d results" %(start_timestamp, len(results_list)))
    return Response(response=json.dumps(results_list),status=200,headers={'Content-type': 'application/json'})


def get_cit_course(start_timestamp, end_timestamp):
    session = DB_SESSION()
    # timestamp_datetime = datetime.d:q:q!atetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    # CITs = session.query(Cit).filter(Cit.date_created >= timestamp_datetime)

    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    CITs = session.query(Cit).filter(and_(Cit.date_created >= start_timestamp_datetime,Cit.date_created < end_timestamp_datetime))

    results_list = []
    for cit in CITs:
        results_list.append(cit.to_dict())
    session.close()
    logger.info("Query for CIT course after %s returns %d results" %(start_timestamp, len(results_list)))
    return Response(response=json.dumps(results_list),status=200,headers={'Content-type': 'application/json'})
    

def add_cit_course(body):
    """receives course information"""
    session =DB_SESSION()
    cit = Cit(body['class_id'],
              body['class_name'],
              body['instructor'],
              body['max_class_size'])
    session.add(cit)
    session.commit()
    session.close()
    unq_id = body['class_id']
    logger.debug(f'Stored event class_id request with a unique id of {unq_id}')
    return NoContent, 201


def add_student_info(body):
    '''receives student information'''
    session =DB_SESSION()
    std = Student(body['student_id'],
                  body['student_name'],
                  body['student_age'],
                  body['start_date'])
    session.add(std)
    session.commit()
    session.close()
    unq_id = body['student_id']
    logger.debug(f'Stored event student_id request with a unique id of {unq_id}')
    return NoContent, 201


def process_messages():
    """ Process event messages """
    logger.info('Processing messages is beginning')
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    max_tries = int(app_config["events"]["max_tries"])
    trying = 0
    while trying < max_tries:
        try:
            logger.info('Connecting to Kafka. Tries: {}'.format(trying))
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
            trying = max_tries
        except:
            trying += 1
            logger.error("Could not connect to Kafka..")
            sleep(2.5)
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',reset_offset_on_start=False,auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        try:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info("Message: %s" % msg)

            payload = msg["payload"]

            if msg["type"] == "cit": # Change this to your event type
                # Store the event1 (i.e., the payload) to the DB
                add_cit_course(payload)

            elif msg["type"] == "student": # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
                add_student_info(payload)
            # Commit the new message as being read
            consumer.commit_offsets()
        except:
            logger.error("Something is wrong. Cannot Store in DB table")


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", base_path="/storage", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)

