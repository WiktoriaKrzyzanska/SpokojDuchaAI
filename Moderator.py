import os

from flask import Flask, request, jsonify
from google.cloud import vision
from transformers import pipeline

app = Flask(__name__)

classifier = pipeline('sentiment-analysis')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_key.json"
vision_client = vision.ImageAnnotatorClient()

offensive_keywords = ["stupid"]


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


@app.route('/check-image', methods=['POST'])
def check_image():
    file = request.files['image']
    content = file.read()

    image = vision.Image(content=content)
    response = vision_client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    print('Safe search results:')
    print(f'Adult: {safe.adult}')
    print(f'Spoof: {safe.spoof}')
    print(f'Medical: {safe.medical}')
    print(f'Violence: {safe.violence}')
    print(f'Racy: {safe.racy}')

    if safe.adult >= vision.Likelihood.LIKELY or safe.violence >= vision.Likelihood.LIKELY or safe.racy >= vision.Likelihood.LIKELY:
        print('The image contains inappropriate content.')
        return jsonify({'isAllowed': False})

    return jsonify({'isAllowed': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
