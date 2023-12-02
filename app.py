from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo;
import utils
from CandidateModel import Candidate
import models

app = Flask(__name__)
CORS(app, origins='*')
app.config['MONGO_URI']="mongodb+srv://khoatranpc:khoatranpc603@cluster0.ujmwmqk.mongodb.net/mindx-k18-build?tls=true&tlsAllowInvalidCertificates=true"
mongo = PyMongo(app)
db=mongo.db


@app.route('/')
def firstConnect():
    return 'Created By Trần Đăng Khoa'
@app.route('/test-cnn')

@app.route('/random-forest')
def accessRandomForest():
    return jsonify({
        "message": "Truyền id của ứng viên để thực hiện dự đoán!"
    })

@app.route('/random-forest/<candidateId>')
def predicWithRandomForest(candidateId):
    query = request.args
    if len(query):
        isPredictCandidate = request.args.get('isPredictCandidate', '').lower() in ['true', '1']
        CD =  Candidate(candidateId, db.recruitments, (isPredictCandidate))
        getData = CD.dataProcessing()
        predictLevel = models.predicWithRandomForest(getData["dataTest"],getData["dataTrain"], "classifyLevel")
        predictRole = models.predicWithRandomForest(getData["dataTest"],getData["dataTrain"], "classifyRole")
    return utils.getResponseJsonFormat({
        "classifyRole": predictRole,
        "classifyLevel": predictLevel
    })
if __name__=="__main__":
    app.run(host="0.0.0.0", port=80, debug=True)