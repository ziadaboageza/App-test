from flask import Flask, request, jsonify
import speech_recognition as sr
import tempfile
import os

app = Flask(__name__)
recognizer = sr.Recognizer()

@app.route('/convert_audio', methods=['POST'])
def convert_audio():
    try:
        # Get the audio file from the request
        audio_file = request.files['audio']
        
        # Save audio data to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
            temp_audio_file.write(audio_file.read())
            temp_audio_file_path = temp_audio_file.name
        
        # Recognize speech from audio file
        text = recognize_speech(temp_audio_file_path)
        
        # Delete temporary file
        os.remove(temp_audio_file_path)
        
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)})

# def save_audio_to_temp_file(audio_file):
#     with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
#         temp_audio_file.write(audio_file.read())
#     return temp_audio_file.name

def recognize_speech(audio_file_path):
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="ar-EG")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "Error connecting to Google Speech Recognition service: {}".format(e)

if __name__ == '__main__':
    app.run(debug=True)