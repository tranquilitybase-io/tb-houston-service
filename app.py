import os
import config
import logging

#print("DEBUG: {}".format(os.environ['DEBUG']))
#print("SQLALCHEMY_DATABASE_URI: {}".format(os.environ['SQLALCHEMY_DATABASE_URI']))

# Get theapplication instance
connex_app = config.connex_app

logging.basicConfig(level=int(os.environ.get('DEBUG')))
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
ch.setFormatter(formatter)
connex_app.app.logger.addHandler(ch)

# connect logging between gunicorn and Flask
#gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn.info")
connex_app.app.logger.handlers = gunicorn_logger.handlers
connex_app.app.logger.setLevel(gunicorn_logger.level)

# Read the swagger.yml file to configure the endpoints
connex_app.add_api('houston_service.yml', strict_validation=True)

if __name__ == "__main__":
    connex_app.run(port=3000)
