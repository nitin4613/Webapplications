from flask import Flask
from flask import request
from flask import render_template


def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def home():
        return render_template('hello.html')

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
