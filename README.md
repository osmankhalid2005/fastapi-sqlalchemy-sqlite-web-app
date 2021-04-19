# fastapi-sqlalchemy-sqlite-web-app
A  complete web application using FastApi, SQLAlchemy, SQLite, and Jinja2 Templates

Developed by: Dr. Osman Khalid

http://osman.pakproject.com

This application is an enhanced form of the following tutorial, and hence requires all packages/softwares needed for this tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/

Basic Requirements:

Python 3.9.4 (installed with updated pip)

fastapi --> pip install fastapi

uvicorn --> pip install uvicorn[standard]

sqlalchemy --> pip install sqlalchemy

jinja2 --> pip install jinja2

pymysql --> pip install pymysql

mysql --> pip install mysql


After all the pre-requisites are installed, use this command (with administrator rights) to run the application:

cd fastapi-sqlalchemy-sqlite-web-app

uvicorn sql_app.main:app --reload

Then, in browser, write: http://127.0.0.1:8000/home

To see docs, write: http://127.0.0.1:8000/docs
