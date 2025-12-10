import os
import logging
import traceback
import time
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from database import Database
# CAMBIO AQUÍ: Importamos la función de barras en lugar de la de torta
from utils import generate_bar_chart 

# --- CONFIGURACIÓN ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
# TOKEN = os.environ.get("TELEGRAM_TOKEN", "TU_TOKEN_AQUI")

DB_PATH = os.getenv("DB_NAME", "data/finance.db")
db = Database(DB_PATH)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
user_chart_cooldowns = {} 

# --- MENÚS ---
def get_persistent_menu():
    keyboard = [
        [KeyboardButton("📉 Registrar Gasto"), KeyboardButton("📈 Registrar Ingreso")],
        [KeyboardButton("📊 Ver Balance"), KeyboardButton("📂 Ver Carpetas")], 
        [KeyboardButton("⚡ Rápido $500"), KeyboardButton("📥 Exportar Excel")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

def get_balance_keyboard():
    keyboard = [
        [InlineKeyboardButton("🗑️ Borrar Último Movimiento", callback_data='undo_last')],
        [InlineKeyboardButton("📊 Ver Gráfico", callback_data='show_chart')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    keyboard = [[InlineKeyboardButton("❌ Cerrar", callback_data='delete_msg')]]
    return InlineKeyboardMarkup(keyboard)

# --- COMANDOS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 *Hola {user}*\n\n¡Bot reiniciado! Listo para graficar.",
        parse_mode='Markdown', 
        reply_markup=get_persistent_menu()
    )

# --- LÓGICA DE TRANSACCIONES ---
async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("❌ Escribe: `/gasto 500 comida`", parse_mode='Markdown')
            return
        amount = float(args[0])
        category = " ".join(args[1:])
        user_id = update.effective_user.id
        
        db.add_transaction(user_id, 'expense', amount, category, "")
        total_today = db.get_daily_total(user_id)
        
        msg = f"✅ *Gasto: ${amount:,.0f}* ({category.capitalize()})\n📉 Total hoy: ${total_today:,.0f}"
        await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_balance_keyboard())
        
    except ValueError:
        await update.message.reply_text("❌ El monto debe ser un número.")

async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("❌ Escribe: `/ingreso 1000 sueldo`", parse_mode='Markdown')
            return
        amount = float(args[0])
        category = " ".join(args[1:])
        
        db.add_transaction(update.effective_user.id, 'income', amount, category, "")
        msg = f"🎉 *Ingreso: ${amount:,.0f}* ({category.capitalize()})"
        await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_balance_keyboard())

    except ValueError:
        await update.message.reply_text("❌ El monto debe ser un número.")

# --- MANEJADOR DE MENSAJES ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    try:
        if text == "📉 Registrar Gasto":
            await update.message.reply_text("📉 Escribe `/gasto` + monto + carpeta\nEj: `/gasto 1200 super`", parse_mode='Markdown')

        elif text == "📈 Registrar Ingreso":
            await update.message.reply_text("📈 Escribe `/ingreso` + monto + fuente\nEj: `/ingreso 50000 sueldo`", parse_mode='Markdown')

        elif text == "⚡ Rápido $500":
            db.add_transaction(user_id, 'expense', 500, 'Varios', 'Gasto Rápido')
            await update.message.reply_text("⚡ ¡Listo! -$500 en Varios.", reply_markup=get_balance_keyboard())

        elif text == "📊 Ver Balance":
            income, expense = db.get_balance(user_id)
            income = income or 0
            expense = expense or 0
            total = income - expense
            
            if total >= 0:
                status_text = f"💚 A Favor: ${total:,.0f}"
            else:
                status_text = f"⚠️ Déficit: ${abs(total):,.0f}" 
            
            msg = (
                f"🏦 *Estado Financiero*\n\n"
                f"{status_text}\n"
                f"──────────────\n"
                f"📈 Ingresos: ${income:,.0f}\n"
                f"📉 Gastos:   ${expense:,.0f}"
            )
            await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_balance_keyboard())

        elif text == "📂 Ver Carpetas":
            categories = db.get_categories_summary(user_id)
            if not categories:
                await update.message.reply_text("📭 No tienes carpetas de gastos aún.")
            else:
                msg = "📂 *Tus Carpetas de Gastos:*\n\n"
                for cat, amount in categories:
                    msg += f"📁 *{cat.capitalize()}:* ${amount:,.0f}\n"
                await update.message.reply_text(msg, parse_mode='Markdown')

        elif text == "📥 Exportar Excel":
            await update.message.reply_text("📎 Creando archivo...")
            csv_file = db.export_to_csv(user_id)
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=csv_file,
                filename=f"mis_finanzas.csv",
                caption="Aquí tienes tus datos para Excel 📊"
            )

        else:
            await update.message.reply_text("🤔 Usa el menú de abajo.", reply_markup=get_persistent_menu())

    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
        await update.message.reply_text("⚠️ Ocurrió un error.")

# --- MANEJADOR DE BOTONES ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id

    if query.data == 'delete_msg':
        await query.message.delete()

    elif query.data == 'undo_last':
        success = db.delete_last_transaction(user_id)
        if success:
            await query.message.reply_text("🗑️ *Último movimiento borrado.*", parse_mode='Markdown')
        else:
            await query.message.reply_text("❌ No hay nada para borrar.")

    elif query.data == 'show_chart':
        # Rate Limit
        current_time = time.time()
        last_request = user_chart_cooldowns.get(user_id, 0)
        if current_time - last_request < 5:
            await query.message.reply_text("⏳ Espera unos segundos...")
            return
        
        user_chart_cooldowns[user_id] = current_time
        await query.message.edit_text("🎨 Pintando gráfico...")
        
        data = db.get_data_for_chart(user_id)
        if not data:
            await query.message.edit_text("📉 Sin datos para graficar.", reply_markup=get_back_keyboard())
        else:
            # CAMBIO AQUÍ: Llamamos a generate_bar_chart en lugar de pie_chart
            photo = generate_bar_chart(data)
            await query.message.delete()
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=photo,
                caption="📊 *Tus Gastos por Categoría*",
                parse_mode='Markdown',
                reply_markup=get_back_keyboard()
            )

def main():
    if not TOKEN:
        print("❌ ERROR: No hay Token.")
        return

    print("🚀 PocketFlow 6.1 (Gráfico de Barras) Iniciando...")
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler(["gasto", "addexpense"], add_expense))
    application.add_handler(CommandHandler(["ingreso", "addincome"], add_income))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()