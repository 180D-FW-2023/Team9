import threading
import time
import speech_recognition as sr
from vosk import Model, KaldiRecognizer

recognizer = sr.Recognizer()

def capture_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def google_speech_recognition(audio, event):
    try:
        text = recognizer.recognize_google(audio)
        print("Google Speech Recognition:", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    event.set()  # Set the event to signal completion

def vosk_speech_recognition(audio, event):
    model = Model("vosks-model-small-en-us-0.15")
    recognizer_vosk = KaldiRecognizer(model, 16000)
    recognizer_vosk.SetWords(True)
    while True:
        data = audio.frame_data
        if len(data) == 0:
            break
        if recognizer_vosk.AcceptWaveform(data):
            result = recognizer_vosk.Result()
            print("Vosk Speech Recognition:", result)
    event.set()  # Set the event to signal completion

def main():
    while True:
        audio = capture_audio()

        event = threading.Event()

        google_thread = threading.Thread(target=google_speech_recognition, args=(audio, event))
        vosk_thread = threading.Thread(target=vosk_speech_recognition, args=(audio, event))

        google_thread.start()
        vosk_thread.start()

        # Wait for either thread to finish
        event.wait()

        # If one thread finishes first, stop the other
        if google_thread.is_alive():
            vosk_thread.join()
            google_thread.join()
        elif vosk_thread.is_alive():
            google_thread.join()
            vosk_thread.join()

if __name__ == "__main__":
    main()
