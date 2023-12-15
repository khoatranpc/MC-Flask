from flask import jsonify
from bson import json_util
from datetime import datetime
import json;

def getResponseJsonFormat(listData):
    data = json.dumps(listData,default=json_util.default) # Fetch all documents from the collection
    return jsonify(json.loads(data))
getScoreLevelTech = {
    "INTERN": 1,
    "FRESHER": 2,
    "JUNIOR": 3,
    "MIDDLE": 4,
    "SENIOR": 5,
    "LEADER": 6,
}
getScoreResourceApply = {
    "AN": 1,
    "FB": 2,
    "RF": 3,
    "LKD": 4
}
mapRoleToScore = {
    "SP": 0,
    "MT": 1,
    "ST": 2
}
getScoreEducation  = {
    "BACHELOR": 1,
    "ENGINEER": 2,
    # // thạc sĩ
    "MASTER": 3,
    # // tiến sĩ
    "DOCTOR": 4
}
def calculate_age(dob):
    # Lấy ngày hiện tại 
    today = datetime.today()
    # Tính toán tuổi
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def getNumberByBoolean(boolean):
    return 1 if bool(boolean) else 0

def handleData(data: dict, isPredictCandidate: bool):
    newData = {}
    for x in data:
        if x == "scoreJobPosition" or x == "scoreTechnique" or x == "classifyRole" or x == "dob" or x == "classifyLevel" or x == "education" or x == "expTimeTech" or x == "expTimeTeach" or x == "graduatedUniversity" or x == "levelTechnique" or x == "resourceApply" or x == "scoreSoftsSkill" or x=="specializedIt" or x =="teacherCertification" or x=="technique":
            newData[x]=data[x]
    # handle data, parse string to number
    newData['dob'] = calculate_age(newData['dob'].date())
    newData['education'] = getScoreEducation[newData['education']]
    newData['graduatedUniversity'] = getNumberByBoolean(newData['graduatedUniversity'])
    newData['levelTechnique'] = getScoreLevelTech[newData['levelTechnique']]
    newData['resourceApply'] = getScoreResourceApply[newData['resourceApply']]
    newData['specializedIt'] = getNumberByBoolean(newData['specializedIt'])
    newData['teacherCertification'] = getNumberByBoolean(newData['teacherCertification'])
    # caculate total tech
    arrayTech = [item.strip() for item in newData['technique'].split(',')]
    newData['technique'] = len(arrayTech)
    if 'classifyLevel' in newData:
        if not isPredictCandidate:
            if 'levelCode' in newData['classifyLevel']:
                newData['classifyLevel'] = newData['classifyLevel']['levelCode']
        else: newData['classifyLevel'] = ""
    return  newData