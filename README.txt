# Udacity Catalog Project #

## Seup ##

This python application requires the following tools

- Flask
- SQLAlchemy
- Flask-GoogleLogin

It's designed to be used in the pre-configured vagrant VM setup by Udacity. However to install
everything you need run the following commands:

    pip install Flask
	pip install SQLAlchemy
	pip install Flask-GoogleLogin

You'll need to have your client_secrets.json file setup with a client id and client secret from Google.

NOTE: The Google interface to setup OAuth changes frequently, these instructions are a "hint" due to that. Hopefully they are closer than the class videos or instructor notes.

1. Visit the [Google Developer Console](https://console.developers.google.com/project).
2. Click on Create a Project at top, fill in your name (Catalog App), and click Create
3. Go to APIs & services, and choose "OAuth Consent Screen" and put in valid email and Product Name and click Save.
4. Go to APIs & services and pick "Create Credentials" and "Web Application" type.
5. Enter http://localhost:5000/oauth2callback in the Authorized redirect URIs field.
6. Click "Create" and you'll see a client ID and secret. Close this and click the download arrow at far right of screen to download a client secret JSON file. Rename this as client_secrets.json and store in the root of this project directory.

To populate the database with a starter set of categories and items run the following command:

	python createCatalog.py

You should now have a file called catalog.db in the directory. This is your database.

## Run the web application ##

Run the following command:
	
	python project.py

Bring up the following URL in your browser:

    http://localhost:5000/

## General Notes ##
- The application has three API endpoints:
	- /api/v1/items/<item_id> - gets a specific item (per project requirements)
    - /api/v1/categories/<category_id>/items - gets all the items in a category
    - /api/v1/categories - gets all the categories
- The app uses bootstrap with some simple breakdowns so somewhat usable responsive interface but more work could be done to improve it on small devices.
- App uses the Flask templating engine. All templates are in the /templates directory
