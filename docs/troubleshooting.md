# Troubleshooting

Common issues and how to solve them.

## 1. "ERROR: EJECUTAR COMO ADMINISTRADOR"
**Cause**: The script was unable to elevate its privileges.
**Solution**: Right-click on your terminal/PowerShell and select "Run as Administrator", then launch the script. If the automated popup appeared and you clicked "No", relaunch the script and click "Yes".

## 2. PyQt5 Import Error
**Cause**: PyQt5 is not installed in your current Python environment.
**Solution**: Run `pip install PyQt5`. If using a virtual environment, make sure it is activated.

## 3. Leviathan-UI Module Not Found
**Cause**: The `leviathan_ui` library is missing.
**Solution**: This is a custom framework. Ensure the library files are present in the project folder or installed via your local package manager.

## 4. Changes Not Visible After Running
**Cause**: Windows Explorer needs to be restarted to reload the registry settings.
**Solution**: Use the "Reiniciar Explorer.exe" button on the final page of the wizard, or manually restart your computer.

## 5. Antivirus Flags
**Cause**: Modifying the Windows Registry and running PowerShell scripts are sensitive actions that trigger some AV software.
**Solution**: AntiSlax Pro is open source. You can inspect the code to verify its safety. Add the application to your antivirus exclusion list if needed.

## 6. App Removal Fails
**Cause**: Some apps are considered "System Apps" and cannot be removed via standard PowerShell commands in newer Windows versions.
**Solution**: This is expected for core components. AntiSlax targets non-essential bloatware only.
