from flask import Flask, request, abort, json
from io import StringIO
from index import index

ALLOWED_EXTENSIONS = {"txt", "csv"}

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9560)