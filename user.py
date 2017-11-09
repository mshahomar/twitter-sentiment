from database import CursorFromConnectionFromPool
from twitter_utils import consumer
import oauth2
import json


class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        # self.email = email
        # self.first_name = first_name
        # self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __str__(self):
        return self.screen_name

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'INSERT INTO users (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
                (self.screen_name, self.oauth_token, self.oauth_token_secret)
                # 'INSERT INTO users (email, first_name, last_name, oauth_token, oauth_secret) VALUES (%s, %s, %s, %s, %s)',
                # (self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_secret)
            )

    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE screen_name=%s',
                (screen_name,)
            )
            user_data = cursor.fetchone()
            if user_data:  # if user_data is not None
                return cls(screen_name=user_data[1], oauth_token=user_data[2],
                           oauth_token_secret=user_data[3], id=user_data[0])

                # return user_data

    def twitter_request(self, uri, method='GET'):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # Make twitter API calls
        response, content = authorized_client.request(
            uri, method)
        if response.status != 200:
            print("An error occurred when searching!")

        return json.loads(content.decode('utf-8'))
