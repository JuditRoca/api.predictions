from flask import Flask, request, jsonify
import os
import pickle
import sqlite3
import pandas as pd


os.chdir(os.path.dirname(__file__))

# Llamamos a la web server para desplegarla
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
    query = ''' SELECT * FROM inversiones'''
    result = cursor.execute(query).fetchall()
    df = pd.DataFrame(result)

    x = df.drop(columns = ["sales"])
    y = df["sales"]

    model = pickle.load(open('data/advertising_model','rb'))
    model.fit(x,y)
    pickle.dump(model, open('data/advertising_model','wb'))

app.run(debug = True, host = '0.0.0.0', port=4000)

