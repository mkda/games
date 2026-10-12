# Builds memory/assets (character pictures, logo, meadow plate) and memory/voices (each friend says their
# name in their own studio Kokoro voice) from the LittleLeap studio folder. Run on the Mac: python3 make_assets.py
import json, os, subprocess, numpy as np
from PIL import Image
from collections import deque
import soundfile as sf
U = os.path.expanduser("~/Movies/AI Kids Stories Studio/_studio/")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")
cast = json.load(open(U + "cast/cast.json"))["characters"]
CHARS = [("TOMO","Tomo"),("ZIPPY","Zippy"),("OLLY","Olly"),("PIP","Pip"),("POP","Pop"),("FREDDIE","Freddie"),("SNAIL","Snail"),
         ("LITTLE_SUGAR","Little Sugar"),("JOHNATAN","Johnatan"),("JULIA","Julia"),("DAVID","David"),("MARCO","Marco"),
         ("SILVIA","Silvia"),("MURIEL","Muriel"),("ALEX","Alex"),("BAO","Bao"),("TARA","Tara"),("LEO","Leo")]
MASTER = {"LITTLE_SUGAR","MARCO","SILVIA","MURIEL","TARA"}
def knock_white(im):
    a = np.array(im.convert("RGBA")); h, w = a.shape[:2]
    rgb = a[:,:,:3].astype(int); near = (rgb.min(2) > 222) & ((rgb.max(2) - rgb.min(2)) < 30)
    seen = np.zeros((h,w), bool); q = deque()
    for x in range(w): q += [(0,x),(h-1,x)]
    for y in range(h): q += [(y,0),(y,w-1)]
    while q:
        y,x = q.popleft()
        if seen[y,x] or not near[y,x]: continue
        seen[y,x] = True
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx = y+dy,x+dx
            if 0<=ny<h and 0<=nx<w and not seen[ny,nx]: q.append((ny,nx))
    a[seen,3] = 0
    return Image.fromarray(a)
meta = []
for cid, short in CHARS:
    src = U + (f"cast/masters/{cid}/CS_{cid}_master.png" if cid in MASTER else f"cast/poses/{cid}/poses/happy.png")
    im = Image.open(src)
    if cid in MASTER: im = knock_white(im)
    im = im.convert("RGBA")
    a = np.array(im)[:,:,3] > 40
    ys, xs = np.where(a); im = im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
    im.thumbnail((380, 380), Image.LANCZOS)
    im.save(OUT + f"assets/{cid.lower()}.webp", "WEBP", quality=88, method=6)
    c = cast[cid]
    meta.append({"id": cid.lower(), "name": short, "species": c.get("species","").split(" (")[0], "color": c["signature"]["hex"]})
json.dump(meta, open("/tmp/mem_meta.json","w"))
# voices
from kokoro_onnx import Kokoro
k = Kokoro(os.path.expanduser("~/.littleleap-studio/tts/") + "kokoro-v1.0.onnx", os.path.expanduser("~/.littleleap-studio/tts/") + "voices-v1.0.bin")
def synth(spk, text, gid):
    v = cast[spk]["voice"]; voice, spd, semi = v["kokoro"], v.get("speed",1.0), v.get("semitones",0)
    audio, sr = k.create(text, voice=voice, speed=spd, lang="en-us" if voice[0]=="a" else "en-gb")
    raw = f"/tmp/{gid}.wav"; sf.write(raw, audio, sr); f=[]
    if semi: r = 2**(semi/12); f.append(f"asetrate={sr}*{r:.4f},aresample={sr},atempo={1/r:.4f}")
    f.append("loudnorm=I=-18:TP=-2:LRA=7,silenceremove=start_periods=1:start_threshold=-50dB")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",",".join(f),"-ar","44100","-ac","1","-b:a","64k",OUT+f"voices/{gid}.mp3"],check=True); os.remove(raw)
lines = {}
for cid, short in CHARS:
    nm = {"OLLY": "Judge Olly", "SNAIL": "Snail"}.get(cid, short)
    t1 = f"I'm {nm}!"; t2 = f"You found me! Hooray!"
    synth(cid, t1, f"{cid.lower()}_name"); synth(cid, t2, f"{cid.lower()}_found")
    lines[f"{cid.lower()}_name"] = t1; lines[f"{cid.lower()}_found"] = t2
NARR = {
 "narr_title": "Meadow Memory!",
 "narr_pick": "How many cards? Pick one!",
 "narr_start": "Tap two cards. Can you find the friends who match?",
 "narr_try": "Try again!",
 "narr_win": "You found all the friends! Hooray!",
 "narr_again": "Let's play again!",
}
for gid, t in NARR.items(): synth("NARRATOR", t, gid); lines[gid] = t
json.dump(lines, open(OUT + "voices/lines.json", "w"), indent=1)
print(json.dumps(meta))
