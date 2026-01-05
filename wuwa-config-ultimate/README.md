# WuWa Mobile Config - Ultimate Edition v3.5

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
| **Characters** | LODBias=-2 | Maximum polygon detail |
| **Foliage** | LODDistanceScale=4.0 | Grass/trees render at 4x distance |
| **Shadows** | 6 CSM cascades, 1536 res | Sharp, stable shadows (crash-safe) |
| **Textures** | Anisotropy=16, MipBias=-2.0, 2GB Pool | Razor-sharp at all angles, no pop-in |
| **Particles** | Niagara GPU + QualityLevel=2 | Maximum skill effects |
| **SSR/SSGI** | Quality=4, Temporal=1 | Screen-space reflections and global illumination |
| **HDR Output** | Enabled | High Dynamic Range color output |
| **Post-FX** | Fog/Blur/Chromatic=OFF | Clean, high-clarity cinematic image |
| **Garbage Collection** | Multi-threaded, Incremental | Smooth frame times during long sessions |
| **Shader Cache** | Full precompilation | Eliminates first-time stuttering |

---

## Version History

### v3.5 (Current)
- **Native Resolution**: Added `r.MobileContentScaleFactor=0` for true native rendering
- **Chaos Physics**: Complete physics simulation tuning block (10 CVars)
- **Kuro Extended Visuals**: Added 11 new Kuro-specific visual CVars (GlobalGI, Tonemapping, etc.)
- **Decal System**: Full decal quality block - fixes blocky artifacts (e.g., motorbike skids)
- **SSR Mobile**: Added 6 mobile-specific SSR enhancements
- **Virtual Textures**: VT system with 16x anisotropic filtering
- **GPU Particles**: Niagara GPU compute + async ticking
- **FX Threading**: Async particle/effect updates
- **URO**: Animation update rate optimization
- **Vulkan Parallel**: Async compute, parallel rendering, preemption
- **Mobile Quality Flags**: Gen4TAA, clustered deferred, HW sRGB
- **Water Reflections**: Full mobile water SSR system
- **Streaming Optimizations**: Eggsie's memory leak fixes
- **Mesh Distance Fields**: Enabled for better shadowing
- **Detail Upgrade**: Increased LOD bias to `-2` for maximum polygon detail

### v3.2
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
- **Eggsie** - Memory leak mitigation recommendations
