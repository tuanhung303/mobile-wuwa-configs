#!/bin/bash
# Phone helper for WuWa tuning over adb. Set ANDROID_SERIAL when more than one device is attached.
# Tap and swipe coordinates are in a 1000-px-wide screenshot space (landscape).
# Output goes to $WUWA_OUT (default ./out).
OUT=${WUWA_OUT:-$PWD/out}
HERE=$(cd "$(dirname "$0")" && pwd)
PKG=com.kurogame.wutheringwaves.global
DB=/sdcard/Android/data/$PKG/files/UE4Game/Client/Client/Saved/LocalStorage/LocalStorage.db
mkdir -p "$OUT/shots" "$OUT/db"
K=${WUWA_K:-$(adb shell wm size | grep -o -E '[0-9]+x[0-9]+' | tail -1 | awk -Fx '{m=($1>$2)?$1:$2; print m/1000}')}
sx() { python3 -c "print(round($1*$K))"; }
case "$1" in
  shot)  # shot NAME [width]
    adb exec-out screencap -p > "$OUT/shots/$2.png" && sips -Z "${3:-1000}" "$OUT/shots/$2.png" --out "$OUT/shots/$2_s.png" >/dev/null && echo "$OUT/shots/$2_s.png" ;;
  tap)   adb shell input tap "$(sx "$2")" "$(sx "$3")" ;;
  swipe) adb shell input swipe "$(sx "$2")" "$(sx "$3")" "$(sx "$4")" "$(sx "$5")" "${6:-300}" ;;
  key)   adb shell input keyevent "$2" ;;
  db)    # db NAME : snapshot of the menu settings (LocalStorage.db), short values only
    adb pull "$DB" "$OUT/db/$2.db" >/dev/null && sqlite3 "$OUT/db/$2.db" "select key,value from LocalStorage where length(value)<40 and key not glob '*_90[0-9]*' order by key" > "$OUT/db/$2.txt" && echo "$OUT/db/$2.txt" ;;
  temp)  adb shell "dumpsys battery | grep -E '^  (temperature|level)'" ;;
  fps)   # fps SECONDS : average fps and frame-time spread of the game layer (SurfaceFlinger timestats)
    adb shell dumpsys SurfaceFlinger --timestats -enable -clear >/dev/null
    sleep "$2"
    adb shell dumpsys SurfaceFlinger --timestats -dump > "$OUT/fps_raw.txt"
    adb shell dumpsys SurfaceFlinger --timestats -disable >/dev/null
    python3 "$HERE/fps_parse.py" "$OUT/fps_raw.txt" ;;
  *) echo "usage: wuwa.sh shot|tap|swipe|key|db|temp|fps" ;;
esac
