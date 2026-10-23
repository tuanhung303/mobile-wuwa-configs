# How WuWa 3.7.1 loads graphics config (Android)

Tested on 2026-10-23, game 3.7.1 global, REDMAGIC 11 Pro (Adreno 840). Every result below comes from the decrypted `Client.log` of that session (`tools/decrypt_log.py`).

## Paths

```
Saved config:  /sdcard/Android/data/com.kurogame.wutheringwaves.global/files/UE4Game/Client/Client/Saved/Config/Android/
Menu settings: .../Saved/LocalStorage/LocalStorage.db   (table LocalStorage, flat key/value)
Logs:          .../Saved/Logs/Client.log                 (encrypted)
```

## Load rules

1. **Cvar priority**, low to high (UE4): Scalability < GameSetting < ProjectSetting < SystemSettingsIni < DeviceProfile < ConsoleVariablesIni < Commandline < Code < Console. A lower priority never overwrites a higher one; the log says `was ignored as it is lower priority than the previous 'SetBy...'`.
2. **Device profile.** The game picks `[Android_Adreno840]` (parent `Android_VeryHigh`, then `Android`). It sets the `sg.*` levels at DeviceProfile priority, so `sg.*` in Scalability.ini or GameUserSettings.ini is ignored.
3. **ConfigMonitor** (Kuro). At launch it dumps each Saved ini to the log, checks its hash, and strips forbidden cvars: `Config '.../Scalability.ini' contained N forbidden CVars which have been removed.` This applies to Scalability.ini too. The list is in `tools/forbidden_cvars.txt`.
4. **Truncation.** At launch the game cuts the Saved `DeviceProfiles.ini` and `Scalability.ini` to 1 byte. A file pushed by adb with mode 444 (owner `shell`) survives.
5. **Section headers.** A header line must end with `]`. `[EffectsQuality@2]  ; comment` makes UE4 drop the whole section with no warning.
6. **Performance.ini** is never read: 0 mentions in `Client.log`.

## Active levels at max menu settings

`ViewDistance@2, AntiAliasing@2, Shadow@3, PostProcess@2, Texture@2, Effects@2, Foliage@2, Shading@Cine`

Kuro's own values at these levels (from the log) include:
- `r.MaterialQualityLevel 2` ("Middle"), set by Effects@2.
- `r.Shadow.MaxCSMResolution 512`.
- `r.Streaming.PoolSize 400`, set by Texture@2.

All three are forbidden, so no Saved file can raise them.

## Tests

Each test: stop the game, push one file read-only, relaunch, go to the same spot, take a screenshot, read the log.

| # | File and change | Result |
|---|---|---|
| 1 | Engine.ini `[SystemSettings]` and `[ConsoleVariables]`, test cvars | The cvars were applied (in the log), but nothing changed on screen. Those cvars have no visible effect in Kuro's renderer. |
| 2 | DeviceProfiles.ini, `+CVars` under 9 profile names | No effect. |
| 3 | Scalability.ini, `[ShadowQuality@3] r.ShadowQuality=0` | Shadows gone. The channel works and Shadow runs at @3. |
| 4 | Scalability.ini v1: view distance, pool size, CSM resolution, LOD | 11 lines stripped as forbidden (4× ViewDistanceScale, 4× PoolSize, MaxCSMResolution, MaxResolution, DistanceScale). ShadowQuality, RadiusThreshold and StaticMeshLODDistanceScale stayed. |
| 5 | Engine.ini `dp.Override=Android_Adreno840` + DeviceProfiles.ini `+CVars=sg.*=3` | No effect: `sg.EffectsQuality` still 2 from the device profile, all passes still @2. |
| 6 | Scalability.ini v2, headers with trailing comments | Only ShadowQuality@3 and ViewDistanceQuality@2 applied (the two headers with no comment). |
| 7 | Scalability.ini v2, clean headers (`config/Scalability.ini` plus `r.Streaming.PoolSizeForMeshes`) | 40 of 41 lines applied; PoolSizeForMeshes stripped as forbidden. `foliage.DensityType` is held by SetByConsole, but its value is already 2. |

## Runtime values seen in the log

- `r.ScreenPercentage = 100` and `r.SecondaryScreenPercentage.GameViewport = 90`: the game renders at 90% of the display. Both cvars are forbidden.
- `r.FidelityFX.FSR.RCAS.Enabled = 1` is set at runtime (FSR On in the menu), so FSR sharpening is on.
- `r.KuroDownsampleTranslucency` ends at 0: particles and other translucency render at full resolution.
- `r.Kuro.KuroBloomEnable = 1` (menu Bloom On). `r.BloomQuality` is 1 at both PostProcess levels in the log (@3 and @2).

## Menu to LocalStorage.db keys

Mapped by changing one option in the menu and comparing the database before and after.

| Menu option | Key | Values |
|---|---|---|
| Anisotropic filtering | `AnisoLevel` | 0–4 = 1x, 2x, 4x, 8x, 16x |
| Shadow | `ShadowQuality` | 2 High, 3 Ultra High |
| LOD bias | `ImageDetail` | 2 High, 3 Ultra High |
| Resolution | `MobileResolution` | 2 High, 3 Ultra High |
| Capsule AO | `SceneAo` | 0 Off, 1 On |
| Frame rate | `CustomFrameRate` | 2 = 90 fps |

The menu also writes `r.MaxAnisotropy` into the Saved Engine.ini `[/Script/Engine.RendererSettings]`.

## Leads not tested yet

- `r.Tonemapper.Sharpen` is 0.5, set in the merged Engine config under `[/Script/Engine.RendererSettings]` (it is not in the Saved Engine.ini). A higher value would sharpen the image. Scalability probably cannot override it (lower priority), but Engine.ini `[SystemSettings]` could. It is not forbidden.
- `r.FidelityFX.FSR.RCAS.Sharpness` is not set, so FSR sharpening runs at its default strength.
- `r.BloomQuality` is not forbidden, but Kuro's bloom (`r.Kuro.KuroBloomEnable`) may not read it.
- UE4CommandLine.txt `-ExecCmds="sg.EffectsQuality 3"` would beat the device profile (Commandline priority) and could raise material quality. It carries more anti-cheat risk.
