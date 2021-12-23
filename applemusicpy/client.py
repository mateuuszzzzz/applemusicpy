import requests
from requests.models import HTTPError
from .auth import AuthBase
from .auth import Auth

class Client:
    """
    Client class implements all endpoints described here:
    https://developer.apple.com/documentation/applemusicapi/
    """

    def __init__(self,
                auth: AuthBase=None,
                proxies=None,
                requests_session=True,
                max_retries=10, 
                requests_timeout=None,
                raw_json=False
                ):
        self.auth = auth
        self.proxies = proxies
        self.request_session = requests_session
        self.max_retries = max_retries
        self.requests_timeout = requests_timeout
        self.raw_json = raw_json
        self.request_root = 'https://api.music.apple.com/v1/'

        if requests_session:
            self._session = requests.Session()
        else:
            self._session = requests.api

    def _catalog_headers(self):
        if self.auth.get_developer_token() is None:
            self.auth.generate_developer_token()

        return {'Authorization': 'Bearer {}'.format(self.auth.get_developer_token())}

    def _library_headers(self):
        if self.auth.get_developer_token() is None or self.auth.is_token_expired():
            self.auth.generate_developer_token()
            self.auth.generate_user_token()
        
        if self.auth.get_user_token() is None:
            self.auth.generate_user_token()

        return {
            'Music-User-Token': '{}'.format(self.auth.get_user_token()),
            'Authorization': 'Bearer {}'.format(self.auth.get_developer_token())
        }

    def __call__(self, method, url, params, type):
        if type == 'catalog':
            headers = self._catalog_headers()
        elif type == 'library':
            headers = self._library_headers()
        else:
            print("ERROR")

        headers['Content-Type'] = 'application/json'

        retries = 0
        while retries < self.max_retries:
            try:
                result = self._session.request(method, 
                                                url, 
                                                headers=headers, 
                                                proxies=self.proxies, 
                                                params=params,
                                                timeout=self.requests_timeout)
                result.raise_for_status()
                return result.json()
            except HTTPError as e:
                pass #to do
            except Exception as e:
                pass
            retries = retries + 1

    def catalog_album(self, storefornt, id, params):
        pass

    def catalog_albums_relationship(self, storefront, id, relationship, params):
        pass

    def catalog_albums_relationship_view(self, storefront, id, view, params):
        pass

    def catalog_albums(self, storefront, params):
        #ids, filter[upc], filter[equivalent]
        pass

    def library_album(self, id, params):
        pass

    def library_albums_relationship(self, id, relationship, params):
        pass

    def library_albums(self, params):
        pass

    def add_resource(self, params):
        pass
    
