[![Build Status](https://travis-ci.org/andela/ah-backend-iroquois.svg?branch=develop)](https://travis-ci.org/andela/ah-backend-iroquois)
[![Coverage Status](https://coveralls.io/repos/github/andela/ah-backend-iroquois/badge.svg)](https://coveralls.io/github/andela/ah-backend-iroquois)
[![Maintainability](https://api.codeclimate.com/v1/badges/a4febbe130449a1e59a7/maintainability)](https://codeclimate.com/github/andela/ah-backend-iroquois/maintainability)

Authors Haven - A Social platform for the creative at heart.
=======

## Vision
Create a community of like minded authors to foster inspiration and innovation
by leveraging the modern web.

---

## API Spec
The preferred JSON object to be returned by the API should be structured as follows:

### Users (for authentication)

```source-json
{
  "user": {
    "email": "jake@jake.jake",
    "token": "jwt.token.here",
    "username": "jake",
    "bio": "I work at statefarm",
    "image": null
  }
}
```
### Profile
```source-json
{
  "profile": {
    "username": "jake",
    "bio": "I work at statefarm",
    "image": "image-link",
    "following": false
  }
}
```
### List of Users with their profiles
```source-json
{
  "users": [
    {
      "email": "jake@jake.jake",
      "username": "jake",
      "profile": {
        "username": "jake",
        "bio": "I work at statefarm",
        "image": "image-link",
        "following": false
      }
  },
  {
    "email": "jake2@jake2.jake",
      "username": "jake2",
      "profile": {
        "username": "jake2",
        "bio": "I work at statefarm2",
        "image": "image-link2",
        "following": false
      }
  }
  ]
}
```
### Single Article
```source-json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```
### Multiple Articles
```source-json
{
  "articles":[{
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }, {

    "slug": "how-to-train-your-dragon-2",
    "title": "How to train your dragon 2",
    "description": "So toothless",
    "body": "It a dragon",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }],
  "articlesCount": 2
}
```
### Single Comment
```source-json
{
  "comment": {
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```
### Multiple Comments
```source-json
{
  "comments": [{
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }],
  "commentsCount": 1
}
```
### List of Tags
```source-json
{
  "tags": [
    "reactjs",
    "angularjs"
  ]
}
```
### Errors and Status Codes
If a request fails any validations, expect errors in the following format:

```source-json
{
  "errors":{
    "body": [
      "can't be empty"
    ]
  }
}
```
### Other status codes:
401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request


Endpoints:
----------

### Authentication:

`POST /api/users/login`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `password`

### Registration:

`POST /api/users`

Example request body:

```source-json
{
  "user":{
    "username": "Jacob",
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `username`, `password`

### Get Current User

`GET /api/user`

Authentication required, returns a User that's the current user

### Update User

`PUT /api/user`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "bio": "I like to skateboard",
    "image": "https://i.stack.imgur.com/xHWG8.jpg"
  }
}
```

Authentication required, returns the User

Accepted fields: `email`, `username`, `password`

### Get Profile

`GET /api/profiles/:username`

Authentication optional, returns a Profile

### Follow user

`POST /api/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### Unfollow user

`DELETE /api/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

## Invoke a password reset

`POST /api/users/reset/password`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake"
  }
}
```
No authentication required, sends a password reset link to the email

Accepted fields: `email`


## Reset password

`PATCH /api/user/reset-password/<token>`

Example request body:

```source-json
{
  "user":{
    "password": "new_password"
  }
}
```
Authentication required, returns the User

Accepted fields: `email`, `username`, `password`

### List Articles

`GET /api/articles`

Returns most recent articles globally by default, provide `tag`, `author` or `favorited` query parameter to filter results

Query Parameters:

Filter by tag:

`?tag=AngularJS`

Filter by author:

`?author=jake`

Favorited by user:

`?favorited=jake`

Limit number of articles (default is 20):

`?limit=20`

Offset/skip number of articles (default is 0):

`?offset=0`

Authentication optional, will return multiple articles, ordered by most recent first

### Feed Articles

`GET /api/articles/feed`

Can also take `limit` and `offset` query parameters like List Articles

Authentication required, will return multiple articles created by followed users, ordered by most recent first.

### Get Article

`GET /api/articles/:slug`

No authentication required, will return single article

### Create Article

`POST /api/articles`

Example request body:

```source-json
{
  "article": {
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "tagList": ["reactjs", "angularjs", "dragons"]
  }
}
```

Authentication required, will return an Article

Required fields: `title`, `description`, `body`

Optional fields: `tagList` as an array of Strings

### Update Article

`PUT /api/articles/:slug`

Example request body:

```source-json
{
  "article": {
    "title": "Did you train your dragon?"
  }
}
```

Authentication required, returns the updated Article

Optional fields: `title`, `description`, `body`

The `slug` also gets updated when the `title` is changed

### Delete Article

`DELETE /api/articles/:slug`

Authentication required

### Add Comments to an Article

`POST /api/articles/:slug/comments`

Example request body:

```source-json
{
  "comment": {
    "body": "His name was my name too."
  }
}
```

Authentication required, returns the created Comment
Required field: `body`

### Get Comments from an Article

`GET /api/articles/:slug/comments`

Authentication optional, returns multiple comments

### Delete Comment

`DELETE /api/articles/:slug/comments/:id`

Authentication required

### Favorite Article

`POST /api/articles/:slug/favorite`

Authentication required, returns the Article
No additional parameters required

### Unfavorite Article

`DELETE /api/articles/:slug/favorite`

Authentication required, returns the Article

No additional parameters required

### Get Tags

`GET /api/tags`

##### Steps to install the project locally. 

1. Install PostgresQL on the machine.
2. Run `pip install -r requirements.txt` to install all the project requirements.
3. Set your environment Variables Below :
    - `SECRET_KEY`
    
4.  Then `RUN` your application.
- To run it **on your local machine;**

    `python3 manage.py runserver`   
    
    ## Deployment
Run `pip install -r requirements.txt` to install all the project requirements.

**Creating your Heroku app**
- Log into your heroku dashboard and create a pipeline

![alt txt](https://drive.google.com/uc?export=view&id=14wYvR9wslAsm-5Sc3ZMYoOGvtt3ygfh-)

- Connect the pipeline apps to your Github repo

![alt txt](https://drive.google.com/uc?export=view&id=1YlECJcQO8UJQXb8UzScwMGtL7s8PMs_j)

- Create staging and production apps and set the staging app to auto deploy from the develop branch and the production app to auto deploy from master.

![alt txt](https://drive.google.com/uc?export=view&id=18g1rPcKuFEfjRM6QFlVdavzn85adHPiS)

- Add a database to the app

![alt txt](https://drive.google.com/uc?export=view&id=1yYGQ5BxzDhS2f8LsQBxNwFJpPi9c4bka)

Read more.... https://devcenter.heroku.com/articles/heroku-postgresql  

- Setup the environment variables in the app settings.

![alt txt](https://drive.google.com/uc?export=view&id=1yYGQ5BxzDhS2f8LsQBxNwFJpPi9c4bka)

Follow this link for more instructions on how to deploy a django application on Heroku.

https://devcenter.heroku.com/articles/django-app-configuration

You may add a review app to your pipeline by enabling Review apps.

More about Review apps, https://devcenter.heroku.com/articles/github-integration-review-apps

After deploying the app, you can select "Open app" from the top right corner of your dashboard. Here you will get access to the link of your deployed app.

## Link to our app

https://ah-backend-staging.herokuapp.com/





