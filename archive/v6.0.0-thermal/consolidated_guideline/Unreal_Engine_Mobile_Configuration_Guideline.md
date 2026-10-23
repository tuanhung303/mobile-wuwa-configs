# Unreal Engine Mobile Configuration Consolidated Guideline

## Overview

This document provides comprehensive configuration guidelines for Unreal Engine mobile development (UE4/UE5), covering device profiles, rendering settings, performance optimization, and platform-specific configurations for Android and iOS.

**Key Reference Sources:**
- Official Epic Games Documentation
- Device Profile System
- Mobile Rendering Path (Alternate rendering path for mobile devices with simplified/performance-oriented models)
- Platform-specific configuration files

---

## 1. Device Profiles Configuration

### 1.1 What Are Device Profiles?

Device Profiles are configuration files containing settings for specific devices or device categories. They can target:
- **Broad categories**: Android_Mid, iOS, Mobile
- **Specific hardware**: iPhone5S, Galaxy S21, Pixel 6
- **GPU families**: Adreno 7xx series

### 1.2 Device Profile File Location

**Project-level configuration:**
```
Config/DefaultDeviceProfiles.ini
```

**Engine-level configuration:**
```
Engine/Config/BaseDeviceProfiles.ini (editable)
```

### 1.3 Device Profile Structure

```ini
[DeviceName DeviceProfile]
DeviceType=IOS|Android
BaseProfileName=IOS|Android
MeshLODSettings=
TextureLODSettings=
+CVars=r.Setting1=value1
+CVars=r.Setting2=value2
```

**Parameters:**
- `DeviceType`: Platform identifier (IOS, Android)
- `BaseProfileName`: Parent profile to inherit settings from
- `MeshLODSettings`: Mesh LOD configuration override
- `TextureLODSettings`: Texture LOD configuration override
- `+CVars`: Console variables to override/add

---

## 2. iOS Configuration

### 2.1 iOS Device Profiles Examples

```ini
[iPhone5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
MeshLODSettings=
TextureLODSettings=
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
MeshLODSettings=
TextureLODSettings=
+CVars=r.MobileContentScaleFactor=2
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPad3 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=1

[iPad4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=2

[iPadAir DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=2
```

### 2.2 Key iOS CVars

**r.MobileContentScaleFactor**
- Adjusts game resolution relative to nominal iOS resolution
- Values:
  - `1`: Standard resolution (older devices)
  - `2`: Retina display support
  - Higher values for newer iPads

**r.RenderTargetSwitchWorkaround**
- `1`: Enables workaround for render target switching issues on older iOS devices

**Post-Processing Quality Settings:**
```ini
+CVars=r.BloomQuality=0|1|2|3
+CVars=r.DepthOfFieldQuality=0|1|2|3
+CVars=r.LightShaftQuality=0|1|2
+CVars=r.MotionBlurQuality=0|1|2|3
+CVars=r.FXAAQuality=0|1|2|3
```

---

## 3. Android Configuration

### 3.1 Android Device Profiles Examples

**Standard Android Profile:**
```ini
[Android DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.MobileContentScaleFactor=1.0
+CVars=sg.ViewDistanceQuality=2
+CVars=sg.AntiAliasingQuality=2
+CVars=sg.ShadowQuality=2
+CVars=sg.PostProcessQuality=2
+CVars=sg.TextureQuality=2
+CVars=sg.EffectsQuality=2
+CVars=r.BloomQuality=2
+CVars=r.LightShaftQuality=1
```

