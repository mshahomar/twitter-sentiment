from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token
import constants


# Get users' information and save all information to database
Database.initialize(constants.DB_CONNECTION_STRING)

user_email = input("Enter your email address: ").strip()

user = User.load_from_db_by_email(user_email)

if not user:
    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    first_name = input("Enter your first name: ").strip().lower()
    last_name = input("Enter your last name: ").strip().lower()

    twitter_user = User(email=user_email, first_name=first_name, last_name=last_name,
                        oauth_token=access_token['oauth_token'], oauth_secret=access_token['oauth_token_secret'],
                        id=None)
    twitter_user.save_to_db()


# print(content.decode('utf-8'))
tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])
