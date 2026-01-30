"""
AntiSlax Pro - Windows Optimization and Privacy Enhancement Tool
===============================================================

This script provides a comprehensive set of tools to clean, optimize, and 
debloat Windows 10/11 systems. It includes registry tweaks, bloatware 
removal, and system cleaning utilities, all wrapped in a modern 
PyQt5-based graphical interface.

Author: JesusQuijada34 (Influent)
Version: 1.0
License: GPLv3
"""

import types
import os
import sys
import ctypes
import subprocess
import logging
REG_DATA = [
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Personalization\\Settings', 'AcceptedPrivacyPolicy', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection', 'AllowTelemetry', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'Start_TrackProgs', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\System', 'PublishUserActivities', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Siuf\\Rules', 'NumberOfSIUFInPeriod', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Siuf\\Rules', 'PeriodInNanoSeconds', '-', 'REG_SZ'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Edge', 'PersonalizationReportingEnabled', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Edge', 'DiagnosticData', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', 'EnableTransparency', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\PolicyManager\\default\\NewsAndInterests\\AllowNewsAndInterests', 'value', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Dsh', 'AllowNewsAndInterests', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-310093Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-338388Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SystemPaneSuggestionsEnabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'Start_IrisRecommendations', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-338389Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SoftLandingEnabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-338393Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-353694Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-353696Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-353698Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\SystemSettings\\AccountNotifications', 'EnableAccountNotifications', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\UserProfileEngagement', 'ScoobeSystemSettingEnabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'ShowSyncProviderNotifications', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SilentInstalledAppsEnabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings\\Windows.SystemToast.Suggested', 'Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Mobility', 'OptedIn', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'Start_AccountNotifications', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings\\Windows.SystemToast.BackupReminder', 'Enabled', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', 'AppsUseLightTheme', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', 'SystemUsesLightTheme', '0', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\TaskbarDeveloperSettings', 'TaskbarEndTask', '1', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'LastActiveClick', '1', 'REG_DWORD'),
    ('HKEY_CURRENT_USER\\Software\\Classes\\CLSID\\{e88865ea-0e1c-4e20-9aa6-edcd0212c87c}', 'System.IsPinnedToNameSpaceTree', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'CheckedValue', '1', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'DefaultValue', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'HKeyRoot', '2147483649', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'Id', '13', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'RegPath', 'Software\\Classes\\CLSID\\{e88865ea-0e1c-4e20-9aa6-edcd0212c87c}', 'REG_SZ'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'Text', 'Show Gallery', 'REG_SZ'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'Type', 'checkbox', 'REG_SZ'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'UncheckedValue', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowGallery', 'ValueName', 'System.IsPinnedToNameSpaceTree', 'REG_SZ'),
    ('HKEY_CURRENT_USER\\Software\\Classes\\CLSID\\{f874310e-b6b7-47dc-bc84-b9e6b38f5903}', '@', 'CLSID_MSGraphHomeFolder', 'REG_SZ'),
    ('HKEY_CURRENT_USER\\Software\\Classes\\CLSID\\{f874310e-b6b7-47dc-bc84-b9e6b38f5903}', 'System.IsPinnedToNameSpaceTree', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'CheckedValue', '1', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'DefaultValue', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'HKeyRoot', '2147483649', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'Id', '13', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'RegPath', 'Software\\Classes\\CLSID\\{f874310e-b6b7-47dc-bc84-b9e6b38f5903}', 'REG_SZ'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'Text', 'Show Home', 'REG_SZ'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'Type', 'checkbox', 'REG_SZ'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'UncheckedValue', '0', 'REG_DWORD'),
    ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\NavPane\\ShowHome', 'ValueName', 'System.IsPinnedToNameSpaceTree', 'REG_SZ'),
    ('-HKEY_CLASSES_ROOT\\CLSID\\{018D5C66-4533-4307-9B53-224DE2ED1FE6}', 'System.IsPinnedToNameSpaceTree', '0', 'REG_DWORD'),
    ('-HKEY_CLASSES_ROOT\\Wow6432Node\\CLSID\\{018D5C66-4533-4307-9B53-224DE2ED1FE6}', 'System.IsPinnedToNameSpaceTree', '0', 'REG_DWORD'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce', 'SetTaskbarSearchbox', 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search /v SearchboxTaskbarMode /t REG_DWORD /d 0 /f', 'REG_SZ'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Search', 'SearchboxTaskbarMode', '0', 'REG_DWORD'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'ShowTaskViewButton', '0', 'REG_DWORD'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'LaunchTo', '3', 'REG_DWORD'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'LaunchTo', '2', 'REG_DWORD'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'LaunchTo', '4', 'REG_DWORD'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'LaunchTo', '1', 'REG_DWORD'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'HideFileExt', '0', 'REG_DWORD'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'Hidden', '1', 'REG_DWORD'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce', 'SetTaskbarSearchbox', 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search /v SearchboxTaskbarMode /t REG_DWORD /d 2 /f', 'REG_SZ'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Search', 'SearchboxTaskbarMode', '2', 'REG_DWORD'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce', 'SetTaskbarSearchbox', 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search /v SearchboxTaskbarMode /t REG_DWORD /d 1 /f', 'REG_SZ'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Search', 'SearchboxTaskbarMode', '1', 'REG_DWORD'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce', 'SetTaskbarSearchbox', 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search /v SearchboxTaskbarMode /t REG_DWORD /d 3 /f', 'REG_SZ'),
    ('hkey_users\\default\\Software\\Microsoft\\Windows\\CurrentVersion\\Search', 'SearchboxTaskbarMode', '3', 'REG_DWORD'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce', 'UninstallMicrosoftEdge', 'cmd.exe /c winget uninstall --accept-source-agreements --disable-interactivity --id Microsoft.Edge', 'REG_SZ'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce', 'UninstallMicrosoftOneDrive', 'cmd.exe /c winget uninstall --accept-source-agreements --disable-interactivity --id Microsoft.OneDrive', 'REG_SZ'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 'OneDriveSetup', '-', 'REG_SZ'),
    ('hkey_users\\default\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 'OneDriveSetup', '-', 'REG_SZ'),
]
# LISTA MASIVA DE DEBLOAT
APPS_TO_REMOVE = [
    'Clipchamp.Clipchamp',
    'Microsoft.3DBuilder',
    'Microsoft.549981C3F5F10',
    'Microsoft.BingFinance',
    'Microsoft.BingFoodAndDrink',
    'Microsoft.BingHealthAndFitness',
    'Microsoft.BingNews',
    'Microsoft.BingSports',
    'Microsoft.BingTranslator',
    'Microsoft.BingTravel',
    'Microsoft.BingWeather',
    'Microsoft.Copilot',
    'Microsoft.Getstarted',
    'Microsoft.Messaging',
    'Microsoft.Microsoft3DViewer',
    'Microsoft.MicrosoftJournal',
    'Microsoft.MicrosoftOfficeHub',
    'Microsoft.MicrosoftPowerBIForWindows',
    'Microsoft.MicrosoftSolitaireCollection',
    'Microsoft.MicrosoftStickyNotes',
    'Microsoft.MixedReality.Portal',
    'Microsoft.NetworkSpeedTest',
    'Microsoft.News',
    'Microsoft.Office.OneNote',
    'Microsoft.Office.Sway',
    'Microsoft.OneConnect',
    'Microsoft.Print3D',
    'Microsoft.PowerAutomateDesktop',
    'Microsoft.SkypeApp',
    'Microsoft.Todos',
    'Microsoft.Windows.DevHome',
    'Microsoft.WindowsAlarms',
    'Microsoft.WindowsFeedbackHub',
    'Microsoft.WindowsMaps',
    'Microsoft.WindowsSoundRecorder',
    'Microsoft.XboxApp',
    'Microsoft.ZuneVideo',
    'MicrosoftCorporationII.MicrosoftFamily',
    'MicrosoftCorporationII.QuickAssist',
    'MicrosoftTeams',
    'MSTeams',
    'ACGMediaPlayer',
    'ActiproSoftwareLLC',
    'AdobeSystemsIncorporated.AdobePhotoshopExpress',
    'Amazon.com.Amazon',
    'AmazonVideo.PrimeVideo',
    'Asphalt8Airborne',
    'AutodeskSketchBook',
    'CaesarsSlotsFreeCasino',
    'COOKINGFEVER',
    'CyberLinkMediaSuiteEssentials',
    'DisneyMagicKingdoms',
    'Disney',
    'DrawboardPDF',
    'Duolingo-LearnLanguagesforFree',
    'EclipseManager',
    'Facebook',
    'FarmVille2CountryEscape',
    'fitbit',
    'Flipboard',
    'HiddenCity',
    'HULULLC.HULUPLUS',
    'iHeartRadio',
    'Instagram',
    'king.com.BubbleWitch3Saga',
    'king.com.CandyCrushSaga',
    'king.com.CandyCrushSodaSaga',
    'LinkedInforWindows',
    'MarchofEmpires',
    'Netflix',
    'NYTCrossword',
    'OneCalendar',
    'PandoraMediaInc',
    'PhototasticCollage',
    'PicsArt-PhotoStudio',
    'Plex',
    'PolarrPhotoEditorAcademicEdition',
    'Royal Revolt',
    'Shazam',
    'Sidia.LiveWallpaper',
    'SlingTV',
    'Spotify',
    'TikTok',
    'TuneInRadio',
    'Twitter',
    'Viber',
    'WinZipUniversal',
    'Wunderlist',
    'XING',
]

AIKON_TWEAKS = [
    ('HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 'LaunchTo', '1', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', 'AppsUseLightTheme', '0', 'REG_DWORD'),
    ('HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', 'AppsUseLightTheme', '0', 'REG_DWORD'),
    ('HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel', '{20D04FE0-3AEA-1069-A2D8-08002B30309D}', '0', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Personalization', 'NoLockScreen', '1', 'REG_DWORD'),
    ('HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer', 'ForceClassicControlPanel', '1', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Error Reporting', 'Disabled', '1', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\MTCUVC', 'EnableMtcUvc', '0', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search', 'AllowCortana', '0', 'REG_DWORD'),
    ('HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem', 'NtfsDisableLastAccessUpdate', '1', 'REG_DWORD'),
    # Tweaks de Velocidad de Interfaz
    ('HKCU\\Control Panel\\Desktop', 'MenuShowDelay', '0', 'REG_SZ'),
    ('HKCU\\Control Panel\\Desktop', 'WaitToKillAppTimeout', '2000', 'REG_SZ'),
    ('HKCU\\Control Panel\\Desktop', 'HungAppTimeout', '1000', 'REG_SZ'),
    ('HKCU\\Control Panel\\Desktop', 'AutoEndTasks', '1', 'REG_SZ'),
    ('HKCU\\Control Panel\\Mouse', 'MouseHoverTime', '10', 'REG_SZ'),
    # Optimizacion de Red y Gaming
    ('HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile', 'NetworkThrottlingIndex', '4294967295', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile', 'SystemResponsiveness', '0', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games', 'GPU Priority', '8', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games', 'Priority', '6', 'REG_DWORD'),
    ('HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games', 'Scheduling Category', 'High', 'REG_SZ'),
    # Deshabilitar servicios innecesarios via registro
    ('HKLM\\SYSTEM\\CurrentControlSet\\Services\\SysMain', 'Start', '4', 'REG_DWORD'), # Superfetch
    ('HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters', 'Size', '3', 'REG_DWORD'), # Optimizacion de Cache
]

PERFORMANCE_COMMANDS = [
    'powercfg /hibernate off',
    'powercfg /duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61', # Ultimate Performance
    'powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61',
    'bcdedit /set increaseuserva 3072',
    'bcdedit /set disabledynamictick yes',
    'bcdedit /deletevalue useplatformclock',
    'fsutil behavior set disablelastaccess 1',
]

class AntiSlaxPro:
    """
    Core logic for Windows optimization.
    
    This class handles the execution of registry tweaks, application removal,
    and system cleaning through shell commands.
    """

    def __init__(self):
        self.is_admin = self.check_admin()

    def check_admin(self):
        try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: return False

    def run_cmd(self, c):
        try: subprocess.run(c, shell=True, capture_output=True, text=True)
        except: pass

    def apply_registry(self):
        logging.info(f"Aplicando {len(REG_DATA)} cambios de registro...")
        for key, name, val, rtype in REG_DATA + AIKON_TWEAKS:
            cmd = f'reg add "{key}" /v "{name}" /t {rtype} /d "{val}" /f'
            self.run_cmd(cmd)

    def remove_apps(self):
        logging.info(f"Eliminando {len(APPS_TO_REMOVE)} aplicaciones de bloatware...")
        for app in APPS_TO_REMOVE:
            self.run_cmd(f'powershell -Command "Get-AppxPackage *{app}* | Remove-AppxPackage"')

    def clean(self):
        logging.info("Limpiando archivos temporales, logs, prefetch y cache profunda...")
        clean_cmds = [
            'del /q /s /f "%TEMP%\\*.*"',
            'del /q /s /f "C:\\Windows\\Temp\\*.*"',
            'del /q /s /f "C:\\Windows\\Prefetch\\*.*"',
            'del /q /s /f "%AppData%\\Local\\Microsoft\\Windows\\Explorer\\thumbcache_*.db"',
            'del /q /s /f "%LocalAppData%\\Google\\Chrome\\User Data\\Default\\Cache\\*.*"',
            'del /q /s /f "%LocalAppData%\\Microsoft\\Edge\\User Data\\Default\\Cache\\*.*"',
            'ipconfig /flushdns',
            'net stop wuauserv',
            'rd /s /q C:\\Windows\\SoftwareDistribution',
            'net start wuauserv',
            'Dism /online /Cleanup-Image /StartComponentCleanup /ResetBase',
            'cleanmgr /sagerun:1'
        ]
        for c in clean_cmds:
            self.run_cmd(c)

    def optimize_performance(self):
        logging.info("Aplicando optimizaciones de alto rendimiento y bcdedit...")
        for c in PERFORMANCE_COMMANDS:
            self.run_cmd(c)

    def run(self):
        """
        Executes the full optimization sequence in CLI mode.
        
        Requires administrator privileges to function correctly.
        """

        if not self.is_admin:
            print("ERROR: EJECUTAR COMO ADMINISTRADOR")
            return
        self.clean()
        self.apply_registry()
        self.optimize_performance()
        self.remove_apps()
        self.run_cmd('taskkill /f /im explorer.exe && start explorer.exe')
        logging.info("AntiSlax Pro finalizado con éxito.")

def _run_cli():
    """Entry point for running the optimizer in Command Line Interface mode."""
    AntiSlaxPro().run()


def ensure_admin():
    """If not running elevated, relaunch the script with admin privileges and exit.
    Returns True when already elevated or after successful relaunch (child will continue).
    """
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        is_admin = False

    if is_admin:
        return True

    # Build parameter string quoting each arg
    try:
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        # ShellExecuteW returns >32 when successful
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        try:
            ok = int(ret) > 32
        except Exception:
            ok = False
        if ok:
            # Relaunched elevated; exit current process to let elevated instance run
            sys.exit(0)
        else:
            print("Error: no se pudo solicitar elevación de privilegios.")
            return False
    except Exception as e:
        print("Error al intentar elevar privilegios:", e)
        return False







# === Asistente tipo QWizard usando Leviathan-UI ===
import sys
import ctypes
import subprocess
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QSizePolicy
from PyQt5.QtCore import Qt
from leviathan_ui import WipeWindow, CustomTitleBar, LeviathanDialog, InmojiTrx, InmersiveSplash


from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup, pyqtSlot, QSize, QPoint
from PyQt5.QtGui import QIcon, QPixmap

class SvgButton(QPushButton):
    """
    A custom QPushButton that renders an SVG icon and applies modern styling.
    
    Features hover and pressed states with smooth color transitions.
    """

    def __init__(self, svg_path, tooltip=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIcon(QIcon(svg_path))
        self.setIconSize(QSize(28, 28))
        self.setFixedHeight(44)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('''
            QPushButton {
                background-color: rgba(255,255,255,0.13);
                color: white;
                border: 2px solid rgba(0,120,212,0.13);
                border-radius: 13px;
                font-weight: 600;
                font-size: 16px;
                padding: 0 22px;
            }
            QPushButton:hover {
                background-color: #e6f1fb;
                color: #0078d4;
                border: 2px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #d0e7fa;
                color: #005fa3;
                border: 2px solid #005fa3;
            }
        ''')
        if tooltip:
            self.setToolTip(tooltip)

def animated_icon_label(svg_path, text):
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setAlignment(Qt.AlignCenter)
    icon = QLabel()
    icon.setPixmap(QIcon(svg_path).pixmap(64, 64))
    icon.setStyleSheet("margin-bottom: 10px;")
    icon.setGraphicsEffect(None)
    icon.setFixedSize(64, 64)
    label = QLabel(text)
    label.setStyleSheet("color: white; font-size: 18px; font-family: 'Segoe UI';")
    lay.addWidget(icon, alignment=Qt.AlignCenter)
    lay.addWidget(label, alignment=Qt.AlignCenter)
    # Fade in animation
    icon.setWindowOpacity(0)
    anim = QPropertyAnimation(icon, b"windowOpacity")
    anim.setDuration(600)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.start()
    return w

class AntiSlaxWizardUI(QWidget):
    """
    The main Wizard interface for AntiSlax Pro.
    
    Uses QStackedWidget to manage multiple pages and provides smooth 
    animated transitions between steps. Integrates with Leviathan-UI 
    for a premium look and feel.
    """

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(700, 420)
        WipeWindow.create().set_mode("ghostBlur").set_background("auto").set_radius(14).apply(self)
        self.title_bar = CustomTitleBar(self, title="AntiSlax Pro", icon="🛡️")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.title_bar)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, 1)

        # Páginas del asistente
        self.pages = [
            self.page_intro(),
            self.page_clean(),
            self.page_registry(),
            self.page_debloat(),
            self.page_finish()
        ]
        for p in self.pages:
            self.stack.addWidget(p)

        # Navegación con SVGs
        nav = QHBoxLayout()
        nav.setContentsMargins(30, 10, 30, 20)
        nav.setSpacing(20)
        self.btn_prev = SvgButton(svg_path="assets/arrow-left.svg", tooltip="Anterior")
        self.btn_next = SvgButton(svg_path="assets/arrow-right.svg", tooltip="Siguiente")
        nav.addWidget(self.btn_prev)
        nav.addWidget(self.btn_next)
        main_layout.addLayout(nav)

        self.btn_prev.clicked.connect(self.go_prev)
        self.btn_next.clicked.connect(self.go_next)
        self.update_nav()

        # Animación de apertura (slide up + fade in)
        self.setWindowOpacity(0)
        self.move(self.x(), self.y() + 60)
        self.anim_open = QParallelAnimationGroup()
        anim1 = QPropertyAnimation(self, b"windowOpacity")
        anim1.setDuration(420)
        anim1.setStartValue(0)
        anim1.setEndValue(1)
        anim1.setEasingCurve(QEasingCurve.OutCubic)
        anim2 = QPropertyAnimation(self, b"pos")
        anim2.setDuration(420)
        anim2.setStartValue(self.pos())
        anim2.setEndValue(self.pos() - QPoint(0, 60))
        anim2.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_open.addAnimation(anim1)
        self.anim_open.addAnimation(anim2)
        self.anim_open.start()

    def closeEvent(self, event):
        # Animación de cierre (slide down + fade out)
        self.anim_close = QParallelAnimationGroup()
        anim1 = QPropertyAnimation(self, b"windowOpacity")
        anim1.setDuration(350)
        anim1.setStartValue(1)
        anim1.setEndValue(0)
        anim1.setEasingCurve(QEasingCurve.InCubic)
        anim2 = QPropertyAnimation(self, b"pos")
        anim2.setDuration(350)
        anim2.setStartValue(self.pos())
        anim2.setEndValue(self.pos() + QPoint(0, 60))
        anim2.setEasingCurve(QEasingCurve.InCubic)
        self.anim_close.addAnimation(anim1)
        self.anim_close.addAnimation(anim2)
        self.anim_close.finished.connect(self._final_close)
        self.anim_close.start()
        event.ignore()

    def _final_close(self):
        self.hide()
        self.deleteLater()
        QApplication.instance().quit()

    def animate_page(self, new_idx):
        # Transición slide desde la derecha y animación de contenido
        old_idx = self.stack.currentIndex()
        if old_idx == new_idx:
            return
        old_widget = self.stack.currentWidget()
        new_widget = self.pages[new_idx]
        direction = 1 if new_idx > old_idx else -1
        w = self.stack.width()
        new_widget.move(direction * w, 0)
        new_widget.show()
        anim_old = QPropertyAnimation(old_widget, b"pos")
        anim_old.setDuration(350)
        anim_old.setStartValue(old_widget.pos())
        anim_old.setEndValue(old_widget.pos() - QPoint(direction * w, 0))
        anim_old.setEasingCurve(QEasingCurve.InOutCubic)
        anim_new = QPropertyAnimation(new_widget, b"pos")
        anim_new.setDuration(350)
        anim_new.setStartValue(new_widget.pos())
        anim_new.setEndValue(QPoint(0, 0))
        anim_new.setEasingCurve(QEasingCurve.InOutCubic)
        group = QParallelAnimationGroup()
        group.addAnimation(anim_old)
        group.addAnimation(anim_new)
        def on_done():
            self.stack.setCurrentIndex(new_idx)
            # Animación de fade in para el contenido de la nueva página
            for child in new_widget.findChildren(QLabel):
                child.setWindowOpacity(0)
                anim = QPropertyAnimation(child, b"windowOpacity")
                anim.setDuration(400)
                anim.setStartValue(0)
                anim.setEndValue(1)
                anim.setEasingCurve(QEasingCurve.OutCubic)
                anim.start()
        group.finished.connect(on_done)
        group.start()

    def go_prev(self):
        idx = self.stack.currentIndex()
        if idx > 0:
            self.animate_page(idx - 1)
        self.update_nav()

    def go_next(self):
        idx = self.stack.currentIndex()
        if idx < len(self.pages) - 1:
            self.animate_page(idx + 1)
        self.update_nav()

    def update_nav(self):
        idx = self.stack.currentIndex()
        self.btn_prev.setEnabled(idx > 0)
        self.btn_next.setEnabled(idx < len(self.pages) - 1)

    # ...existing page_xxx, run_xxx, restart_explorer methods sin cambios...

    def page_intro(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        label = QLabel("<b>Bienvenido a AntiSlax Pro</b><br><br>Este asistente le guiará para optimizar, limpiar y desbloatar su sistema Windows con estilo moderno Leviathan-UI.<br><br><i>Requiere privilegios de administrador.</i>")
        label.setWordWrap(True)
        label.setStyleSheet("color: white; font-size: 18px; font-family: 'Segoe UI';")
        lay.addWidget(label)
        # Animación de fade in
        label.setWindowOpacity(0)
        anim = QPropertyAnimation(label, b"windowOpacity")
        anim.setDuration(600)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        return w

    def page_clean(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        label = QLabel("Se eliminarán archivos temporales, se limpiará la caché de DNS y Windows Update.")
        label.setWordWrap(True)
        label.setStyleSheet("color: white; font-size: 16px; font-family: 'Segoe UI';")
        btn = QPushButton("Ejecutar limpieza ahora")
        btn.setFixedHeight(40)
        btn.setFocusPolicy(Qt.NoFocus)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet('''
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 16px;
                padding: 0 30px;
                min-width: 220px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #005fa3;
                color: #e6f1fb;
            }
            QPushButton:pressed {
                background-color: #003e6b;
                color: #e6f1fb;
            }
        ''')
        btn.clicked.connect(self.run_clean)
        lay.addWidget(label)
        lay.addWidget(btn)
        # Animación de fade in
        label.setWindowOpacity(0)
        anim = QPropertyAnimation(label, b"windowOpacity")
        anim.setDuration(600)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        return w

    def page_registry(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        label = QLabel("Se aplicarán optimizaciones y tweaks de privacidad y rendimiento en el registro de Windows.")
        label.setWordWrap(True)
        label.setStyleSheet("color: white; font-size: 16px; font-family: 'Segoe UI';")
        btn = QPushButton("Aplicar tweaks de registro")
        btn.setFixedHeight(40)
        btn.setFocusPolicy(Qt.NoFocus)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet('''
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 16px;
                padding: 0 30px;
                min-width: 220px;
                min-height: 40px;
                box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
                transition: background 0.2s, color 0.2s;
            }
            QPushButton:hover {
                background-color: #005fa3;
                color: #e6f1fb;
            }
            QPushButton:pressed {
                background-color: #003e6b;
                color: #e6f1fb;
            }
        ''')
        btn.clicked.connect(self.run_registry)
        lay.addWidget(label)
        lay.addWidget(btn)
        # Animación de fade in
        label.setWindowOpacity(0)
        anim = QPropertyAnimation(label, b"windowOpacity")
        anim.setDuration(600)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        return w

    def page_debloat(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        label = QLabel("Se eliminarán aplicaciones preinstaladas y bloatware de Windows.")
        label.setWordWrap(True)
        label.setStyleSheet("color: white; font-size: 16px; font-family: 'Segoe UI';")
        btn = QPushButton("Eliminar apps bloatware")
        btn.setFixedHeight(40)
        btn.setFocusPolicy(Qt.NoFocus)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet('''
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 16px;
                padding: 0 30px;
                min-width: 220px;
                min-height: 40px;
                box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
                transition: background 0.2s, color 0.2s;
            }
            QPushButton:hover {
                background-color: #005fa3;
                color: #e6f1fb;
            }
            QPushButton:pressed {
                background-color: #003e6b;
                color: #e6f1fb;
            }
        ''')
        btn.clicked.connect(self.run_debloat)
        lay.addWidget(label)
        lay.addWidget(btn)
        # Animación de fade in
        label.setWindowOpacity(0)
        anim = QPropertyAnimation(label, b"windowOpacity")
        anim.setDuration(600)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        return w

    def page_finish(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        label = QLabel("¡Optimización finalizada! Puede reiniciar el explorador de Windows para aplicar todos los cambios.")
        label.setWordWrap(True)
        label.setStyleSheet("color: white; font-size: 16px; font-family: 'Segoe UI';")
        btn = QPushButton("Reiniciar Explorer.exe")
        btn.setFixedHeight(40)
        btn.setFocusPolicy(Qt.NoFocus)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet('''
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 16px;
                padding: 0 30px;
                min-width: 220px;
                min-height: 40px;
                box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
                transition: background 0.2s, color 0.2s;
            }
            QPushButton:hover {
                background-color: #005fa3;
                color: #e6f1fb;
            }
            QPushButton:pressed {
                background-color: #003e6b;
                color: #e6f1fb;
            }
        ''')
        btn.clicked.connect(self.restart_explorer)
        lay.addWidget(label)
        lay.addWidget(btn)
        # Animación de fade in
        label.setWindowOpacity(0)
        anim = QPropertyAnimation(label, b"windowOpacity")
        anim.setDuration(600)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        return w

    def go_prev(self):
        idx = self.stack.currentIndex()
        if idx > 0:
            self.stack.setCurrentIndex(idx - 1)
        self.update_nav()

    def go_next(self):
        idx = self.stack.currentIndex()
        if idx < len(self.pages) - 1:
            self.stack.setCurrentIndex(idx + 1)
        self.update_nav()

    def update_nav(self):
        idx = self.stack.currentIndex()
        self.btn_prev.setEnabled(idx > 0)
        if idx == len(self.pages) - 1:
            self.btn_next.setEnabled(False)
        else:
            self.btn_next.setEnabled(True)

    def run_clean(self):
        try:
            AntiSlaxPro().clean()
            LeviathanDialog.launch(self, "Limpieza completada", "Archivos temporales y caché limpiados correctamente.", mode="success")
        except Exception as e:
            LeviathanDialog.launch(self, "Error", f"Error al limpiar: {e}", mode="error")

    def run_registry(self):
        try:
            AntiSlaxPro().apply_registry()
            LeviathanDialog.launch(self, "Tweaks aplicados", "Optimización y tweaks de registro aplicados.", mode="success")
        except Exception as e:
            LeviathanDialog.launch(self, "Error", f"Error al aplicar tweaks: {e}", mode="error")

    def run_debloat(self):
        try:
            AntiSlaxPro().remove_apps()
            LeviathanDialog.launch(self, "Bloatware eliminado", "Las aplicaciones innecesarias han sido eliminadas.", mode="success")
        except Exception as e:
            LeviathanDialog.launch(self, "Error", f"Error al eliminar apps: {e}", mode="error")

    def restart_explorer(self):
        try:
            subprocess.run('taskkill /f /im explorer.exe && start explorer.exe', shell=True)
            LeviathanDialog.launch(self, "Explorer reiniciado", "El explorador de Windows se ha reiniciado.", mode="info")
        except Exception as e:
            LeviathanDialog.launch(self, "Error", f"No se pudo reiniciar explorer.exe: {e}", mode="error")


def main():
    ensure_admin()
    app = QApplication(sys.argv)
    try:
        icon = InmojiTrx("app/antislax-icon.ico").apply(app)
    except Exception:
        icon = None
    wizard = AntiSlaxWizardUI()
    if icon: wizard.setWindowIcon(icon)
    wizard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
