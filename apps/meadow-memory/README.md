# Meadow Memory: iOS and Android apps

The apps wrap the web game in `../../memory` with Capacitor 8; there is no separate app code. `prepare-www.js` copies the game into `www/`, leaving out the web-only and store files.

Build on the Mac with `python3 build_mac.py setup | android | ios | upload-ios`. The steps are described at the top of `build_mac.py`.

- App id: `com.littleleapstudios.meadowmemory`.
- Version: 1.0.0, build 1.
- Android target: API 36. Google Play requires it for new apps from 31 Aug 2026.
- `assets/`: the source icon (1024) and the splash screens; `npm run assets` makes every size.
- Store texts and screenshots are in `../../memory/store/`.
