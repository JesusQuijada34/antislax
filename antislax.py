#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AntiSlax - Sistema de Optimización para Gaming y Proyectos
Elimina bloatware, limpia archivos basura y optimiza servicios de Windows
"""

import sys
import os
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QListWidget, QTextEdit,
    QProgressBar, QCheckBox, QGroupBox, QMessageBox, QStatusBar,
    QListWidgetItem, QSplitter, QFrame
)
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5.QtGui import QIcon, QFont

# Import custom modules
from lib.custom_titlebar import CustomTitleBar
from lib.system_utils import get_os_info, get_disk_usage, format_bytes
from lib.optimization_modules import OptimizationWorker
from lib.platform_detector import PlatformDetector
from lib.admin_utils import AdminUtils
from lib.optimization.windows import WindowsOptimizer
from lib.optimization.linux import LinuxOptimizer
from lib.optimization.macos import MacOSOptimizer


class AntiSlaxWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Check admin privileges
        self.is_admin = AdminUtils.is_admin()
        self.os_type = PlatformDetector.get_os()
        self.distro_info = PlatformDetector.get_distro()
        
        # Initialize appropriate optimizer
        if PlatformDetector.is_windows():
            self.optimizer = WindowsOptimizer()
        elif PlatformDetector.is_linux():
            self.optimizer = LinuxOptimizer()
        elif PlatformDetector.is_macos():
            self.optimizer = MacOSOptimizer()
        else:
            self.optimizer = None
        
        # Current worker thread
        self.current_worker = None
        
        # Data storage
        self.bloatware_data = {}
        self.junk_data = {}
        self.services_data = {}
        
        self.init_ui()
        self.load_stylesheet()
        self.update_status()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Remove native title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        # Set window properties
        self.setWindowTitle("AntiSlax - Optimizador de Sistema")
        self.setMinimumSize(900, 650)
        self.resize(1000, 700)
        
        # Main container
        main_container = QWidget()
        main_container.setObjectName("centralWidget")
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        icon_path = Path(__file__).parent / "app" / "app-icon.ico"
        self.title_bar = CustomTitleBar(self, "AntiSlax", str(icon_path) if icon_path.exists() else None)
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self.toggle_maximize)
        self.title_bar.close_clicked.connect(self.close)
        main_layout.addWidget(self.title_bar)
        
        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(8)
        
        # Header
        header = QLabel("🚀 AntiSlax - Optimizador de Sistema")
        header.setObjectName("headerLabel")
        header.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(header)
        
        # Admin warning with elevation button
        if not self.is_admin:
            warning_frame = QFrame()
            warning_frame.setStyleSheet("""
                QFrame {
                    background-color: #3d2a10;
                    border: 1px solid #d97452;
                    border-radius: 6px;
                }
                QLabel {
                    color: #ff9e7a;
                    border: none;
                    background: transparent;
                }
            """)
            warning_layout = QVBoxLayout(warning_frame)
            warning_layout.setContentsMargins(12, 12, 12, 12)
            
            warning_label = QLabel("⚠️ Modo Restringido: Se requieren privilegios de administrador")
            warning_label.setAlignment(Qt.AlignCenter)
            warning_label.setStyleSheet("font-weight: bold; font-size: 13px;")
            warning_layout.addWidget(warning_label)
            
            desc_label = QLabel("Para acceder a todas las funciones de optimización y limpieza, la aplicación debe ejecutarse con permisos elevados.")
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("font-size: 11px; margin-top: 4px;")
            warning_layout.addWidget(desc_label)
            
            admin_btn = QPushButton("🔒 Reiniciar como Administrador")
            admin_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d97452, stop:1 #bf5b3d);
                    border: 1px solid #ff9e7a;
                    margin-top: 8px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e68565, stop:1 #d97452);
                }
            """)
            admin_btn.setCursor(Qt.PointingHandCursor)
            admin_btn.clicked.connect(self.request_admin)
            warning_layout.addWidget(admin_btn)
            
            content_layout.addWidget(warning_frame)
        
        # Tab widget
        self.tabs = QTabWidget()
        content_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_bloatware_tab()
        self.create_junk_tab()
        self.create_services_tab()
        self.create_gaming_tab()
        self.create_info_tab()
        
        main_layout.addWidget(content_widget)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.setCentralWidget(main_container)
    
    def create_bloatware_tab(self):
        """Create bloatware removal tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header
        header = QLabel("Eliminar Bloatware")
        header.setObjectName("subHeaderLabel")
        layout.addWidget(header)
        
        desc = QLabel("Detecta y elimina aplicaciones preinstaladas innecesarias.")
        layout.addWidget(desc)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        scan_btn = QPushButton("🔍 Escanear Bloatware")
        scan_btn.clicked.connect(self.scan_bloatware)
        btn_layout.addWidget(scan_btn)
        
        self.remove_bloat_btn = QPushButton("🗑️ Eliminar Seleccionados")
        self.remove_bloat_btn.setObjectName("dangerButton")
        self.remove_bloat_btn.clicked.connect(self.remove_bloatware)
        self.remove_bloat_btn.setEnabled(False)
        if self.is_admin:  # Only show if admin
            btn_layout.addWidget(self.remove_bloat_btn)
        else:
            self.remove_bloat_btn.setVisible(False)
        
        layout.addLayout(btn_layout)
        
        # List widget
        self.bloatware_list = QListWidget()
        layout.addWidget(self.bloatware_list)
        
        # Progress bar
        self.bloat_progress = QProgressBar()
        self.bloat_progress.setVisible(False)
        layout.addWidget(self.bloat_progress)
        
        self.tabs.addTab(tab, "🗑️ Bloatware")
    
    def create_junk_tab(self):
        """Create junk cleaner tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header
        header = QLabel("Limpiar Archivos Basura")
        header.setObjectName("subHeaderLabel")
        layout.addWidget(header)
        
        desc = QLabel("Limpia archivos temporales, caché y otros archivos innecesarios.")
        layout.addWidget(desc)
        
        # Info label
        self.junk_info_label = QLabel("Haz clic en 'Escanear' para comenzar")
        self.junk_info_label.setStyleSheet("background: #e8c9a0; padding: 12px; border-radius: 6px; font-weight: bold;")
        layout.addWidget(self.junk_info_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        scan_junk_btn = QPushButton("🔍 Escanear Basura")
        scan_junk_btn.clicked.connect(self.scan_junk)
        btn_layout.addWidget(scan_junk_btn)
        
        self.clean_junk_btn = QPushButton("🧹 Limpiar Ahora")
        self.clean_junk_btn.setObjectName("successButton")
        self.clean_junk_btn.clicked.connect(self.clean_junk)
        self.clean_junk_btn.setEnabled(False)
        if self.is_admin:  # Only show if admin
            btn_layout.addWidget(self.clean_junk_btn)
        else:
            self.clean_junk_btn.setVisible(False)
        
        layout.addLayout(btn_layout)
        
        # Log area
        self.junk_log = QTextEdit()
        self.junk_log.setReadOnly(True)
        self.junk_log.setMaximumHeight(200)
        layout.addWidget(self.junk_log)
        
        # Progress bar
        self.junk_progress = QProgressBar()
        self.junk_progress.setVisible(False)
        layout.addWidget(self.junk_progress)
        
        self.tabs.addTab(tab, "🧹 Limpieza")
    
    def create_services_tab(self):
        """Create services optimization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header
        header = QLabel("Optimizar Servicios")
        header.setObjectName("subHeaderLabel")
        layout.addWidget(header)
        
        desc = QLabel("Detiene y deshabilita servicios innecesarios para mejorar el rendimiento.")
        layout.addWidget(desc)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        scan_services_btn = QPushButton("🔍 Escanear Servicios")
        scan_services_btn.clicked.connect(self.scan_services)
        btn_layout.addWidget(scan_services_btn)
        
        self.optimize_services_btn = QPushButton("⚡ Optimizar Seleccionados")
        self.optimize_services_btn.setObjectName("successButton")
        self.optimize_services_btn.clicked.connect(self.optimize_services)
        self.optimize_services_btn.setEnabled(False)
        if self.is_admin:  # Only show if admin
            btn_layout.addWidget(self.optimize_services_btn)
        else:
            self.optimize_services_btn.setVisible(False)
        
        layout.addLayout(btn_layout)
        
        # List widget
        self.services_list = QListWidget()
        layout.addWidget(self.services_list)
        
        # Progress bar
        self.services_progress = QProgressBar()
        self.services_progress.setVisible(False)
        layout.addWidget(self.services_progress)
        
        self.tabs.addTab(tab, "⚙️ Servicios")
    
    def create_gaming_tab(self):
        """Create gaming mode tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header
        header = QLabel("Modo Gaming")
        header.setObjectName("subHeaderLabel")
        layout.addWidget(header)
        
        desc = QLabel("Aplica optimizaciones específicas para mejorar el rendimiento en juegos y proyectos.")
        layout.addWidget(desc)
        
        # Optimizations group
        group = QGroupBox("Optimizaciones Disponibles")
        group_layout = QVBoxLayout(group)
        
        self.gaming_checks = []
        optimizations = [
            ("Deshabilitar Game DVR", "Desactiva la grabación de juegos de Windows"),
            ("Plan de energía alto rendimiento", "Activa el plan de máximo rendimiento"),
            ("Deshabilitar optimizaciones de pantalla completa", "Mejora el rendimiento en juegos"),
            ("Configurar Windows Update", "Evita actualizaciones durante el juego"),
        ]
        
        for opt_name, opt_desc in optimizations:
            check = QCheckBox(opt_name)
            check.setToolTip(opt_desc)
            check.setChecked(True)
            self.gaming_checks.append(check)
            group_layout.addWidget(check)
        
        layout.addWidget(group)
        
        # Apply button
        apply_gaming_btn = QPushButton("🎮 Aplicar Modo Gaming")
        apply_gaming_btn.setObjectName("successButton")
        apply_gaming_btn.clicked.connect(self.apply_gaming_mode)
        if self.is_admin:  # Only show if admin
            layout.addWidget(apply_gaming_btn)
        else:
            apply_gaming_btn.setVisible(False)
            no_admin_label = QLabel("⚠️ Requiere privilegios de administrador para aplicar optimizaciones")
            no_admin_label.setStyleSheet("color: #909090; font-style: italic; padding: 8px;")
            layout.addWidget(no_admin_label)
        
        # Log area
        self.gaming_log = QTextEdit()
        self.gaming_log.setReadOnly(True)
        self.gaming_log.setMaximumHeight(200)
        layout.addWidget(self.gaming_log)
        
        # Progress bar
        self.gaming_progress = QProgressBar()
        self.gaming_progress.setVisible(False)
        layout.addWidget(self.gaming_progress)
        
        layout.addStretch()
        
        self.tabs.addTab(tab, "🎮 Gaming")
    
    def create_info_tab(self):
        """Create system info tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header
        header = QLabel("Información del Sistema")
        header.setObjectName("subHeaderLabel")
        layout.addWidget(header)
        
        # System info
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        layout.addWidget(self.info_text)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Actualizar Información")
        refresh_btn.clicked.connect(self.update_system_info)
        layout.addWidget(refresh_btn)
        
        self.tabs.addTab(tab, "ℹ️ Info")
        
        # Load initial info
        self.update_system_info()
    
    def load_stylesheet(self):
        """Load the material design stylesheet"""
        qss_path = Path(__file__).parent / "assets" / "material.qss"
        if qss_path.exists():
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.isMaximized():
            self.showNormal()
            self.title_bar.update_maximize_icon(False)
        else:
            self.showMaximized()
            self.title_bar.update_maximize_icon(True)
    
    def request_admin(self):
        """Request admin privileges"""
        AdminUtils.request_elevation()
    
    def update_status(self):
        """Update status bar"""
        admin_status = "Administrador" if self.is_admin else "Usuario Normal"
        self.status_bar.showMessage(f"Estado: {admin_status} | AntiSlax v1.1 (Material)")
    
    def update_system_info(self):
        """Update system information display using Markdown"""
        os_info = get_os_info()
        disk_info = get_disk_usage()
        
        # Markdown formatted info
        md_text = f"""
# 🖥️ Información del Sistema

## Sistema Operativo
* **Sistema:** {os_info['system']} {os_info['release']}
* **Versión:** {os_info['version']}
* **Arquitectura:** {'64-bit' if os_info['is_64bit'] else '32-bit'}
* **Procesador:** {os_info['processor']}

## 💾 Almacenamiento (C:)
"""
        
        if disk_info:
            md_text += f"""
* **Total:** `{format_bytes(disk_info['total'])}`
* **Usado:** `{format_bytes(disk_info['used'])}` ({disk_info['percent']:.1f}%)
* **Libre:** `{format_bytes(disk_info['free'])}`
"""
        
        md_text += f"""
## 🚀 AntiSlax
* **Versión:** `IO-1.1-Material`
* **Privilegios:** `{'Administrador ✓' if self.is_admin else 'Usuario Normal ⚠️'}`
* **Desarrollador:** `JesusQuijada34`
* **UI:** `Reactive Material Design`
"""
        
        try:
            self.info_text.setMarkdown(md_text)
        except AttributeError:
            # Fallback for older PyQt5 versions
            self.info_text.setText(md_text)
    
    # Bloatware methods
    @pyqtSlot()
    def scan_bloatware(self):
        """Scan for bloatware"""
        if self.current_worker:
            return
        
        self.bloat_progress.setVisible(True)
        self.bloat_progress.setValue(0)
        self.bloatware_list.clear()
        
        self.current_worker = OptimizationWorker("scan_bloatware", self.optimizer)
        self.current_worker.progress.connect(self.on_bloat_progress)
        self.current_worker.finished.connect(self.on_bloat_scan_finished)
        self.current_worker.start()
    
    def on_bloat_progress(self, value, message):
        """Handle bloatware scan progress"""
        self.bloat_progress.setValue(value)
        self.status_bar.showMessage(message)
    
    def on_bloat_scan_finished(self, success, summary):
        """Handle bloatware scan completion"""
        self.bloat_progress.setVisible(False)
        self.status_bar.showMessage(summary)
        
        if success and self.current_worker:
            self.bloatware_data = self.current_worker.task_data
            found_bloatware = self.bloatware_data.get('found_bloatware', [])
            
            for app in found_bloatware:
                item = QListWidgetItem(f"📦 {app['name']} - {app['description']}")
                item.setCheckState(Qt.Checked)
                item.setData(Qt.UserRole, app)
                self.bloatware_list.addItem(item)
            
            self.remove_bloat_btn.setEnabled(len(found_bloatware) > 0 and self.is_admin)
        
        self.current_worker = None
    
    @pyqtSlot()
    def remove_bloatware(self):
        """Remove selected bloatware"""
        if not self.is_admin:
            QMessageBox.warning(self, "Permiso Denegado", "Se requieren privilegios de administrador.")
            return
        
        # Get selected apps
        apps_to_remove = []
        for i in range(self.bloatware_list.count()):
            item = self.bloatware_list.item(i)
            if item.checkState() == Qt.Checked:
                apps_to_remove.append(item.data(Qt.UserRole))
        
        if not apps_to_remove:
            QMessageBox.information(self, "Sin Selección", "No hay aplicaciones seleccionadas para eliminar.")
            return
        
        reply = QMessageBox.warning(
            self,
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar {len(apps_to_remove)} aplicaciones?\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.bloat_progress.setVisible(True)
            self.bloat_progress.setValue(0)
            
            self.current_worker = OptimizationWorker("remove_bloatware", self.optimizer, {'items_to_remove': apps_to_remove})
            self.current_worker.progress.connect(self.on_bloat_progress)
            self.current_worker.finished.connect(self.on_bloat_remove_finished)
            self.current_worker.start()
    
    def on_bloat_remove_finished(self, success, summary):
        """Handle bloatware removal completion"""
        self.bloat_progress.setVisible(False)
        self.status_bar.showMessage(summary)
        
        if success:
            QMessageBox.information(self, "Completado", summary)
            self.scan_bloatware()  # Rescan
        
        self.current_worker = None
    
    # Junk cleaner methods
    @pyqtSlot()
    def scan_junk(self):
        """Scan for junk files"""
        if self.current_worker:
            return
        
        self.junk_progress.setVisible(True)
        self.junk_progress.setValue(0)
        self.junk_log.clear()
        
        self.current_worker = OptimizationWorker("scan_junk", self.optimizer)
        self.current_worker.progress.connect(self.on_junk_progress)
        self.current_worker.finished.connect(self.on_junk_scan_finished)
        self.current_worker.start()
    
    def on_junk_progress(self, value, message):
        """Handle junk scan progress"""
        self.junk_progress.setValue(value)
        self.status_bar.showMessage(message)
        self.junk_log.append(message)
    
    def on_junk_scan_finished(self, success, summary):
        """Handle junk scan completion"""
        self.junk_progress.setVisible(False)
        self.status_bar.showMessage(summary)
        self.junk_log.append(f"\n✓ {summary}")
        
        if success and self.current_worker:
            self.junk_data = self.current_worker.task_data
            junk_size = self.junk_data.get('total_size', 0)
            junk_count = len(self.junk_data.get('junk_items', []))
            
            self.junk_info_label.setText(
                f"📊 Archivos encontrados: {junk_count} | Espacio a liberar: {format_bytes(junk_size)}"
            )
            
            self.clean_junk_btn.setEnabled(junk_count > 0 and self.is_admin)
        
        self.current_worker = None
    
    @pyqtSlot()
    def clean_junk(self):
        """Clean junk files"""
        if not self.is_admin:
            QMessageBox.warning(self, "Permiso Denegado", "Se requieren privilegios de administrador.")
            return
        
        reply = QMessageBox.warning(
            self,
            "Confirmar Limpieza",
            "¿Estás seguro de eliminar todos los archivos temporales?\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.junk_progress.setVisible(True)
            self.junk_progress.setValue(0)
            
            self.current_worker = OptimizationWorker("clean_junk", self.optimizer, self.junk_data)
            self.current_worker.progress.connect(self.on_junk_progress)
            self.current_worker.finished.connect(self.on_junk_clean_finished)
            self.current_worker.start()
    
    def on_junk_clean_finished(self, success, summary):
        """Handle junk cleaning completion"""
        self.junk_progress.setVisible(False)
        self.status_bar.showMessage(summary)
        self.junk_log.append(f"\n✓ {summary}")
        
        if success:
            QMessageBox.information(self, "Completado", summary)
            self.junk_info_label.setText("✓ Limpieza completada")
            self.clean_junk_btn.setEnabled(False)
        
        self.current_worker = None
    
    # Services methods
    @pyqtSlot()
    def scan_services(self):
        """Scan Windows services"""
        if self.current_worker:
            return
        
        self.services_progress.setVisible(True)
        self.services_progress.setValue(0)
        self.services_list.clear()
        
        self.current_worker = OptimizationWorker("scan_services", self.optimizer)
        self.current_worker.progress.connect(self.on_services_progress)
        self.current_worker.finished.connect(self.on_services_scan_finished)
        self.current_worker.start()
    
    def on_services_progress(self, value, message):
        """Handle services scan progress"""
        self.services_progress.setValue(value)
        self.status_bar.showMessage(message)
    
    def on_services_scan_finished(self, success, summary):
        """Handle services scan completion"""
        self.services_progress.setVisible(False)
        self.status_bar.showMessage(summary)
        
        if success and self.current_worker:
            self.services_data = self.current_worker.task_data
            optimizable_services = self.services_data.get('optimizable_services', [])
            
            for service in optimizable_services:
                safe_icon = "✓" if service.get('safe_for_gaming', True) else "⚠️"
                item = QListWidgetItem(
                    f"{safe_icon} {service['name']} - {service.get('description', '')} "
                    f"[{service.get('status', 'Unknown')}]"
                )
                item.setCheckState(Qt.Checked if service.get('safe_for_gaming', False) else Qt.Unchecked)
                item.setData(Qt.UserRole, service)
                self.services_list.addItem(item)
            
            self.optimize_services_btn.setEnabled(len(optimizable_services) > 0 and self.is_admin)
        
        self.current_worker = None
    
    @pyqtSlot()
    def optimize_services(self):
        """Optimize selected services"""
        if not self.is_admin:
            QMessageBox.warning(self, "Permiso Denegado", "Se requieren privilegios de administrador.")
            return
        
        # Get selected services
        services_to_optimize = []
        for i in range(self.services_list.count()):
            item = self.services_list.item(i)
            if item.checkState() == Qt.Checked:
                services_to_optimize.append(item.data(Qt.UserRole))
        
        if not services_to_optimize:
            QMessageBox.information(self, "Sin Selección", "No hay servicios seleccionados para optimizar.")
            return
        
        reply = QMessageBox.warning(
            self,
            "Confirmar Optimización",
            f"¿Estás seguro de optimizar {len(services_to_optimize)} servicios?\n\n"
            "Los servicios serán detenidos y deshabilitados.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.services_progress.setVisible(True)
            self.services_progress.setValue(0)
            
            self.current_worker = OptimizationWorker("optimize_services", self.optimizer, {'services_to_optimize': services_to_optimize})
            self.current_worker.progress.connect(self.on_services_progress)
            self.current_worker.finished.connect(self.on_services_optimize_finished)
            self.current_worker.start()
    
    def on_services_optimize_finished(self, success, summary):
        """Handle services optimization completion"""
        self.services_progress.setVisible(False)
        self.status_bar.showMessage(summary)
        
        if success:
            QMessageBox.information(self, "Completado", summary)
            self.scan_services()  # Rescan
        
        self.current_worker = None
    
    # Gaming mode methods
    @pyqtSlot()
    def apply_gaming_mode(self):
        """Apply gaming mode optimizations"""
        if not self.is_admin:
            QMessageBox.warning(self, "Permiso Denegado", "Se requieren privilegios de administrador.")
            return
        
        reply = QMessageBox.question(
            self,
            "Aplicar Modo Gaming",
            "¿Deseas aplicar las optimizaciones para gaming?\n\n"
            "Esto modificará configuraciones del sistema.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.gaming_progress.setVisible(True)
            self.gaming_progress.setValue(0)
            self.gaming_log.clear()
            
            self.current_worker = OptimizationWorker("gaming_mode", self.optimizer)
            self.current_worker.progress.connect(self.on_gaming_progress)
            self.current_worker.finished.connect(self.on_gaming_finished)
            self.current_worker.start()
    
    def on_gaming_progress(self, value, message):
        """Handle gaming mode progress"""
        self.gaming_progress.setValue(value)
        self.status_bar.showMessage(message)
        self.gaming_log.append(message)
    
    def on_gaming_finished(self, success, summary):
        """Handle gaming mode completion"""
        self.gaming_progress.setVisible(False)
        self.status_bar.showMessage(summary)
        self.gaming_log.append(f"\n✓ {summary}")
        
        if success:
            QMessageBox.information(self, "Completado", "Modo gaming aplicado exitosamente!")
        
        self.current_worker = None


def main(args):
    """Main application entry point"""
    app = QApplication(args)
    app.setApplicationName("AntiSlax")
    app.setOrganizationName("influent")
    
    # Set application font
    # Set application font
    font = QFont("Roboto", 9)
    font.setStyleStrategy(QFont.PreferAntialias)
    # Fallback to Arial if Roboto is not available
    if not font.exactMatch():
        font = QFont("Arial", 9)
    app.setFont(font)
    
    # Create and show main window
    window = AntiSlaxWindow()
    window.show()
    
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
