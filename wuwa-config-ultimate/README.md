# WuWa Mobile Config - Ultimate Edition v3.2

**Target Device:** Snapdragon 8 Elite (Gen 5) / 16GB RAM (RedMagic 11 Pro)  
**CPU Architecture:** 2x Oryon Prime (4.6GHz) + 6x Oryon Performance (3.6GHz)  
**Target FPS:** 120 FPS via Native Frame Generation (in-game option)  
**Style:** Max Quality | Warm Colors | Minimal Ghosting | Frame Gen Optimized

---

## Quick Start

1. Copy all `.ini` files to your device
2. Place them in: `Android/data/com.kurogame.wutheringwaves.global/files/Client/Saved/Config/Android/`
3. **IMPORTANT:** Keep **Bloom ON** in game settings for best skill effects
4. Launch game and enjoy crisp visuals

---

## What This Config Does

| Feature | Setting | Result |
|---------|---------|--------|
| **Frame Generation** | 120 FPS ceiling, DynamicMaxFPS=True | Native frame gen can reach full 120 FPS |
| **Bloom** | Ultra-tight (SizeScale=0.005) | Near-invisible spread, skills still glow |
| **Color Palette** | Warm (R+3%, G-6%, B=neutral) | Natural skin tones, reduced yellow/green tint |
| **TAA Anti-Ghosting** | Weight=0.28, Sharpen=0.2 | Minimal trails on fast combat, no ringing |
| **Characters** | LODBias=-1 | Maximum polygon detail |
| **Foliage** | LODDistanceScale=4.0 | Grass/trees render at 4x distance |
| **Shadows** | 6 CSM cascades, 1536 res | Sharp, stable shadows (crash-safe) |
| **Textures** | Anisotropy=16, MipBias=-0.5, 2GB Pool | Razor-sharp at all angles, no pop-in |
| **Particles** | Niagara GPU + QualityLevel=2 | Maximum skill effects |
| **SSR/SSGI** | Quality=4, Temporal=1 | Screen-space reflections and global illumination |
| **HDR Output** | Enabled | High Dynamic Range color output |
| **Post-FX** | Fog/Blur/Chromatic=OFF | Clean, high-clarity cinematic image |
| **Garbage Collection** | Multi-threaded, Incremental | Smooth frame times during long sessions |
| **Shader Cache** | Full precompilation | Eliminates first-time stuttering |

---

## Native Frame Generation Setup

This config is optimized for **Wuthering Waves' native frame generation** (in-game graphics option):

### How It Works
1. **Native Rendering:** Game renders base frames at variable rate
2. **Interpolation:** Kuro's built-in frame gen creates synthetic frames
3. **Output:** Smooth 120 FPS on your 120Hz display

### Key Settings for Native Frame Gen
```ini
t.MaxFPS=120                     ; Output ceiling (must be 120 for full frame gen)
FrameRateLimit=120.0             ; Must match t.MaxFPS
bEnableDynamicMaxFPS=True        ; CRITICAL: Allows frame gen to adjust FPS dynamically
r.Vulkan.MaxFrameLatency=2       ; Buffer for interpolation analysis
a.UseSwappyForFramePacing=0      ; Disabled: Native frame gen handles pacing
```

### If You Want Lower FPS Target (90 FPS)
Change these values:
```ini
t.MaxFPS=90
FrameRateLimit=90.0
; Also update GameUserSettings.ini:
FrameRateLimit=90.000000
FramePace=90
```

---

## Experimental Settings (v3.1)

These new settings can be reverted if they cause issues:

### GPU-Accelerated TAA
```ini
; In Engine.ini - Comment out to revert
r.TemporalAA.MobileUseCompute=1      ; Offloads TAA to GPU compute
r.TemporalAA.MobileCatmullRom=1      ; Higher quality interpolation
```

### Velocity Rendering
```ini
; In Engine.ini - Comment out all three to revert
r.Mobile.EnableOutlineVelocity=1     ; Improves TAA motion detection
r.Mobile.RenderVelocity=1
r.BasePassOutputsVelocity=1
```

---

## Troubleshooting

### Black/White Flickering Boxes
Already fixed in v3.1 with `r.HZBOcclusion=0`. If still occurring:
```ini
r.HZBOcclusion=1   ; Try HZB system instead
```

### Bloom Still Too Bright
The config already uses ultra-tight bloom. If still too bright:
```ini
r.Bloom.Intensity=0.01      ; Default is 0.02
r.Bloom.Threshold=8.0       ; Default is 5.0
```

### Skills Look Flat/No Glow
Make sure **Bloom is ON** in the game's graphics settings.

### Colors Look Washed Out
```ini
r.Color.Min=-0.01           ; Slightly deeper blacks
```

### Colors Look Too Dark/Crushed
```ini
r.Color.Min=0               ; Neutral (default)
```

### Game Crashes on Launch
Try reducing streaming pool size:
```ini
r.Streaming.PoolSize=1024   ; Default is 2048
```

### Overheating / Thermal Throttling
Reduce GPU clock scale in Performance.ini:
```ini
r.Vulkan.MaxGPUClockScale=0.75  ; Default is 0.85
```

### Ghosting/Blurry Trails on Characters
Increase current frame weight (reduces ghosting but may increase flicker):
```ini
r.TemporalAA.CurrentFrameWeight=0.35  ; Default is 0.28
```

### Over-Sharpening / Ringing Artifacts
Reduce TAA sharpening:
```ini
r.TemporalAASharpen=0.1     ; Default is 0.2
```

---

## File Overview & Architecture

