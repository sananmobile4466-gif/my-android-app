# AI Video Clip Maker — Android APK Build Package

## Important
This is a build-ready source package, not a precompiled APK. An Android APK must be compiled with Android Studio / Android SDK on a computer. This environment does not have the Android SDK installed, so it cannot produce a tested APK binary here.

## Windows 10 prerequisites
1. Install Python 3 and FFmpeg (required by the backend).
2. Install Node.js LTS: https://nodejs.org/
3. Install Android Studio: https://developer.android.com/studio
4. In Android Studio, install the Android SDK and accept SDK licenses.

## Build Android project
1. Extract this ZIP.
2. Double-click `BUILD_ANDROID_APK.bat` in the extracted main folder.
3. It installs Capacitor dependencies, creates/syncs the Android project, and opens Android Studio.
4. Wait for Gradle sync.
5. In Android Studio select **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
6. Debug APK normally appears at:
   `frontend/android/app/build/outputs/apk/debug/app-debug.apk`

## Run the app
The Android app is a mobile wrapper for the dashboard. Video processing runs on the Python + FFmpeg backend:
1. Start the backend on your PC using the existing Windows launcher or backend instructions.
2. Find your PC's local IPv4 address using `ipconfig`.
3. Open the app's Backend server address field and enter `http://YOUR_PC_IP:8000`, e.g. `http://192.168.1.5:8000`.
4. Keep the phone and PC on the same Wi-Fi network, and keep the backend running.
5. Select a video, choose 1 minute and 9:16 if desired, then create clips.

## Included features
- Upload video from Android device/browser
- Consecutive 60-second clips (or selectable durations)
- 9:16 vertical center crop or original aspect ratio
- Clip preview and individual downloads
- Smart Highlights heuristic ranking using audio loudness and scene-change activity

Smart Highlights is a lightweight heuristic, not semantic AI. The backend uses FFmpeg; it is not embedded inside the APK. For a fully standalone offline Android app, the processing engine would need to be ported into the app separately.
