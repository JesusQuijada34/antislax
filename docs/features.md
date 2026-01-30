# Feature Breakdown

AntiSlax Pro is divided into four main operational modules.

## 1. System Cleaning (`clean()` method)
Targets temporary files and system caches that accumulate over time.
-   **Temp Files**: Clears `%TEMP%` and `C:\Windows\Temp`.
-   **Prefetch & Thumbnails**: Purges the Prefetch folder and Explorer thumbnail cache.
-   **Browser Cache**: Targets Google Chrome and Microsoft Edge cache directories.
-   **DNS Cache**: Flushes the DNS resolver cache via `ipconfig /flushdns`.
-   **Windows Update**: Stops the `wuauserv` service and purges `C:\Windows\SoftwareDistribution`.
-   **Component Cleanup**: Runs `Dism /Cleanup-Image` and `cleanmgr /sagerun:1` for deep storage recovery.

## 2. Registry Optimization (`apply_registry()` method)
Applies a massive list of tweaks categorized into:
-   **Privacy**: Disables `AllowTelemetry`, `TrackProgs`, `PublishUserActivities`, and Cortana.
-   **UI / UX**: Disables News and Interests, Transparency (optional), and adds specific Explorer tweaks like `LastActiveClick`.
-   **System**: Disables Windows Error Reporting and NTFS Last Access Update for performance.
-   **Personalization**: Forces dark mode for apps and system.

## 3. Proactive Debloating (`remove_apps()` method)
Removes pre-installed UWP packages that are often considered bloatware.
-   **Microsoft Apps**: Copilot, 3D Builder, Bing Finance, News, weather, Xbox, etc.
-   **Third-Party Pre-installs**: TikTok, Facebook, Instagram, Spotify, Netflix, etc.
-   **Performance Impact**: Dramatically reduces the number of background services and start-up items.

## 4. Ultimate Performance & BCD
New in v1.1, these tweaks focus on hardware-level responsiveness:
-   **Power Plan**: Unlocks the hidden "Ultimate Performance" scheme for maximum CPU frequency.
-   **BCD Tweaks**: Disables dynamic ticks and synthetic timers (`useplatformclock`) to reduce input lag.
-   **Hibernation**: Disables hibernation to reclaim several gigabytes of disk space and reduce disk writes.

## 5. Leviathan-UI Wizard
A high-end graphical interface that:
-   **Guided Workflow**: Breaks down the optimization into steps.
-   **Animated Feedback**: Uses smooth slide transitions and fade-in effects.
-   **Real-time Interaction**: Users can trigger specific modules manually within the wizard.
