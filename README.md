TodoAgain
=========

Yes, Another Todo list. This version is the one I wanted for my needs. Maybe it would fit your needs.

Features
========

* Checkable list elements
* Crossable list elements
* Todo categories
* Archivable check elements for checked elements (by selected category)
* (Basic) Authentication via a json file
* Auto sorted priorities on tasks

Authentication
==============

Write the **/etc/check_auth.json** file that have to look like:

	[
		{"username": "me", "password": "plain-text-secret"}
	]

Deployment
==========

I serve this flask application with gunicorn and a nginx reverse proxy in a virtual env. (requires pip and virtualenv on your host)

Run the following commands to get a working installation:

	git clone "this repository"
	cd "this repository folder"
	virtualenv . [-p /usr/bin/python3]
	source bin/activate
	pip install -r requirements.txt
	python models # db initialization
	"this repository folder"/bin/gunicorn --bind 0.0.0.0:<PORT> wsgi:app

Notes
=====

* I use supervisord to serve this app *forever* !
* I also use this app in as a chromium extension with an *ugly Iframed* empty extension


Sample
======

![Todo Again](/sample.png)

Licence
=======

MIT