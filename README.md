# AI Video Clip Maker (Web + Android)

A starter project for uploading a long video, splitting it into consecutive 60-second clips,
previewing them, and downloading each clip. It includes a lightweight "Smart Highlights" mode
that ranks 60-second segments using audio loudness and scene-change activity. This is a heuristic,
not a cloud AI model; it works locally and needs no API key.

## Requirements
- Python 3.10+
- FFmpeg installed and available on PATH
- Node.js 18+ (only for Android packaging)
- Android Studio + Android SDK (for APK build)

## Run the backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Run the web app
Open `frontend/index.html` in a browser, or serve it:
```bash
cd frontend
python -m http.server 5173
```
The app expects the backend at `http://localhost:8000`. Change `API_BASE` in
`frontend/app.js` when hosting the backend elsewhere.

## Android APK (Capacitor wrapper)
```bash
cd frontend
npm install
npx cap add android
npx cap sync android
npx cap open android
```
In Android Studio choose **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
Set `API_BASE` in `app.js` to your computer/server's reachable LAN or HTTPS address
before syncing. `localhost` on an Android phone means the phone itself, not your PC.

## Notes
- Standard mode makes sequential clips: 00:00–01:00, 01:00–02:00, etc.
- Vertical mode center-crops to 9:16. Keep the original aspect ratio if you want the full frame.
- Smart Highlights ranks segments; it does not understand story context or guarantee viral moments.
- For public deployment, add authentication, upload limits, HTTPS, storage cleanup, and a job queue.
