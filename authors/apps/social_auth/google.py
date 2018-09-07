import os

from google.auth.exceptions import RefreshError
from google.auth.transport import requests
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials


class GoogleAuth:

    @staticmethod
    def validate(auth_token, refresh_token=None, access_token=None):
        try:
            token_uri = "https://accounts.google.com/o/oauth2/token"
            key = os.environ.get("GOOGLE_API_KEY", None)
            secret = os.environ.get("GOOGLE_API_SECRET", None)

            credentials = Credentials(access_token, refresh_token=refresh_token, id_token=auth_token,
                                      token_uri=token_uri, client_id=key, client_secret=secret)
            # and now we refresh the token
            # but not if we know that its not a valid token.
            request = requests.Request()
            try:
                credentials.refresh(request)
            except RefreshError:
                pass

            auth_token = credentials.id_token

            # Specify the CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request(),
                                                   os.environ.get("GOOGLE_API_KEY", None))

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            return id_info
        except ValueError:
            # Invalid token
            return "The token is either invalid or has expired"
