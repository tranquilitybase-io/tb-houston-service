from datetime import datetime
import json

class ModelTools():

    @staticmethod
    def get_utc_epoch():
        return datetime.utcnow().strftime('%s')

    @staticmethod
    def get_utc_timestamp():
        return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def datetime_as_string(dt):
        if dt is None:
            return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def json_dump(obj):
        #return json.dumps(obj, indent=2, sort_keys=True)
        return json.dumps(obj)

    # simple redact function, used prior to logging
    @staticmethod
    def redact_dict(my_dict):
        new_dict = my_dict.copy()
        new_dict['username'] = "XXXXX"
        new_dict['password'] = "XXXXX"
        return new_dict
