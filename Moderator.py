from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

classifier = pipeline('sentiment-analysis')

#Here you add words you don't want to be contained
offensive_keywords = [
    "stupid"
]
def contains_offensive_keywords(text):
    for word in offensive_keywords:
        if word.lower() in text.lower():
            return True
    return False


@app.route('/check-text', methods=['POST'])
def check_text():
    data = request.json
    text = data['text']

    if contains_offensive_keywords(text):
        return jsonify({'isAllowed': False})

    return jsonify({'isAllowed': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
