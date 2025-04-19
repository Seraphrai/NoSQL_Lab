# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Michael:root@cluster0.gn5rqjv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# Test function
@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/processVote', methods=["POST"])
def processVote():

    data = request.get_json()

    db = client["NoSQL_Lab"]
    votes = db["Votes"]

    voterID = data.get("voterID")
    regPIN = data.get("regPIN")
    candidate1 = data.get("candidate1")
    candidate2 = data.get("candidate2")
    candidate3 = data.get("candidate3")

    vote = {
        "voterID": voterID,
        "regPIN": regPIN,
        "candidate1": candidate1,
        "candidate2": candidate2,
        "candidate3": candidate3 
    }

    result = votes.insert_one(vote)
    
    print(result)
    return result

@app.route('/checkDuplicate')
def checkDuplicate ():
    db = client["NoSQL_Lab"]
    votes = db["Votes"]

    data = request.get_json()

    myquery = { "voterID": data.get("voterID"), "regPIN": data.get("regPIN") }

    if votes.find(myquery) == None or votes.find(myquery) == "" or votes.find(myquery) == []:
        return False
    else:
        return True


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
