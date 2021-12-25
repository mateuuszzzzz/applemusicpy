import json
from urllib.parse import urljoin
import requests
from requests.models import HTTPError

from applemusicpy.exceptions import ResourceTypeException
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

    def __call__(self, method, url, params, type = ResourceType.CATALOG, body = None):
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
                                                json=body,
                                                proxies=self.proxies, 
                                                params=params,
                                                timeout=self.requests_timeout)
                result.raise_for_status()
                if result.status_code == 204:
                    return result
                return result.json()
            except HTTPError as e:
                print(e)
            except Exception as e:
                print(e)
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
            raise ResourceTypeException()

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
            raise ResourceTypeException()

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
            raise ResourceTypeException()
        
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
            raise ResourceTypeException()
        
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
            raise ResourceTypeException()

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
            raise ResourceTypeException()

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
            raise ResourceTypeException()

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
            raise ResourceTypeException()

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
            raise ResourceTypeException()
        
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
            raise ResourceTypeException()

        return self.__call__('GET', url, params, type)

    def music_video_relationship(self, 
                                id, 
                                relationship, 
                                storefront = 'en', 
                                params = None, 
                                type = ResourceType.CATALOG
                                ):

        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/music-videos/{id}/{relationship}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/music-videos/{id}/{relationship}')
        else:
            raise ResourceTypeException()

        return self.__call__('GET', url, params, type)

    def music_video_relationship_view(self, 
                                        id, 
                                        view, 
                                        storefront = 'en', 
                                        params = None
                                    ):

        url = self._join(f'catalog/{storefront}/music-videos/{id}/view/{view}')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def playlist(self, 
                id, 
                storefront = 'en', 
                params = None, 
                type = ResourceType.CATALOG
                ):

        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/playlists/{id}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/playlists/{id}')
        else:
            raise ResourceTypeException()

        return self.__call__('GET', url, params, type)

    def playlists(self, 
                    storefront = 'en', 
                    params = None, 
                    type = ResourceType.CATALOG
                ):

        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/playlists')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/playlists')
        else:
            raise ResourceTypeException()

        return self.__call__('GET', url, params, type)

    def playlist_relationship(self, 
                                id, 
                                relationship, 
                                storefront = 'en', 
                                params = None, 
                                type = ResourceType.CATALOG
                            ):
        
        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/playlists/{id}/{relationship}')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/playlists/{id}/{relationship}')
        else:
            raise ResourceTypeException()

        return self.__call__('GET', url, params, type)

    def playlist_relationship_view(self, id, view, storefront = 'en', params = None):
        
        url = self._join(f'catalog/{storefront}/playlists/{id}/view/{view}')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def create_playlist(self, body = None, params = None):

        url = self._join(f'me/library/playlists')
        return self.__call__('POST', url, params, ResourceType.LIBRARY, body)

    def add_tracks_to_playlist(self, id, body = None, params = None):

        url = self._join(f'me/library/playlists/{id}/tracks')
        return self.__call__('POST', url, params, ResourceType.LIBRARY, body)

    def playlist_folder(self, id, params = None):
        
        url = self._join(f'me/library/playlist-folders/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def playlist_folders(self, params = None):

        url = self._join(f'me/library/playlist-folders')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def playlist_folder_relationship(self, id, relationship, params = None):

        url = self._join(f'me/library/playlist-folders/{id}/{relationship}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def create_playlist_folder(self, body = None, params = None):

        url = self._join(f'me/library/playlist-folders')
        return self.__call__('POST', url, params, ResourceType.LIBRARY, body)
    
    def station(self, id, storefront = 'en', params = None):
        
        url = self._join(f'catalog/{storefront}/stations/{id}')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def stations(self, storefront = 'en', params = None):

        url = self._join(f'catalog/{storefront}/stations')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def station_genre(self, id, storefront = 'en', params = None):

        url = self._join(f'catalog/{storefront}/station-genres/{id}')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def station_genres(self, storefront = 'en', params = None):

        url = self._join(f'catalog/{storefront}/station-genres')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def station_genre_relationship(self, id, relationship, storefront = 'en', params = None):

        url = self._join(f'catalog/{storefront}/station-genres/{id}/{relationship}')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def search(self, storefront = 'en', params = None, type = ResourceType.CATALOG):
        
        url = None

        if type == ResourceType.CATALOG:
            url = self._join(f'catalog/{storefront}/search')
        elif type == ResourceType.LIBRARY:
            url = self._join(f'me/library/search')
        else:
            raise ResourceTypeException()

        return self.__call__('GET', url, params, type)

    def hints(self, storefront = 'en', params = None):

        url = self._join(f'catalog/{storefront}/search/hints')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def suggestions(self, storefront = 'en', params = None):

        url = self._join(f'catalog/{storefront}/search/suggestions')
        return self.__call__('GET', url, params, ResourceType.CATALOG)

    def personal_album_rating(self, id, params = None):

        url = self._join(f'me/ratings/albums/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_music_video_rating(self, id, params = None):

        url = self._join(f'me/ratings/music-videos/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_playlist_rating(self, id, params = None):

        url = self._join(f'me/ratings/playlists/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_song_rating(self, id, params = None):

        url = self._join(f'me/ratings/songs/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_station_rating(self, id, params = None):

        url = self._join(f'me/ratings/stations/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_album_ratings(self, params = None):

        url = self._join(f'me/ratings/albums')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_music_video_ratings(self, params = None):

        url = self._join(f'me/ratings/music-videos')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_playlist_ratings(self, params = None):

        url = self._join(f'me/ratings/playlists')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_song_ratings(self, params = None):

        url = self._join(f'me/ratings/songs')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_station_ratings(self, params = None):

        url = self._join(f'me/ratings/stations')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def add_personal_album_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/albums/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_music_video_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/music-videos/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_playlist_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/playlists/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_song_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/songs/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_station_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/stations/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def delete_personal_album_rating(self, id, params = None):

        url = self._join(f'me/ratings/albums/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_music_video_rating(self, id, params = None):

        url = self._join(f'me/ratings/music-videos/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_playlist_rating(self, id, params = None):

        url = self._join(f'me/ratings/playlists/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_song_rating(self, id, params = None):

        url = self._join(f'me/ratings/songs/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_station_rating(self, id, params = None):

        url = self._join(f'me/ratings/stations/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    #personal library ratings

    def personal_library_album_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-albums/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_music_video_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-music-videos/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_playlist_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-playlists/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_song_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-songs/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_station_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-stations/{id}')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_album_ratings(self, params = None):

        url = self._join(f'me/ratings/library-albums')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_music_video_ratings(self, params = None):

        url = self._join(f'me/ratings/library-music-videos')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_playlist_ratings(self, params = None):

        url = self._join(f'me/ratings/library-playlists')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_song_ratings(self, params = None):

        url = self._join(f'me/ratings/library-songs')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def personal_library_station_ratings(self, params = None):

        url = self._join(f'me/ratings/library-stations')
        return self.__call__('GET', url, params, ResourceType.LIBRARY)

    def add_personal_library_album_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/library-albums/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_library_music_video_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/library-music-videos/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_library_playlist_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/library-playlists/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_library_song_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/library-songs/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def add_personal_library_station_rating(self, id, body, params = None):

        url = self._join(f'me/ratings/library-stations/{id}')
        return self.__call__('PUT', url, params, ResourceType.LIBRARY, body)

    def delete_personal_library_album_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-albums/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_library_music_video_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-music-videos/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_library_playlist_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-playlists/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_library_song_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-songs/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)

    def delete_personal_library_station_rating(self, id, params = None):

        url = self._join(f'me/ratings/library-stations/{id}')
        return self.__call__('DELETE', url, params, ResourceType.LIBRARY)