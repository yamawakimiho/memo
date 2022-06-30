# Memo Django

<p align="center">
<a href="https://memo-memo.herokuapp.com/" target="_blank"><img src="readme_assets/memo-logo.png" width="50%"></a>
</p>

![Heroku](https://pyheroku-badge.herokuapp.com/?app=memo-memo&style=flat)

<p >
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-memo">About The Memo</a>
      <ul>
        <li><a href="#screenshots">Screenshots</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
        <ul>
        <li><a href="#local-environment">Local Environment</a></li>
        <li><a href="#using-celery">Using celery</a></li>
      </ul>
    </li>
</details>

## About the memo

Memo is a flashcard-like web application built with Django, Django Rest Framework, jQuery, Bootstrap and Celery. You can create your own deck and also create flashcards about contents you want to learn. The object of this application is to make learning interesting and fun.

You can check the deployed project [here](https://memo-memo.herokuapp.com/).

Use the login credencial below to access the web application:

```
  Username: visitor
  Password: v1s1t0r@123
```

### Screenshots

<table>
  <tr>
    <td>
      <img src="readme_assets/index.png" width="100%">
    </td>
    <td>
      <img src="readme_assets/deck.png" width="100%">
    </td>
  </tr>
</table>

<table> 
  <tr>
    <td>
      <img src="readme_assets/assigment.png" width="100%">
    </td>
    <td>
      <img src="readme_assets/result.png" width="100%">
    </td>
  </tr>
</table>

### Project Structure

```sh
root ┐
     ├─ accounts (login)
     ├─ memo (api)
     │  └─ tests
     ├─ memo_front (app)
     ├─ project (core of memo)
     ├─ static
     └─ templates
        ├─ frontend
        └─ registration
```

## Getting Started

Before the setup, make sure you have:

-   Python 3.9
-   Pip
-   Docker compose

#### Clone this repository:

```sh
$ git clone https://github.com/yamawakimiho/memo_django.git
```

Create a virtual environment running **Python 3.9**:

```sh
virtualenv venv -p $(which python3)
```

or

```sh
$ mkvirtualenv -p $(which python3) venv
```

### Activate the virtual environment:

```sh
$ source venv/bin/activate
```

or

```sh
$ workon venv
```

### Update pip

```sh
$ pip install -U pip setuptools wheel pip-tools
```

Install the project requirements:

```sh
$ pip-sync
```

### Local Environment

Make a copy of `.env_example` file and named it to `.env`

Use the command below to build, create and start the docker compose:

```sh
$ docker-compose up
```

Migrate your model:

```sh
$ python manage.py migrate
```

Run the localhost (make sure docker is up in your localhost!):

```sh
$ python manage.py runserver
```

### Using Celery

You can use Celery locally by using this command:

```sh
$  celery -A project  worker -l info
```

If you want to activate task manually, run:

```sh
$  python manage.py shell
Python 3.9.7 (default, Sep 10 2021, 14:59:43)
[GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from project.tasks import send_email_task
>>> send_email_task()
>>> 'Email sent'
```

-   Remember: To receive a email, you need at least 1 deck with activate = True or notification ON and your registered email should be a valid email.

Or run periodic scheduling with celery beat (scheduler). <a href="https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html">See this documentation. </a>
** You can change the scheduler configuration in settings.py **

```sh
$  celery -A project.celery beat
```

or using beat with the worker:

```sh
$  celery -A project  worker -l info -beat
```
