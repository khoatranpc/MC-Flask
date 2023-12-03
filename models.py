from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import numpy as np
import json;

def predicWithRandomForest(dataTest, dataTrain, label: str):
    # Dữ liệu mẫu
    # Chuyển đổi dữ liệu JSON thành list
    data = dataTrain
    

    # Chia thành đặc trưng và nhãn
    features = np.array([[item["scoreTechnique"],item["scoreJobPosition"],item["dob"], item["education"], item["expTimeTech"], item["graduatedUniversity"], item["levelTechnique"], item["resourceApply"], item["scoreSoftsSkill"], item["specializedIt"], item["teacherCertification"], item["technique"]] for item in data])
    labels = np.array([item[label] for item in data])

    # Chia thành tập huấn luyện và tập kiểm thử
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Khởi tạo và huấn luyện mô hình
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Dự đoán trên tập kiểm thử
    predictions = model.predict(X_test)

    # Đánh giá độ chính xác
    accuracy = accuracy_score(y_test, predictions)

    # Dữ liệu mới cần dự đoán
    new_features = np.array([[item["scoreTechnique"],item["scoreJobPosition"],item["dob"], item["education"], item["expTimeTech"], item["graduatedUniversity"], item["levelTechnique"], item["resourceApply"], item["scoreSoftsSkill"], item["specializedIt"], item["teacherCertification"], item["technique"]] for item in [dataTest]])

    # Dự đoán nhãn
    predicted_label = model.predict(new_features)

    # Tính ma trận confusion
    # conf_matrix = confusion_matrix(y_test, predictions)
    # y_pred = model.predict(X_test)
    # print(classification_report(y_test, y_pred))

    # Tính precision, recall và F1-Score
    precision = precision_score(y_test, predictions, average='weighted')
    recall = recall_score(y_test, predictions, average='weighted')
    f1 = f1_score(y_test, predictions, average='weighted')

    return {
        "predict": {
            "result": predicted_label[0],
            "precision": precision,
            "recall": recall,
            "f1": f1,
        },
        "accuracy": accuracy,
    }