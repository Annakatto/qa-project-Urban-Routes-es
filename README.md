# Proyecto de Automatización de Pruebas - Urban Routes

## Descripción del Proyecto
Este proyecto es una suite de pruebas automatizadas para la aplicación Urban Routes, que simula la reserva de un taxi. Las pruebas están diseñadas para verificar el flujo completo de reserva, desde la selección de la ruta hasta la confirmación del conductor.

## Tecnologías y Técnicas Utilizadas
- **Lenguaje de programación**: Python
- **Framework de pruebas**: Selenium WebDriver
- **Gestión de dependencias**: pip
- **Control de versiones**: Git
- **Integración continua**: GitHub Actions (opcional)
- **Técnicas**:
  - Patrón Page Object Model (POM) para organizar el código.
  - Uso de `WebDriverWait` para manejar sincronización.
  - Pruebas automatizadas con `pytest`.

## Instrucciones para Ejecutar las Pruebas

### Requisitos Previos
1. **Python**: Asegúrate de tener Python instalado. Puedes descargarlo desde [python.org](https://www.python.org/).
2. **Selenium**: Instala Selenium usando pip:
   ```bash
   pip install selenium
   pip install pytest
   

3. Ejecución de prueba: pytest main.py