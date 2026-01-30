# Installation & Usage Guide

Follow these steps to set up AntiSlax Pro on your system.

## Prerequisites

1.  **Python 3.8+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).
2.  **Git** (Optional): To clone the repository.

## Setup Steps

1.  **Download the Code**:
    ```bash
    git clone https://github.com/JesusQuijada34/antislax.git
    cd antislax
    ```

2.  **Environment Setup**:
    It is recommended to use a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Requirements**:
    ```bash
    pip install PyQt5
    ```

    *Note: If `leviathan_ui` is provided as a local module, ensure it is in the same directory or Python path.*

## Usage

### Graphical Mode
To launch the wizard, run:
```bash
python antislax.py
```

### Command Line Interface (CLI)
You can also run the core logic without the GUI by calling the `_run_cli()` function. This is useful for automated deployments.
*(To use CLI natively, you would need to modify the `if __name__ == "__main__":` block or call the class directly from a Python REPL).*

## Compilation
To create an executable (.exe), you can use `PyInstaller`:
```bash
pyinstaller --onefile --noconsole --icon=app/app-icon.ico antislax.py
```
*(Make sure to include assets in the bundle or keep them in the same folder as the .exe).*
