# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1] - 2026-01-29

### Added
- **Ultimate Performance Plan**: Unlocks and activates the hidden Windows Ultimate Performance power scheme.
- **Gaming Optimization**: Added registry tweaks for Network Throttling, System Responsiveness, and GPU Priority.
- **Deep Cleaning Engine**: Expanded cleaning to include Prefetch, Thumbnail cache, Chrome/Edge cache, and DISM component cleanup.
- **BCD Tweaks**: Implemented low-latency boot configuration tweaks (Disabling dynamic ticks).
- **Interface Speedups**: Added tweaks for MenuShowDelay and MouseHoverTime to make the OS feel snappier.

### Changed
- **clean() method**: Now targets more system directories and uses `cleanmgr`.
- **apply_registry()**: Expanded with 15+ new technical tweaks for power users.

## [1.0] - 2026-01-29
- **Leviathan-UI Integration**: Implemented a modern, animated wizard interface.
- **Massive Debloat List**: Added tracking for over 100+ Windows pre-installed apps for removal.
- **Advanced Registry Tweaks**: Included optimizations for Explorer, Privacy, and System performance.
- **Deep Cleaning**: Added functionality to clear temporary files and Windows Update cache.
- **Admin Elevation**: Integrated automatic privilege escalation for Windows systems.
- **Splash Screen**: Added immersive splash screens for application startup.

### Changed
- Refactored core logic into the `AntiSlaxPro` class for better maintainability.
- Updated SVG icons for navigation.

### Fixed
- Fixed issues with registry key paths in certain Windows versions.
- Resolved crash when running without administrator privileges.

---

## [1.0-0.0-0.0] - Initial Release

- Initial core logic for registry tweaks.
- Basic CLI interface.
- Basic cleaning functions.
