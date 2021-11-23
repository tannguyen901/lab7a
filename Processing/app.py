from datetime import datetime
import connexion
from connexion import NoContent
import json
import requests, yaml, logging, logging.config, uuid, datetime
from apscheduler.schedulers.background import BackgroundScheduler
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

def get_stats():
    logger.info(f'Received event get_stats request {uuid.uuid4}')
    try:
        with open(app_config['datastore']['filename'], 'r') as file:
            file_data = file.read()
            logger.debug(f"loaded statistics: {json.loads(file_data)}")
            logger.info("get_stats request is completed")
            return json.loads(file_data), 200
    except:
        logger.error("Statistic file not found")
        return "statistics dne", 404


def populate_stats():
    logger.info("Start Periodic Processing")
    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            stats = json.loads(f.read())
    except:
        with open(app_config['datastore']['filename'], 'w') as f:
            f.write(json.dumps({"most_popular_cit_class": "Service Based Architecture", "student_count": 0,"class_count": 0,"num_students_in_class": 0,"last_updated": "2016-08-29T09:12:33Z"}))
    

    current_date = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%SZ")

    student_req = requests.get(app_config['get_student_url']['url']+"?start_timestamp="+stats['last_updated']+"&end_timestamp="+current_date)
    cit_req = requests.get(app_config['get_cit_url']['url']+"?start_timestamp="+stats['last_updated']+"&end_timestamp="+current_date)


    if student_req.status_code != 200:
        logger.error("ERROR receiving data for student.")
    else:
        logger.info("Successfully received student info")
    if cit_req.status_code != 200:
        logger.error("ERROR receiving data on cit info.")
    else:
        logger.info("Successfully received data on cit information.")

    student_data = json.loads(student_req.content)
    cit_data = json.loads(cit_req.content)
    print("Hello student", student_data)
    print("Hello cit", cit_data)
    
    class_type_list = []
    most_class_type = ""
    student_len = len(student_data) + stats['student_count']
    cit_len = len(cit_data) + stats['class_count']
    num_students_in_class = stats['num_students_in_class']
    

    for cit in cit_data:
        print(type(cit))
        class_type_list.append(cit['class_name'])
    if len(class_type_list) > 0:
        most_class_type = max(class_type_list)
    else:
        most_class_type = "Enterprise Systems Integrations"

    for student in student_data:
        if len(student['student_name']) >0:
            num_students_in_class += 1 


    data_obj = {"most_popular_cit_class": most_class_type, "student_count": student_len,"class_count": cit_len,"num_students_in_class": num_students_in_class,"last_updated": current_date}
    with open(app_config['datastore']['filename'],'w') as file:
        file.write(json.dumps(data_obj))
    logger.debug("Successfully saved the new stats: {}".format(data_obj))


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml", 
            strict_validation=True, 
            validate_responses=True)


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)