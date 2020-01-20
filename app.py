import random, os, io, base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

#TODO: Enter code to create face client
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

credentials = CognitiveServicesCredentials(os.environ['COGSVCS_KEY'])
client = FaceClient(
    os.environ['COGSVCS_CLIENTURL'],
    credentials=credentials
)

emotions = ['neutral', 'fear','happiness','sadness']

@app.route('/')
def home():
    page_data = {
        'emotion' : random.choice(emotions)
    }
    return render_template('home.html', page_data = page_data)

@app.route('/result', methods=['POST'])
def check_results():
    body = request.get_json()
    desired_emotion = body['emotion']

    #PiCamera class
    faces = client.face.detect_with_stream(open('filename', 'r'),
        return_face_attributes=['emotion'])

    # image_bytes = base64.b64decode(body['image_base64'].split(',')[1])
    # image = io.BytesIO(image_bytes)

    # # TODO: Enter code to detect emotion
    # faces = client.face.detect_with_stream(image, 
    # return_face_attributes=['emotion'])

    if len(faces) == 1:
        detected_emotion = best_emotion(faces[0].face_attributes.emotion)
        #first face
        #has face_attributes
        #this will give us emotion

        #{anger: 0.5, contempt: 0.2}
        #best_emotion(anger)
        #does not return value

        if detected_emotion == body['emotion']:
            return jsonify({
                'message': '✅ You won! You showed ' + desired_emotion
            })
        else:
            return jsonify({
                'message': '❌ You failed! You needed to show ' + 
                           desired_emotion + 
                           ' but you showed ' + 
                           detected_emotion
            })
    else:
        return jsonify({
            'message': '☠️ ERROR: No faces detected'
        })

def best_emotion(emotion):
    emotions = {}   
    emotions['anger'] = emotion.anger
    emotions['contempt'] = emotion.contempt
    emotions['disgust'] = emotion.disgust
    emotions['fear'] = emotion.fear
    emotions['happiness'] = emotion.happiness
    emotions['neutral'] = emotion.neutral
    emotions['sadness'] = emotion.sadness
    emotions['surprise'] = emotion.surprise
    return max(zip(emotions.values(), emotions.keys()))[1]
