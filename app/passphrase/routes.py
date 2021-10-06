import re
from app import db
from app.passphrase import bp
from app.models import tracks, albums, artists
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@bp.route("/passphrase/basic", methods=["POST"])
def passphrase_basic():
    """
    End-point assess basic list of passphrases.
    - Expecting list: 'aa bb cc dd ee\naa bb cc dd aa\naa bb cc dd aaa'
    
    Usage:
    $ curl -X POST -H "Content-Type: application/json" -d '{"passphrases": "aa bb cc dd ee\naa bb cc dd aa\naa bb cc dd aaa"}' "http://localhost:5000/passphrase/basic"
    """

    number_valid = 0
    phrases = request.json['passphrases'].strip()
    for phrase in phrases.split("\n"):
        if len(phrase.split()) == len(list(set(phrase.split()))):
            number_valid += 1
    return jsonify({'number_valid_passphrases': number_valid})


@bp.route("/passphrase/advanced", methods=["POST"])
def passphrase_advanced():
    """
    End-point assess basic list of passphrases.
    - Expecting list: 'abcde fghij\nabcde xyz ecdab\na ab abc abd abf abj\niiii oiii ooii oooi oooo\noiii ioii iioi iiio'
    
    Usage:
    $ curl -X POST -H "Content-Type: application/json" -d '{"passphrases": "abcde fghij\nabcde xyz ecdab\na ab abc abd abf abj\niiii oiii ooii oooi oooo\noiii ioii iioi iiio"}' "http://localhost:5000/passphrase/advanced"
    """
    
    number_valid = 0
    phrases = request.json['passphrases'].strip()
    
    for phrase in phrases.split("\n"):
        phras = [''.join(sorted(ph)) for ph in phrase.split()]
        if len(phras) == len(list(set(phras))):
            number_valid += 1    
    
    return jsonify({'number_valid_passphrases': number_valid})

    