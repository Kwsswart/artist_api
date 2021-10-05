from app import db

class Users(db.Model):
    """
    User database model
    """

    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd

    def __repr__(self):
        return "<User: Username - {}; email - {}; password - {};>".format(self.username, self.email, self.pwd)


class artists(db.Model):
    
    __table_args__ = {'extend_existing': True}
    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

    album = db.relationship('albums', backref='artist', lazy='dynamic')
    artist_image = db.Column(db.String(10000), nullable=True)
    
    def __init__(self, name, artist_image=None):
        self.artist_image = artist_image
        self.Name = name
        
    def as_dict(self):
        return {'ArtistId': self.ArtistId, 'Name': self.Name, 'artist_image': self.artist_image}


    def __repr__(self):
        return "<Artist: Name - {}>".format(self.Name)


class albums(db.Model):
    
    __table_args__ = {'extend_existing': True}
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(120), nullable=False)
    ArtistId = db.Column(db.Integer, db.ForeignKey("artists.ArtistId"), nullable=False)
    Artist = db.relationship('artists', foreign_keys=ArtistId)
    track = db.relationship('tracks', backref='album', lazy='dynamic')

    def __init__(self, title, artist):
        self.Name = title
        self.Artist = artist
        
    def as_dict(self):
        return {'AlbumId': self.AlbumId, 'Title': self.Title, 'Artist': self.Artist.as_dict()}


    def __repr__(self):
        return "<Album: Name - {}; Artist - {}>".format(self.Title, self.Artist)


class genres(db.Model):
    
    __table_args__ = {'extend_existing': True}
    GenreId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))
    track = db.relationship('tracks', backref='genre', lazy='dynamic')
    
    def __init__(self, name):
        self.Name = name
        
    def as_dict(self):
        return {'GenreId': self.GenreId, 'name': self.Name}

    def __repr__(self):
        return "<Genre: Name - {}>".format(self.Name, )


class media_types(db.Model):
    
    __table_args__ = {'extend_existing': True}
    MediaTypeId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))
    track = db.relationship('tracks', backref='media_type', lazy='dynamic')

    def __init__(self, name):
        self.Name = name

    def as_dict(self):
        return {'MediaTypeId': self.MediaTypeId, 'name': self.Name}
    
    def __repr__(self):
        return "<Media Type: Name - {}>".format(self.Name)


class tracks(db.Model):
    
    __table_args__ = {'extend_existing': True}
    TrackId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    AlbumId = db.Column(db.Integer, db.ForeignKey("albums.AlbumId"))
    Album = db.relationship('albums', foreign_keys=AlbumId)
    MediaTypeId = db.Column(db.Integer, db.ForeignKey("media_types.MediaTypeId"), nullable=False)
    MediaType = db.relationship('media_types', foreign_keys=MediaTypeId)
    GenreId = db.Column(db.Integer, db.ForeignKey("genres.GenreId"))
    Genre = db.relationship('genres', foreign_keys=GenreId)
    Composer = db.Column(db.String(220))
    Milliseconds = db.Column(db.Integer, nullable=False)
    Bytes = db.Column(db.Integer)
    UnitPrice = db.Column(db.Numeric(), nullable=False)

    def __init__(self, name, album, media_type, genre, composer, milliseconds, bytes, unit_price):
        self.Name = name
        self.Album = album
        self.MediaType = media_type
        self.Genre = genre
        self.Composer = composer
        self.Milliseconds = milliseconds
        self.Bytes = bytes
        self.UnitPrice = unit_price
   
    def as_dict(self):
        return {'TrackId': self.TrackId, 'name': self.Name, 'album': self.Album.as_dict(), 'media_type': self.MediaType.as_dict(), 'genre': self.Genre.as_dict(), 'composer': self.Composer, 'milliseconds': self.Milliseconds, 'bytes': self.Bytes, 'unit_price': self.UnitPrice}

    def __repr__(self):
        return "<Track: Name - {}; Album - {}; Media Type - {}; Genre - {}; Composer - {}; Milliseconds - {}; Bytes - {}; Unit_Price - {}>".format(self.Name, self.Album, self.MediaType, self.Genre, self.Composer, self.Milliseconds, self.Bytes, self.UnitPrice)



class InvalidToken(db.Model):
    """
    Blacklisted token storage
    """

    __tablename__ = "invalid_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_invalid(cls, jti):
        """ Determine whether the jti key is on the blocklist return bool"""
        q = cls.query.filter_by(jti=jti).first()
        return bool(q)
    
