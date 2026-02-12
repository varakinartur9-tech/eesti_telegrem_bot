import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from data import WORDS, TEXTS
from database import cursor, conn

TOKEN = "8546815504:AAGtgAQYKV8QZU4NebQdL6qc7abR_H1iTww"