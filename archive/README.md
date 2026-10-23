# Archive

Old packs that do not work on WuWa 3.7.1. They are kept for reference only. Do not push them to a phone.

## v6.0.0-thermal (2026-01-15)

Checked against the game's decrypted `Client.log` on 2026-10-23 (details in [../FINDINGS.md](../FINDINGS.md)).

| File | Why it does not work on 3.7.1 |
|---|---|
| `Engine.ini` | 582 distinct cvars, 14 of them forbidden (ConfigMonitor strips them), for example `r.MaterialQualityLevel`, `r.Shadow.MaxCSMResolution`, `r.Streaming.PoolSize`, `r.MobileContentScaleFactor`. On the test phone, the game's own 4.5 KB Engine.ini had replaced this file before the 2026-10-23 tests. When `[SystemSettings]` cvars do load, the ones tested had no visible effect in Kuro's renderer. |
| `DeviceProfiles.ini` | The game empties the Saved copy at launch. A read-only copy survives, but its `+CVars` changed nothing (tests 2 and 5 in FINDINGS). 4 of its cvars are forbidden. |
| `Performance.ini` | The game never reads it: 0 mentions in `Client.log`. |
| `consolidated_guideline/` | Notes for this Engine.ini and DeviceProfiles.ini approach. Not checked against 3.7.1. |
| `README.md` | The v5.x changelog (v5.5–v5.9.9) and design notes for this pack. |

The pack in use now is [../config/Scalability.ini](../config/Scalability.ini).
