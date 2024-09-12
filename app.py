import json
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/wordcounter", methods=['POST'])
def countWords():
    text = json.loads(request.data)['body']
    numWords = len(text.split(' '))
    return jsonify({'result': f'There are {numWords} words in the input text.'}), 200


if __name__ == '__main__':
    app.run(port=5000)
