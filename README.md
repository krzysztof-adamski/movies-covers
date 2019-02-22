# netguru-movies

*netguru-movies is a REST API application to allow on collection information about movies from external provider OMDB http://www.omdbapi.com*

You can:

  - search movie by title and save information about them on database
  - fetch list of all movies already present in application database and sort and filter the results 
  - you can view and comment on each video and also filter the results by pass movie ID
  - see the rank of movies according to the most frequently commented and filter the results by movie date

# Tasks:

### Movie database

We'd like you to build simple REST API for us - a basic movie database interacting with external API.
Here's full specification of endpoints that we'd like it to have:
* POST /api/movies:
    - Request body should contain only movie title, and its presence should be validated.
    - Based on passed title, other movie details should be fetched from http://www.omdbapi.com/ (or other similar, public movie database) - and saved to application database.
    - Request response should include full movie object, along with all data fetched from external API.
* GET /api/movies:
    - Should fetch list of all movies already present in application database.
    - Additional filtering, sorting is fully optional - but some implementation is a bonus
* POST /api/comments:
    - Request body should contain ID of movie already present in database, and comment text body.
    - Comment should be saved to application database and returned in request response.
* GET /api/comments:
    - Should fetch list of all comments present in application database.
    - Should allow filtering comments by associated movie, by passing its ID.
* GET /api/top:
    - Should return top movies already present in the database ranking based on a number of comments added to the movie (as in the example) in the specified date range. The response should include the ID of the movie, position in rank and total number of comments (in the specified date range).
    - Movies with the same number of comments should have the same position in the ranking.
    - Should require specifying a date range for which statistics should be generated.
    ### Example response:
    ```json
    [
        {
            "movie_id": 2,
            "total_comments": 4,
            "rank": 1
        },
        {
            "movie_id": 3,
            "total_comments": 2,
            "rank": 2
        },
        {
            "movie_id": 4,
            "total_comments": 2,
            "rank": 2
        },
        {
            "movie_id": 1,
            "total_comments": 0,
            "rank": 3
        }
    ]
    ```

### Rules & hints:
1. Your goal is to implement REST API in Django, however you're free to use any third-party libraries and database of your choice, but please share your reasoning behind choosing them.
2. At least basic tests of endpoints and their functionality are obligatory. Their exact scope and form is left up to you.
3. The application's code should be kept in a public repository so that we can read it, pull it and build it ourselves. Remember to include README file or at least basic notes on application requirements and setup - we should be able to easily and quickly get it running.
4. Written application must be hosted and publicly available for us online - we recommend Heroku.

# Installation:
You should have installed and configured: *[virtualenv][virtualenv]* or *[virtualenvwrapper][virtualenvwrapper]*

* application reguired OMDB_API_KEY to use external movie OMDB API, grab yourself http://www.omdbapi.com/apikey.aspx
* clone project from [public repository][git-repo-url] on GitHub.
* In ***local*** or ***production*** environment set up variables, install the dependencies and start the server.
```
set OMDB_API_KEY=<your_api_key>
set SECRET_KEY=<any random string>
set ENV=<local|prod> 
```
> some easie instruction to installation on local environment by Makefile:
```bash
git clone https://github.com/te0dor/netguru-movies.git
cd netguru-movies
make develop
make migrations
make start
```
> manual instruction to installation on local environment:
```bash
git clone https://github.com/te0dor/netguru-movies.git
cd netguru-movies
virtualenv --python=python3 env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
> run test:
```bash
make test
```
> check report:
```bash
make report
```

### Todos

 - Write MORE Tests
 

   [virtualenvwrapper]: <https://virtualenvwrapper.readthedocs.io/en/latest/>
   [virtualenv]: <https://virtualenv.pypa.io/en/latest/>
   [git-repo-url]: <https://github.com/te0dor/netguru-movies.git>
