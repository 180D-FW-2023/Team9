import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

freq = 44100
duration = 3
model = whisper.load_model("tiny.en")
c = 'c'
while True:
    c = input("Press c to run again or press s to stop \n")
    if c == 's':
        break
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    print('Speak')
    sd.wait()
    print('Stop')
    write("recording0.wav", freq, recording)

    result = model.transcribe("recording0.wav", fp16=False)
    if "Hey Jarvis" in result["text"]:
        print(result["text"])
        print("Hello sir do you have a question?")
    elif "Hey David" in result["text"]:
        print(result["text"])
        print("I am intimidated by Didier!")
    #print(result["text"])