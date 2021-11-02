import sqlite3
from sqlite3.dbapi2 import connect
from flask import Flask
from flask import request
from flask import render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        database_server = sqlite3.connect(':memory:')
        database_server.row_factory = sqlite3.Row
       
        database_server.execute("CREATE TABLE IF NOT EXISTS userInfo(fname VARCHAR(20) PRIMARY KEY, mname VARCHAR(20), lname VARCHAR(20) );")
        database_server.execute("""INSERT INTO userInfo(fname) Values("CircleCi, CoolCi, CoolerCi");""")
        database_server.commit()

        posts = database_server.execute('SELECT * FROM userInfo').fetchall()
        #print(posts)
        database_server.close()
        return render_template('hello.html', posts=posts)

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        
    @app.route('/shutdown', methods=['GET'])
    def shutdown():
        shutdown_server()
        return 'Server shutting down...'
    
    # from app import routes
    return app
