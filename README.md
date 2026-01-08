# WuWa Mobile Config - Ultimate Edition v4.6

![Target Device](https://img.shields.io/badge/Target_Device-Snapdragon_8_Elite-red?style=for-the-badge)
![Memory](https://img.shields.io/badge/Memory-16GB_RAM-blue?style=for-the-badge)
![FPS](https://img.shields.io/badge/Target_FPS-120-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-v4.6-gold?style=for-the-badge)

Welcome to the **Ultimate Edition v4.6** configuration for Wuthering Waves on Android. This project is meticulously tuned for next-generation mobile hardware, specifically the **Snapdragon 8 Elite (Gen 5)** and devices with **16GB+ RAM** (like the RedMagic 10/11 Pro).

Experience Wuthering Waves with desktop-class fidelity, stable 120 FPS performance via **Hardware Frame Generation (AFME 2.0)**, and a professional-grade visual presentation.

---

## 🚀 Key Features Overview

| Feature        | Technical Implementation     | Impact                                                                  |
| :------------- | :--------------------------- | :---------------------------------------------------------------------- |
| **Frame Rate** | 120 FPS via AFME 2.0         | Silky smooth combat with hardware-level frame interpolation.            |
| **Vulkan 1.3** | Bindless Descriptor Indexing | Desktop-class rendering that offloads driver overhead to the GPU.       |
| **Resolution** | 1:1 Native Pixel Rendering   | Eliminates mobile upscaling blur; crystal clear image.                  |
| **Aesthetics** | 16x Anisotropy + Mobile SSS  | PC-equivalent texture sharpness and character skin light diffusion.     |
| **Shadows**    | Contact Shadows + Full GTAO  | Superior grounding and depth with optimized HPM cache usage.            |
| **Memory**     | 4GB Texture Pool + PSO Cache | Razor-sharp assets and zero shader stutter during region traversal.     |
| **Stability**  | 16k Descriptor Pool          | Prevents "Device Lost" crashes even during high-intensity skill bursts. |

---

## 🔍 Technical Deep Dive

### 🎨 Visual Excellence

The "Ultimate Edition" philosophy moves beyond simply turning everything to "Ultra." It balances rendering techniques to achieve a cinematic look:

- **TAA Anti-Ghosting**: By increasing the `CurrentFrameWeight` to `0.28` and reducing sharpening to `0.2`, we eliminate the "trailing" effects common in mobile TAA while maintaining edge stability.
- **Ultra-Tight Bloom**: A custom `SizeScale` of `0.005` prevents the "bloom blowout" that masks character details, keeping skill effects punchy but contained.
- **Warm Color Palette**: Meticulously adjusted RGB gains (`R=1.03, G=0.95, B=1.0`) provide a more natural, vibrant look, moving away from the flat, greenish default profile.
- **Kuro-Specific Enhancements**: Unlocks advanced character rendering features like `Kuro.HairQuality=2` and `Kuro.CharacterShadowQuality=3` for high-fidelity protagonists.

### ⚡ Performance & Stability (v4.6 Major)

Harnessing the power of the Oryon cores and Adreno 840:

- **AFME 2.0 Hardware Frame Gen**: v4.6 moves from software pacing to the Adreno 840's native hardware frame motion engine for superior 120 FPS stability.
- **Vulkan 1.3 Bindless Rendering**: Leverages the 8 Elite's desktop-class driver to access resources directly, reclaiming massive CPU overhead during draw call emission.
- **512MB PSO Cache**: Expanded and optimized shader pipeline cache to ensure a completely hitch-free traversal experience across Solaris-3.
- **Vulkan Descriptor Expansion**: Pre-reserves 2048 descriptor sets and raises the limit to 16,384. This is critical for preventing "Device Lost" crashes during complex skill bursts.
- **IO Dispatcher Overhaul**: Expanded buffer memory and cache. Combined with UFS 4.0 storage, this creates a "hitch-free" traversal experience during fast grappling.

### 💾 Memory & Streaming

Optimized for the massive 16GB RAM ceiling:

- **Aggressive Purging**: Set `LevelStreamingLowMemoryPendingPurgeCount` to maximum to ensure RAM is freed immediately after region transitions.
- **4GB Texture Pool**: Allocates a dedicated 4GB buffer for textures—the optimal balance between visual fidelity and Android LMK stability.

---

## 🛠️ Installation Guide (Android - No Root Required)

Modern Android versions (Android 11+) restrict access to the `Android/data` folder. Follow this professional setup to deploy the config safely using **Shizuku** and **ZArchiver**.

### 1. Initial Setup

- **Install Shizuku**: Download it from the [Google Play Store](https://play.google.com/store/apps/details?id=moe.shizuku.privileged.api).
- **Install ZArchiver**: Download it from the [Google Play Store](https://play.google.com/store/apps/details?id=ru.zdevs.zarchiver).

### 2. Pair Shizuku (Wireless Debugging)

1.  Open **Shizuku** and tap on **Pairing**.
2.  Tap **Developer options** (ensure they are enabled in your phone settings first).
3.  Scroll down and enable **Wireless debugging**. Tap "Allow" when prompted.
4.  Tap on **Wireless debugging** (the text itself) to enter its submenu.
5.  Select **Pair device with pairing code**. Note the 6-digit code.
6.  Swipe down your notification bar, find the Shizuku notification, tap **Enter pairing code**, and type the code.
7.  Return to the Shizuku app and tap **Start** to initialize the service.

### 3. Configure ZArchiver for Data Access

1.  Open **ZArchiver**.
2.  Tap the **Three Dots (⋮)** at the top right → **Settings**.
3.  Navigate to **Root option**.
4.  Under **Type of root access**, select **Shizuku**.
5.  Enable **"Used for Android file operations"** and the related option below it.
6.  ZArchiver now has permission to modify the protected `Android/data` directory.

### 4. Deploy the Configuration

1.  **Backup**: Navigate to the path below and backup your existing `.ini` files.
    - `Android/data/com.kurogame.wutheringwaves.global/files/Client/Saved/Config/Android/`
2.  **Deploy**: Copy all 5 `.ini` files from this repository into the directory above, overwriting existing ones.
3.  **Permissions**: (Optional) Set files to **Read-Only** within ZArchiver to prevent game resets.

### 5. Final In-Game Settings

- Set **Bloom** to **ON** (Critical for v3.5 VFX).
- Set **Frame Rate** to **60** or **120**.
- Enable **Anti-Aliasing**.

---

## 🏗️ Configuration Architecture

The "Ultimate Edition" is split across 5 specialized files for modular performance:

1.  **Engine.ini**: The core engine overrides. Contains the bulk of the visual, threading, and GC optimizations.
2.  **Scalability.ini**: Defines the "Level 4" quality presets, ensuring that when the game calls for "Cinematic" quality, it uses our high-fidelity parameters.
3.  **DeviceProfiles.ini**: The "Brain" of the config. It tricks the game into identifying your device as a high-end target (`DeviceScore=1300`) and routes all Adreno GPUs to the Ultimate profile.
4.  **GameUserSettings.ini**: Handles high-level user preferences like native resolution scaling and HDR output.
5.  **Performance.ini**: Fine-tunes CPU core affinity (Prime vs. Performance cores) and sets thermal thresholds for sustained 120 FPS.

---

## ❓ Troubleshooting

| Issue                 | Potential Solution            | CVar to Adjust                                                        |
| :-------------------- | :---------------------------- | :-------------------------------------------------------------------- |
| **Screen Flickering** | Some GPUs dislike HZB.        | Set `r.HZBOcclusion=0` in `Engine.ini`.                               |
| **Overheating**       | 8 Elite is powerful but hot.  | Reduce `r.Vulkan.MaxGPUClockScale` to `0.80` in `Performance.ini`.    |
| **Vulkan Crashes**    | RobustBufferAccess stability. | Set `r.Vulkan.RobustBufferAccess=1` in `Engine.ini` (costs 3-5% FPS). |
| **Micro-Stuttering**  | RHI Pacing conflict.          | Ensure `r.Vulkan.CPURHIThreadFramePacer=0` if using AFME.             |

---

## 📜 Changelog

### **v4.6 (Latest)**

- **Hardware Frame Gen (AFME 2.0)**: Switched to native hardware-level interpolation (Level 5) for 120 FPS.
- **Vulkan 1.3 Bindless**: Enabled Descriptor Indexing and Bindless Rendering for reduced CPU driver overhead.
- **Elite Core Affinity**: Rerouted RHI/FG threads to Performance cores (4-5) to give Oryon Primes (6-7) breathing room.
- **Aesthetic Overhaul**: Enabled 16x Anisotropic Filtering, Mobile SSS, and high-fidelity Contact Shadows.
- **Memory Scaling**: Expanded PSO cache to 512MB and Texture Pool to 4GB for seamless 16GB RAM utilization.

### **v4.1**

- **Threading Refinement**: Reduced Physics workers to 4 to prevent Performance core contention with RHI/Streaming threads.
- **Exclusive AA Logic**: Disabled the redundant TAA stack in favor of pure FSR3 processing for maximum clarity.
- **GPU Throughput Boost**: Disabled RobustBufferAccess to reclaim 3-5% GPU performance on adreno 840.
- **Latency Reduction**: Reduced MaxFrameLatency to 1 for faster input response on Oryon Prime cores.

### **v4.0**

- **Vectorization Upgrade**: Enabled 30+ ISPC SIMD optimizations for Chaos Physics and Animations to leverage Oryon core efficiency.
- **IO Pipeline Expansion**: Increased Dispatcher Cache to 1.5GB and Buffer to 384MB for hitch-free map traversal.
- **Vulkan Pacing Logic**: Switched to `r.Vulkan.CPURHIThreadFramePacer=1` for consistent frame delivery.
- **adreno 840 Safety**: Added descriptor set pre-reservation to prevent "Device Lost" crashes.
- **Memory Optimization**: Set aggressive streaming purging and massive object limits (25M) for 16GB RAM devices.

### **v3.7**

- **LOD Philosophy Overhaul**: Removed all view distance, NPC distance, landscape LOD, and foliage cull overrides. Kuro's engine defaults are well-tuned for their game.
- **Streaming Trust**: Removed world partition loading range overrides—let Kuro handle streaming.
- **Preserved Character Detail**: Kept toon outline/eye/face shadow draw distances and mesh LOD biases for crisp character rendering at distance.

### **v3.6**

- **UFS 4.0 Optimization**: Increased streaming bandwidth to 100MB/s and enabled amortized CPU usage for seamless loading.
- **Physics Threading**: Increased Chaos worker threads to 6 to fully utilize the Snapdragon 8 Elite's performance cluster.
- **Shader Cache Enhancement**: Enabled Vulkan pipeline cache (256MB) and mobile shader cache to eliminate region-entry stutters.

---

## 🤝 Credits

This project is a culmination of community research and testing. Special thanks to:

- **[Arglax](https://github.com/Arglax/Mobile-WuWa-Config)** - Base V3.x working configurations.
- **[em00se](https://pastebin.com/ewk6wz9W)** - Comprehensive CVars dump and documentation.
- **[AlteriaX / Brandy](https://github.com/AlteriaX/WuWa-Configs-Android)** - Cleaned CVars reference and logic.
- **RGCloud** - Honami Escalator discovery.
- **Eggsee** - Essential memory leak mitigation and streaming recommendations.
- **Kuro Games Community** - For constant testing and feedback on various Adreno chipsets.

---

_Disclaimer: This is a community project and is not affiliated with Kuro Games. Use at your own risk. Modifying .ini files is generally safe but can lead to crashes if your hardware cannot handle the settings._
