# 💰 PocketFlow - Tu Asistente Financiero Personal

PocketFlow es un bot de Telegram profesional diseñado para registrar gastos e ingresos a la velocidad de la luz. Sin suscripciones, sin compartir datos con terceros, 100% privado y tuyo.

## ✨ Características Principales

* 🚀 **Registro Instantáneo:** `/gasto 500 almuerzo` y listo.
* 📊 **Gráficos en Tiempo Real:** Visualiza tu distribución de gastos sin esperar imágenes pesadas.
* 📂 **Sistema de Carpetas:** Agrupa tus gastos automáticamente (Comida, Casa, Ocio...).
* 📥 **Exportable:** Descarga todo tu historial a Excel/CSV con un clic.
* 🛡️ **Modo Pánico:** Opción de "Borrar Todo" protegida para reiniciar tu cuenta.
* 🗑️ **Corrección de Errores:** ¿Te equivocaste? Botón de deshacer inmediato.

## 🛠️ Instalación (En 3 Pasos)

### 1. Preparar
Necesitas tener Python instalado. Clona este repositorio y entra en la carpeta:
```bash
git clone [https://github.com/tu-usuario/pocketflow.git](https://github.com/tu-usuario/pocketflow.git)
cd pocketflow

# En Windows
python -m venv venv
venv\Scripts\activate

# En Mac/Linux
# python3 -m venv venv
# source venv/bin/activate

# Instalar librerías
pip install -r requirements.txt

# Copia el archivo de ejemplo (Windows)
copy .env.example .env

# En Mac/Linux
# cp .env.example .env

#¡Arrancar!
python src/bot.py

