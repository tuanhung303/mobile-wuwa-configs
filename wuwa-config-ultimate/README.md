# WuWa Mobile Config - Ultimate Edition v3

**Target Device:** Snapdragon 8 Gen 5 / 16GB RAM (RedMagic 11 Pro)  
**Target FPS:** 90 FPS (120 FPS optional)  
**Style:** Max Quality | Ultra-Tight Bloom | Deep Contrast

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
| **Bloom** | Ultra-tight (SizeScale=0.005) | Near-invisible spread, skills still glow |
| **Characters** | LODBias=-2, HairQuality=2 | Maximum polygon detail, best hair rendering |
| **Foliage** | LODDistanceScale=4.0 | Grass/trees render at 4x distance |
| **Shadows** | 10 CSM cascades, 2048 res | Sharp, detailed shadows |
| **Textures** | Anisotropy=16, MipBias=-1 | Razor-sharp at all angles |
| **Small Objects** | StaticMeshLODBias=-2, DetailMode=2 | High-detail props and environment |
| **Particles** | Niagara GPU + QualityLevel=2 | Maximum skill effects |
| **TAA** | 30+ tuned parameters | Sharp edges, minimal ghosting |
| **Tonemapper** | Sharpen=1.2, deep contrast | Punchy, vivid colors |
| **HDR Output** | Enabled (unified) | High Dynamic Range color output |
| **SSR/SSGI** | Quality=4, full resolution | Screen-space reflections and global illumination |
| **Ambient Occlusion** | Mobile AO Quality=3 | Realistic contact shadows |
| **Water** | WaterSSR + Mesh rendering | High-quality water reflections |
| **Light Shafts** | Quality=1, 8 samples | Subtle god rays |
| **NPC Distance** | 30000 appear distance | NPCs visible from far away |
| **GPU Clock** | 85% default | Thermal headroom for sustained performance |

---

## Switching from 90 FPS to 120 FPS

If your device supports 120Hz display, follow these steps:

### Step 1: Edit Engine.ini

Find these lines and change `90` to `120`:

```ini
; Before (90 FPS)
t.MaxFPS=90
FrameRateLimit=90.0

; After (120 FPS)
t.MaxFPS=120
FrameRateLimit=120.0
```

Also find the `[/Script/Engine.GameUserSettings]` section:

```ini
; Before
t.MaxFPS=90
FrameRateLimit=90.00000

; After
t.MaxFPS=120
FrameRateLimit=120.00000
```

### Step 2: Edit GameUserSettings.ini

Find these lines and change:

```ini
; Before (90 FPS)
FrameRateLimit=90.000000
FramePace=90

; After (120 FPS)
FrameRateLimit=120.000000
FramePace=120
```

### Step 3: (Optional) Reduce Quality for Stable 120 FPS

If you experience frame drops at 120 FPS, consider these tweaks:

```ini
; In Engine.ini - reduce shadow quality
r.Shadow.MaxCSMResolution=1024        ; Was 2048
r.Shadow.CSM.MaxCascades=4            ; Was 10

; In Engine.ini - reduce foliage distance
foliage.LODDistanceScale=2.0          ; Was 4.0

; In DeviceProfiles.ini - reduce resolution
CVars=r.SecondaryScreenPercentage.GameViewport=85  ; Was 100
```

---

## Troubleshooting

### Black/White Flickering Boxes
Add this line to `[SystemSettings]` in Engine.ini:
```ini
r.HZBOcclusion=0
```

### Bloom Still Too Bright
The config already uses ultra-tight bloom. If still too bright:
```ini
r.Bloom.Intensity=0.01      ; Default is 0.02
r.Bloom.Threshold=8.0       ; Default is 5.0
```

### Skills Look Flat/No Glow
Make sure **Bloom is ON** in the game's graphics settings. The config relies on in-game Bloom being enabled.

### Colors Look Washed Out
Adjust the black level in Engine.ini:
```ini
r.Color.Min=-0.01           ; Slightly deeper blacks
```

