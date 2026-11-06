import os, uuid, shutil, subprocess, json, re
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

BASE = Path(__file__).parent
DATA = BASE / "data"
UPLOADS = DATA / "uploads"
OUTPUTS = DATA / "outputs"
for p in (UPLOADS, OUTPUTS):
    p.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="AI Video Clip Maker API")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
app.mount("/files", StaticFiles(directory=str(DATA)), name="files")

def run(cmd):
    try:
        return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    except FileNotFoundError:
        raise HTTPException(500, "FFmpeg/FFprobe is not installed or not on PATH.")
    except subprocess.CalledProcessError as e:
        raise HTTPException(500, (e.stderr or "Video processing failed")[-1800:])

def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", str(path)])
    return float(out.strip())

def smart_score(path, start, length):
    # Lightweight local heuristic: average audio loudness + visual scene-change count.
    # It ranks segments; it is not semantic AI.
    audio_cmd = ["ffmpeg", "-ss", str(start), "-t", str(length), "-i", str(path),
                 "-vn", "-af", "volumedetect", "-f", "null", "-"]
    try:
        p = subprocess.run(audio_cmd, capture_output=True, text=True)
        m = re.search(r"mean_volume:\s*(-?[\d.]+)\s*dB", p.stderr)
        loudness = max(0.0, min(1.0, (float(m.group(1)) + 60) / 60)) if m else 0.0
    except Exception:
        loudness = 0.0
    scene_cmd = ["ffmpeg", "-ss", str(start), "-t", str(length), "-i", str(path),
                 "-vf", "select='gt(scene,0.30)',showinfo", "-an", "-f", "null", "-"]
    try:
        p = subprocess.run(scene_cmd, capture_output=True, text=True)
        scenes = len(re.findall(r"showinfo", p.stderr))
        visual = min(1.0, scenes / 12.0)
    except Exception:
        visual = 0.0
    return round(0.55 * loudness + 0.45 * visual, 3)

@app.get("/health")
def health():
    return {"ok": True, "service": "AI Video Clip Maker"}

@app.post("/process")
async def process_video(
    video: UploadFile = File(...),
    clip_seconds: int = Form(60),
    vertical: bool = Form(True),
    smart_highlights: bool = Form(False)
):
    if clip_seconds < 10 or clip_seconds > 600:
        raise HTTPException(400, "Clip duration must be between 10 and 600 seconds.")
    ext = Path(video.filename or "video.mp4").suffix.lower()
    if ext not in {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}:
        raise HTTPException(400, "Unsupported video type.")
    job = uuid.uuid4().hex[:12]
    src_dir = UPLOADS / job
    out_dir = OUTPUTS / job
    src_dir.mkdir(parents=True)
    out_dir.mkdir(parents=True)
    source = src_dir / ("source" + ext)
    with source.open("wb") as f:
        shutil.copyfileobj(video.file, f)

    total = duration(source)
    if total <= 0:
        raise HTTPException(400, "Could not read video duration.")
    count = int((total + clip_seconds - 1) // clip_seconds)
    clips = []
    scores = []
    for i in range(count):
        start = i * clip_seconds
        length = min(clip_seconds, total - start)
        name = f"clip_{i+1:03d}.mp4"
        target = out_dir / name
        cmd = ["ffmpeg", "-y", "-ss", str(start), "-i", str(source), "-t", str(length)]
        if vertical:
            # Center crop to 9:16; scale to 1080x1920.
            cmd += ["-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(target)]
        run(cmd)
        score = smart_score(source, start, length) if smart_highlights else None
        if score is not None:
            scores.append((score, i))
        clips.append({
            "name": name, "start": round(start, 2), "duration": round(length, 2),
            "url": f"/files/outputs/{job}/{name}", "score": score
        })
    if smart_highlights:
        clips.sort(key=lambda c: c["score"] or 0, reverse=True)
    return {"job_id": job, "total_seconds": round(total, 2),
            "clip_count": len(clips), "clips": clips,
            "message": "Completed. Smart Highlights are heuristic rankings, not semantic AI."}
