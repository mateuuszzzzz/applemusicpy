"""
Module implements different resource objects
"""


class Albums:

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
            self._genreNames = list(attributes.get('genreNames'))
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
                self._href = albumsArtistsRelationship.get('href')
                self._next = albumsArtistsRelationship.get('next')
                self._data = [Artists(artist) for artist in albumsArtistsRelationship.get('data')]

        class AlbumsGenresRelationship:
            def __init__(self, albumsGenresRelationship : dict):
                self._href = albumsGenresRelationship.get('href')
                self._next = albumsGenresRelationship.get('next')
                self._data = [Genres(genre) for genre in albumsGenresRelationship.get('data')]
        
        class AlbumsTracksRelationship:
            def __init__(self, albumsTracksRelationship : dict):
                self._data = [
                    Songs(track) if track.get('type') == 'songs' else MusicVideos(track) 
                    for track in albumsTracksRelationship.get('data')
                ]
                self._href = albumsTracksRelationship.get('href')
                self._next = albumsTracksRelationship.get('next')

        class AlbumsLibraryRelationship:
            def __init__(self, albumsLibraryRelationship : dict):
                self._href = albumsLibraryRelationship.get('href')
                self._next = albumsLibraryRelationship.get('next')
                self._data = [LibraryAlbums(album) for album in albumsLibraryRelationship.get('data')]

        class AlbumsRecordLabelsRelationship:
            def __init__(self, albumsRecordLabelsRelationship : dict):
                self._href = albumsRecordLabelsRelationship.get('href')
                self._next = albumsRecordLabelsRelationship.get('next')
                self._data = [RecordLabels(label) for label in albumsRecordLabelsRelationship.get('data')]

        def __init__(self, relationships : dict):
            self._artists = self.AlbumsArtistsRelationship(relationships.get('artists'))
            self._genres = self.AlbumsGenresRelationship(relationships.get('genres'))
            self._tracks = self.AlbumsTracksRelationship(relationships.get('tracks'))
            self._library = self.AlbumsLibraryRelationship(relationships.get('library'))
            self._record_labels = self.AlbumsRecordLabelsRelationship(relationships.get('record-labels'))

    class Views:

        class AlbumsAppearsOnView:

            class Attributes:
                def __init__(self, attributes : dict):
                    self._title = attributes.get('title')

            def __init__(self, albumsAppearsOnView : dict):
                self._href = albumsAppearsOnView.get('href')
                self._next = albumsAppearsOnView.get('next')
                self._attributes = self.Attributes(albumsAppearsOnView.get('attributes'))
                self._data = [Playlists(playlist) for playlist in albumsAppearsOnView.get('data')]

        class AlbumsOtherVersionsView:

            class Attributes:
                def __init__(self, attributes : dict):
                    self._title = attributes.get('title')

            def __init__(self, albumsOtherVersionsView : dict):
                self._href = albumsOtherVersionsView.get('href')
                self._next = albumsOtherVersionsView.get('next')
                self._attributes = self.Attributes(albumsOtherVersionsView.get('attributes'))
                self._data = [Albums(album) for album in albumsOtherVersionsView.get('data')]
        
        class AlbumsRelatedAlbumsView:

            class Attributes:
                def __init__(self, attributes : dict):
                    self._title = attributes.get('attributes')

            def __init__(self, albumsRelatedVersionsView : dict):
                self._href = albumsRelatedVersionsView.get('href')
                self._next = albumsRelatedVersionsView.get('next')
                self._attributes = self.Attributes(albumsRelatedVersionsView.get('attributes'))
                self._data = [Albums(album) for album in albumsRelatedVersionsView.get('data')]

        class AlbumsRelatedVideosView:

            class Attributes:
                def __init__(self, attributes : dict):
                    self._title = attributes.get('attributes')
            
            def __init__(self, albumsRelatedVideosView : dict):
                self._href = albumsRelatedVideosView.get('href')
                self._next = albumsRelatedVideosView.get('next')
                self._attributes = self.Attributes(albumsRelatedVideosView.get('attributes'))
                self._data = [MusicVideos(music_video) for music_video in albumsRelatedVideosView.get('data')]

        def __init__(self, views : dict):
            self._appears_on = self.AlbumsAppearsOnView(views.get('appears-on'))
            self._other_versions = self.AlbumsOtherVersionsView(views.get('other-versions'))
            self._related_albums = self.AlbumsRelatedAlbumsView(views.get('related-albums'))
            self._related_videos = self.AlbumsRelatedVideosView(views.get('related-videos'))

    def __init__(self, albums : dict):
        self._id = albums.get('id')
        self._type = albums.get('type')
        self._href = albums.get('href')

        self._attributes = self.Attributes(albums.get('attributes'))
        self._relationships = self.Relationships(albums.get('relationships'))
        self._views = self.Views(albums.get('views'))


