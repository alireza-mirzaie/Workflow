from gtts import gTTS
import os

os.makedirs("out", exist_ok=True)
text = open("out/script.txt", "r", encoding="utf-8").read().strip()
if not text:
    text = "سلام! امروز یک خبر کوتاه تکنولوژی داریم."
gTTS(text, lang="fa").save("out/voice.mp3")
print("voice_ready=1")
