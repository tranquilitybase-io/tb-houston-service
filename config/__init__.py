import os
import sys
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_executor import Executor


basedir = os.path.join(os.path.dirname(__file__), "..")
# print("basedir: {}".format(basedir))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir + "/openapi")

# Get the underlying Flask app instance
app = connex_app.app

# We want to see all background exceptions
app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True 

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_ECHO"] = os.environ["SQLALCHEMY_ECHO"].lower() == "True".lower()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"].lower() == "True".lower()
)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 10,
        "max_overflow": 5,
        "pool_pre_ping": True,
        "pool_recycle": 1200,
}

if app.config["SQLALCHEMY_DATABASE_URI"] is None:
    print("SQLALCHEMY_DATABASE_URI is not set")
    app.logging.error("SQLALCHEMY_DATABASE_URI is not set")
    sys.exit(0)

if app.config["SQLALCHEMY_ECHO"] is None:
    app.logging.error("SQLALCHEMY_ECHO is not set")
    sys.exit(0)

if app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is None:
    app.logging.error("SQLALCHEMY_TRACK_MODIFICATIONS is not set")
    sys.exit(0)

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# For running background tasks
executor = Executor(app)
