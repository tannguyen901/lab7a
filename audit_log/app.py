from datetime import datetime
import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from flask_cors import CORS, cross_origin
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open (app_conf_file, 'r') as f:
    app_config= yaml.safe_load(f.read())

with open(log_conf_file,'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

def get_students(index):
    """ Get student Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                        app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=1000)
    my_ls = []
    logger.info("Retrieving BP at index %d" % index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str)
        # Find the event at the index you want and # return code 200
        # i.e., return event, 200
            if msg["type"] == "student":
                my_ls.append(msg['payload'])
        if len(my_ls) > index:
            event = my_ls[index]
            return event, 200
    except:
        logger.error("No more messages found")
        logger.error("Could not find student at index %d" % index)
    return { "message": "Not Found"}, 404


def get_cit_course(index):
    """ Get cit course Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
    app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=1000)
    my_ls = []
    logger.info("Retrieving BP at index %d" % index)
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str)
        # Find the event at the index you want and # return code 200
        # i.e., return event, 200
            if msg["type"] == "cit":
                my_ls.append(msg['payload'])
        if len(my_ls) > index:
            event = my_ls[index]
            return event, 200

    except:
        logger.error("No more messages found")

        logger.error("Could not find cit at index %d" % index)
    return { "message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", 
            strict_validation=True, 
            validate_responses=True)


if __name__ == "__main__":
    app.run(port=8110, debug=True)
