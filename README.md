# WuWa Mobile Config - Ultimate Edition v3.6

![Target Device](https://img.shields.io/badge/Target_Device-Snapdragon_8_Elite-red?style=for-the-badge)
![Memory](https://img.shields.io/badge/Memory-16GB_RAM-blue?style=for-the-badge)
![FPS](https://img.shields.io/badge/Target_FPS-120-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-v3.6-gold?style=for-the-badge)

Welcome to the **Ultimate Edition v3.6** configuration for Wuthering Waves on Android. This project is meticulously tuned for next-generation mobile hardware, specifically the **Snapdragon 8 Elite (Gen 5)** and devices with **16GB+ RAM** (like the RedMagic 11 Pro). 

Experience Wuthering Waves with desktop-class fidelity, stable 120 FPS performance via native frame generation, and a professional-grade visual presentation.

---

## 🚀 Key Features Overview

| Feature | Technical Implementation | Impact |
| :--- | :--- | :--- |
| **Frame Rate** | 120 FPS Native Target | Silky smooth combat with Frame Generation compatibility. |
| **Resolution** | 1:1 Native Pixel Rendering | Eliminates mobile upscaling blur; crystal clear image. |
| **Anti-Aliasing** | TAA Anti-Ghosting (Weight 0.28) | High-stability edges with minimal ghosting in fast combat. |
| **Color Palette** | Professional Warm Tone (R+3%) | Natural skin tones and reduced "yellow-green" tint. |
| **Physics** | Chaos Simulation V2 | High-fidelity cloth, hair, and environmental interactions. |
| **Textures** | 2GB VRAM Pool + Virtual Textures | Razor-sharp textures at all distances with no pop-in. |
| **API** | Vulkan Parallel Rendering | Multi-threaded draw calls for maximum GPU utilization. |
| **Stability** | Incremental Multi-threaded GC | Eliminates micro-stutters during long gaming sessions. |

---

## 🔍 Technical Deep Dive

### 🎨 Visual Excellence
The "Ultimate Edition" philosophy moves beyond simply turning everything to "Ultra." It balances rendering techniques to achieve a cinematic look:
- **TAA Anti-Ghosting**: By increasing the `CurrentFrameWeight` to `0.28` and reducing sharpening to `0.2`, we eliminate the "trailing" effects common in mobile TAA while maintaining edge stability.
- **Ultra-Tight Bloom**: A custom `SizeScale` of `0.005` prevents the "bloom blowout" that masks character details, keeping skill effects punchy but contained.
- **Warm Color Palette**: Meticulously adjusted RGB gains (`R=1.03, G=0.95, B=1.0`) provide a more natural, vibrant look, moving away from the flat, greenish default profile.
- **Kuro-Specific Enhancements**: Unlocks advanced character rendering features like `Kuro.HairQuality=2` and `Kuro.CharacterShadowQuality=3` for high-fidelity protagonists.

### ⚔️ Physics & Interaction
Combat is the heart of WuWa, and v3.5 brings desktop-grade simulation to mobile:
- **Chaos Physics Tuning**: Complete migration to the Chaos solver with dedicated threading (`p.Chaos.DedicatedThreadEnabled=1`) for realistic cloth and hair movement.
- **C++ Water Interaction**: Enabled `UseCppWaterEffect=1` for high-performance, realistic ripples and interactions when characters move through water.

### ⚡ Performance & Stability
Harnessing the power of the Oryon cores and Adreno 8xx series GPUs:
- **Vulkan Parallel Rendering**: Fully utilizes multi-core architectures for parallel command buffer generation, significantly reducing CPU bottlenecks.
- **GPU Niagara Particles**: Skills and effects are offloaded to the GPU compute pipeline (`r.Niagara.GPUCompute=1`), allowing for more complex VFX without dropping frames.
- **Tuned Garbage Collection**: A specialized incremental GC system (`gc.IncrementalGCTimePerFrame=0.001`) ensures memory is cleaned up in tiny intervals, preventing the "periodic hitch" common in Unreal Engine mobile titles.

### 💾 Memory & Streaming
Optimized for the massive 16GB RAM ceiling:
- **Virtual Texturing (VT)**: Enabled `r.VirtualTextures=1` with 16x anisotropic filtering for sharp textures at extreme angles without the memory overhead of traditional mipmaps.
- **Memory Leak Mitigation**: Integrated **Eggsie's** recommended streaming group boosts to ensure stable performance during extended map exploration.
- **2GB Texture Pool**: Allocates a dedicated 2GB buffer for textures, ensuring high-res assets are always ready for rendering.

---

## 🛠️ Installation Guide (Android - No Root Required)

Modern Android versions (Android 11+) restrict access to the `Android/data` folder. Follow this professional setup to deploy the config safely using **Shizuku** and **ZArchiver**.

### 1. Initial Setup
*   **Install Shizuku**: Download it from the [Google Play Store](https://play.google.com/store/apps/details?id=moe.shizuku.privileged.api).
*   **Install ZArchiver**: Download it from the [Google Play Store](https://play.google.com/store/apps/details?id=ru.zdevs.zarchiver).

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
    *   `Android/data/com.kurogame.wutheringwaves.global/files/Client/Saved/Config/Android/`
2.  **Deploy**: Copy all 5 `.ini` files from this repository into the directory above, overwriting existing ones.
3.  **Permissions**: (Optional) Set files to **Read-Only** within ZArchiver to prevent game resets.

### 5. Final In-Game Settings
*   Set **Bloom** to **ON** (Critical for v3.5 VFX).
*   Set **Frame Rate** to **60** or **120**.
*   Enable **Anti-Aliasing**.

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

| Issue | Potential Solution | CVar to Adjust |
| :--- | :--- | :--- |
| **Screen Flickering** | Some GPUs dislike HZB. | Set `r.HZBOcclusion=0` in `Engine.ini`. |
| **Overheating** | 8 Elite is powerful but hot. | Reduce `r.Vulkan.MaxGPUClockScale` to `0.75` in `Performance.ini`. |
| **Crashes during Combat** | VRAM overflow from shadows. | Reduce `r.Shadow.MaxCSMResolution` to `1024` in `Engine.ini`. |
| **Blurred Image** | TAA might be too soft for you. | Increase `r.TemporalAASharpen` to `0.5` or `0.8`. |

---

## 📜 Changelog

### **v3.6 (Latest)**
- **UFS 4.0 Optimization**: Increased streaming bandwidth to 100MB/s and enabled amortized CPU usage for seamless loading.
- **Physics Threading**: Increased Chaos worker threads to 6 to fully utilize the Snapdragon 8 Elite's performance cluster.
- **Shader Cache Enhancement**: Enabled Vulkan pipeline cache (256MB) and mobile shader cache to eliminate region-entry stutters.
- **Architectural Cleanup**: Centralized all engine logic into `Engine.ini` and streamlined `DeviceProfiles.ini` to prevent priority conflicts.
- **Kuro Extended GI**: Enabled full-resolution Global Illumination and high-fidelity particle interactions.
- **Shadow Refinement**: Standardized shadow resolution at 1024 for optimal sharpness-to-thermal balance.

### **v3.5**
- **Native Resolution**: Added `r.MobileContentScaleFactor=0` for true native rendering.
- **Chaos Physics**: Complete physics simulation tuning block (10+ CVars).
- **Kuro Extended Visuals**: Added 11 new Kuro-specific visual CVars (GlobalGI, Tonemapping, etc.).
- **Decal System**: Full decal quality block - fixes blocky artifacts (e.g., motorbike skids).
- **Virtual Textures**: VT system with 16x anisotropic filtering.
- **GPU Particles**: Niagara GPU compute + async ticking.
- **Vulkan Parallel**: Async compute, parallel rendering, and preemption.

### **v3.2 - v3.4**
- **Planar Reflections**: Added crisp reflections on water and floors.
- **Toon Rendering**: Adjusted draw distances for outlines and facial details.
- **Color Grading**: Refined warm palette (R+3%, G-6%, B=neutral).

### **v3.0 - v3.1**
- **Anti-Ghosting**: Initial TAA weight tuning (0.28).
- **Shader Cache**: Full precompilation to eliminate first-time stutters.
- **Log Suppression**: Disabled 30+ log categories to reduce Disk I/O.

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

*Disclaimer: This is a community project and is not affiliated with Kuro Games. Use at your own risk. Modifying .ini files is generally safe but can lead to crashes if your hardware cannot handle the settings.*
