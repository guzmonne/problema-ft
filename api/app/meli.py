import os
from urllib.parse import urlencode
import requests
from meli.rest import ApiException

class Meli(object):
    host="https://api.mercadolibre.com"
    response_type="code"
    grant_type="authorization_code"
    client_id=os.environ.get("MELI_APP_ID")
    client_secret=os.environ.get("MELI_SECRET_KEY")
    redirect_uri=f"https://{os.environ.get('DOMAIN')}/api/callback"
    code=None
    refresh_token=None
    user_id=None
    scope=None
    expires_in=None

    def __init__(self):
        pass

    @property
    def authorization_url(self):
        params = urlencode(dict(
            response_type=self.response_type,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri
        ))
        return f"https://auth.mercadolibre.com/authorization?{params}" 

    def get_authorization_token(self, code):
        url = "https://api.mercadolibre.com/oauth/token"
        data = dict(
            grant_type=self.grant_type,
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=self.redirect_uri,
        )
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        response = requests.post(url, data=data, headers=headers)
        data = response.json()
        self.access_token = data.get("access_token")
        self.token_type = data.get("token_type")
        self.expires_in = data.get("expires_in")
        self.scope = data.get("scope")
        self.user_id = data.get("user_id")
        self.refresh_token = data.get("refresh_token")
        return "Done. You can start using the app"

    def get_token(self):
        try:
            print(self.authorization_url)
            requests.get(self.authorization_url) 
        except ApiException as e:
            print("Exception when calling OAuth20Api->get_token: %s\n" % e)

    def get_item(self, item_id):
        response = requests.get(self.host + f"/items/{item_id}", params=dict(
            access_token=self.access_token
        ))
        return response.json()
