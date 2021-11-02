import connexion
from connexion import NoContent
import json
import os



def add_cit_course(body):
    # create a simple logging mechanism that writes the last 12
    event_list = [] 
    if os.path.exists('events.json'):
        with open('events.json', 'r') as fh:
            file_read = fh.read()
            if len(file_read) > 0:
                old_json = json.loads(file_read)
                event_list = old_json
                if len(event_list) >=12:
                    event_list = event_list[-11:]
    with open('events.json', 'w') as to_write:
        event_list.append(body)
        to_write.write(json.dumps(event_list,indent=2))
    return NoContent, 201

def add_student_info(body):
    event_list = [] 
    if os.path.exists('events.json'):
        with open('events.json', 'r') as fh:
            file_read = fh.read()
            if len(file_read) > 0:
                old_json = json.loads(file_read)
                event_list = old_json
                if len(event_list) >=12:
                    event_list = event_list[-11:]
    with open('events.json', 'w') as to_write:
        event_list.append(body)
        to_write.write(json.dumps(event_list,indent=2))
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi_original.yaml", 
            strict_validation=True, 
            validate_responses=True)


if __name__ == "__main__":
    app.run(port=8080)