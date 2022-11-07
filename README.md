### Hexlet tests and linter status:
[![Actions Status](https://github.com/Unshock/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Unshock/python-project-52/actions)
[![linter-and-test-check](https://github.com/Unshock/python-project-52/actions/workflows/test_and_lint_check.yml/badge.svg)](https://github.com/Unshock/python-project-52/actions/workflows/test_and_lint_check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/fd67eb27d9343d5bb408/maintainability)](https://codeclimate.com/github/Unshock/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fd67eb27d9343d5bb408/test_coverage)](https://codeclimate.com/github/Unshock/python-project-52/test_coverage)

## Task manager study project for Hexlet.io 
### Description:

##### Task manager is the final project of the Python course on the Hexlet online school.
##### The task manager allows you to register user, create new tasks using self defined statuses and labels. Tasks can be managed - you can assign executors on them, change statuses, descriptions and so on.



### Deployment:

##### Task manager is made with Django using Django ORM and deployed on Heroku.
[![Heroku](https://pyheroku-badge.herokuapp.com/?app=task-manager-artem&style=flat)](https://unshock-task-manager.herokuapp.com/)

### Installation:

##### You can install the project locally.
##### First of all, you need to clone the repository to your local machine:
    (venv) demo $ git clone git@github.com:Unshock/python-project-52.git
##### Then you need to install projects dependencies (you need python 3.10 at least):
    (venv) demo $ cd python-project-52/

    (venv) demo $ pip install -r requirement.txt
##### Now you need to modify the "*.env.example*" file located in the root project directory. You need to set your Django secret key as the value of the *SECRET_KEY_DJANGO* in the file.
    DEBUG=True
    SECRET_KEY_DJANGO=Your_Django_key
    ROLLBAR_TOKEN=
    CREATOR=
##### Also, you need to rename the "*.env.example*" into "*.env*".
##### At this stage you need to apply migrations and after that you can run the project locally using *runserver* command:
    (venv) demo $ python manage.py makemigrations
    (venv) demo $ python manage.py migrate
    (venv) demo $ python manage.py runserver
    
    Performing system checks...

    System check identified no issues (0 silenced).
    November 07, 2022 - 18:59:59
    Django version 4.1.2, using settings 'task_manager.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
