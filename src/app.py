from quart import Quart, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from os import environ
from pymongo import MongoClient

shitstring = 'mongodb://%s:%s@%s:27017/%s' % (environ['MONGODB_USER'], environ['MONGODB_PASSWORD'], environ['MONGODB_HOST'], environ['MONGODB_DB'])
print("shitdtting", shitstring)
connection = MongoClient(shitstring)
db = connection[environ['MONGODB_DB']]
collection = db["errors"]

app = Quart("MongoDB Logger")

AUTH_PW = generate_password_hash(environ["AUTH_PW"])
environ["AUTH_PW"] = ""

def logged_in(msg):
    appname = msg["appname"]
    message = msg["errorjson"]
    resp = collection.insert_one({"appname": appname, "error": message, "timestamp": datetime.now()})
    return resp.acknowledged

@app.route('/', methods=['POST'])
async def index():
    # receives json with 
    # appname
    # password
    # errorjson
    msg = await request.json
    try:
        if check_password_hash(AUTH_PW,msg["password"]):
            # correct password
            success = logged_in(msg)
            if success:
                return json.dumps({"code":200, "message": "success"})
            else:
                json.dumps({"code":500, "message": "insert into mongodb didnt work"})
        else:
            return json.dumps({"code": "401", "error":"incorrect password"})
    except Exception as e:
        msg = {
            "code": "500",
            "help" : "Endpoint expects json with: appname, password, errorjson",
            "error" : repr(e)
        }
        return json.dumps(msg)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')