# Winslax - Optimizador de Rendimiento para Windows

**Winslax** es una herramienta de optimización en PowerShell diseñada para mejorar el rendimiento de su sistema operativo Windows, especialmente para juegos.

Este script realiza las siguientes acciones:

1.  **Eliminación de Bloatware:** Desinstala aplicaciones preinstaladas de la Tienda de Windows (AppX) que no son necesarias y consumen recursos.
2.  **Desactivación de Telemetría:** Deshabilita la recopilación de datos y la telemetría de Windows para proteger su privacidad y reducir la carga del sistema.
3.  **Optimización de Servicios:** Desactiva servicios de Windows innecesarios (Modo Gamer) que se ejecutan en segundo plano y consumen CPU/RAM.
4.  **Ajustes de Rendimiento:** Configura el plan de energía en "Alto Rendimiento" y desactiva la hibernación para liberar espacio en disco.

## Uso

1.  Descargue el repositorio completo.
2.  Haga clic derecho en el archivo `Lanzar_Winslax.bat` y seleccione **"Ejecutar como administrador"**.
3.  El script de PowerShell (`Winslax.ps1`) se ejecutará automáticamente, aplicando las optimizaciones.
4.  Al finalizar, se le preguntará si desea reiniciar el sistema para aplicar todos los cambios.

**ADVERTENCIA:** Este script realiza cambios en el sistema operativo. Úselo bajo su propia responsabilidad. Se recomienda crear un punto de restauración del sistema antes de ejecutarlo.

## Contenido del Repositorio

*   `Winslax.ps1`: El script principal de optimización en PowerShell.
*   `Lanzar_Winslax.bat`: Archivo de lote para ejecutar `Winslax.ps1` con permisos de administrador.
*   `README.md`: Este archivo.
