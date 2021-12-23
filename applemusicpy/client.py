from urllib.parse import urljoin
import requests
from requests.models import HTTPError
from .auth import AuthBase
from .auth import Auth
from .types import *

class ResourceType:
    CATALOG = 0
    LIBRARY = 1

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
        self.url_root = 'https://api.music.apple.com/v1/'

        if requests_session:
            self._session = requests.Session()
        else:
            self._session = requests.api

    def _get_catalog_headers(self):
        if self.auth.get_developer_token() is None:
            self.auth.generate_developer_token()

        return {'Authorization': 'Bearer {}'.format(self.auth.get_developer_token())}

    def _get_library_headers(self):
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
        if type == ResourceType.CATALOG:
            headers = self._get_catalog_headers()
        elif type == ResourceType.LIBRARY:
            headers = self._get_library_headers()
        else:
            print('ERROR')

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
    
    def _join(self, components):

        if type(components) is not list:
            return urljoin(self.url_root, components)

        url = self.url_root

        for component in components:
            url = urljoin(url, component) + '/'

        return url

    def album(self, 
                id, 
                storefront = 'en', 
                params = None, 
                type = ResourceType.CATALOG
            ):

        url = None
        
        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/albums/{id}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/albums/{id}')
        else:
            print('ERROR')

        return self.__call__('GET', url, params, type)

    def album_relationship(self, 
                            id, 
                            relationship, 
                            storefront = 'en', 
                            params = None, 
                            type = ResourceType.CATALOG
                        ):

        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/albums/{id}/{relationship}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/albums/{id}/{relationship}')
        else:
            print('ERROR')

        return self.__call__('GET', url, params, type)

    def album_relationship_view(self, 
                                id, 
                                view, 
                                storefront = 'en', 
                                params = None
                            ):
        url = self._join(f'catalog/{storefront}/albums/{id}/view/{view}')
        return self.__call__('GET', url, params, ResourceType.CATALOG)
    
    def albums(self, 
                storefront = 'en', 
                params = None, 
                type = ResourceType.CATALOG
            ):
        
        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/albums')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/albums')
        else:
            print('ERROR')
        
        return self.__call__('GET', url, params, type)

    def add_resource(self, params = None):
        url = self._join(f'me/library')
        return self.__call__('POST', url, params, ResourceType.LIBRARY)

    def artist(self, 
                id, 
                storefront = 'en', 
                params = None, 
                type = ResourceType.CATALOG
            ):

        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/artists/{id}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/artists/{id}')
        else:
            print('ERROR')
        
        return self.__call__('GET', url, params, type)

    def artists(self, 
                storefront = 'en', 
                params = None, 
                type = ResourceType.CATALOG
            ):
        
        url = None

        if type == ResourceType.CATALOG:
            url = self.__join(f'catalog/{storefront}/artists')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/artists')
        else:
            print('ERROR')

        return self.__call__('GET', url, params, type)

    def artist_relationship(self, 
                            id, 
                            relationship, 
                            storefront = 'en', 
                            params = None, 
                            type = ResourceType.CATALOG
                        ):
        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/artists/{id}/{relationship}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/artists/{id}/{relationship}')
        else:
            print('ERROR')

        return self.__call__('GET', url, params, type)

    def artist_relationship_view(self, 
                                id, 
                                view, 
                                storefront = 'en', 
                                params = None
                                ):
        
        url = self._join(f'catalog/{storefront}/artists/{id}/view/{view}')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def song(self, 
            id, 
            storefront = 'en', 
            params = None, 
            type = ResourceType.CATALOG
            ):
        
        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/songs/{id}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/songs/{id}')
        else:
            print('ERROR')

        return self.__call__('GET', url, params, type)

    def songs(self, 
                id, 
                storefront = 'en', 
                params = None, 
                type = ResourceType.CATALOG
            ):
        
        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/songs')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/songs')
        else:
            print('ERROR')

        return self.__call__('GET', url, params, type)

    def song_relationship(self, 
                            id, 
                            relationship, 
                            storefront = 'en', 
                            params = None, 
                            type = ResourceType.CATALOG
                        ):

        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/songs/{id}/{relationship}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/songs/{id}/{relationship}')

        return self.__call__('GET', url, params, type)

    def music_video(self, 
                    id, 
                    storefront = 'en', 
                    params = None, 
                    type = ResourceType.CATALOG
                    ):

        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/music-videos/{id}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/music-videos/{id}')
        else:
            print('ERROR')
        
        return self.__call__('GET', url, params, type)

    def music_videos(self, 
                        storefront = 'en', 
                        params = None, 
                        type = ResourceType.CATALOG
                    ):
        
        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/music-videos')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/music-videos')
        else:
            print('ERROR')

        return self.__call__('GET', url, params, type)

    #TO DO