**Android Vulkan SM5 Profile (High-End Devices):**
```ini
[Android_Vulkan_SM5 DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=sg.ViewDistanceQuality=2
+CVars=sg.AntiAliasingQuality=1
+CVars=sg.ShadowQuality=2
+CVars=sg.GlobalIlluminationQuality=2
+CVars=sg.ReflectionQuality=2
+CVars=sg.PostProcessQuality=2
+CVars=sg.TextureQuality=2
+CVars=sg.EffectsQuality=2
+CVars=sg.FoliageQuality=2
+CVars=sg.ShadingQuality=2
+CVars=sg.LandscapeQuality=2
+CVars=r.BloomQuality=2
+CVars=r.LightShaftQuality=1

; Shadows
+CVars=r.Shadow.MaxResolution=2048
+CVars=r.Shadow.MaxCSMResolution=2048
+CVars=r.Shadow.WholeSceneShadowCacheMb=40
+CVars=r.Shadow.CachedShadowsCastFromMovablePrimitives=0
+CVars=r.Shadow.MaxNumPointShadowCacheUpdatesPerFrame=1
+CVars=r.Shadow.MaxNumSpotShadowCacheUpdatesPerFrame=1
+CVars=r.Shadow.DistanceScale=1.0
+CVars=r.Shadow.CSM.MaxCascades=2
+CVars=r.ShadowQuality=2
+CVars=r.Shadow.CSMShadowDistanceFadeoutMultiplier=2.5

; Screen Space Effects
+CVars=r.SSS.Quality=0
+CVars=r.SSS.Scale=0
+CVars=r.SSR.Quality=0

; Vulkan & Ray Tracing
+CVars=r.Android.DisableVulkanSM5Support=0
+CVars=r.Android.DisableVulkanSupport=0
+CVars=r.DistanceFields=1
+CVars=r.Vulkan.RayTracing.AllowCompaction=0
+CVars=r.Vulkan.RayTracing.TLASPreferFastTraceTLAS=0
+CVars=r.RayTracing.RequireSM6=0
```

### 3.2 Adreno GPU Optimization

**Adreno Occlusion Fast Mode:**
```ini
r.Mobile.AdrenoOcclusionMode=1
```
- Enables faster hardware occlusion queries on Qualcomm Adreno GPUs
- Particularly beneficial for Meta Quest and similar devices

**Adreno High Performance Memory (HPM) Cache:**
- **Adreno 840 (Snapdragon 8 Elite)**: 12MB L2 Cache
- **Recommended Setting**: `r.Vulkan.Adreno.HPMCacheSize=12288`
- **Impact**: Maximizes tile residency in GMEM, reducing system RAM bandwidth usage.

---

## 4. Memory Buckets Configuration

### 4.1 Android Memory Buckets

**AndroidEngine.ini:**
```ini
[PlatformMemoryBuckets]
LargestMemoryBucket_MinGB=8
LargerMemoryBucket_MinGB=6
DefaultMemoryBucket_MinGB=4
SmallerMemoryBucket_MinGB=3
SmallestMemoryBucket_MinGB=3
```

### 4.2 Memory-Based CVars

**DefaultDeviceProfiles.ini:**
```ini
[Mobile DeviceProfile]
+CVars_Default=r.Streaming.PoolSize=180
+CVars_Smaller=r.Streaming.PoolSize=150
+CVars_Smallest=r.Streaming.PoolSize=70
+CVars_Tiniest=r.Streaming.PoolSize=16
```

---

## 5. Rendering Configuration

### 5.1 Mobile Rendering Paths

**r.Mobile.ShadingPath** (Set in Engine.ini)

| Value | Shading Mode | Description |
|-------|--------------|-------------|
| 0 | Mobile Forward Shading | Processes lighting/shadows at runtime. Preferred for precomputed lighting projects |
| 1 | Mobile Deferred Shading | Processes lighting/shadows using deferred rendering |

**Engine.ini setting:**
```ini
[SystemSettings]
r.Mobile.ShadingPath=0
```

### 5.2 Mobile HDR

**Check if Mobile HDR is enabled:**
```cpp
bool IsMobileHDR();
```

**Mobile HDR Considerations:**
- Provides higher quality rendering with HDR features
- Significant performance cost
- Must be carefully optimized for mobile devices

### 5.3 Mobile Rendering Features Check Functions

```cpp
bool IsMobileCapsuleShadowsEnabled(const FStaticShaderPlatform Platform);
bool IsMobileDeferredShadingEnabled(const FStaticShaderPlatform Platform);
bool IsMobileDistanceFieldAOEnabled(const FStaticShaderPlatform Platform);
bool IsMobileDistanceFieldEnabled(const FStaticShaderPlatform Platform);
bool IsMobileMovableSpotlightShadowsEnabled(const FStaticShaderPlatform Platform);
bool IsForwardShadingEnabled(const FStaticShaderPlatform Platform);
bool IsMobileAmbientOcclusionEnabled(const FStaticShaderPlatform Platform);
bool IsMobileCapsuleDirectShadowsEnabled(const FStaticShaderPlatform Platform);
```

### 5.4 Scene Color Format Optimization

