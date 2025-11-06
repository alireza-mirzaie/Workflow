import subprocess, os

os.makedirs("out", exist_ok=True)

BG = os.getenv(
    "BG_URL",
    "https://images.pexels.com/photos/586339/pexels-photo-586339.jpeg"
)
MUSIC = os.getenv(
    "MUSIC_URL",
    "https://cdn.pixabay.com/download/audio/2021/10/26/audio_tech_demo.mp3?filename=tech-demo.mp3"
)

# دانلود بک‌گراند و موزیک
subprocess.check_call(["bash","-lc",f"wget -O out/bg.jpg '{BG}'"])
subprocess.check_call(["bash","-lc",f"wget -O out/music.mp3 '{MUSIC}'"])

# ساخت ویدیو عمودی 1080x1920 + ducking موزیک زیر صدا
cmd = [
  "ffmpeg","-y",
  "-loop","1","-i","out/bg.jpg",
  "-i","out/voice.mp3","-i","out/music.mp3",
  "-filter_complex",
  "[1:a]volume=1.0[aud];[2:a]volume=0.35[bgm];"
  "[aud][bgm]sidechaincompress=threshold=0.05:ratio=8:attack=5:release=150[mix];"
  "[0:v]scale=1080:1920,format=yuv420p[v]",
  "-map","[v]","-map","[mix]","-c:v","libx264","-pix_fmt","yuv420p","-r","30",
  "-preset","veryfast","-b:v","4500k","-c:a","aac","-b:a","160k","-shortest",
  "out/final_vertical.mp4"
]
subprocess.check_call(cmd)
print("video_ready=1")
