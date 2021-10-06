from app import db
from app.scraper import bp
from app.models import ArtistImages, artists
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from app.scraper.spider import *


@bp.route("/scraper/enrich_data", methods=["GET"])
@jwt_required()
def enrich_data():
    """
    End-point to start the process of enriching the database
    Usage:
    $ curl -H "Authorization: Bearer <JWT_KEY>" "http://localhost:5000/scraper/enrich_data"
    """
    
    try:
        scraper = Spider(seedlist=[artist.as_dict() for artist in artists.query.all()])
        seedlist = scraper.run()
        
        for seed in seedlist:    
            artist = artists.query.filter_by(ArtistId=seed['ArtistId']).first()
            img = ArtistImages(seed['artist_image'], artist.ArtistId) 
            db.session.add(img)
            db.session.commit()       
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})



    