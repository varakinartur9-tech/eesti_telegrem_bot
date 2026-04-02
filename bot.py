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

# ÕPI SÕNU

async def learn(update,context):

    level = context.user_data["level"]
    direction = context.user_data["direction"]

    text = "📚 Sõnad:\n\n"

    for w in WORDS[level]:
        q,a = tr(w,direction)
        text += f"{q} — {a}\n"

    await update.message.reply_text(text)
    
    # TEXT

async def read(update,context):

    await update.message.reply_text(
        TEXTS[context.user_data["level"]]
    )
    
#TEST START
async def test_start(update,context):

    context.user_data["mode"]="test"
    context.user_data["words"]=WORDS[context.user_data["level"]].copy()
    context.user_data["repeat"]={}
    context.user_data["correct"]=0
    context.user_data["wrong"]=0
    context.user_data["mistakes"]=[]

    await next_word(update,context)
async def next_word(update,context):

    if not context.user_data["words"]:
        await test_finish(update,context)
        return

    word=random.choice(context.user_data["words"])
    context.user_data["current"]=word

    q,_=tr(word,context.user_data["direction"])

    await update.message.reply_text(f"Tõlgi: {q}")


async def test_answer(update,context):

    word=context.user_data["current"]
    q,a=tr(word,context.user_data["direction"])

    if update.message.text.lower()==a.lower():
        context.user_data["correct"]+=1
    else:
        context.user_data["wrong"]+=1
        context.user_data["mistakes"].append(f"{q}-{a}")

    count=context.user_data["repeat"].get(word,0)+1
    context.user_data["repeat"][word]=count

    if count>=2:
        context.user_data["words"].remove(word)

    await next_word(update,context)
async def test_finish(update,context):

    correct=context.user_data["correct"]
    wrong=context.user_data["wrong"]

    total=correct+wrong
    percent=int(correct/total*100) if total>0 else 0

    text=f"""Test lõppetud 

Õiged: {correct}
Valed: {wrong}
Tulemus: {percent}%"""

    if context.user_data["mistakes"]:
        text+="Vead:\n"
        for m in context.user_data["mistakes"]:
            text+=m+"\n"

    await update.message.reply_text(text)

    user=update.message.from_user.id

    cursor.execute("SELECT * FROM stats WHERE user_id=?",(user,))
    row=cursor.fetchone()

    if not row:
        cursor.execute("INSERT INTO stats VALUES(?,?,?,?)",
                       (user,1,correct,wrong))
    else:
        cursor.execute(
            "UPDATE stats SET tests=tests+1, correct=correct+?, wrong=wrong+? WHERE user_id=?",
            (correct,wrong,user)
        )

    conn.commit()

    context.user_data["mode"]=None
    
    # ADD WORD

async def add(update,context):

    context.user_data["mode"]="add"
    await update.message.reply_text("Kirjuta sõna")


async def save(update,context):

    user=update.message.from_user.id
    word=update.message.text

    cursor.execute(
        "INSERT INTO my_words VALUES(?,?)",
        (user,word)
    )
    conn.commit()

    await update.message.reply_text("Lisatud")
    context.user_data["mode"]=None
