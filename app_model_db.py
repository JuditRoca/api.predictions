from flask import Flask, request, jsonify
import os
import pickle
import sqlite3


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"


@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[int(tv),int(radio),int(newspaper)]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'


@app.route('/v2/ingest_data', methods=['POST'])
def new_entry():
    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)
    sales = request.args.get("sales", None)

    connection = sqlite3.connect('data/Adver.db')
    cursor = connection.cursor()
    query = ''' INSERT INTO inversiones (?,?,?,?)'''
    result = cursor.execute(query, (tv, radio, newspaper, sales)).fetchall()

    query = ''' SELECT * from inversiones '''
    result = cursor.execute(query).fetchall()
    connection.commit()
    connection.close()
    return jsonify(result)


@app.route('/v2/retrain', methods=['PUT'])
def train_model():
    connection = sqlite3.connect('data/Adver.db')
    cursor = connection.cursor()

   #me he vuelto loca buscando en internet y ni el chat gpt me dice algo decente xddd me rindo.


app.run()

