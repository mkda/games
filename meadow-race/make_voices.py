# Builds meadow-race/voices/*.mp3: EP01 movie lines reused as-is, new game lines made with the studio's
# own Kokoro settings (cast.json voice, speed, semitones, -18 LUFS), exactly like _studio/engine/voices_en.py.
import json, os, subprocess
import soundfile as sf
from kokoro_onnx import Kokoro
U = os.path.expanduser("~/Movies/AI Kids Stories Studio/")  # the LittleLeap studio folder
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voices/")
cast = json.load(open(U + "_studio/cast/cast.json"))["characters"]
k = Kokoro(os.path.expanduser("~/.littleleap-studio/tts/kokoro-v1.0.onnx"), os.path.expanduser("~/.littleleap-studio/tts/voices-v1.0.bin"))

MOVIE = {  # game id -> EP01 file
 "olly_marks": "S18_1_OLLY", "olly_go": "S18_2_OLLY", "zippy_seeyou": "S18_3_ZIPPY", "tomo_steady": "S20_2_TOMO",
 "tomo_strawberries": "S17_2_TOMO", "snail_excuse": "S08_2_SNAIL", "tomo_sleeping": "S35_2_TOMO",
 "zippy_carrots": "S26_2_ZIPPY", "tomo_dreams": "S36_2_TOMO", "pippop_gotomo": "S40_2_PIPPOP",
 "narr_cheer": "S40_3_NARRATOR", "olly_winner": "S42_2_OLLY", "narr_meadow": "S42_3_NARRATOR",
 "zippy_how": "S43_1_ZIPPY", "tomo_didnt_stop": "S43_2_TOMO", "zippy_champion": "S44_1_ZIPPY",
 "pippop_steady": "S45_2_PIPPOP", "narr_sing": "S13_1_NARRATOR",
}
NEW = {
 "narr_welcome": ("NARRATOR", "Welcome to the Big Meadow Race! Zippy and Tomo are waiting at the Big Oak."),
 "narr_tap_olly": ("NARRATOR", "Tap Judge Olly to start the race!"),
 "narr_hold": ("NARRATOR", "Now it's your turn to help Tomo. Press and hold your finger on the screen to make him walk."),
 "narr_hold_hint": ("NARRATOR", "Press and hold, and Tomo will walk!"),
 "narr_stream": ("NARRATOR", "Splish, splash! Here is Giggle Stream."),
 "snail_luck": ("SNAIL", "Good luck, Tomo!"),
 "narr_shh": ("NARRATOR", "Shhh! Zippy is having a nap. Let's tiptoe past, very quietly."),
 "narr_count": ("NARRATOR", "Let's count Tomo's strawberries together!"),
 "narr_ten": ("NARRATOR", "Ten strawberries! What a super picnic!"),
 "narr_some": ("NARRATOR", "Yummy strawberries! Well done!"),
 "narr_none": ("NARRATOR", "Next time, let's find some strawberries!"),
 "tomo_share": ("TOMO", "Strawberries for everyone! Thank you for helping me."),
 "narr_title": ("NARRATOR", "The Big Meadow Race!"),
}
for i, w in enumerate(["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"], 1):
    NEW[f"n{i}"] = ("NARRATOR", w + "!")

def mp3(src, dst, filters="loudnorm=I=-18:TP=-2:LRA=7"):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", filters + ",silenceremove=start_periods=1:start_threshold=-50dB",
                    "-ar", "44100", "-ac", "1", "-b:a", "64k", dst], check=True)

for gid, f in MOVIE.items():
    mp3(U + f"01 Tortoise and Hare pilot/03 Voices/{f}.wav", OUT + gid + ".mp3", "anull")
for gid, (spk, text) in NEW.items():
    v = cast[spk]["voice"]; voice, spd, semi = v["kokoro"], v.get("speed", 1.0), v.get("semitones", 0)
    audio, sr = k.create(text, voice=voice, speed=spd, lang="en-us" if voice[0] == "a" else "en-gb")
    raw = f"/tmp/{gid}.wav"; sf.write(raw, audio, sr)
    f = []
    if semi:
        r = 2 ** (semi / 12); f.append(f"asetrate={sr}*{r:.4f},aresample={sr},atempo={1 / r:.4f}")
    f.append("loudnorm=I=-18:TP=-2:LRA=7")
    mp3(raw, OUT + gid + ".mp3", ",".join(f)); os.remove(raw)
lines = {**{g: {"from": MOVIE[g]} for g in MOVIE}, **{g: {"speaker": s, "text": t} for g, (s, t) in NEW.items()}}
json.dump(lines, open(OUT + "lines.json", "w"), indent=1)
print(len(lines), "lines")
