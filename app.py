from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {"$set":{"num_of_users":new_num}})
        return str("Hello user " + str(new_num))


def checkPostedData(postedData, functionName):
    if functionName == "add" or functionName == "subtract" or functionName == "multiply":
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif functionName == "division":
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "add")
        if status_code != 200:
            retJson ={
                "Messgage": "An error ",
                "Status Code": status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x+y
        retMap = {
            'sum': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Subtract(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "subtract")
        if status_code != 200:
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x-y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Multiply(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "multiply")
        if status_code != 200:
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x*y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Divide(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "division")
        if status_code != 200:
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = (x*1.0)/y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit, "/hello")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hithere')
def hi_there_everyone():
    return "I just hit /hithere"


@app.route('/add_two_nums', methods=["POST"])
def add_two_nums():
    dataDict = request.get_json()
    if "x" not in dataDict:
        return "ERROR", 305
    x = dataDict["x"]
    y = dataDict["y"]
    z = x + y
    retJSON = {
        "z": z
    }
    return jsonify(retJSON), 200


@app.route('/bye')
def bye():

    age = 2*15
    # s = str(c)
    # c = 1/0
    retJson = {
        'Name': 'zofiya',
        'Age': age,
        "phones": [
            {
                "phoneName": "Iphone10",
                "phoneNumber": 1111111
            },
            {
                "phoneName": "Nokia",
                "phoneNumber": 1111221
            }
        ]
    }
    return jsonify(retJson)


if __name__ == '__main__':
    # app.run(host="127.0.0.1", port=80)
    # app.run(debug=True)
    app.run(host='0.0.0.0')