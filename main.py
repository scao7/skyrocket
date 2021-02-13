from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, emit
import time 
import requests
import json
import numpy as np 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)
class Comments(db.Model):
    id = db.Column(db.Integer)
    stock = db.Column(db.String(200),nullable= False)
    comment_body = db.Column(db.String(500),nullable=False)
    link_title = db.Column(db.String(200),nullable = False)
    emotion = db.Column(db.Float, nullable = False)
    author = db.Column(db.String(50),nullable = False)
    data_created = db.Column(db.DateTime, default = datetime.utcnow)
    created_utc = db.Column(db.String,nullable =False,primary_key = True)
    
    def __repr__(self):
        return '<Name %r> ' % self.id

class Sentimental(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    stock= db.Column(db.String(20),nullable=False)
    overall_emotion = db.Column(db.Float,nullable=False)
    mentioned_times = db.Column(db.Integer,nullable=False)
    data_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r> ' % self.id


app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app)
# check if company exist in stock market
def check_stock(text):
    company = []
    for word in text.split():
        if( word.isalpha() and word.isupper()):
            response = requests.get('https://ticker-2e1ica8b9.now.sh/keyword/{}'.format(word))
            for symbol in response.json():
                if(symbol['symbol'] == word):
                    company.append(word)
    return np.unique(company)

#check if stock exist in json return index 
def exist_in_json(stock):
    count = 0 
    for item in stockSentimental:
        if(stock == item['stock']):
            return count
        count = count + 1
    return -1

from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()
language= 'en'

def request_comments():
    headers = {
            'authority': 'www.reddit.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
            # 'cookie': 'csv=1; edgebucket=UX5wgOq4Y4GSAJfBLR; __gads=ID=0a17fc3c4a323e05:T=1612549170:S=ALNI_MbiaOZWd2gnEzZoPrsV7YFC-01AAg; pc=xy; __aaxsc=2; loid=0000000000a0w0894p.2.1611778369817.Z0FBQUFBQmdJRHh4SU0xdW1WVHlqdUpGaHQ0d3BfSGNkcldodkN5T0hiNDVzWGo4TTVBU1huWjcxeXBHNmF4eDZubVJhM2tLUXhDakMtOFZGeU9OYS1mNXp5b25zVXVJZkFBLUlLR3pjOUQxZ2hPNGQ3WldGOE9CM1dVX29zeWtYU3FJZ0xGZDJTTWY; g_state={"i_l":0,"i_t":1612821216952}; G_ENABLED_IDPS=google; reddit_session=785576943673%2C2021-02-07T21%3A53%3A45%2C9eb1e8632ca55d673a2df524483c1ba519958948; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTI3NDE5MjEsInN1YiI6Ijc4NTU3Njk0MzY3My1tdnpMcDUwWl9kSDM1eDM0em9FSDUxWUpmV2ciLCJsb2dnZWRJbiI6dHJ1ZSwic2NvcGVzIjpbIioiLCJlbWFpbCJdfQ.CBsEyIWGP3hqq9w-SMPx6GFfOs_QZw5k1pbEzJkWW7Y; Unusual_Beat8097_recentclicks2=t3_leneyw%2Ct3_levf1j%2Ct3_lef7fe%2Ct3_let1bn%2Ct3_lexq6t; session=3ca5ade2f3f64757fea795fd722336d3326f8eecgASVSQAAAAAAAABK128gYEdB2AgKx6vS0X2UjAdfY3NyZnRflIwoMTk5ZTE0MjA3YjFiY2E2YTU3OGQ3YzBjMGU2NjYyN2EwODAzZmQyYZRzh5Qu; recent_srs=t5_2th52%2Ct5_2qjfk%2Ct5_2qizd%2Ct5_2r8ot%2Ct5_2s1s3%2Ct5_2rfi7%2Ct5_2r97t%2Ct5_2clyzt%2C; aasd=12%7C1612737691537; session_tracker=6lm8Y4dm4eyOI8i4gN.0.1612738558093.Z0FBQUFBQmdJR18tVG44UjgtdzlwajZ5bmFjNlFEUkxRRnBPVlFHdGdNeVlSVWMyb3ZPY182SWcyaVRFSmdUZXl1elRRSGhjV1BRck84bG4xQm50NHdQdGpJcGtOdzBhN2M5VkljTkx1akJqaloxNHJaR3lZZjVIbnQwcGw4Y3RKeWJJdmdYdnVHRm8',
        }
            
    response = requests.get('https://www.reddit.com/r/wallstreetbets/comments.json', headers=headers)
    json_response = response.json()
    # print(json_response)

    for item in json_response['data']['children']:
        content = item['data']['body']
        created_utc = item['data']['created_utc']
        link_title = item['data']['link_title']
        author = item['data']['author']
        stocks = check_stock(content)
        if(len(stocks)!=0):
            for stock in stocks:
                print("item ####: {}".format(link_title))
                print('created ###: {}'.format(created_utc))
                print('content: ### {}'.format(content))
                print('stock ### {}'.format(str(stock)))
                print('author ### {}'.format(author))
                emotion = 0.0
                # if(db.session.query(Comments.id).filter_by(created_utc=created_utc).scalar() is None):
                
                # if(not Comments.query.filter_by(created_utc=created_utc).first()):
                print("query utc result: not same utc")
                try:
                    output = client.specific_resource_analysis(body={"document": {"text": content}}, params={'language': language, 'resource': 'sentiment'})
                    emotion = output.sentiment.overall
                except:
                    print('no emotion')
                    emotion = 0.0
                print('emotion ###: {}'.format(emotion))
                #create value to push to database
                new_comment= Comments(stock = stock,comment_body =content,link_title=link_title,emotion=emotion, author = author, created_utc=created_utc)
                                # push to database
                try:
                    db.session.add(new_comment)
                    db.session.commit()
                    print('sucess added to database')
                except:
                    print('can nott add to database')
                        
                # add to sentimental database
                get_sentimental = Sentimental.query.filter_by(stock=stock).first()
                if(get_sentimental):
                    get_sentimental.mentioned_times +=1
                    get_sentimental.overall_emotion += emotion
                    db.session.commit()
                else:
                    new_sentimental = Sentimental(stock = stock, overall_emotion=emotion, mentioned_times=1)
                    db.session.add(new_sentimental)
                    db.session.commit()
            




