import os
import base64
from app import db


def get_response_image(image_path):
    try:
        with open(image_path, 'rb') as f:
            img = f.read()
        return base64.encodebytes(img).decode('utf-8')
    except Exception as e:
        print(e)

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
    artist_image = db.relationship('ArtistImages', backref='artist', lazy='dynamic')
    
    def __init__(self, name):
        self.Name = name
        
    def get_image(self):
        try:
            encoded_img = get_response_image(os.path.join(os.getcwd(), "downloaded_images", f"{self.ArtistId}.jpg"))
        except Exception as e: 
            encoded_img =  None
        try:
            image_url = ArtistImages.query.filter(ArtistImages.ArtistId==self.ArtistId).first().as_dict()
        except Exception as e: 
            image_url = None
        return encoded_img, image_url
    
    def as_dict_with_images(self):
        try:
            encoded_img, image_url = self.get_image()
            
            return {'ArtistId': self.ArtistId, 'Name': self.Name, 'EncodedImage': encoded_img, "ImageUrl": image_url}
        except: return self.as_dict()

    def as_dict(self):
        
        return {'ArtistId': self.ArtistId, 'Name': self.Name}

    def __repr__(self):
        return "<Artist: Name - {}>".format(self.Name)


class ArtistImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    artist_image = db.Column(db.String(10000), nullable=True)
    
    ArtistId = db.Column(db.Integer, db.ForeignKey("artists.ArtistId"))
    
    def __init__(self, artist_image, artist_id):
        self.artist_image = artist_image
        self.ArtistId = artist_id
        
    def as_dict(self):
        return {'ArtistImageId': self.id, 'artist_image': self.artist_image}

    def __repr__(self):
        return "<Album: artist_image - {}>".format(self.artist_image)
    
    
class albums(db.Model):
    
    __table_args__ = {'extend_existing': True}
    
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(120), nullable=False)
    
    ArtistId = db.Column(db.Integer, db.ForeignKey("artists.ArtistId"), nullable=False)
    
    track = db.relationship('tracks', backref='album', lazy='dynamic')

    def __init__(self, title, artist):
        self.Name = title
        self.Artist = artist
        
    def as_dict(self):
        return {'AlbumId': self.AlbumId, 'Title': self.Title, 'Artist': artists.query.filter(artists.ArtistId==self.ArtistId).first().as_dict_with_images()}


    def __repr__(self):
        return "<Album: Name - {}; Artist - {}>".format(self.Title, artists.query.filter(artists.ArtistId==self.ArtistId).first().as_dict_with_images())


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
    MediaTypeId = db.Column(db.Integer, db.ForeignKey("media_types.MediaTypeId"), nullable=False)
    GenreId = db.Column(db.Integer, db.ForeignKey("genres.GenreId"))
    
    Composer = db.Column(db.String(220))
    Milliseconds = db.Column(db.Integer, nullable=False)
    Bytes = db.Column(db.Integer)
    UnitPrice = db.Column(db.Numeric(), nullable=False)

    def __init__(self, name, album, media_type, genre, composer, milliseconds, bytes, unit_price):
        self.Name = name
        self.AlbumId = album
        self.MediaTypeId = media_type
        self.GenreId = genre
        self.Composer = composer
        self.Milliseconds = milliseconds
        self.Bytes = bytes
        self.UnitPrice = unit_price
   
    def as_dict(self):
        return {
            'TrackId': self.TrackId, 
            'name': self.Name, 
            'album': albums.query.filter(albums.AlbumId==self.AlbumId).first().as_dict(), 
            'media_type':media_types.query.filter(media_types.MediaTypeId==self.MediaTypeId).first().as_dict(), 
            'genre': genres.query.filter(genres.GenreId==self.GenreId).first().as_dict(), 
            'composer': self.Composer, 
            'milliseconds': self.Milliseconds, 
            'bytes': self.Bytes, 
            'unit_price': self.UnitPrice}

    def __repr__(self):
        return "<Track: Name - {}; Album - {}; Media Type - {}; Genre - {}; Composer - {}; Milliseconds - {}; Bytes - {}; Unit_Price - {}>".format(
            self.Name, self.AlbumId, self.MediaTypeId, self.GenreId, self.Composer, self.Milliseconds, self.Bytes, self.UnitPrice)



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
    