### Why 5 files instead of two?
Wuthering Waves (and UE4) checks multiple configuration layers. By populating all five, we lock the "Cinematic" visuals and prevent the game from resetting your quality.

| File | Primary Function | Why it's necessary |
|------|------------------|-------------------|
| **Engine.ini** | **The Visual Core.** TAA, Bloom, SSR, SSGI, GC, Shaders. | Controls "how" the game renders. |
| **Scalability.ini** | **The Quality Guardrail.** Defines what "Ultimate" means. | Prevents game from switching to lower tiers. |
| **DeviceProfiles.ini** | **The Hardware Unlocker.** GPU recognition and CVars. | Unlocks "Cinematic" menu and Adreno optimizations. |
| **GameUserSettings.ini** | **The User Interface.** Resolution, FPS limits, tiers. | Syncs menu settings with our configuration. |
| **Performance.ini** | **The Hardware Scheduler.** CPU cores, thermals, memory. | Separates performance logic from visuals. |

---

## Key Settings Explained

### Ultra-Tight Bloom
```ini
r.DefaultFeature.Bloom=1         ; Keep bloom system ON
r.Bloom.Intensity=0.02           ; Barely visible base intensity
r.Bloom.Threshold=5.0            ; Only extreme brightness glows
r.Bloom.SizeScale=0.005          ; Near-zero spread radius
```

### Warm Color Palette (v3.2 Refined)
```ini
r.TonemapperFilm=1               ; Filmic tonemapper preserves warm highlights
r.Color.Gain.R=1.03              ; +3% red boost (counters yellow tint)
r.Color.Gain.G=0.94              ; -6% green reduction (fixes yellowish cast)
r.Color.Gain.B=1.0               ; Standard blue (neutral)
```

### Anti-Ghosting TAA (v3)
```ini
r.TemporalAA.CurrentFrameWeight=0.28  ; Higher = less ghosting, more flicker
r.TemporalAASharpen=0.2               ; Lower = less ringing artifacts
r.TemporalAASamples=8                 ; Balanced sample count
r.TemporalAA.HistoryScreenPercentage=100  ; Native resolution (200% causes OOM)
```

### Shadow System (Crash-Safe)
```ini
r.Shadow.CSM.MaxCascades=6       ; Stability sweet spot (10 causes crashes)
r.Shadow.MaxCSMResolution=1536   ; High quality (2048 causes VRAM crashes)
r.Shadow.DistanceScale=1.5       ; Extended shadow distance
r.Shadow.RadiusThreshold=0.0001  ; Small objects cast shadows
```

### Screen Space Effects
```ini
r.SSR.Quality=4                  ; Maximum SSR quality
r.SSR.MaxRoughness=0.7           ; Wide reflection coverage
r.SSR.Temporal=1                 ; Temporal stability
r.SSGI.Enable=1                  ; Screen-space global illumination
r.SSGI.Quality=1                 ; Stable GI (Level 4 too expensive)
r.SSGI.HalfRes=1                 ; Performance-friendly resolution
```

### Enhanced Garbage Collection (v3.1)
```ini
gc.AllowParallelGC=1             ; Multi-core GC
gc.ContinuousIncrementalGC=1     ; Spread GC across frames
gc.MultithreadedDestructionEnabled=1  ; Faster cleanup
gc.ActorClusteringEnabled=1      ; Efficient object grouping
```

---

## Version History

### v3.2 (Current)
- **Color Grading Refined**: Red bias +3%, green reduced -6%, blue neutral (R=1.03, G=0.94, B=1.0)
- **Documentation**: Updated color palette description

### v3.1
- **Native Frame Gen Fix**: Changed from 60 FPS base to 120 FPS ceiling
- **Dynamic FPS**: Enabled `bEnableDynamicMaxFPS=True` for frame gen compatibility
- **HZB Safeguard**: Added `r.HZBOcclusion=0` to prevent flickering
- **Garbage Collection**: Expanded from 2 to 18 tuned parameters
- **Shader Precompilation**: Added full shader cache system
- **Log Suppression**: Added 30+ log categories disabled
- **Streaming Settings**: Added async loading and background streaming
- **[EXPERIMENTAL] GPU TAA**: Added `r.TemporalAA.MobileUseCompute=1`
- **[EXPERIMENTAL] Velocity Rendering**: Added motion detection for TAA
- **Performance.ini Sync**: Fixed all v2→v3 conflicts
- **Android Runtime**: Added proper section with Frame Gen settings

### v3.0
- **Frame Generation**: Converted from 90 FPS to 60 FPS base for interpolation
- **Anti-Ghosting**: Increased TAA weight to 0.28, reduced sharpen to 0.2
- **Color Correction**: Added warm palette (R+2%, G-3%, B-1%)
- **Texture Pool**: Increased to 2GB for 16GB RAM devices
- **Frame Latency**: Set to 2 for interpolator buffer
- **Swappy**: Disabled for external frame generation

### v2.x
- Shadows: 6 CSM cascades, 1536 resolution
- Tonemapper: Sharpen=0.8, PreExposure=0.9
- Bloom: Ultra-tight with SizeScale=0.005
- SSR/SSGI: Quality=4 with temporal stability

### v1.0
- Initial "Crisp Light" config
- Bloom blowout fix
- Basic quality settings

---

## Credits

- **Arglax** - V3.x Working Configs (reference)
- **em00se** - CVars dump
- **AlteriaX/Brandy** - Cleaned CVars reference
- **RGCloud** - Honami Escalator discovery
- **Reddit Thread** - [Mobile In-Game Configs Reference](https://www.reddit.com/r/WutheringWaves/comments/1nu3y40/mobile_ingame_configs/)
