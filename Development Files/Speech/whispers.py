from faster_whisper import WhisperModel
import speech_recognition as sr

model_size = "base.en"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
r = sr.Recognizer()

def initial(source): 
    print("Waiting for 'hey buddy' ")
    while True:
        audio = r.listen(source)
        try:
            segments, _ = model.transcribe(audio, vad_filter=True)
            for segment in segments:
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            text = r.recognize_google(audio)
           # print(text)
            if "hey buddy" in text.lower():
                print("Entering Menu")
                break
        except sr.UnknownValueError:
            pass

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")



with sr.Microphone() as source:
    while True:
        initial(source)
   