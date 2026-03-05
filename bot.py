import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from data import WORDS, TEXTS
from database import cursor, conn

TOKEN = ""

def menu():
    return ReplyKeyboardMarkup([
        ["📚 Õpi sõnu","📖 Loe teksti"],
        ["📝 Test","➕ Lisa sõna"],
        ["📌 Minu sõnad","📊 Minu statistika"],
        ["🔄 Reset"]
    ], resize_keyboard=True)
    
    # START

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Vali tase:",
        reply_markup=ReplyKeyboardMarkup(
            [["A1","A2"],["B1","B2"]],
            resize_keyboard=True
        )
    )
    
    # LEVEL

async def level(update,context):

    context.user_data.clear()
    context.user_data["level"] = update.message.text

    await update.message.reply_text(
        "Vali suund:",
        reply_markup=ReplyKeyboardMarkup(
            [["RU-EE","EE-RU"]],
            resize_keyboard=True
        )
    )
    
async def direction(update,context):

    context.user_data["direction"] = update.message.text

    await update.message.reply_text(
        "Valmis!",
        reply_markup=menu()
    )
    
    # TRANSLATE

def tr(word,direction):
    if direction == "RU-EE":
        return word[1],word[0]
    return word[0],word[1]
