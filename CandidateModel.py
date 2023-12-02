from bson import ObjectId
import utils

class Candidate:
    def __init__(self, candidateId, collection, isPredictCandidate: bool):
        self.id = candidateId
        self.collection = collection
        self.isPredictCandidate = isPredictCandidate
        
    def findOneCandidateById(self):
        pipeline = [
                {
                    "$match": {
                        "_id": ObjectId(self.id)
                    }
                }
            ]
        if not self.isPredictCandidate:
            pipeline.append({
                     "$lookup": {
                        "from": "courselevels",
                        "localField": "classifyLevel",
                        "foreignField": "_id",
                        "as": "classifyLevel"
                    }
            })
            pipeline.append({
                    "$unwind": "$classifyLevel"
            })
        findCandidate = list(self.collection.aggregate(pipeline))
        if len(findCandidate):
            return findCandidate[0]
        return None
    def getAllCandidate(self):
        listCandidate = list(self.collection.find({}))
        return listCandidate
    def getAllCandidateWithCondition(self, condition):
        listCandidate = list(self.collection.aggregate([
            {
                "$match": condition
            },
            {
                "$lookup": {
                    "from": "courselevels",
                    "localField": "classifyLevel",
                    "foreignField": "_id",
                    "as": "classifyLevel"
                }
            },
            {
                "$unwind": "$classifyLevel"
            }
        ]))
        return listCandidate
    def dataProcessing(self):
        currentCandidate = self.findOneCandidateById()
        if currentCandidate != None:
            dataTest = utils.handleData(currentCandidate, self.isPredictCandidate)
            dataTrain = self.getAllCandidateWithCondition({
                "courseApply": {
                    "$eq": currentCandidate['courseApply']
                },
                "classifyLevel": {
                    "$exists": True
                },
                "classifyRole": {
                    "$exists": True
                }
            })
            listDataTrain = []
            for i in range(len(dataTrain)) :
                listDataTrain.append(utils.handleData(dataTrain[i], False))
            return {
                "dataTest": dataTest,
                "dataTrain": listDataTrain
            }
        return {}