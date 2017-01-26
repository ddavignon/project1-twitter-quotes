import os
from flask import Flask, render_template
import urllib3, json, base64

app = Flask(__name__)


def twitterApiData():
    
    CONSUMER_KEY = 'nicys670TghYuxNKJbrFHA8Yt'
    CONSUMER_SECRET = 'jyn2MvSLxvG7XdjQuYFomZ808GSbjs2r4it8XH5Df6G7ogwOVA'
    ACCESS_TOKEN = '800599760902045696-782ZftuV0oe8aCMZ2qbsmtB0GnB5c9K'
    ACCESS_SECRET = 'AY1y2y7NAqJzOXFOJZuZXL5HQQtNbSQPzVx8zkAXxULVF'

        # # Create a HTTP connection pool manager
    manager = urllib3.PoolManager()
    
    # Set the variable to Twitter OAuth 2 endpoint
    oauth_url = 'https://api.twitter.com/oauth2/token' 
    
    # Set the HTTP request headers, including consumer key and secret
    http_headers={'Authorization': "Basic %s" % base64.b64encode("%s:%s" % (CONSUMER_KEY,CONSUMER_SECRET)), 'Content-Type': 'application/x-www-form-urlencoded'} 
    
    # Set the payload to the required OAuth grant type, in this case client credentials
    request_body="grant_type=client_credentials" 
    
    # Send the request
    response = manager.urlopen("POST", oauth_url, headers=http_headers, body=request_body)
    
    # Read the response as JSON
    app_token = json.loads(response.data) 
    
    # Set the variable to the ProgrammableWeb timeline
    #url='https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=ProgrammableWeb'
    
    # Set variable for search
    url='https://api.twitter.com/1.1/search/tweets.json?q=%23trump'
    
    # Set the Authorization header using the value of the access_token key from the app_token dictionary created above
    http_header={'Authorization': 'Bearer %s' % app_token ['access_token']}
    
    # Send the request
    response = manager.urlopen('GET', url , headers=http_header) 
    
    # Read the response, create dictionary and render HTML using data and template
    return json.loads(response.data)
    

@app.route('/')
def hello():
    return render_template('index.html',token=twitterApiData())
    

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))