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
    