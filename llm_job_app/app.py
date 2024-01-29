from chalice import Chalice
from chalicelib.main import run_job_scrapper_ETL
import json

app = Chalice(app_name="job_rec_app")


@app.route("/")
def index():
    jobs = run_job_scrapper_ETL()
    if not jobs:
        return {"400": "No jobs found"}

    return {"200": "Success!"}


@app.schedule("cron(0 0 * * ? *)")
def cron_job(event):
    jobs = run_job_scrapper_ETL()
    if not jobs:
        return {"400": "No jobs found"}

    return {"200": "Success!"}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