```ini
r.Mobile.SceneColorFormat=3
```
- Uses R8G8B8_UNORM format when supported
- Optimizes mobile rendering by reducing memory usage
- Particularly effective when alpha is not needed

---

## 6. Scalability Settings

### 6.1 Scalability Categories

**Quality Presets (sg.*):**

| Category | Quality Levels |
|----------|----------------|
| sg.ViewDistanceQuality | 0-3 |
| sg.AntiAliasingQuality | 0-3 |
| sg.ShadowQuality | 0-3 |
| sg.GlobalIlluminationQuality | 0-3 |
| sg.ReflectionQuality | 0-3 |
| sg.PostProcessQuality | 0-3 |
| sg.TextureQuality | 0-3 |
| sg.EffectsQuality | 0-3 |
| sg.FoliageQuality | 0-3 |
| sg.ShadingQuality | 0-3 |
| sg.LandscapeQuality | 0-3 |

### 6.2 Scalability Configuration Files

**File Precedence (highest to lowest):**
1. Project/Platform-specific ini files
2. Project/DefaultDeviceProfiles.ini
3. Engine/Platform-specific config files (e.g., Android/AndroidScalability.ini)
4. Engine/Config/BaseScalability.ini

### 6.3 Low Overhead Mobile Configuration

**DefaultEngine.ini:**
```ini
[/Script/Engine.StreamingSettings]
s.PriorityAsyncLoadingExtraTime=275.0
s.LevelStreamingActorsUpdateTimeLimit=250.0
s.PriorityLevelStreamingActorsUpdateExtraTime=250.0
```

---

## 7. Rendering CVars Reference

### 7.1 Mobile-Specific CVars

**Content Scaling:**
```ini
r.MobileContentScaleFactor=1.0    ; Resolution scale (1.0 = native)
r.Mobile.MiniMaxUInteger=0        ; Mini-map rendering optimization
```

**Post-Processing:**
```ini
r.BloomQuality=0|1|2|3            ; Bloom effect quality
r.DepthOfFieldQuality=0|1|2|3     ; Depth of field quality
r.LightShaftQuality=0|1|2         ; Light shaft quality
r.MotionBlurQuality=0|1|2|3       ; Motion blur quality
r.FXAAQuality=0|1|2|3             ; FXAA anti-aliasing quality
r.Upscale.Quality=1|2|3           ; Upscale quality
```

**Shadows:**
```ini
r.ShadowQuality=0|1|2             ; Overall shadow quality
r.Shadow.MaxResolution=1024|1536|2048  ; Max shadow map resolution (1536 recommended for high-end stability)
r.Shadow.MaxCSMResolution=1024|1536|2048 ; Max cascaded shadow resolution
r.Shadow.CSM.MaxCascades=1|2|3|4  ; Number of CSM cascades
r.Shadow.DistanceScale=1.0        ; Shadow draw distance scale
r.Shadow.CSMShadowDistanceFadeoutMultiplier=2.5
```

**Mobile HDR:**
```ini
r.MobileHDR=1|0                   ; Enable/disable Mobile HDR
r.Mobile.SceneColorFormat=3       ; Scene color format optimization
```

**Vulkan Support (Android):**
```ini
r.Android.DisableVulkanSupport=0|1
r.Android.DisableVulkanSM5Support=0|1
r.Vulkan.RayTracing.AllowCompaction=0|1
r.Vulkan.RayTracing.TLASPreasFastTraceTLAS=0|1
```

**OpenXR Passthrough (Quest, etc.):**
```ini
r.Mobile.PropagateAlpha=True|False
```

### 7.2 Texture Streaming CVars

```ini
r.Streaming.PoolSize=180          ; Texture pool size in MB
r.Streaming.MaxTempMemoryAllowed=64
r.Streaming.ThreadPriority=0
```

### 7.3 Mobile Forward Shading CVars

```ini
r.Mobile.Shaders.FastMath=1       ; Enable fast math operations
r.Mobile.Shaders.IntegratedLightweight=1 ; Integrated lighting
```

---

## 8. Platform-Specific Features

### 8.1 iOS Features

**Rendering Features:**
- Metal API support
- Retina display support via r.MobileContentScaleFactor
- iOS-specific workarounds via r.RenderTargetSwitchWorkaround

### 8.2 Android Features

**Rendering APIs:**
- OpenGL ES 3.x
- Vulkan (optional, for high-end devices)

