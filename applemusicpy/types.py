"""
Module implements different resources types
"""


class RequestData:
    def __init__(self, request : dict):
        self.resources = {
            'albums': [],
            'library-albums': [],
            'artists': [],
            'library-artists': [],
            'songs': [],
            'library-songs': [],
            'music-videos': [],
            'library-music-videos': [],
            'playlists': [],
            'library-playlists': [],
            'stations': [],
        }

        self.next = request.get('next')

        for resource in request.get('data'):
            type = resource.get('type')
            if type == 'albums':
                self.resources['albums'].append(Album(resource))
            elif type == 'library-albums':
                self.resources['library-albums'].append(Album(resource))
            elif type == 'artists':
                self.resources['artists'].append(Artist(resource))
            elif type == 'library-artists':
                self.resources['library-artists'].append(Artist(resource))
            elif type == 'songs':
                self.resources['songs'].append(Song(resource))
            elif type == 'library-songs':
                self.resources['library-songs'].append(Song(resource))
            elif type == 'music-videos':
                self.resources['music_videos'].append(MusicVideo(resource))
            elif type == 'library-music-videos':
                self.resources['library-music-videos'].append(MusicVideo(resource))
            elif type == 'playlists':
                self.resources['playlists'].append(Playlist(resource))
            elif type == 'library-playlists':
                self.resources['library-playlists'].append(Playlist(resource))
            elif type == 'stations':
                self.resources['stations'].append(Station(resource))

    def get_albums(self):
        return self.resources['albums']

    def get_library_albums(self):
        return self.resources['library-albums']

    def get_artists(self):
        return self.resources['artists']

    def get_library_artists(self):
        return self.resources['library-artists']

    def get_songs(self):
        return self.resources['songs']

    def get_library_songs(self):
        return self.resources['library-songs']

    def get_music_videos(self):
        return self.resources['music-videos']

    def get_library_music_videos(self):
        return self.resources['library-music-videos']

    def get_playlists(self):
        return self.resources['playlists']

    def get_library_playlists(self):
        return self.resources['library-playlists']

    def get_stations(self):
        return self.resources['stations']
        

class Album:

    class Attributes:

        class Artwork:
            def __init__(self, artwork : dict):
                self._bgColor = artwork.get('bgColor')
                self._height = artwork.get('height')
                self._width = artwork.get('width')
                self._textColor1 = artwork.get('textColor1')
                self._textColor2 = artwork.get('textColor2')
                self._textColor3 = artwork.get('textColor3')
                self._textColor4 = artwork.get('textColor4')
                self._url = artwork.get('url')

        class EditorialNotes:
            def __init__(self, editorialNotes : dict):
                self._short = editorialNotes.get('short')
                self._standard = editorialNotes.get('standard')
                self._name = editorialNotes.get('name')
                self._tagline = editorialNotes.get('tagline')

        class PlayParameters:
            def __init__(self, playParams : dict):
                self._id = playParams.get('id')
                self._kind = playParams.get('kind')

        def __init__(self, attributes : dict):
            self._artistName = attributes.get('artistName')
            self._artistUrl = attributes.get('artistUrl')
            self._artwork = self.Artwork(attributes.get('artwork'))
            self._contentRating = attributes.get('contentRating')
            self._copyright = attributes.get('copyright')
            self._editorialNotes = self.EditorialNotes(attributes.get('editorialNotes'))
            self._genreNames = attributes.get('genreNames')
            self._isCompilation = attributes.get('isCompilation')
            self._isComplete = attributes.get('isComplete')
            self._isMasteredForItunes = attributes.get('isMasteredForItunes')
            self._isSingle = attributes.get('isSingle')
            self._name = attributes.get('name')
            self._playParams = self.PlayParameters(attributes.get('playParams'))
            self._recordLabel = attributes.get('recordLabel')
            self._releaseDate = attributes.get('releaseDate')
            self._trackCount = attributes.get('trackCount')
            self._upc = attributes.get('upc')
            self._url = attributes.get('url')

    class Relationships:

        class AlbumsArtistsRelationship:
            def __init__(self, albumsArtistsRelationship : dict):
                pass

        class AlbumsGenresRelationship:
            def __init__(self, albumsGenresRelationship : dict):
                pass
        
        class AlbumsTracksRelationship:
            def __init__(self, albumsTracksRelationship : dict):
                pass

        def __init__(self, relationships : dict):
            self._artists = relationships.get('artists')

    class Views:
        def __init__(self, views : dict):
            pass

    def __init__(self, resource : dict):
        self._id = resource.get('id')
        self._type = resource.get('type')
        self._href = resource.get('href')

        self._attributes = self.Attributes(resource.get('attributes'))
        self._relationships = self.Relationships(resource.get('relationships'))
        self._views = self.Views(resource.get('views'))

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property 
    def href(self):
        return self._href

    @property
    def attributes(self):
        return self._attributes

    @property
    def relationships(self):
        return self._relationships
    
    @property
    def views(self):
        return self._views


class Artist:
    def __init__(self, resource : dict):
        self.resource = resource

class Song:
    def __init__(self, resource : dict):
        self.resource = resource

class MusicVideo:
    def __init__(self, resource : dict):
        self.resource = resource

class Playlist:
    def __init__(self, resource : dict):
        self.resource = resource

class Station:
    def __init__(self, resource : dict):
        self.resource = resource