# skyrocket

# how to run it 
create a python environment 

use `pip install -r requirements.txt`  to install the dependency

use `python main.py` to run the project. Open the `localhost:5000` for the demo

## Inspiration
Inspired from the recent story from the wallstreetbet reddit group. They talked on the reddit and spread information about raise the GameStop stock to against the shorts institution. The story is very impressive that the GameStop stock reaches to $420 form $20 in several days. One of the user in the wallstreetbet call have earned huge profit. 

I kept an eye on the event and go in in a late stage and didn't capture the profit. But in one of the discord group they mentioned buy DOGE coin, I instantly bought some and right onw it's 250% profit. 

Therefore, the stories tell me that if we can go in in the early stage of those even. We could gain huge profit. I decide to build an app to auto grab the newest comments from reddit and analysis the emotion of those comment and build a stock promote webapp.  I called it Skyrocket Stocks. 
## What it does
Skyrocket Stocks can get the comments from the wallstreetbet reddit group newest comments and evaluate the emotion to the stock and give suggest buy, sell or hold. You can directly click the suggestion to get the stock information from yahoo. 

## How we built it
This is a solo project, I use python in my college. And I have no experience to build such an app before. First, I search through the internet that which framework is good to build a webapp using python. 
Second, how people get the newest comments from Reddit
Third, where to deploy my app. 
Fourth, how to use the expertai-nlapi. 

The first two and the last one is pretty straightforward . I decided to use Flask as my web framework. And I directly use requests  to get the newest comments in json format. Very fast I parsed the information out such as author, date, comment and title. 

The algorithm part is straightforward:  1. request comments json file. 2. parse out the stock, I used the free stock api to get all stocks in the market include  NYSE and NASDAQ. 3. use the expert ai api to get sentimental score. 4. add up the sentimental score and out put buy, sell and hold signal. 

## Challenges we ran into

The pain point is the deploy stage and web related development with python. I never used the flask before. First I try to store my processed result the json files and re-read to make my app remember previous result and I found that is not good because of the json cache in chrome. I then learn the knowledge about how to build database with Flask. 

At first I want to build an real time app that run 24 hours and synchronize with Reddit. That requires me using socket between client side and server side. I speed a lot of time on this and I got the display in real-time. However, the process time for those comments using exert ai takes a  lot of time and make my app crashed several times. Also due to the limitation of the 10 million character restriction, I couldn't make my app run 24 hours all the time. 

I slightly changed the strategy, I make my app request new stock when at list one client is using the app. That save lot of works. 

## Accomplishments that we're proud of
I am proud of myself for learning new concepts all the time including asynchronous design. Socket communication between  client and server. 

I am proud of I finally make this app deployed on the server and can help other people to get the latest information about the reddit stocks. 

I am proud of I can incorporate the expert ai api to this project and deployed since there is some version mismatch with cloud and localhost. I think expert ai is a good tool for my tasks overall. 
## What we learned
During the 2 weeks, I learned json ,http request, flask, flask_alchemy, jinja2 dynamic template, sockitio, jquery, heroku web server, experai-nlapi,  and finally finished the app. 

## What's next for SkyRocket Stock Purchase
I would like to include the twitter data, YouTube data together. Also I would like to incorporate more experai-nlapi for the user profiling to verify if some are robot or they are varying in two opinions often for more accurate stock prediction.  
