import os
import sys
import connexion
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))
#print("basedir: {}".format(basedir))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir + "/openapi") 

# Get the underlying Flask app instance
app = connex_app.app

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_ECHO'] = os.environ['SQLALCHEMY_ECHO'].lower() == 'True'.lower()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'].lower() == 'True'.lower()

if app.config['SQLALCHEMY_DATABASE_URI'] == None:
    print("SQLALCHEMY_DATABASE_URI is not set")
    app.logging.error("SQLALCHEMY_DATABASE_URI is not set")
    sys.exit(0)

if app.config['SQLALCHEMY_ECHO'] == None:
    app.logging.error("SQLALCHEMY_ECHO is not set")
    sys.exit(0)

if app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == None:
    app.logging.error("SQLALCHEMY_TRACK_MODIFICATIONS is not set")
    sys.exit(0)

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
