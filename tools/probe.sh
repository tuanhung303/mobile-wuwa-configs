#!/bin/bash
# probe.sh NAME LOCAL_FILE|none REMOTE_INI : stop the game, push the file read-only,
# relaunch, tap through the title screen, take a screenshot and pull + decrypt Client.log.
# Tap point (500,419) is the title screen "tap to start" area; timings fit a fast phone.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${WUWA_OUT:-$PWD/out}
PKG=com.kurogame.wutheringwaves.global
SAVED=/sdcard/Android/data/$PKG/files/UE4Game/Client/Client/Saved
CFG=$SAVED/Config/Android
mkdir -p "$OUT/logs"
adb shell am force-stop $PKG
sleep 2
if [ "$2" != "none" ]; then
  chmod 444 "$2"                      # read-only, or the game truncates the file at launch
  adb shell rm -f "$CFG/$3"           # a push over a read-only file is not reliable
  adb push "$2" "$CFG/$3" >/dev/null
  adb shell ls -la "$CFG/$3"
fi
adb shell monkey -p $PKG -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
sleep 45
"$HERE/wuwa.sh" shot "$1_title" 600 >/dev/null
"$HERE/wuwa.sh" tap 500 419; sleep 4; "$HERE/wuwa.sh" tap 500 419
sleep 45
"$HERE/wuwa.sh" shot "$1"
adb pull "$SAVED/Logs/Client.log" "$OUT/logs/$1.log" >/dev/null && python3 "$HERE/decrypt_log.py" "$OUT/logs/$1.log"
