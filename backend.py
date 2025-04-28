# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
from datetime import datetime
from bson.json_util import dumps
from bson.json_util import loads
uri = "mongodb+srv://Michael:root@cluster0.gn5rqjv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)

@app.route('/retrieveBallot', methods=["POST"])
def retrieveBallot():
    data = request.get_json()
    db = client["NoSQL_Lab"]
    votes = db["Votes"]
    voterID = data.get("voterID") 
    return dumps(votes.find_one({"voter.voterID": voterID}))


@app.route('/deleteBallot', methods=["POST"])
def deleteBallot():
    data = request.get_json()
    db = client["NoSQL_Lab"]
    votes = db["Votes"]
    voterID = data.get("voterID")  
    regPIN = data.get("regPIN")
    success = votes.delete_one({"voter.voterID": voterID, "voter.regPIN": regPIN})

    return success

# Test function
@app.route('/hello')
def hello_world():
    db = client["NoSQL_Lab"]
    votes = db["Votes"]
    return 'Hello World'

@app.route('/processVote', methods=["POST"])
def processVote():

    data = request.get_json()

    db = client["NoSQL_Lab"]
    votes = db["Votes"]

    voterID = data.get("voterID")
    regPIN = data.get("regPIN")
    electionID = data.get("electionID")
    electionName = data.get("electionName")
    electionDate = str(datetime.date(datetime.now()))
    timestamp = str(datetime.now())
    candidate1ID = data.get("candidate1ID")
    candidate2ID = data.get("candidate2ID")
    candidate3ID = data.get("candidate3ID")
    candidate1Name = data.get("candidate1Name")
    candidate2Name = data.get("candidate2Name")
    candidate3Name = data.get("candidate3Name")
    candidate1Party = data.get("candidate1Party")
    candidate2Party = data.get("candidate2Party")
    candidate3Party = data.get("candidate3Party")

    ballot = {
        "voter":{
            "voterID": voterID,
            "regPIN": regPIN
        },

        "election": {
            "electionID": electionID,
            "name": electionName, 
            "date": electionDate
        },

        "timestamp": timestamp,
        
        "rankings": [
            {"rank": 1, "nominee": { "nomineeID": candidate1ID, "name": candidate1Name, "party": candidate1Party}},
            {"rank": 2, "nominee": { "nomineeID": candidate2ID, "name": candidate2Name, "party": candidate2Party}},
            {"rank": 3, "nominee": { "nomineeID": candidate3ID, "name": candidate3Name, "party": candidate3Party}}
        ]
    }

    result = votes.insert_one(ballot)
    
    return str(result)

@app.route('/updateVote', methods=["POST"])
def updateVote():

    data = request.get_json()
    db = client["NoSQL_Lab"]
    votes = db["Votes"]

    voterID = data.get("voterID")
    regPIN = data.get("regPIN")
    electionID = data.get("electionID")
    electionName = data.get("electionName")
    electionDate = str(datetime.date(datetime.now()))
    timestamp = str(datetime.now())
    candidate1ID = data.get("candidate1ID")
    candidate2ID = data.get("candidate2ID")
    candidate3ID = data.get("candidate3ID")
    candidate1Name = data.get("candidate1Name")
    candidate2Name = data.get("candidate2Name")
    candidate3Name = data.get("candidate3Name")
    candidate1Party = data.get("candidate1Party")
    candidate2Party = data.get("candidate2Party")
    candidate3Party = data.get("candidate3Party")

    filterVote = {"voter.voterID": voterID, "voter.regPIN": regPIN}
    newValues = {
        "election": {
            "electionID": electionID,
            "name": electionName, 
            "date": electionDate
        },

        "timestamp": timestamp,
        
        "rankings": [
            {"rank": 1, "nominee": { "nomineeID": candidate1ID, "name": candidate1Name, "party": candidate1Party}},
            {"rank": 2, "nominee": { "nomineeID": candidate2ID, "name": candidate2Name, "party": candidate2Party}},
            {"rank": 3, "nominee": { "nomineeID": candidate3ID, "name": candidate3Name, "party": candidate3Party}}
        ]
    }

    #result = votes.update_one(filterVote, {"$set": {"election": {"electionID": electionID,"name": electionName, "date": electionDate}}})
    result = votes.update_one(filterVote, {"$set": newValues})
    return str(result)

@app.route('/checkDuplicate', methods=["POST"])
def checkDuplicate ():
    db = client["NoSQL_Lab"]
    votes = db["Votes"]

    data = request.get_json()

    myquery = { "voter.voterID": data.get("voterID"), "voter.regPIN": data.get("regPIN") }

    if votes.find_one(myquery) is None:
        print("False")
        return "False"
    else:
        print("True")
        return "True"


@app.route('/ping')
def pingServer ():
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


# main driver function
if __name__ == '__main__':
    # runs application
    app.run()
