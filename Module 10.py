#Mario Ruiz-Leon
#Devin Christoffersen

import pyodbc
from flask import Flask, g, render_template, abort, request
import json

'''
2) Create the following Routes in your Flask Application (Use the data you persisted in Module 9)

Default Route ("/") - Go to a simple html template page that tells about your data.
GET ("/item/<id>") - Will return a single item from your data, by ID. If you data does not have a unique identifier then please let me know and I will help you get one added.
DELETE("/item/<id>") - Will delete a single item (again, you will need a unique column name)
POST ("/item") - As opposed to GET, POST will create a new item in your database. The body of the request will contain the item to be added.
'''


# Global Connection String
connection_string = 'Driver={ODBC Driver 17 for SQl server};Server=DESKTOP-1U0PR0M\SQLEXPRESS;Database=Avocado;Trusted_Connection=yes;'

# The requred info to start the Flask API
app = Flask(__name__)
app.config.from_object(__name__)


# Set Up/ Teardown of the API
@app.before_request
def before_request():
    try:
        g.sql_conn = pyodbc.connect(connection_string, autocommit=True)
    except Exception:
        abort(500, "No database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    try:
        g.sql_conn.close()
    except AttributeError:
        pass


# This is the section that renders a HTML template that describes the data contained within the database
@app.route('/')
def index():
    return render_template('avocado.html')


# Get some data about Avocados!
@app.route('/avoall', methods=['GET'])
def get_avocado_data():
    cursor = g.sql_conn.cursor()
    query = 'select * from dbo.Avocado_data'
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    data = []

    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)


# Get some data about a single Avocado!
@app.route('/avosingle/<string:id>', methods=['GET'])
def get_single_avocado(id):
    cursor = g.sql_conn.cursor()
    cursor.execute("select * from dbo.Avocado_data where ID = ?", id)

    columns = [column[0] for column in cursor.description]
    data = []

    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)


# This will delete a row in the database depending on the ID that you provide.
@app.route('/avodelete/<string:id>', methods=['DELETE'])
def drop_data(id):
    cursor = g.sql_conn.cursor()
    cursor.execute("DELETE dbo.Avocado_data where ID = ?", id)
    cursor.commit()
    return 'item successfully deleted', 200


# Post about some avocados. When writing to the database the only required field is the Id field which is default an auto incrementing PK.
@app.route('/avopost', methods=['POST'])
def insertnew():
    data = request.get_json()

    curs = g.sql_conn.cursor()

    query = 'dbo.Avocado_data (ID) VALUES (?)'

    if isinstance(data, dict):
        curs.execute(query, data["ID"])
        curs.commit()

    if isinstance(data, list):
        for row in data:
            curs.execute(query, row["ID"])
            curs.commit()

    return 'success', 200


if __name__ == "__main__":
    app.run()