### Colors Look Too Dark/Crushed
```ini
r.Color.Min=0               ; Neutral (default)
```

### Game Crashes on Launch
Try reducing streaming pool size in Engine.ini:
```ini
r.Streaming.PoolSize=1024   ; Default is 2048
```

### Overheating / Thermal Throttling
Reduce GPU clock scale further in Performance.ini:
```ini
r.Vulkan.MaxGPUClockScale=0.75  ; Default is 0.85
```

---

## File Overview

| File | Purpose |
|------|---------|
| `Engine.ini` | Core graphics, bloom, TAA, shadows, particles, SSR, AO |
| `DeviceProfiles.ini` | GPU-specific overrides, DeviceScore trick |
| `GameUserSettings.ini` | Resolution, FPS limits, scalability groups |
| `Scalability.ini` | Quality tier definitions with full settings |
| `Performance.ini` | CPU/GPU scheduling, memory budgets |

---

## Key Settings Explained

### Ultra-Tight Bloom
```ini
r.Bloom=1                    ; Keep bloom system ON
r.Bloom.Intensity=0.02       ; Barely visible base intensity
r.Bloom.Threshold=5.0        ; Only extreme brightness glows
r.Bloom.SizeScale=0.005      ; Near-zero spread radius
r.Kuro.KuroBloomStreak=1     ; Stylized light streaks
r.LightShaftQuality=1        ; Subtle god rays
r.HDR.EnableHDROutput=1      ; High Dynamic Range Output
```

### Deep Contrast Tonemapper
```ini
r.Tonemapper.Sharpen=1.2     ; Strong edge sharpening
r.Color.Max=1.1              ; Bright highlights
r.Color.Mid=0.5              ; Balanced midtones
r.Color.Min=0                ; Neutral black level
```

### Maximum Character Detail
```ini
r.SkeletalMeshLODBias=-2     ; Highest poly characters
r.Kuro.HairQuality=2         ; Best hair rendering
r.Kuro.ClothSimulate=1       ; Physics cloth
r.Kuro.CharacterShadowQuality=3
r.KuroMobile.FacialAnimationQuality=2
r.KuroMobile.SkinCacheQuality=2
```

### Sharp Anti-Aliasing
```ini
r.TemporalAACurrentFrameWeight=0.35  ; Reduces ghosting
r.TemporalAASharpen=0.8              ; Edge sharpening
r.TemporalAA.Quality=3               ; Highest TAA quality
r.TemporalAA.HistoryScreenPercentage=200 ; High-res history buffer
r.TemporalAA.MobileUseCompute=1      ; GPU-accelerated TAA
```

### Ultimate Shadow System
```ini
r.ShadowQuality=4                    ; Maximum shadow quality
r.Shadow.CSM.MaxCascades=10          ; 10 cascade levels
r.Shadow.MaxCSMResolution=2048       ; High-resolution shadow maps
r.Shadow.MinResolution=1024          ; High minimum resolution
r.CapsuleShadows=1                   ; Character capsule shadows
r.Mobile.AllowDistanceFieldShadows=1 ; Distance field shadows
```

### Screen Space Reflections & GI
```ini
r.SSR.Quality=4                      ; Maximum SSR quality
r.SSR.MaxRoughness=1.0               ; Reflections on all surfaces
r.SSR.Temporal=1                     ; Temporal stability
r.SSGI.Enable=1                      ; Screen-space global illumination
r.SSGI.Quality=4                     ; Maximum SSGI quality
```

### Ambient Occlusion
```ini
r.AOQuality=2                        ; High AO quality
r.Mobile.AmbientOcclusionQuality=3   ; Maximum mobile AO
r.AmbientOcclusion.UseHistory=1      ; Temporal stability
r.AmbientOcclusionRadiusScale=1.5    ; Wider AO radius
```

### Niagara Particles (GPU)
```ini
fx.Niagara.QualityLevel=2            ; Maximum particle quality
r.Niagara.AllowGPUParticles=1        ; GPU-accelerated particles
r.Niagara.GPUCompute=1               ; GPU compute for particles
r.Niagara.EmitterViewDistanceScale=10.0 ; Far particle visibility
```

