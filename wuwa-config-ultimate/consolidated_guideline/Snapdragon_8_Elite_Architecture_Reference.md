# Snapdragon 8 Elite (Gen 5) Architecture Reference
## For Wuthering Waves UE4 Optimization

> **Document Version**: v1.0 (January 2026)  
> **Target Config Version**: v5.9.8-thermal  
> **Purpose**: Comprehensive hardware reference for AI agents optimizing Wuthering Waves configs

---

## Table of Contents
1. [CPU Architecture](#1-cpu-architecture)
2. [GPU Architecture (Adreno 840)](#2-gpu-architecture-adreno-840)
3. [Thread Configuration Guide](#3-thread-configuration-guide)
4. [AFME Frame Generation](#4-afme-frame-generation)
5. [SGSR2 Temporal Upscaling](#5-sgsr2-temporal-upscaling)
6. [Thermal Optimization CVars](#6-thermal-optimization-cvars)
7. [Common Pitfalls & Conflicts](#7-common-pitfalls--conflicts)
8. [CVar Quick Reference](#8-cvar-quick-reference)

---

## 1. CPU Architecture

### 1.1 Oryon CPU Topology

The Snapdragon 8 Elite uses Qualcomm's custom **Oryon** CPU cores. This is NOT a traditional ARM big.LITTLE design.

| Attribute | Value |
|-----------|-------|
| **Total Cores** | 8 |
| **Prime Cores** | 2x Oryon Phoenix-L @ 4.32-4.60 GHz |
| **Performance Cores** | 6x Oryon Phoenix-M @ 3.53-3.62 GHz |
| **Efficiency Cores** | **NONE** (all cores are high-performance) |
| **Process Node** | TSMC 3nm (N3P) |
| **L2 Cache** | 12MB per cluster (24MB total) |

### 1.2 Core Numbering (Android)

Based on Android Perfetto documentation and kernel conventions:

| Core ID | Type | Frequency | Recommended Use |
|---------|------|-----------|-----------------|
| **0** | Performance | 3.53 GHz | TaskGraph Worker |
| **1** | Performance | 3.53 GHz | TaskGraph Worker |
| **2** | Performance | 3.53 GHz | TaskGraph Worker |
| **3** | Performance | 3.53 GHz | TaskGraph Worker |
| **4** | Performance | 3.53 GHz | TaskGraph Worker |
| **5** | Performance | 3.53 GHz | **FREE** (OS/AFME driver) |
| **6** | Prime | 4.60 GHz | Game Thread (GT) |
| **7** | Prime | 4.60 GHz | Render Thread (RT) |

### 1.3 Key Insight: No Little Cores

> **CRITICAL**: The CVar `r.Threading.LittleCoreAffinity` is a **misnomer** on Snapdragon 8 Elite.  
> There are NO little/efficiency cores. This CVar should be interpreted as:
> - `LittleCoreAffinity` = Worker Core Affinity (Performance cores 0-5)
> - `BigCoreAffinity` = Critical Thread Affinity (Prime cores 6-7)

### 1.4 N-1 Rule for AFME

When using AFME frame generation, reserve **one core** for the AFME driver and OS tasks:

```
Total Performance Cores: 6 (cores 0-5)
Active Worker Threads:   5 (cores 0-4)
Reserved for AFME:       1 (core 5)
```

This prevents context switching overhead and cache thrashing during frame interpolation.

---

## 2. GPU Architecture (Adreno 840)

### 2.1 Specifications

| Attribute | Value |
|-----------|-------|
| **Architecture** | Sliced (3 independent shader slices) |
| **Clock Speed** | 1.2 GHz |
| **Shaders** | 1536 shader units |
| **Execution Units** | 12 EUs |
| **TMUs** | 96 Texture Mapping Units |
| **ROPs** | 48 Render Output Units |
| **HPM (High Performance Memory)** | 12MB on-die |
| **L2 Cache** | 1MB |
| **L3 Cache** | 18MB (shared with system) |
| **TDP** | ~5W |
| **FP16 Performance** | 7.37 TFLOPS |
| **FP32 Performance** | 3.69 TFLOPS |
| **Vulkan Support** | 1.3 |

### 2.2 TBDR Architecture

Adreno uses **Tile-Based Deferred Rendering (TBDR)**:

1. **Binning Pass**: Geometry is sorted into screen tiles
2. **Rendering Pass**: Each tile is rendered entirely in GMEM (on-chip memory)
3. **Resolve Pass**: Final tile is written to system DRAM

**Optimization Goal**: Keep data in GMEM as long as possible to reduce DRAM bandwidth.

### 2.3 HPM Cache Configuration

```ini
r.Vulkan.Adreno.HPMCacheSize=12288  ; 12MB (Adreno 840 specification)
```

> **WARNING**: Do NOT set this to 24MB. The 24MB figure refers to combined L2 cache across CPU clusters, not GPU HPM.

### 2.4 VRS vs UBWC Tradeoff

VRS (Variable Rate Shading) and UBWC (Universal Bandwidth Compression) are **mutually exclusive** on Adreno:

| Feature | Benefit | Best For |
|---------|---------|----------|
| **VRS** | 10-30% fragment shader reduction | Post-processing heavy (WuWa) |
| **UBWC** | 30-40% memory bandwidth reduction | Texture-heavy, simple shaders |

**Recommendation for Wuthering Waves**: Use **VRS** (anime style, heavy post-processing, skill VFX).

---

## 3. Thread Configuration Guide

### 3.1 Recommended Settings

```ini
; Performance.ini
r.Threading.BigCoreAffinity=6-7        ; Prime cores (GT/RT)
r.Threading.LittleCoreAffinity=0-4     ; 5 Performance cores (workers)
TaskGraph.MaxThreads=5                  ; N-1 rule for AFME

; Engine.ini
r.Vulkan.NumWorkerThreads=4            ; Vulkan command encoding
t.MaxWorkerThreads=5                   ; General worker threads
```

### 3.2 Thread Allocation Visualization

```
+------------------------------------------------------------------+
|                    SNAPDRAGON 8 ELITE CPU                        |
+------------------------------------------------------------------+
|  PERFORMANCE CLUSTER (6x Oryon @ 3.53 GHz)                       |
|  +--------+--------+--------+--------+--------+--------+         |
|  | Core 0 | Core 1 | Core 2 | Core 3 | Core 4 | Core 5 |         |
|  | Worker | Worker | Worker | Worker | Worker |  FREE  |         |
|  | Thread | Thread | Thread | Thread | Thread | OS/AFME|         |
|  +--------+--------+--------+--------+--------+--------+         |
|                                                                   |
|  PRIME CLUSTER (2x Oryon @ 4.60 GHz)                             |
|  +------------------+------------------+                          |
|  |     Core 6       |     Core 7       |                          |
|  |   Game Thread    |  Render Thread   |                          |
|  |      (GT)        |      (RT)        |                          |
|  +------------------+------------------+                          |
+------------------------------------------------------------------+
```

### 3.3 Why r.Vulkan.NumWorkerThreads=4?

Vulkan command buffer encoding is lightweight. Using fewer threads:
- Prevents L2 cache thrashing between Vulkan workers
- Reduces context switching overhead
- 4 threads is sufficient for command encoding on Adreno 840

---

## 4. AFME Frame Generation

### 4.1 What is AFME?

**Adreno Frame Motion Engine (AFME)** is Qualcomm's hardware-accelerated frame generation technology:

- Takes 60 FPS native input
- Interpolates to 120 FPS output
- Uses motion vectors from the engine (not optical flow)
- Lower latency than FSR3 Frame Interpolation (~8-12ms vs ~15-20ms)

### 4.2 AFME CVars

```ini
; Core AFME Settings
r.Kuro.AFME.Enable=5                     ; Level 5 = Elite mode for Adreno 840
r.AFME2.Enable=1                         ; AFME 2.0 generation

; Motion Vector Enhancement (Critical for quality)
r.VertexDeformationOutputsVelocity=1     ; Skeletal mesh motion vectors
r.SkeletalMesh.VelocityRendering=1       ; Forced skinned mesh velocity
r.Mobile.BasePassOutputsVelocity=1       ; Explicit mobile velocity pass
r.BasePassOutputsVelocity=1              ; Base pass velocity output

; Latency & Quality
r.Kuro.AFME.LowLatencyMode=1             ; Processing latency reduction
r.Kuro.AFME.UIOptimization=1             ; Prevents UI ghosting

; Frame Pacing
t.MaxFPS=60                              ; MUST be 60 for AFME
r.Vulkan.MaxFrameLatency=4               ; Frame buffer depth
```

### 4.3 AFME Levels

| Level | Quality | Use Case |
|-------|---------|----------|
| 0 | Off | Disabled |
| 1-4 | Increasing | Standard devices |
| **5** | Elite | **Adreno 840 (recommended)** |

### 4.4 AFME Conflicts

**DO NOT enable these with AFME:**

```ini
; CONFLICTS - These will cause ghosting/artifacts:
r.FidelityFX.FSR3.FI=1                   ; FSR3 Frame Interpolation
r.FidelityFX.FI.Enabled=1                ; FI module
r.FakeFrameRate=XX                       ; FSR3 timing reference
```

---

## 5. SGSR2 Temporal Upscaling

### 5.1 ⚠️ NOT IMPLEMENTED IN WUTHERING WAVES

**CRITICAL**: Research confirms that Kuro Games has **NOT** integrated the SGSR2 plugin into Wuthering Waves.

| Technology | Developer Integration Status |
|------------|------------------------------|
| **AFME** | ✅ Implemented by Kuro Games |
| **AFME 2.0** | ✅ Implemented by Kuro Games |
| **SGSR2** | ❌ NOT integrated |
| **SGSR1** | ❌ NOT integrated |

Adding `r.SGSR2.*` CVars to Engine.ini will have **NO EFFECT** as the required shaders and engine hooks are missing from the game binary.

### 5.2 Why SGSR2 Requires Developer Integration

Unlike AFME (which is a driver-level hardware feature), SGSR2 is a developer-level plugin. It requires:

1. **Plugin Compilation**: The developer must include the Qualcomm SGSR2 library in the game build.
2. **Shader Integration**: The SGSR2 GLSL/HLSL shaders must be compiled into the game's PSO cache.
3. **Buffer Routing**: The engine must explicitly feed SGSR2 the required buffers (Color, Depth, and Motion Vectors).

### 5.3 If Kuro Adds SGSR2 in Future

If a future update integrates SGSR2, the following configuration would be the optimal "Ultra Quality" (1.18x upscale) pathway:

```ini
; [HYPOTHETICAL - DO NOT USE YET]
r.SGSR2.Enabled=1
r.SGSR2.Quality=0                        ; 0=Ultra(1.18x), 1=Quality(1.5x)
r.SGSR2.Variant=0                        ; 0=2-pass-FS (Fastest)
r.SGSR2.Sharpness=1.0
r.MobileContentScaleFactor=0.85          ; Render at 85% resolution
```

---

## 6. Thermal Optimization CVars

### 6.1 TBDR Memory Bandwidth Reduction

```ini
; Prevents expensive GMEM->DRAM resolve operations
r.Mobile.DiscardDepthStencil=1           ; Don't write depth/stencil to DRAM
r.Mobile.DisableDepthAndStencilAfterShadowPass=1  ; Further DRAM reduction

; Precision optimization
r.Mobile.FullPrecision=0                 ; Use FP16 ALU (2x power efficiency)

; Subpass merging
r.Vulkan.AllowSubpass=1                  ; Keeps data in GMEM between passes
r.Vulkan.DescriptorSetStrategy=1         ; Reduces descriptor churn
```

### 6.2 Anisotropic Filtering

```ini
; Base textures
r.Anisotropy=4                           ; 4x (was 8x, reduced for thermal)
r.MaxAnisotropy=4                        ; Synced

; Virtual textures (MUST match base)
r.VT.AnisotropicFiltering=4              ; [v5.9.8] Aligned with base
r.VT.MaxAnisotropy=4                     ; [v5.9.8] Aligned with base

; Compensation for lower AF
r.MipMapLODBias=-0.2                     ; Slight sharpening (no shimmer)
```

### 6.3 Shadow Optimization

```ini
r.Shadow.CSM.MaxCascades=3               ; 3 cascades (was 4)
r.Shadow.MaxResolution=1024              ; Stable memory packing
r.Shadow.MaxCSMResolution=1024           ; Synced
r.Shadow.MaxNumPointShadowCacheUpdatesPerFrame=2  ; Reduced from 4
r.Shadow.MaxNumSpotShadowCacheUpdatesPerFrame=2   ; Reduced from 4
```

### 6.4 Estimated Impact

| Optimization | GPU Power Reduction | DRAM Bandwidth Reduction |
|--------------|---------------------|--------------------------|
| DiscardDepthStencil | 5-8% | 15-20% |
| FullPrecision=0 | 10-15% | - |
| AllowSubpass | 5-10% | 30-40% |
| AF 4x (was 8x) | 3-5% | 10-15% |
| **Combined** | **25-35%** | **50-60%** |

---

## 7. Common Pitfalls & Conflicts

### 7.1 Duplicate CVars

**Problem**: Same CVar defined multiple times with different values.

| CVar | Common Conflict | Resolution |
|------|-----------------|------------|
| `gc.MaxObjectsNotConsideredByGC` | 200 vs 200000 | Keep only 200000 |
| `t.MaxWorkerThreads` | 5 vs 8 (ConsoleVariables section) | Keep only 5 |
| `r.VT.AnisotropicFiltering` | 16 vs base AF 4 | Align to 4 |

### 7.2 Section Override Order

UE4 CVars can be overridden by later sections:

```
[SystemSettings] → [RendererSettings] → [ConsoleVariables] → DeviceProfile
```

CVars in `[ConsoleVariables]` often override `[SystemSettings]`. Check for conflicts!

### 7.3 DeviceProfile Sync

Settings in `Engine.ini` should be mirrored in `DeviceProfiles.ini` for the target device profile. Missing CVars may cause inconsistent behavior.

### 7.4 VRS + UBWC Conflict

These are mutually exclusive on Adreno. If VRS is enabled, UBWC is partially disabled. Choose one based on workload.

### 7.5 AFME + FSR3 FI Conflict

**NEVER enable both.** This causes:
- Double interpolation artifacts
- 30-50ms additional latency
- UI ghosting on damage numbers

---

## 8. CVar Quick Reference

### 8.1 Resolution & Scaling

| CVar | Value | Notes |
|------|-------|-------|
| `r.MobileContentScaleFactor` | 0 or 1.0 | 0=native, 1.0=explicit native |
| `r.SecondaryScreenPercentage.GameViewport` | 100 | No internal downscaling |

### 8.2 Threading

| CVar | Recommended | Range |
|------|-------------|-------|
| `r.Threading.BigCoreAffinity` | 6-7 | Prime cores |
| `r.Threading.LittleCoreAffinity` | 0-4 | Performance cores (N-1) |
| `TaskGraph.MaxThreads` | 5 | Match affinity |
| `r.Vulkan.NumWorkerThreads` | 4 | Vulkan encoding |
| `t.MaxWorkerThreads` | 5 | General workers |

### 8.3 Adreno 840 Hardware

| CVar | Value | Notes |
|------|-------|-------|
| `r.Vulkan.Adreno.HPMCacheSize` | 12288 | 12MB (spec) |
| `r.Vulkan.Adreno.LRZ.Enable` | 1 | Low-Resolution Z |
| `r.Vulkan.Adreno.TBDR.Optimize` | 1 | TBDR optimizations |
| `r.Vulkan.Adreno.FastZClear` | 1 | Fast Z-clear |

### 8.4 VRS

| CVar | Value | Notes |
|------|-------|-------|
| `r.VRS.Enable` | 1 | Master toggle |
| `r.VRS.GPUTier` | 2 | Adreno 840 Tier 2 |
| `r.VRS.FoveationPattern` | 1 | 1=Low, 2=High |
| `r.VRS.ContentAdaptive` | 1 | Dynamic shading |
| `r.Vulkan.AllowVRS` | 1 | Vulkan VRS support |

### 8.5 Frame Generation

| CVar | Value | Notes |
|------|-------|-------|
| `r.Kuro.AFME.Enable` | 5 | Level 5 Elite |
| `r.AFME2.Enable` | 1 | AFME 2.0 |
| `t.MaxFPS` | 60 | **MUST be 60** |
| `r.Vulkan.MaxFrameLatency` | 4 | Frame buffer depth |

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| v1.1 | Jan 2026 | Updated SGSR2 status to NOT IMPLEMENTED |
| v1.0 | Jan 2026 | Initial documentation for v5.9.8-thermal |

---

## Sources

1. Android Authority - Snapdragon 8 Elite Deep Dive
2. Qualcomm Developer Blog - SGSR2, AFME 2.0
3. HMC Tech - Adreno 840 Specifications
4. Android Perfetto Documentation - CPU Core Analysis
5. Qualcomm Snapdragon Game Plugins for Unreal Engine (GitHub)
6. RedMagic 11 Pro UE4 Optimization Guide (consolidated_guideline/)
