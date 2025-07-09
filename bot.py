from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

TOKEN = os.getenv("TOKEN")

produtos = {
    "btn1": ("Morango do amor", 5.00),
    "btn2": ("Maçã do amor", 4.00),
    "btn3": ("Maçã do amor 3 por 10", 10.00),
    "btn4": ("Bala baiana", 3.00),
    "btn5": ("Caldo de feijão P", 5.00),
    "btn6": ("Caldo de feijão G", 10.00),
    "btn7": ("Caldo de Kenga P", 5.00),
    "btn8": ("Caldo de Kenga G", 10.00),
    "btn9": ("Cachorro quente", 10.00),
    "btn10": ("Cachorro quente + refri", 12.00)
}

somas = {}

def start(update: Update, context: CallbackContext):
    enviar_menu(update.effective_chat.id, context)

def enviar_menu(chat_id, context: CallbackContext):
    botoes = [
        [InlineKeyboardButton(f"{nome} - R$ {valor:.2f}", callback_data=btn_id)]
        for btn_id, (nome, valor) in produtos.items()
    ]
    reply_markup = InlineKeyboardMarkup(botoes)
    context.bot.send_message(chat_id, "🛒 Selecione um produto para registrar a venda:", reply_markup=reply_markup)

def nova_venda(update: Update, context: CallbackContext):
    q = update.callback_query; q.answer()
    enviar_menu(q.message.chat_id, context)

def produto_clicado(update: Update, context: CallbackContext):
    q = update.callback_query; q.answer()
    user = q.from_user.id; pid = q.data
    nome, valor = produtos[pid]
    total = somas.get(user, 0.0) + valor
    somas[user] = total
    texto = f"✅ Venda: *{nome}*\n💰 R$ {valor:.2f}\n📊 Total acumulado: R$ {total:.2f}"
    q.edit_message_text(text=texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Nova venda", callback_data="nova_venda")]
    ]))

def main():
    updater = Updater(TOKEN, use_context=True); dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(produto_clicado, pattern="^btn"))
    dp.add_handler(CallbackQueryHandler(nova_venda, pattern="^nova_venda$"))
    updater.start_polling(); print("Bot rodando..."); updater.idle()

if __name__=="__main__":
    main()
