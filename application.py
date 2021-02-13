from flask import Flask, render_template, url_for,request
import requests
import json
from flask_socketio import SocketIO


f= open('json/posts.json')
posts = json.load(f)
f.close

# Opening JSON file 
f = open('json/sentimental.json',) 
# returns JSON object as  
# a dictionary 
stockSentimental = json.load(f)
highesetTimes = stockSentimental[0]["times"]
f.close()

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)

@application.route("/")
@application.route("/stocks")
def home():
    return render_template('stocks.html', posts=posts, stockSentimental=stockSentimental, highesetTimes= highesetTimes)


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

# run the app.
if __name__ == "__main__":
    socketio.run(application, debug = True)