### Water & Reflections
```ini
r.Mobile.EnableWaterReflection=1     ; Enable water reflections
r.Mobile.WaterQuality=1              ; High water quality
r.Mobile.WaterSSR=1                  ; Screen-space water reflections
r.Water.WaterMesh.EnableRendering=1  ; Water mesh rendering
```

### Small Object Texture Detail
```ini
r.MipMapLODBias=-1.0                 ; Forces higher-res mip levels
r.StaticMeshLODBias=-2               ; Highest poly props/environment
r.StaticMeshLODDistanceScale=2.0     ; Keeps detail at distance
r.imp.SSMbScaleLod0=1.0              ; Proper impostor scaling
r.imp.SSMbScaleLod1=0.5              ; Proper impostor LOD1 scaling
r.Streaming.MipBias=-1               ; Additional mip boost
r.Streaming.BoostPlayerTextures=8.0  ; Prioritize nearby textures
r.DetailMode=2                       ; Maximum detail level
```

---

## Credits

- **Arglax** - V3.x Working Configs (reference)
- **em00se** - CVars dump
- **AlteriaX/Brandy** - Cleaned CVars reference
- **RGCloud** - Honami Escalator discovery
- **Reddit Thread** - [Mobile In-Game Configs Reference](https://www.reddit.com/r/WutheringWaves/comments/1nu3y40/mobile_ingame_configs/)

---

## Version History

### v3.0 (Current)
- **Shadows**: Upgraded to 10 CSM cascades with 2048 resolution (was 3 cascades, 768 res)
- **Ambient Occlusion**: Added full AO system with Mobile AO Quality=3
- **SSR/SSGI**: Added complete screen-space reflections and global illumination
- **Particles**: Added Niagara GPU particle system with quality level 2
- **Water**: Added water reflection and SSR system
- **Light Shafts**: Added configurable god rays with 8 samples
- **TAA**: Expanded from 6 to 30+ tuning parameters
- **NPC Distances**: Added far visibility (30000 appear distance)
- **Character Quality**: Added HairQuality, ClothSimulate, FacialAnimationQuality
- **Virtual Textures**: Added VT system with 2048 pool size
- **Lighting/GI**: Added global light quality and skylight settings
- **Tessellation**: Added tessellation support with factor=4
- **Scalability.ini**: Expanded with proper tier definitions for all quality groups
- **Fixed**: Removed duplicate CVars and resolved conflicts
- **Fixed**: r.SceneColorFormat upgraded to 4 (higher precision)

### v2.3
- Unified HDR settings to enabled across all config files
- Enabled Landscape SSR for enhanced reflections
- Reduced GPU clock to 85% for sustained thermal stability
- Fixed HDR conflicts in Engine.ini and DeviceProfiles.ini

### v2.2
- Fixed small object texture detail (props, items, environment)
- Added r.StaticMeshLODBias=-2 for higher quality static meshes
- Fixed impostor LOD scaling (was 0.00, now 1.0/0.5)
- Added texture streaming optimizations for small objects
- Increased r.MipMapLODBias from -0.5 to -1.0
- Added r.DetailMode=2 for maximum detail level

### v2.1
- Ultra-tight bloom (SizeScale=0.005, Threshold=5.0)
- Deep contrast tonemapper (Sharpen=1.2, balanced colors)
- Fine-tuned r.Color values for natural look

### v2.0
- Added 40+ quality settings from V3.x reference
- Complete Honami Escalator CVars for stability
- Full shadow system with CSM cascades
- SSR and water reflections
- Virtual textures for sharper detail
- NPC draw distances
- Streaming and garbage collection optimization
- Shader precompilation
- Log suppression for performance
- Fixed HDR conflict in GameUserSettings.ini
- Comprehensive GPU device mappings
- 90-120 FPS switching instructions

### v1.0
- Initial "Crisp Light" config
- Bloom blowout fix
- Basic quality settings