**GPU Families:**
- Adreno (Qualcomm)
- Mali (ARM)
- PowerVR
- Tegra (NVIDIA)

**Device-Specific Optimizations:**
- Adreno occlusion mode
- Vulkan SM5 support
- Memory bucket system

---

## 9. Performance Optimization Guidelines

### 9.1 Performance Budget Factors

Key factors affecting mobile performance:
1. **GPU limitations**: Shader complexity, draw calls, fill rate
2. **Memory constraints**: Texture pool, streaming, asset loading
3. **Thermal throttling**: Sustained performance vs. peak performance
4. **Battery life**: Power consumption considerations

### 9.2 Rendering Optimization Best Practices

**Reduce Draw Calls:**
- Use instanced static meshes
- Enable mesh auto-instancing on mobile
- Minimize unique materials per mesh

**Optimize Materials:**
- Use simple shaders
- Minimize instruction count
- Avoid complex node networks
- Use unlit materials when possible

**Optimize Lighting:**
- Use static lighting where possible
- Limit dynamic lights
- Use light functions sparingly
- Consider distance-based lighting

**Optimize Textures:**
- Use appropriate resolution
- Implement texture streaming
- Use texture compression (ASTC, ETC2)
- Implement texture atlases

### 9.3 Post-Processing Optimization

**Disable or reduce quality of expensive effects:**
```ini
r.BloomQuality=0           ; Disable bloom
r.DepthOfFieldQuality=0    ; Disable DoF
r.LightShaftQuality=0      ; Disable light shafts
r.MotionBlurQuality=0      ; Disable motion blur
r.FXAAQuality=0            ; Disable FXAA
```

### 9.4 Frame Pacing

Enable and customize frame pacing for smoother rendering:
```ini
r.Android.PauseBetweenFrames=0
r.Android.ContinuousRendering=1
```

---

## 10. Debugging and Profiling

### 10.1 Mobile Debugging Tools

**Android:**
- Visual Studio debugger
- Android Studio debugging
- In-device debugging via Unreal tools

**iOS:**
- Xcode debugging
- In-device debugging

### 10.2 Performance Profiling

**In-Editor:**
- GPU Profiler
- Shader Complexity view
- Rendering statistics

**On-Device:**
- Unreal Insights
- Platform-specific profilers
- Device health monitoring

### 10.3 Common Mobile Issues

**Render Target Switch Workaround (iOS):**
- Symptom: Visual artifacts on iOS devices
- Solution: Set r.RenderTargetSwitchWorkaround=1

**Occlusion Query Performance (Adreno):**
- Symptom: Slow occlusion culling
- Solution: Enable r.Mobile.AdrenoOcclusionMode=1

**Memory Exhaustion:**
- Symptom: Crashes, texture pop-in
- Solution: Adjust r.Streaming.PoolSize based on device memory bucket

---

## 11. Quality Presets Examples

### 11.1 High-End Mobile (Vulkan SM5)

```ini
[Android_Vulkan_SM5 DeviceProfile]
DeviceType=Android
BaseProfileName=Android

; Scalability
+CVars=sg.ViewDistanceQuality=3
+CVars=sg.AntiAliasingQuality=2
+CVars=sg.ShadowQuality=3
+CVars=sg.GlobalIlluminationQuality=2
+CVars=sg.ReflectionQuality=2
+CVars=sg.PostProcessQuality=2
+CVars=sg.TextureQuality=3
+CVars=sg.EffectsQuality=3
+CVars=sg.FoliageQuality=2
+CVars=sg.ShadingQuality=2

; Rendering
+CVars=r.MobileContentScaleFactor=2.0
+CVars=r.BloomQuality=2
+CVars=r.LightShaftQuality=1
+CVars=r.MotionBlurQuality=2

; Shadows
+CVars=r.Shadow.MaxResolution=2048
+CVars=r.Shadow.MaxCSMResolution=2048
+CVars=r.Shadow.CSM.MaxCascades=4
+CVars=r.ShadowQuality=2

; Memory
+CVars=r.Streaming.PoolSize=512
```

### 11.2 Mid-Range Mobile

