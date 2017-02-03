import os
from flask import Flask, render_template, url_for, send_from_directory
import urllib3, json, base64
import random

app = Flask(__name__)

phrase = 'cute puppies'
search_term = phrase.replace(' ', '%20').lower()

def twitterApiData():
    
    # api keys
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

    # Create a HTTP connection pool manager
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
    # Set variable for search
    url='https://api.twitter.com/1.1/search/tweets.json?q=%23' + search_term + '&result_type=recent'
    # Set the Authorization header using the value of the access_token key from the app_token dictionary created above
    http_header={'Authorization': 'Bearer %s' % app_token ['access_token']}
    # Send the request
    response = manager.urlopen('GET', url , headers=http_header)  
        
    try:
        tweet = json.loads(response.data)['statuses'][random.randint(0,len(json.loads(response.data)['statuses']) )]
    except:
        tweet = ""
        
    return tweet


def gettyApiImage():
    
    # api keys
    API_KEY = os.environ['API_KEY']

    # # Create a HTTP connection pool manager
    manager = urllib3.PoolManager()
    # Set variable for search
    url='https://api.gettyimages.com:443/v3/search/images?fields=display_set&file_types=jpg&minimum_size=large&phrase=' + search_term
    # Set the Authorization header using the value of the access_token key from the app_token dictionary created above
    http_header={'Api-Key': API_KEY}
    # Send the request
    response = manager.urlopen('GET', url , headers=http_header) 
    
    # Read the response, create dictionary and render HTML using data and template
    try:
        image = json.loads(response.data)['images'][random.randint(0, len(json.loads(response.data)['images']))]
    except:
        image = ""
    
    return image


@app.route('/')
def hello():
    return render_template('index.html', tweet=twitterApiData(), img=gettyApiImage())
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/png')

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)
    
    #switch for deploy to heroku
    #app.run()