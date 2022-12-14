from flask import Flask, request, abort, json
from io import StringIO
from index import index
from ml import predict
import pickle as pkl
import os

ALLOWED_EXTENSIONS = {"txt", "csv"}

app = Flask(__name__)

stored_model = pkl.load(open('model/flatz.pkl', 'rb'))

def is_valid_extension(filename: str) -> bool:
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/import/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, 'No file provided')
    file = request.files['file']
    if file.filename == '':
        abort(400, 'Empty file provided')
    if not file or not is_valid_extension(file.filename):
        abort(400, 'Only .txt and .csv files are supported')
    csv_file = StringIO(file.stream.read().decode("utf-8"))
    created, updated = index(csv_file)
    return json.dumps({'created': created, 'updated': updated}), 200, {'ContentType':'application/json'}

@app.route('/predict/', methods=['GET'])
def process_predict():
    data = request.get_json(force=True)
    predict_request = [
        data['area'], 
        data['livingArea'], 
        data['rooms'], 
        data['floor'],
        data['total_floor'],
        data['buildYear'],
        data['walk_to_metro']
        ]
    output = predict(predict_request, stored_model)
    return json.dumps({'price': output})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9560)