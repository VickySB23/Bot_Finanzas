# Bot_Finanzas# 💰 PocketFlow - Bot de Finanzas Personales para Telegram

**PocketFlow** es la solución más rápida y privada para llevar el control de tus gastos directamente desde tu app de mensajería favorita. Sin suscripciones mensuales, sin compartir datos con bancos, 100% tuyo.

## ✨ Características

* 🚀 **Registro ultrarrápido:** `/gasto 250 comida` y listo.
* 📊 **Visualización clara:** Balances y resúmenes semanales con un diseño limpio.
* 🥧 **Gráficos automáticos:** Visualiza en qué gastas tu dinero con un comando.
* 🔒 **Privacidad total:** Tus datos viven en tu propio servidor/bot.
* 💾 **Persistencia:** Base de datos SQLite incluida y fácil de respaldar.

## 🛠️ Instalación Rápida

### Prerrequisitos
* Python 3.9 o superior.
* Un Token de Telegram (consíguelo gratis en @BotFather).

### Pasos

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/pocketflow-bot.git](https://github.com/tu-usuario/pocketflow-bot.git)
    cd pocketflow-bot
    ```

2.  **Crear entorno virtual e instalar dependencias:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configurar:**
    Copia el archivo de ejemplo y añade tu token.
    ```bash
    cp .env.example .env
    # Edita .env con tu editor favorito y pega tu TELEGRAM_TOKEN
    ```

4.  **Ejecutar:**
    ```bash
    python src/bot.py
    ```

## 🐳 Docker (Opcional)

Si prefieres usar Docker, simplemente corre:

```bash
docker build -t pocketflow .
docker run -d --env-file .env pocketflow