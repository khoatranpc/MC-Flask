from flask import Flask, jsonify, request
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import numpy as np
from flask_cors import CORS
import json;
from flask_pymongo import PyMongo;
import utils
from CandidateModel import Candidate
import models

app = Flask(__name__)
CORS(app, origins='*')
app.config['MONGO_URI']="mongodb+srv://khoatranpc:khoatranpc603@cluster0.ujmwmqk.mongodb.net/mindx-k18-build?tls=true&tlsAllowInvalidCertificates=true"
mongo = PyMongo(app)
db=mongo.db

@app.route('/test-cnn')
def tesCnn():
    # Tạo dữ liệu mẫu dưới dạng JSON
    json_data = '[{"expYear":1,"expTeach":1,"label":"Supporter"},{"expYear":2,"expTeach":1,"label":"Supporter"},{"expYear":1,"expTeach":2,"label":"Supporter"},{"expYear":2,"expTeach":2,"label":"Mentor"},{"expYear":1,"expTeach":3,"label":"Mentor"},{"expYear":2,"expTeach":3,"label":"Lecture"},{"expYear":3,"expTeach":1,"label":"Lecture"},{"expYear":3,"expTeach":2,"label":"Lecture"},{"expYear":3,"expTeach":3,"label":"Lecture"},{"expYear":4,"expTeach":1,"label":"Lecture"},{"expYear":4,"expTeach":2,"label":"Lecture"},{"expYear":4,"expTeach":3,"label":"Lecture"},{"expYear":5,"expTeach":1,"label":"Lecture"},{"expYear":5,"expTeach":2,"label":"Lecture"},{"expYear":5,"expTeach":3,"label":"Lecture"},{"expYear":6,"expTeach":1,"label":"Lecture"},{"expYear":6,"expTeach":2,"label":"Lecture"},{"expYear":6,"expTeach":3,"label":"Lecture"},{"expYear":7,"expTeach":1,"label":"Lecture"},{"expYear":7,"expTeach":2,"label":"Lecture"}]'
    data = json.loads(json_data)

    # Chuyển đổi dữ liệu JSON thành numpy array
    features = np.array([[item["expYear"], item["expTeach"]] for item in data])
    labels = np.array([1 if item["label"] == "Lecture" else (2 if item["label"] == "Mentor" else 3) for item in data])

    # Tạo mô hình
    model = Sequential()
    model.add(Dense(32, input_dim=2, activation='relu'))
    model.add(Dense(1, activation='softmax'))

    # Biên soạn mô hình
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Đào tạo mô hình
    model.fit(features, labels, epochs=10)

    # Lưu mô hình
    model.save('my_model.h5')

    # Load mô hình
    loaded_model = load_model('my_model.h5')

    # Dữ liệu mới cần dự đoán
    new_json_data = '[{"expYear": 10, "expTeach": 10}]'
    new_data = json.loads(new_json_data)
    new_features = np.array([[item["expYear"], item["expTeach"]] for item in new_data])

    # Thực hiện dự đoán
    predictions = loaded_model.predict(new_features)
    # data = utils.getJsonFormat(predictions)
    print("Predictions:", predictions)
    return str(predictions)

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
        getData = CD.dataProcessing();
        predict = models.predicWithRandomForest(getData["dataTest"],getData["dataTrain"])
    return utils.getResponseJsonFormat(predict)
if __name__=="__main__":
    app.run(debug=True)