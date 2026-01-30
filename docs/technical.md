# Technical Architecture

This document describes the internal structure of the `antislax.py` codebase.

## Core Logic: `AntiSlaxPro` Class
The logic is encapsulated in a central class to allow both CLI and GUI usage.

### Key Methods
-   `check_admin()`: Uses `ctypes` to verify if the process has elevated privileges.
-   `run_cmd(c)`: A wrapper around `subprocess.run` to execute shell commands silently.
-   `apply_registry()`: Iterates through `REG_DATA` and `AIKON_TWEAKS` lists, executing `reg add` for each entry.
-   `remove_apps()`: Uses PowerShell commands (`Get-AppxPackage` | `Remove-AppxPackage`) to uninstall bloatware.
-   `optimize_performance()`: Executes high-level system commands from the `PERFORMANCE_COMMANDS` list, including power plans and BCD edits.

## User Interface: `AntiSlaxWizardUI` Class
Inherits from `PyQt5.QtWidgets.QWidget` and utilizes the `leviathan_ui` framework.

### UI Components
-   **QStackedWidget**: Manages the multi-page wizard flow.
-   **CustomTitleBar**: A custom-drawn title bar with "ghostBlur" mode.
-   **SvgButton**: Custom buttons that render SVG icons and handle hover states.
-   **Animations**: Uses `QPropertyAnimation` and `QParallelAnimationGroup` for premium transitions.

### Privilege Escalation: `ensure_admin()`
This function checks for admin rights at startup. If missing, it uses `ShellExecuteW` with the `runas` verb to relaunch the script with elevated permissions.

## Dependencies
-   `PyQt5`: Core GUI library.
-   `leviathan_ui`: Custom UI framework for advanced styling and dialogs.
-   `subprocess`, `ctypes`, `sys`, `logging`: Standard Python libraries for system interaction.

## Resource Management
The application expects an `assets/` and `app/` folder for icons and graphics.
-   `assets/arrow-left.svg` & `assets/arrow-right.svg`: Navigation icons.
-   `app/antislax-icon.ico`: Main application icon.