@app.route('/')
@app.route('/index')
def index():
    query = Comments.query.order_by(Comments.data_created.desc())
    Sentimental_query = Sentimental.query.order_by(Sentimental.mentioned_times.desc())
    for item in Sentimental_query:
        print(item.mentioned_times)
        highestTimes=item.mentioned_times
        break
    # print('query is : {}'.format(query))
    # print('query type is : {}'.format(type(query)))
    # stocks_emotion =  [{'stock': 'example','mentioned_times': 1, 'emotion': 0 }]
    # for item in query:
    #     if(not any(emotion.get('stock') == item.stock for emotion in stocks_emotion)):
    #         stocks_emotion.append({'stock': item.stock,'mentioned_times': 1, 'emotion':item.emotion})
    #     else:
    #         for emotion in stocks_emotion:
    #             if(emotion['stock'] == item.stock):
    #                 emotion['emotion'] += item.emotion
    #                 emotion['mentioned_times'] += 1

    # Sentimental_query = Sentimental.query.order_by(Sentimental.mentioned_times.desc())

    # sorted_stock_emotion = sorted(stocks_emotion, key=lambda k: k['mentioned_times'],reverse=True)  
    return render_template('index.html', comments = query.limit(20), stockSentimental=Sentimental_query,highestTimes=highestTimes)

@socketio.on('message')
def receive_message(message): 
    print('########: {}'.format(message))
    while True:
        request_comments()
        send(1)
        emit('redirect', {'url': url_for('index')})

    # send(coments)

    # send(stockSentimental)
    # send(highesetTimes)
if __name__ == '__main__':
    socketio.run(app)