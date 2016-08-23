[![Build Status](https://travis-ci.org/andela-aabdulwahab/bucketlist-api.svg?branch=develop)](https://travis-ci.org/andela-aabdulwahab/bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/andela-aabdulwahab/bucketlist-django-application/badge.svg?branch=develop)](https://coveralls.io/github/andela-aabdulwahab/bucketlist-django-application?branch=develop)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-aabdulwahab/bucketlist-django-application/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-aabdulwahab/bucketlist-django-application/?branch=develop)


### Bucketlist Django Application (Buppli)
A bucketlist application in Django with API endpoint

### Introduction

Buppli is an application for creating and managing a bucketlist, with available API to perform the actions. Built with [django-restful-framework](http://www.django-rest-framework.org/), it implements token Based Authentication for the API and only methods to register and login are accessible to unauthenticated users. Data is exchanged as JSON.

## API Documentation
Documentation is available [here](buppli.herokuapp.com/api/v1/docs/)

## Installation
Clone the repo
```
git clone https://github.com/andela-aabdulwahab/bucketlist-django-application.git
```
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

 ```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements
 ```
 If you are on Windows, then use the following commands instead:

 ```sh
$ virtualenv venv
$ venv\Scripts\activate
(venv) $ pip install -r requirements.txt
```

## Perform migrations
```
python manage.py makemigrations
python manage.py migrate
```

## Testing
To run the tests for the app, and see the coverage, run
```
python manage.py test
```
