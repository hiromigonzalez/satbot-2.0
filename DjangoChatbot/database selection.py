from flask import Flask, jsonify
import os
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve database connection details from environment variables
    db_host = os.environ.get('DB_HOST')
    print("DB_HOST")
    db_port = os.environ.get('DB_PORT')
    print("DB_PORT")
    db_user = os.environ.get('DB_USER')
    print("DB_USER")
    db_password = os.environ.get('DB_PASSWORD')
    print("DB_PASSWORD")
    db_name = os.environ.get('DB_NAME')
    print("DB_NAME")

    # Connect to MySQL database
    connection = pymysql.connect(
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_password,
        db=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    # Perform a sample query
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM example_table')
        result = cursor.fetchall()

    # Close database connection
    connection.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
