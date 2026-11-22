"""Builds the Meadow Memory apps on the Mac (store release, 22 Nov 2026).

usage: python3 build_mac.py setup | android | ios | upload-ios
  setup       clone/pull github.com/mkda/games into _studio/apps/games, npm install, add the iOS/Android projects,
              generate icons + splash, apply the native settings below
  android     signed release bundle (.aab) for Google Play  -> apps/meadow-memory/release/
  ios         signed App Store archive + .ipa             -> apps/meadow-memory/release/
  upload-ios  uploads the archive to App Store Connect (the app record must exist first)

Signing:
- Android: an upload key is made once at ~/.littleleap-keys/meadow-memory-upload.jks. Its password is kept in the
  macOS Keychain (service "meadow-memory-upload"). Google Play App Signing holds the real app key, and a lost upload
  key can be reset in the Play Console.
- iOS: automatic signing with the Apple Developer team that is signed into Xcode (-allowProvisioningUpdates).
"""
import json, os, re, secrets, shutil, subprocess, sys

HOME = os.path.expanduser("~")
STUDIO = os.path.join(HOME, "Movies", "AI Kids Stories Studio", "_studio")
REPO = os.path.join(STUDIO, "apps", "games")
APP = os.path.join(REPO, "apps", "meadow-memory")
REL = os.path.join(APP, "release")
KEYS = os.path.join(HOME, ".littleleap-keys")
KS = os.path.join(KEYS, "meadow-memory-upload.jks")
APP_ID = "com.littleleapstudios.meadowmemory"
VERSION, BUILD = "1.0.0", 1
JAVA_HOME = "/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
ENV = dict(os.environ, PATH=f"/opt/homebrew/bin:/opt/homebrew/sbin:{JAVA_HOME}/bin:/usr/bin:/bin:/usr/sbin:/sbin",
           JAVA_HOME=JAVA_HOME, ANDROID_HOME=os.path.join(HOME, "Library", "Android", "sdk"),
           ANDROID_SDK_ROOT=os.path.join(HOME, "Library", "Android", "sdk"),
           DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer", HOMEBREW_NO_AUTO_UPDATE="1", CI="1")


def run(cmd, cwd=None, check=True, quiet=False):
    print("$", cmd, flush=True)
    r = subprocess.run(cmd, shell=True, cwd=cwd, env=ENV, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout or ""
    print(out[-4000:] if not quiet else out[-600:], flush=True)
    if check and r.returncode: print(f"FAILED ({r.returncode}): {cmd}"); sys.exit(1)
    return out


def sub(path, pattern, repl, count=1):
    s = open(path).read(); n = re.sub(pattern, repl, s, count=count)
    if n != s: open(path, "w").write(n); print("edited", os.path.relpath(path, APP))
    return n != s


def setup():
    os.makedirs(os.path.dirname(REPO), exist_ok=True)
    if os.path.isdir(os.path.join(REPO, ".git")): run("git pull --ff-only", cwd=REPO)
    else: run(f'git clone https://github.com/mkda/games "{REPO}"')
    run("npm install --no-audit --no-fund", cwd=APP, quiet=True)
    run("node prepare-www.js", cwd=APP)
    for p in ("ios", "android"):
        if not os.path.isdir(os.path.join(APP, p)): run(f"npx cap add {p}", cwd=APP)
    run("npm run assets", cwd=APP, quiet=True)
    run("npx cap sync", cwd=APP)
    # ---- Android: SDK 36, version, landscape + portrait, release signing from the Keychain password
    var = os.path.join(APP, "android", "variables.gradle")
    sub(var, r"compileSdkVersion = \d+", "compileSdkVersion = 36"); sub(var, r"targetSdkVersion = \d+", "targetSdkVersion = 36")
    gradle = os.path.join(APP, "android", "app", "build.gradle")
    sub(gradle, r"versionCode \d+", f"versionCode {BUILD}"); sub(gradle, r'versionName "[^"]*"', f'versionName "{VERSION}"')
    g = open(gradle).read()
    if "littleleapUpload" not in g:
        g = g.replace("    buildTypes {", """    signingConfigs {
        littleleapUpload {
            storeFile file(System.getenv("LL_KEYSTORE") ?: "missing.jks")
            storePassword System.getenv("LL_KEY_PASS") ?: ""
            keyAlias "upload"
            keyPassword System.getenv("LL_KEY_PASS") ?: ""
        }
    }
    buildTypes {""", 1)
        g = re.sub(r"(release \{\n)", r"\1            signingConfig signingConfigs.littleleapUpload\n", g, count=1)
        open(gradle, "w").write(g); print("edited android/app/build.gradle (signing)")
    # ---- iOS: version, no encryption, full screen, no status bar
    plist = os.path.join(APP, "ios", "App", "App", "Info.plist")
    pb = "/usr/libexec/PlistBuddy"
    for k, t, v in (("ITSAppUsesNonExemptEncryption", "bool", "false"), ("UIStatusBarHidden", "bool", "true"),
                    ("UIViewControllerBasedStatusBarAppearance", "bool", "false"), ("UIRequiresFullScreen", "bool", "true")):
        run(f'{pb} -c "Delete :{k}" "{plist}"', check=False, quiet=True)
        run(f'{pb} -c "Add :{k} {t} {v}" "{plist}"', quiet=True)
    pbx = os.path.join(APP, "ios", "App", "App.xcodeproj", "project.pbxproj")
    sub(pbx, r"MARKETING_VERSION = [^;]+;", f"MARKETING_VERSION = {VERSION};", count=0)
    sub(pbx, r"CURRENT_PROJECT_VERSION = [^;]+;", f"CURRENT_PROJECT_VERSION = {BUILD};", count=0)
    print("SETUP DONE")


def key_pass():
    r = subprocess.run(["security", "find-generic-password", "-s", "meadow-memory-upload", "-a", "upload", "-w"], text=True, capture_output=True)
    if r.returncode == 0: return r.stdout.strip()
    pw = secrets.token_urlsafe(24)
    subprocess.run(["security", "add-generic-password", "-s", "meadow-memory-upload", "-a", "upload", "-w", pw,
                    "-j", "Meadow Memory Google Play upload key (keystore ~/.littleleap-keys/meadow-memory-upload.jks)"], check=True)
    return pw


def android():
    pw = key_pass()
    os.makedirs(KEYS, exist_ok=True)
    if not os.path.exists(KS):
        ENV["LL_TMP_PASS"] = pw
        run(f'keytool -genkeypair -v -keystore "{KS}" -alias upload -keyalg RSA -keysize 4096 -validity 10000 '
            f'-storepass:env LL_TMP_PASS -keypass:env LL_TMP_PASS -dname "CN=Mikael Dell\'Anna, O=LittleLeap Studios, L=Zurich, C=CH"', quiet=True)
        ENV.pop("LL_TMP_PASS")
    ENV["LL_KEYSTORE"], ENV["LL_KEY_PASS"] = KS, pw
    run("npx cap sync android", cwd=APP, quiet=True)
    run("./gradlew --no-daemon bundleRelease", cwd=os.path.join(APP, "android"), quiet=True)
    ENV.pop("LL_KEY_PASS")
    os.makedirs(REL, exist_ok=True)
    src = os.path.join(APP, "android", "app", "build", "outputs", "bundle", "release", "app-release.aab")
    dst = os.path.join(REL, f"MeadowMemory-{VERSION}-{BUILD}.aab"); shutil.copy(src, dst)
    print("ANDROID DONE", dst, os.path.getsize(dst))


def team_id():
    pem = run('security find-certificate -c "Apple Development" -p', quiet=True)
    open("/tmp/ll_dev.pem", "w").write(pem)
    subj = subprocess.run("openssl x509 -noout -subject -in /tmp/ll_dev.pem", shell=True, text=True, capture_output=True).stdout
    m = re.search(r"OU\s*=\s*([A-Z0-9]{10})", subj)
    if not m: print("no team id in", subj); sys.exit(1)
    return m.group(1)


def ios():
    team = team_id(); print("team", team)
    run("npx cap sync ios", cwd=APP, quiet=True)
    os.makedirs(REL, exist_ok=True)
    arch = os.path.join(REL, "MeadowMemory.xcarchive")
    shutil.rmtree(arch, ignore_errors=True)
    proj = os.path.join(APP, "ios", "App", "App.xcodeproj")
    run(f'xcodebuild -project "{proj}" -scheme App -configuration Release -destination "generic/platform=iOS" '
        f'-archivePath "{arch}" -allowProvisioningUpdates DEVELOPMENT_TEAM={team} CODE_SIGN_STYLE=Automatic archive', quiet=True)
    opts = os.path.join(REL, "ExportOptions.plist")
    open(opts, "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>method</key><string>app-store-connect</string><key>teamID</key><string>{team}</string>
<key>signingStyle</key><string>automatic</string><key>destination</key><string>export</string>
<key>uploadSymbols</key><true/><key>manageAppVersionAndBuildNumber</key><false/>
</dict></plist>""")
    run(f'xcodebuild -exportArchive -archivePath "{arch}" -exportOptionsPlist "{opts}" -exportPath "{REL}" -allowProvisioningUpdates', quiet=True)
    print("IOS DONE", [f for f in os.listdir(REL)])


def upload_ios():
    arch = os.path.join(REL, "MeadowMemory.xcarchive"); opts = os.path.join(REL, "ExportOptions-upload.plist")
    s = open(os.path.join(REL, "ExportOptions.plist")).read().replace("<string>export</string>", "<string>upload</string>")
    open(opts, "w").write(s)
    run(f'xcodebuild -exportArchive -archivePath "{arch}" -exportOptionsPlist "{opts}" -exportPath "{REL}/upload" -allowProvisioningUpdates', quiet=True)
    print("UPLOAD DONE")


if __name__ == "__main__":
    {"setup": setup, "android": android, "ios": ios, "upload-ios": upload_ios}[sys.argv[1]]()
    print("DONE")
