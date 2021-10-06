import os
from app import db
from app.main import bp
from app.models import tracks, albums, artists
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@bp.route("/api/get_artists", methods=["GET"])
def get_artists():
    """
    End-point to return a list of artists.
    Usage:
    $ curl "http://localhost:5000/api/get_artists"
    """   

    return jsonify([artist.as_dict_with_images() for artist in artists.query.all()])


@bp.route("/api/albums", methods=["GET"])
@jwt_required() 
def get_albums():
    """
    End-point to return list of albums along with their tracks.
    Usage:
    $ curl -H "Authorization: Bearer <JWT_KEY>" "http://localhost:5000/api/albums"
    """

    try:
        albums_list = [{
            'album':a.as_dict(),
            "tracks": [track.as_dict() for track in tracks.query.filter(tracks.AlbumId==a.AlbumId).all()]} 
                       for a in albums.query.all()]
        return jsonify(albums_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@bp.route("/api/artist_albums/<artist_id>", methods=["GET"])
@jwt_required()
def get_artist_albums(artist_id):
    """
    End-point to return list of albums from a specific artist.
    Usage:
    $ curl -H "Authorization: Bearer <JWT_KEY>" "http://localhost:5000/api/artist_albums/<id>"
    i.e: 
    $ curl -H "Authorization: Bearer <JWT_KEY>" "http://localhost:5000/api/artist_albums/1"
    """
    
    try:
        return jsonify([album.as_dict() for album in albums.query.filter(albums.ArtistId==artists.query.get(artist_id).ArtistId).all()])
    except Exception as e:
        return jsonify({"error": str(e)})


@bp.route("/api/albums_detailed", methods=["GET"])
@jwt_required()
def get_detailed_albums():
    """
    End-point to return list of albums from a specific artist.
    Usage:
    $ curl -H "Authorization: Bearer <JWT_KEY>" "http://localhost:5000/api/albums_detailed"
    """
    
    try:
        albums_list = [{
            'album': a.as_dict(),
            "tracks": [track.as_dict() for track in tracks.query.filter(tracks.AlbumId==a.AlbumId).all()]} 
                       for a in albums.query.all()]
        for album in albums_list:
            try:
                
                album.update({
                    'track_count': len(album['tracks']), 
                    'total_duration': sum([track['milliseconds'] for track in album['tracks']]),
                    'longest_track_duration':sorted([album['milliseconds'] for album in album['tracks']])[-1],
                    'shortest_track_duration':sorted([album['milliseconds'] for album in album['tracks']])[0],
                    })
                del album['tracks']
            except: pass
        return jsonify(albums_list)
    except Exception as e:
        return jsonify({"error": str(e)})
  
