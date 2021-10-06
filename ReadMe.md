## Usage:

#### If running with the provided images and database follow the usage further below, else if running without provided images and database:
*Note: I have made it in a way that everything is functional with or without enriching the database*

Follow the folliwing steps to run the application:
1) Download the [Sample Database](https://www.sqlitetutorial.net/sqlite-sample-database/)
2) Extract and rename db to 'app_database.db' and place it within the cloned project route directory
3) Create a python environment and activate it.
4) Run:

```
pip install -r requirements.txt
```

5) Create a file called ".env" 
6) Run within a Python terminal:

```Python
>>> from cryptography.fernet import Fernet
>>> Fernet.generate_key().decode()
'key'
```

7) Open the ".env" file and copy the key and save the following variables:

```
FLASK_APP = api.py
KEY = "key"
```

8) Run within the route directory once environment is active:

```Python
flask db upgrade
```

9) Follow the steps indicated in testing to enrich the database and test the api


Testing the Application:

- Ensure the development server is running with:

```
flask run
```

- from a separate terminal run:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"username": "test2", "email": "email2@test.com", "pwd": "password"}' "http://localhost:5000/api/register"
```

- Once Registered take the 'token' from the responce to handle any requests that require login to receive:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"email": "email2@test.com", "pwd": "password"}' "http://localhost:5000/api/login"

{"refreshToken":"key","token":"key"}
```


- Run the spider to enrich the database: 

```
curl -H "Authorization: Bearer <key_from_earlier>" "http://localhost:5000/scraper/enrich_data"

```

- Unprotected artists endpoint:

```
$ curl "http://localhost:5000/api/get_artists"
```

- Protected albums with their songs endpoint:

```
$ curl -H "Authorization: Bearer <key_from_earlier>" "http://localhost:5000/api/albums"
```

- Protected list of albums from a artist endpoint:

```
$ curl -H "Authorization: Bearer <key_from_earlier>" "http://localhost:5000/api/artist_albums/<artist_id>"
```

- Protected list of albums with artist and details on albums endpoint:

```
$ curl -H "Authorization: Bearer <key_from_earlier>" "http://localhost:5000/api/albums_detailed"
```

- passphrase/basic end-point:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"passphrases": "aa bb cc dd ee\naa bb cc dd aa\naa bb cc dd aaa"}' "http://localhost:5000/passphrase/basic"
```

- passphrase/advanced end-point:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"passphrases": "abcde fghij\nabcde xyz ecdab\na ab abc abd abf abj\niiii oiii ooii oooi oooo\noiii ioii iioi iiio"}' "http://localhost:5000/passphrase/advanced"
```



## Usage with the provided images and database

1) Create a python environment and activate it.
2) Run: 

```
pip install -r requirements.txt
```

3) Create a file called ".env" 
4) Run within a Python terminal:

```Python
>>> from cryptography.fernet import Fernet
>>> Fernet.generate_key().decode()
'key'
```
5) Open the ".env" file and copy the key and save the following variables:
```
FLASK_APP = api.py
KEY = "key"
```

6) Follow the steps indicated in testing to enrich the database and test the api


*Note:* You do not need to enrich the database as it has already been done.

Testing the Application:

- Ensure the development server is running with 
```
flask run
```
- from a separate terminal run:
```
$ curl -X POST -H "Content-Type: application/json" -d '{"username": "test2", "email": "email2@test.com", "pwd": "password"}' "http://localhost:5000/api/register"

```

- Once Registered take the 'token' from the responce to handle any requests that require login to receive

```
$ curl -X POST -H "Content-Type: application/json" -d '{"email": "email2@test.com", "pwd": "password"}' "http://localhost:5000/api/login"

{"refreshToken":"key","token":"key"}
```


- Unprotected artists endpoint:

```
$ curl "http://localhost:5000/api/get_artists"
```

- Protected albums with their songs endpoint:

```
$ curl -H "Authorization: Bearer <key_from_earlier>" "http://localhost:5000/api/albums"
```

- Protected list of albums from a artist endpoint:

```
$ curl -H "Authorization: Bearer <key_from_earlier>" "http://localhost:5000/api/artist_albums/<artist_id>"
```

- Protected list of albums with artist and details on albums endpoint:

```
$ curl -H "Authorization: Bearer <key_from_earlier>" "http://localhost:5000/api/albums_detailed"
```

- passphrase/basic end-point:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"passphrases": "aa bb cc dd ee\naa bb cc dd aa\naa bb cc dd aaa"}' "http://localhost:5000/passphrase/basic"

```

- passphrase/advanced end-point:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"passphrases": "abcde fghij\nabcde xyz ecdab\na ab abc abd abf abj\niiii oiii ooii oooi oooo\noiii ioii iioi iiio"}' "http://localhost:5000/passphrase/advanced"
```


