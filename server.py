Александр Р, [07.09.2025 16:25]
# -*- coding: utf-8 -*-
import os
import json
import sqlite3
import time
from datetime import datetime
from flask import Flask, request, abort
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ---------------- Configuration ----------------
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Переменная окружения BOT_TOKEN не установлена. Установи её в Render → Environment.")

DB_PATH = os.environ.get("DB_PATH", "dosha.db")
WEBHOOK_PATH = "/webhook"  # рекомендую ставить webhook на этот путь
# ------------------------------------------------

bot = telebot.TeleBot(TOKEN, parse_mode=None)
app = Flask(__name__)

# ----- Questions (24) -----
QUESTIONS = [
    # 1–8 -> Vata
    "Вы чувствуете приливы энергии утром или легко просыпаетесь?",
    "Часто ли вы испытываете сухость кожи или волос?",
    "Часто ли у вас быстрые перемены настроения?",
    "Есть ли у вас склонность к нервозности или беспокойству?",
    "У вас часто бывает неустойчивый аппетит (то большое, то маленькое)?",
    "Часто ли у вас возникают проблемы со сном (трудно уснуть)?",
    "Часто ли вы худеете при стрессе или легко теряете вес?",
    "Часто ли у вас холодные руки или ноги?",

    # 9–16 -> Pitta
    "Вы легко раздражаетесь или становитесь вспыльчивым?",
    "Легко ли вам переносить жару или вы чувствуете дискомфорт при жаре?",
    "Часто ли у вас сильный голод (регулярный и острый аппетит)?",
    "Есть ли у вас склонность к кислотности/изжоге?",
    "Ваша кожа склонна к покраснениям, прыщам или воспалениям?",
    "Вы энергичны и целенаправленны, но иногда чувствуете перенапряжение?",
    "Часто ли у вас высокая сила воли и критичность по отношению к себе?",
    "Склонны ли вы к частым головным болям напряжения (особенно в жару)?",

    # 17–24 -> Kapha
    "Вы склонны легко набирать вес?",
    "Часто ли вы чувствуете медлительность или вялость?",
    "Есть ли у вас склонность к отёкам?",
    "Ваша кожа обычно мягкая, влажная и холодная на ощупь?",
    "Вы предпочитаете тёплые и сухие условия?",
    "Склонны ли вы к спокойствию и терпению (медленный темп)?",
    "Часто ли у вас сильный и стабильный сон?",
    "Часто ли у вас хорошая выносливость, но медленные реакции?"
]

NUM_QUESTIONS = len(QUESTIONS)
if NUM_QUESTIONS != 24:
    raise RuntimeError("Ожидается ровно 24 вопроса в QUESTIONS.")

# ----- DB helpers -----
def _get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            chat_id INTEGER PRIMARY KEY,
            current_q INTEGER NOT NULL,
            answers TEXT NOT NULL,
            updated_at INTEGER NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            vata INTEGER,
            pitta INTEGER,
            kapha INTEGER,
            result TEXT,
            answers TEXT,
            created_at INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_session(chat_id):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT current_q, answers FROM sessions WHERE chat_id = ?", (chat_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"current_q": row["current_q"], "answers": json.loads(row["answers"])}

def set_session(chat_id, current_q, answers):
    now = int(time.time())
    answers_json = json.dumps(answers, ensure_ascii=False)
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO sessions (chat_id, current_q, answers, updated_at) VALUES (?, ?, ?, ?)",
                (chat_id, current_q, answers_json, now))
    conn.commit()
    conn.close()

def clear_session(chat_id):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

Александр Р, [07.09.2025 16:26]
# -*- coding: utf-8 -*-
import os
import json
import sqlite3
import time
from datetime import datetime
from flask import Flask, request, abort
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ---------------- Configuration ----------------
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Переменная окружения BOT_TOKEN не установлена. Установи её в Render → Environment.")

DB_PATH = os.environ.get("DB_PATH", "dosha.db")
WEBHOOK_PATH = "/webhook"  # рекомендую ставить webhook на этот путь
# ------------------------------------------------

bot = telebot.TeleBot(TOKEN, parse_mode=None)
app = Flask(__name__)

# ----- Questions (24) -----
QUESTIONS = [
    # 1–8 -> Vata
    "Вы чувствуете приливы энергии утром или легко просыпаетесь?",
    "Часто ли вы испытываете сухость кожи или волос?",
    "Часто ли у вас быстрые перемены настроения?",
    "Есть ли у вас склонность к нервозности или беспокойству?",
    "У вас часто бывает неустойчивый аппетит (то большое, то маленькое)?",
    "Часто ли у вас возникают проблемы со сном (трудно уснуть)?",
    "Часто ли вы худеете при стрессе или легко теряете вес?",
    "Часто ли у вас холодные руки или ноги?",

    # 9–16 -> Pitta
    "Вы легко раздражаетесь или становитесь вспыльчивым?",
    "Легко ли вам переносить жару или вы чувствуете дискомфорт при жаре?",
    "Часто ли у вас сильный голод (регулярный и острый аппетит)?",
    "Есть ли у вас склонность к кислотности/изжоге?",
    "Ваша кожа склонна к покраснениям, прыщам или воспалениям?",
    "Вы энергичны и целенаправленны, но иногда чувствуете перенапряжение?",
    "Часто ли у вас высокая сила воли и критичность по отношению к себе?",
    "Склонны ли вы к частым головным болям напряжения (особенно в жару)?",

    # 17–24 -> Kapha
    "Вы склонны легко набирать вес?",
    "Часто ли вы чувствуете медлительность или вялость?",
    "Есть ли у вас склонность к отёкам?",
    "Ваша кожа обычно мягкая, влажная и холодная на ощупь?",
    "Вы предпочитаете тёплые и сухие условия?",
    "Склонны ли вы к спокойствию и терпению (медленный темп)?",
    "Часто ли у вас сильный и стабильный сон?",
    "Часто ли у вас хорошая выносливость, но медленные реакции?"
]

NUM_QUESTIONS = len(QUESTIONS)
if NUM_QUESTIONS != 24:
    raise RuntimeError("Ожидается ровно 24 вопроса в QUESTIONS.")

# ----- DB helpers -----
def _get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            chat_id INTEGER PRIMARY KEY,
            current_q INTEGER NOT NULL,
            answers TEXT NOT NULL,
            updated_at INTEGER NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            vata INTEGER,
            pitta INTEGER,
            kapha INTEGER,
            result TEXT,
            answers TEXT,
            created_at INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_session(chat_id):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT current_q, answers FROM sessions WHERE chat_id = ?", (chat_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"current_q": row["current_q"], "answers": json.loads(row["answers"])}

def set_session(chat_id, current_q, answers):
    now = int(time.time())
    answers_json = json.dumps(answers, ensure_ascii=False)
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO sessions (chat_id, current_q, answers, updated_at) VALUES (?, ?, ?, ?)",
                (chat_id, current_q, answers_json, now))
    conn.commit()
    conn.close()

def clear_session(chat_id):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()