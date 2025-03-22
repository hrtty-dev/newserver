from flask import Flask, request, jsonify
import redis
import uuid
import json
r = redis.Redis(
    host='redis-14429.c251.east-us-mz.azure.redns.redis-cloud.com',
    port=14429,
    decode_responses=True,
    username="default",
    password="MLqNAy48u6P7jjW7UzI5pOVDrFLiofcz",
)
app = Flask(__name__)

data_store = []  

@app.route('/quiz', methods=['POST'])
def handle_data():
    quiz = request.json
    if not quiz:
        return jsonify({'error':'No data recieved'})
    qz = {'id':str(uuid.uuid4()),'questions':json.dumps(quiz['questions']),'answers':json.dumps(quiz['answers']),'owner':quiz['owner']}
    r.hset(quiz['title'],mapping=qz)
    return jsonify({'message':'successfully added to database!'})
@app.route('/quizzes',methods = ['GET'])
def get_quizzes():
    kys = r.scan_iter()
    nk = []
    for key in kys:
        owner = r.hget(key,'owner')
        nk.append(f'{key} by {owner}')
    return jsonify({"quizzes":nk})
@app.route('/quizq',methods = ['POST'])
def getquiz():
    quizn = request.json
    name = quizn['quizname']
    questions = r.hget(name,"questions")
    if questions:
        questions = json.loads(questions)
        answers = r.hget(name,"answers")
        answers = json.loads(answers)
        data = {"owner":r.hget(name,"owner"),"questions":questions,"answers":answers}
        return jsonify({"data":data})
    else:
        return jsonify({"message":"not a valid quiz name"})
@app.route('/')
def home():
    return "Flask app is running on Render!"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