```ini
[Android_Mid DeviceProfile]
DeviceType=Android
BaseProfileName=Android

; Scalability
+CVars=sg.ViewDistanceQuality=2
+CVars=sg.AntiAliasingQuality=1
+CVars=sg.ShadowQuality=2
+CVars=sg.GlobalIlluminationQuality=1
+CVars=sg.ReflectionQuality=1
+CVars=sg.PostProcessQuality=1
+CVars=sg.TextureQuality=2
+CVars=sg.EffectsQuality=2
+CVars=sg.FoliageQuality=1
+CVars=sg.ShadingQuality=1

; Rendering
+CVars=r.MobileContentScaleFactor=1.0
+CVars=r.BloomQuality=1
+CVars=r.LightShaftQuality=0
+CVars=r.MotionBlurQuality=0

; Shadows
+CVars=r.Shadow.MaxResolution=1024
+CVars=r.Shadow.MaxCSMResolution=1024
+CVars=r.Shadow.CSM.MaxCascades=2
+CVars=r.ShadowQuality=1

; Memory
+CVars=r.Streaming.PoolSize=256
```

### 11.3 Low-End Mobile

```ini
[Android_Low DeviceProfile]
DeviceType=Android
BaseProfileName=Android

; Scalability
+CVars=sg.ViewDistanceQuality=1
+CVars=sg.AntiAliasingQuality=0
+CVars=sg.ShadowQuality=1
+CVars=sg.GlobalIlluminationQuality=0
+CVars=sg.ReflectionQuality=0
+CVars=sg.PostProcessQuality=0
+CVars=sg.TextureQuality=1
+CVars=sg.EffectsQuality=1
+CVars=sg.FoliageQuality=0
+CVars=sg.ShadingQuality=0

; Rendering
+CVars=r.MobileContentScaleFactor=0.75
+CVars=r.BloomQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.MotionBlurQuality=0

; Shadows
+CVars=r.Shadow.MaxResolution=512
+CVars=r.Shadow.MaxCSMResolution=512
+CVars=r.Shadow.CSM.MaxCascades=1
+CVars=r.ShadowQuality=0

; Memory
+CVars=r.Streaming.PoolSize=128
```

---

## 12. Quick Reference: Common CVars

### 12.1 Essential Mobile CVars

```ini
; Resolution
r.MobileContentScaleFactor=1.0

; Quality
sg.ViewDistanceQuality=2
sg.AntiAliasingQuality=2
sg.ShadowQuality=2
sg.PostProcessQuality=2
sg.TextureQuality=2

; Post-Processing
r.BloomQuality=2
r.DepthOfFieldQuality=2
r.LightShaftQuality=1
r.MotionBlurQuality=1

; Memory
r.Streaming.PoolSize=256
```

### 12.2 Disable All Post-Processing (Maximum Performance)

```ini
r.BloomQuality=0
r.DepthOfFieldQuality=0
r.LightShaftQuality=0
r.MotionBlurQuality=0
r.FXAAQuality=0
r.Upscale.Quality=0
r.SSS.Quality=0
r.SSR.Quality=0
sg.PostProcessQuality=0
sg.EffectsQuality=0
```

### 12.3 Enable All Features (Maximum Quality)

```ini
r.MobileContentScaleFactor=2.0
sg.ViewDistanceQuality=3
sg.AntiAliasingQuality=3
sg.ShadowQuality=3
sg.GlobalIlluminationQuality=3
sg.ReflectionQuality=3
sg.PostProcessQuality=3
sg.TextureQuality=3
sg.EffectsQuality=3
sg.FoliageQuality=3
sg.ShadingQuality=3
r.BloomQuality=3
r.DepthOfFieldQuality=3
r.LightShaftQuality=2
r.MotionBlurQuality=3
r.ShadowQuality=3
```

---

## 13. Configuration File Locations Summary

| File | Purpose | Location |
|------|---------|----------|
| DefaultDeviceProfiles.ini | Project device profiles | Project/Config/ |
| AndroidEngine.ini | Android-specific settings | Engine/Config/Android/ |
| iOSEngine.ini | iOS-specific settings | Engine/Config/IOS/ |
| BaseScalability.ini | Default scalability settings | Engine/Config/ |
| BaseDeviceProfiles.ini | Default device profiles | Engine/Config/ |
| AndroidScalability.ini | Android scalability | Engine/Config/Android/ |

---

## 14. Troubleshooting Common Issues

### Issue: Poor Performance on Android
**Solution:**
```ini
r.Streaming.PoolSize=128
sg.EffectsQuality=1
sg.TextureQuality=1
r.MobileContentScaleFactor=0.75
```

