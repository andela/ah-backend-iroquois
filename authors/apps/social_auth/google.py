import os

from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleAuth:

    @staticmethod
    def validate(auth_token):
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request(),
                                                   os.environ.get("GOOGLE_OAUTH2_KEY", None))

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            return id_info
        except ValueError:
            # Invalid token
            return "The token is either invalid or has expired"