class LibraryAlbums:

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

        class PlayParameters:
            def __init__(self, playParams : dict):
                self._id = playParams.get('id')
                self._kind = playParams.get('kind')

        def __init__(self, attributes : dict):
            self._artistName = attributes.get('artistName')
            self._artwork = self.Artwork(attributes.get('artwork'))
            self._contentRating = attributes.get('contentRating')
            self._dateAdded = attributes.get('dateAdded')
            self._name = attributes.get('name')
            self._playParams = self.PlayParameters(attributes.get('playParams'))
            self._releaseDate = attributes.get('releaseDate')
            self._trackCount = attributes.get('trackCount')
            self._genreNames = list(attributes.get('genreNames'))

    class Relationships:

        class LibraryAlbumsArtistsRelationship:
            def __init__(self, libraryAlbumsArtistsRelationship : dict):
                self._href = libraryAlbumsArtistsRelationship.get('href')
                self._next = libraryAlbumsArtistsRelationship.get('next')
                self._data = [LibraryArtists(library_artist) for library_artist in libraryAlbumsArtistsRelationship.get('data')]

        class LibraryAlbumsCatalogRelationship:
            def __init__(self, libraryAlbumsCatalogRelationship : dict):
                self._href = libraryAlbumsCatalogRelationship.get('href')
                self._next = libraryAlbumsCatalogRelationship.get('next')
                self._data = [Albums(album) for album in libraryAlbumsCatalogRelationship.get('data')]

        class LibraryAlbumsTracksRelationship:
            def __init__(self, libraryAlbumsTracksRelationship : dict):
                self._href = libraryAlbumsTracksRelationship.get('href')
                self._next = libraryAlbumsTracksRelationship.get('next')
                self._data = [
                    LibrarySongs(track) if track.get('type') == 'library-songs' else LibraryMusicVideos(track) 
                    for track in libraryAlbumsTracksRelationship
                ]

        def __init__(self, relationships : dict):
            self._artists = self.LibraryAlbumsArtistsRelationship(relationships.get('artists'))
            self._catalog = self.LibraryAlbumsCatalogRelationship(relationships.get('catalog'))
            self._tracks = self.LibraryAlbumsTracksRelationship(relationships.get('tracks'))

    def __init__(self, libraryAlbums : dict):
        self._id = libraryAlbums.get('id')
        self._type = libraryAlbums.get('type')
        self._href = libraryAlbums.get('href')

        self._attributes = self.Attributes(libraryAlbums.get('attributes'))
        self._relationships = self.Relationships(libraryAlbums.get('relationships'))

class Artists:

    class Attributes:
        pass

    class Relationships:
        pass

    class Views:
        pass

    def __init__(self, artists : dict):
        self._id = artists.get('id')
        self._type = artists.get('type')
        self._href = artists.get('href')


class LibraryArtists:
    def __init__(self, resource : dict):
        self.resource = resource

class Songs:
    def __init__(self, resource : dict):
        self.resource = resource

class LibrarySongs:
    def __init__(self, resource : dict):
        self.resource = resource

class MusicVideos:
    def __init__(self, resource : dict):
        self.resource = resource

class LibraryMusicVideos:
    def __init__(self, resource : dict):
        self.resource = resource

class Playlists:
    def __init__(self, resource : dict):
        self.resource = resource

class Stations:
    def __init__(self, resource : dict):
        self.resource = resource

class Genres:
    def __init__(self, resource : dict):
        self.resource = resource

class RecordLabels:
    def __init__(self, resource : dict):
        self.resource = resource