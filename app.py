import speech_recognition as sr
import requests

# Function to record audio from the microphone
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording audio...")
        audio = recognizer.listen(source)
        print("Finished recording.")
    return audio

# Function to send audio data to Flask backend server
def send_audio_to_server(audio):
    url = 'http://127.0.0.1:5000/convert_audio'
    try:
        with open('recorded_audio.wav', 'wb') as f:
            f.write(audio.get_wav_data())
        with open('recorded_audio.wav', 'rb') as audio_file:
            files = {'audio': audio_file}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                print("Audio sent to server successfully.")
                print("Server response:", response.json())  # Print server response
            else:
                print("Error sending audio to server. Status code:", response.status_code)
    except Exception as e:
        print("Error occurred while sending audio to server:", str(e))

# Main function to orchestrate the process
def main():
    audio = record_audio()
    if audio:
        send_audio_to_server(audio)

if __name__ == "__main__":
    main()
