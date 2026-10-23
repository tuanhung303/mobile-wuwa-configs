# Mobile WuWa configs

Graphics tuning for Wuthering Waves on Android, tested on version 3.7.1 (global) on 2026-10-23.

Test phone: REDMAGIC 11 Pro (NX809J, SM8850, Adreno 840, 16 GB), Android 16. The game selects the device profile `Android_Adreno840`.

Every claim here was checked in the game's own decrypted `Client.log`. How the game loads config, and what each test showed, is in [FINDINGS.md](FINDINGS.md).

## What works on 3.7.1

Two layers:

1. **In-game menu at max.** These settings changed:

   | Setting | From | To |
   |---|---|---|
   | Anisotropic filtering | 1x | 16x |
   | Shadow | High | Ultra High |
   | LOD bias | High | Ultra High |
   | Resolution | High | Ultra High |
   | Capsule AO | Off | On |

   Kept: Effects High (max), Foliage Ultra High, FSR On, Frame Generation Off, 90 fps. For 60 fps with frame generation, turn Frame Generation On.

2. **[config/Scalability.ini](config/Scalability.ini), pushed read-only.** Its PostProcess, Effects, Foliage and Texture sections copy Kuro's own higher-tier values into the levels the menu runs at. Its Shadow@3 and ViewDistance@2 sections are custom values above Kuro's top tier. It holds no forbidden cvars, so ConfigMonitor strips nothing.

   | Area | Stock (active level) | With this file |
   |---|---|---|
   | Shadow filtering (PCF), 4 cascades | 2 | 3 |
   | Per-object (character) shadow resolution | 512 | 1024 |
   | Shadow mask scale | 0.5 | 1.0 |
   | Skeletal mesh shadow LOD bias | 4 | 0 |
   | Screen-space reflections (SSR) | 2, half-res scene color | 3, full res |
   | Screen-space GI (SSGI) | 2 | 3 |
   | Subsurface scattering (skin) | -1 (auto), half res | 1, full res |
   | Particle spawn rate | 0.5 | 1.0 |
   | Niagara quality | 1 | 2 |
   | Particle lights | 1 | 2 |
   | Sky atmosphere samples | 64 | 128 |
   | Static mesh LOD distance scale | not set (engine default 1.0) | 0.75 |
   | DOF and AO post-process | @2 set | @3 set |

The levels the file targets (ViewDistance@2, AA@2, Shadow@3, PostProcess@2, Texture@2, Effects@2, Foliage@2) are what the menu runs at max settings on this phone. If you change Shadow, Effects or Post-process in the menu, or your phone picks another profile, the matching section stops applying. Check your levels with `tools/sections.py` and rebuild the file with `tools/gen_scalability.py`.

## Install

```sh
PKG=com.kurogame.wutheringwaves.global
CFG=/sdcard/Android/data/$PKG/files/UE4Game/Client/Client/Saved/Config/Android
adb shell am force-stop $PKG
chmod 444 config/Scalability.ini            # read-only, or the game empties the file at launch
adb shell rm -f $CFG/Scalability.ini        # a push over a read-only file is not reliable
adb push config/Scalability.ini $CFG/Scalability.ini
adb shell ls -la $CFG/Scalability.ini       # expect -r--r--r--
```

Check it worked after one launch:

```sh
adb pull /sdcard/Android/data/$PKG/files/UE4Game/Client/Client/Saved/Logs/Client.log
python3 tools/decrypt_log.py Client.log
python3 tools/sections.py Client.log.txt | grep -E 'EffectsQuality@2|ShadowQuality@3'
grep -a 'forbidden CVars' Client.log.txt    # expect no line for Scalability.ini
```

## Undo

```sh
adb shell rm -f $CFG/Scalability.ini        # the game creates an empty one at next launch
```

Then set the menu back by hand.

## What Kuro blocks

These cannot be raised through any Saved ini file. ConfigMonitor strips them, even inside Scalability.ini:

- Material quality (`r.MaterialQualityLevel`, `r.KuroMaterialQualityLevel`), which stays at "Middle" at max menu settings.
- Cascaded shadow map resolution (`r.Shadow.MaxCSMResolution`, 512), `r.Shadow.MaxResolution`, `r.Shadow.DistanceScale`.
- View distance (`r.ViewDistanceScale`), texture pool (`r.Streaming.PoolSize`, `r.Streaming.PoolSizeForMeshes`).
- Render resolution (`r.ScreenPercentage`, `r.MobileContentScaleFactor`, `r.SecondaryScreenPercentage.GameViewport`, which the game sets to 90).

`sg.*` levels come from the device profile, so `sg.*` lines in Scalability.ini or GameUserSettings.ini do nothing. A Saved DeviceProfiles.ini and `dp.Override` did not change them either. The full list is in [tools/forbidden_cvars.txt](tools/forbidden_cvars.txt).

## Risk

ConfigMonitor logs every edited Saved ini ("has been modified, because its hash doesn't match"). There are community reports that Kuro watches this, but I found no confirmed ban for it. This file holds no forbidden cvars; most of its values are Kuro's own higher-tier values, and the shadow and LOD lines are custom. Use it at your own risk.

## Results on the test phone

Average FPS of the game layer, standing still at the same spot, 20–30-second SurfaceFlinger sample:

| State | Avg FPS | Battery |
|---|---|---|
| Stock menu | 89.8 | 41–42 °C |
| Menu at max | 76.5 | 42 °C |
| Menu at max, phone hot and charging (control) | 50.0 | 44 °C |
| Menu at max + Scalability.ini, same conditions | 50.1 (1% low ~45.5) | 44 °C |

The last two rows were taken while the CPU was throttled (prime core capped at 2.88 of 4.61 GHz, read 8 minutes after the last sample). Under that cap, the file cost no FPS against the control. The cost on a cool phone in combat was not measured.

## Tools

| File | Use |
|---|---|
| `tools/decrypt_log.py` | Decrypt `Client.log` (3.x builds encrypt it). |
| `tools/sections.py` | Print what each Scalability section sets, and which cvars a higher priority kept. |
| `tools/gen_scalability.py` | Rebuild `config/Scalability.ini` from a decrypted log. |
| `tools/forbidden_cvars.txt` | Cvars ConfigMonitor strips. |
| `tools/probe.sh` | Push a file read-only, relaunch, screenshot, pull and decrypt the log. |
| `tools/wuwa.sh` | Screenshot, tap, FPS sample, battery temperature, menu settings snapshot. |
| `tools/fps_parse.py` | Parse SurfaceFlinger timestats for `wuwa.sh fps`. |

## Archive

The old v6.0.0-thermal pack (Engine.ini, DeviceProfiles.ini, Performance.ini and its guides) does not work on 3.7.1. It is in [archive/v6.0.0-thermal](archive/v6.0.0-thermal), with the reasons in [archive/README.md](archive/README.md).

## Credits

Log format, forbidden cvar list and the ConfigMonitor findings that started this: [Arglax/Mobile-WuWa-Config](https://github.com/Arglax/Mobile-WuWa-Config).
