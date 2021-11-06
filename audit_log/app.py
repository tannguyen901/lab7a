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


logger = logging.getLogger('basicLogger')


with open ('app_conf.yml', 'r') as f:
    app_config= yaml.safe_load(f.read())

with open('log_conf.yml','r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


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
app.add_api("openapi.yml", 
            strict_validation=True, 
            validate_responses=True)


if __name__ == "__main__":
    app.run(port=8110, debug=True)