### Issue: Visual Artifacts on iOS
**Solution:**
```ini
[iPhone5 DeviceProfile]
+CVars=r.RenderTargetSwitchWorkaround=1
```

### Issue: Memory Crashes
**Solution:**
```ini
[PlatformMemoryBuckets]
LargestMemoryBucket_MinGB=6
LargerMemoryBucket_MinGB=4
DefaultMemoryBucket_MinGB=3
SmallerMemoryBucket_MinGB=2
SmallestMemoryBucket_MinGB=2

[Mobile DeviceProfile]
+CVars_Default=r.Streaming.PoolSize=180
+CVars_Smaller=r.Streaming.PoolSize=150
+CVars_Smallest=r.Streaming.PoolSize=70
```

### Issue: Low FPS on Mid-Range Devices
**Solution:**
```ini
r.MobileContentScaleFactor=1.0
sg.ViewDistanceQuality=2
sg.AntiAliasingQuality=1
sg.ShadowQuality=1
sg.PostProcessQuality=1
sg.TextureQuality=2
r.BloomQuality=1
r.ShadowQuality=1
r.Shadow.MaxResolution=1024
```

---

## 15. Best Practices Summary

### DO:
- [ ] Use device profiles for platform-specific tuning
- [ ] Implement memory bucket system for varying device capabilities
- [ ] Test on real devices throughout development
- [ ] Profile performance regularly
- [ ] Use static lighting when possible
- [ ] Implement texture streaming
- [ ] Optimize materials for mobile
- [ ] Use appropriate quality presets per device tier

### DON'T:
- [ ] Use complex shaders on low-end devices
- [ ] Enable too many post-processing effects
- [ ] Use high-resolution textures without compression
- [ ] Forget to test different device profiles
- [ ] Ignore memory constraints
- [ ] Overuse dynamic lights
- [ ] Use expensive effects without fallbacks

---

## References

**Official Documentation:**
- Unreal Engine Documentation: https://dev.epicgames.com/documentation/en-us/unreal-engine
- Setting Up Device Profiles: https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-device-profiles-in-unreal-engine
- Mobile Rendering: https://dev.epicgames.com/documentation/en-us/unreal-engine/debugging-and-optimization-for-mobile-in-unreal-engine
- Mobile Optimization: https://dev.epicgames.com/documentation/en-us/unreal-engine/optimization-and-development-best-practices-for-mobile-projects-in-unreal-engine

---

## 16. Special Topic: Frame Generation Architecture & Conflicts

### 16.1 Architecture Overview
For modern mobile devices (Snapdragon 8 Gen 3/Elite), there are two primary paths for high-frame-rate rendering:
1.  **AFME (Adreno Frame Motion Engine)**: Kuro's hardware-accelerated implementation.
2.  **FSR3 Frame Interpolation (FI)**: Software-based temporal interpolation.

### 16.2 CRITICAL CONFLICT: AFME vs FSR3 FI
**DO NOT ENABLE BOTH SIMULTANEOUSLY.** 

| Issue | Impact |
|-------|--------|
| **Double Interpolation** | Extreme ghosting, smearing, and "jelly" UI artifacts. |
| **Input Latency** | FSR3 FI adds 30-50ms; AFME adds 8-12ms. Combined = Unplayable. |
| **Pacing Conflicts** | Both systems attempt to control the frame clock, causing micro-stutter. |

### 16.3 Problematic CVars (Do Not Use with AFME)
The following CVars are part of the FSR3 FI stack and should be **removed** when using AFME Level 5:
- `r.FakeFrameRate`
- `r.FidelityFX.FI.FrameRateMin`
- `r.FidelityFX.FI.FrameRateMax`
- `r.FidelityFX.FI.DebugOutput`
- `r.FidelityFX.FSR3.FI=1`
- `r.FidelityFX.FI.Enabled=1`

### 16.4 Recommended Configuration
- **Native Target**: 60 FPS (`t.MaxFPS=60`)
- **Frame Gen**: AFME Level 5 (`r.Kuro.AFME.Enable=5`)
- **Upscaling**: FSR3 Upscaling Only (`r.FidelityFX.FSR3.Enabled=1`, `r.FSR3.FI=0`)

---

*Document compiled from official Epic Games Unreal Engine documentation and Qualcomm Adreno optimization guides. Last updated: January 2026*
