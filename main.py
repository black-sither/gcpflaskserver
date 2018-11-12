# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging
import argparse
import datetime
from google.cloud import datastore
from flask import Flask

project_id = "iotj-222300"

app = Flask(__name__)


def create_client(project_id):
    return datastore.Client(project_id)


client = create_client(project_id)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'IOT Attendence new'


@app.route('/create/<name>')
def hello1(name):
    key = client.key('AttendanceVIT')

    task = datastore.Entity(key)
    query = client.query(kind='AttendanceVIT')
    query.add_filter('name', '=', name)
    query = client.query()
    ispresent = len(list(query.fetch()))
    if ispresent == 0:
        task.update({
            'name': name,
            'count': 0,
        })
    else:
        results = list(query.fetch())
        task = results[0]
        count = task['count']
        task.update({
            'name': name,
            'count': count + 1,
        })
    client.put(task)
    return "Created/Updated entry"


@app.route('/total')
def present():
    query = client.query(kind='AttendanceVIT')
    query = client.query()
    results = len(list(query.fetch()))
    return str(results)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
