# -*- coding: utf-8 -*-
"""
Telegram-бот "Arabic & Quran Learning Bot"
Функции:
  - Выбор языка интерфейса: Русский / O'zbek / العربية
  - Изучение арабского алфавита (28 букв, транслитерация, произношение)
  - Кнопка "Читать Коран" -> https://alqurankarim.net/
  - Кнопка "Учиться с учителями" -> 3 ссылки:
        https://alquran.uz/en/
        https://ummah.su/quran/slushat/ayman-suveyd
        https://qurancentral.com/audio/yasser-al-dossari
  - Кнопка "История Корана" -> текст об истории ниспослания Корана
  - Кнопка "Онлайн учитель" -> 

Установка:
    pip install python-telegram-bot --upgrade

Запуск:
    1. Получите токен у @BotFather в Telegram
    2. Вставьте токен в переменную BOT_TOKEN ниже (или задайте переменную окружения BOT_TOKEN)
    3. python quran_arabic_bot.py
"""

import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==================== НАСТРОЙКИ ====================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8816549688:AAF6mI0ud79hYCbaDUjvnjYtwUHcf6LRNG4")

QURAN_READ_URL = "https://alqurankarim.net/"
TEACHER_LINKS = [
    ("📗 alquran.uz — уроки и учителя", "https://alquran.uz/en/"),
    ("🎧 Айман Сувейд (аудио)", "https://ummah.su/quran/slushat/ayman-suveyd"),
    ("🎧 Ясер ад-Доссари (аудио)", "https://qurancentral.com/audio/yasser-al-dossari"),
]
ONLINE_TEACHER_PHONE = ""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== ТЕКСТЫ / ПЕРЕВОДЫ ====================

TEXTS = {
    "ru": {
        "choose_lang": "🌍 Выберите язык интерфейса:",
        "welcome": (
            "Ассаляму алейкум! 👋\n\n"
            "Добро пожаловать в бота для изучения арабского языка и Корана.\n"
            "Выберите, что вас интересует:"
        ),
        "btn_alphabet": "🔤 Алфавит арабского языка",
        "btn_read_quran": "📖 Читать Коран",
        "btn_teachers": "👨‍🏫 Учиться с учителями",
        "btn_history": "📜 История Корана",
        "btn_online_teacher": "☎️ Онлайн учитель",
        "btn_back": "⬅️ Назад в меню",
        "btn_change_lang": "🌍 Сменить язык",
        "read_quran_text": (
            "📖 Нажмите на кнопку ниже, чтобы открыть Коран на сайте alqurankarim.net"
        ),
        "teachers_text": (
            "👨‍🏫 Ниже вы найдёте сайты и аудиозаписи для обучения чтению Корана "
            "с преподавателями и известными чтецами:"
        ),
        "online_teacher_text": (
            "☎️ Покачто У нас Нету Онлайн Учителя Скоро Пояавится Учитель:\n\n"
            f"{ONLINE_TEACHER_PHONE}"
        ),
        "history_title": "📜 История ниспослания Корана",
        "history_text": (
            "Первое откровение: Мухаммед получил первые аяты в возрасте 40 лет "
            "в пещере Хира близ Мекки. Это были первые стихи суры «Аль-Аляк».\n\n"
            "• Продолжительность: Текст ниспосылался частями на протяжении 23 лет.\n"
            "• Способы фиксации: Пророк зачитывал откровения сподвижникам, которые "
            "учили их наизусть или записывали на подручных материалах (костях, "
            "пергаменте, пальмовых листьях, камнях).\n"
            "• Разделение: Текст делится на две хронологические группы: мекканские "
            "суры (до переселения в Медину) и мединские суры (после переселения)."
        ),
        "alphabet_title": "🔤 Арабский алфавит (28 букв)",
        "alphabet_footer": "\nНажмите «Назад», чтобы вернуться в меню.",
    },
    "uz": {
        "choose_lang": "🌍 Interfeys tilini tanlang:",
        "welcome": (
            "Assalomu alaykum! 👋\n\n"
            "Arab tili va Qur'onni o'rganish botiga xush kelibsiz.\n"
            "Nima bilan qiziqasiz?"
        ),
        "btn_alphabet": "🔤 Arab alifbosi",
        "btn_read_quran": "📖 Qur'on o'qish",
        "btn_teachers": "👨‍🏫 Ustozlar bilan o'rganish",
        "btn_history": "📜 Qur'on tarixi",
        "btn_online_teacher": "☎️ Onlayn ustoz",
        "btn_back": "⬅️ Menyuga qaytish",
        "btn_change_lang": "🌍 Tilni o'zgartirish",
        "read_quran_text": (
            "📖 Qur'onni o'qish uchun quyidagi tugmani bosing — alqurankarim.net saytiga o'tasiz."
        ),
        "teachers_text": (
            "👨‍🏫 Quyida Qur'on o'qishni ustozlar va mashhur qorilar yordamida "
            "o'rganish uchun saytlar va audiolar keltirilgan:"
        ),
        "online_teacher_text": (
            "☎️ Xozircha Bizda Online Ustoz Yoq Tez Orada Online Darslar Boladi!:\n\n"
            f"{ONLINE_TEACHER_PHONE}"
        ),
        "history_title": "📜 Qur'onning nozil bo'lish tarixi",
        "history_text": (
            "Birinchi vahiy: Muhammad (s.a.v.) 40 yoshida Makka yaqinidagi Hiro g'orida "
            "birinchi oyatlarni oldilar. Bular «Al-Aloq» surasining dastlabki oyatlari edi.\n\n"
            "• Davomiyligi: Qur'on matni 23 yil davomida bo'lib-bo'lib nozil bo'lgan.\n"
            "• Yozib olinishi: Payg'ambar vahiylarni sahobalariga o'qib bergan, ular esa "
            "ularni yodlab olishgan yoki mavjud materiallarga (suyak, pergament, xurmo "
            "bargi, tosh) yozib qo'yishgan.\n"
            "• Bo'linishi: Matn ikki xronologik guruhga bo'linadi: makkiy suralar "
            "(Madinaga ko'chishdan oldin) va madaniy suralar (ko'chishdan keyin)."
        ),
        "alphabet_title": "🔤 Arab alifbosi (28 harf)",
        "alphabet_footer": "\nMenyuga qaytish uchun «Orqaga» tugmasini bosing.",
    },
    "ar": {
        "choose_lang": "🌍 اختر لغة الواجهة:",
        "welcome": (
            "السلام عليكم! 👋\n\n"
            "مرحبًا بك في بوت تعلّم اللغة العربية والقرآن الكريم.\n"
            "ماذا تريد أن تفعل؟"
        ),
        "btn_alphabet": "🔤 الأبجدية العربية",
        "btn_read_quran": "📖 قراءة القرآن",
        "btn_teachers": "👨‍🏫 التعلّم مع معلمين",
        "btn_history": "📜 تاريخ القرآن",
        "btn_online_teacher": "☎️ معلّم عبر الإنترنت",
        "btn_back": "⬅️ العودة إلى القائمة",
        "btn_change_lang": "🌍 تغيير اللغة",
        "read_quran_text": "📖 اضغط على الزر أدناه لفتح القرآن الكريم عبر موقع alqurankarim.net",
        "teachers_text": (
            "👨‍🏫 فيما يلي مواقع وتسجيلات صوتية لتعلّم قراءة القرآن مع معلمين وقرّاء مشهورين:"
        ),
        "online_teacher_text": (
            f"☎️ للتواصل مع معلّم عبر الإنترنت، اتصل على الرقم:\n\n{ONLINE_TEACHER_PHONE}"
        ),
        "history_title": "📜 تاريخ نزول القرآن الكريم",
        "history_text": (
            "الوحي الأول: تلقّى النبي محمد ﷺ أولى الآيات في سن الأربعين في غار حراء "
            "بالقرب من مكة المكرمة، وكانت هذه أوائل آيات سورة «العلق».\n\n"
            "• المدة: نزل النص على أجزاء على مدى 23 عامًا.\n"
            "• طرق التدوين: كان النبي ﷺ يتلو الوحي على الصحابة الذين كانوا يحفظونه أو "
            "يكتبونه على وسائل بدائية (العظام، الرقوق، سعف النخيل، الحجارة).\n"
            "• التقسيم: يُقسّم النص إلى مجموعتين زمنيتين: السور المكية (قبل الهجرة إلى "
            "المدينة) والسور المدنية (بعد الهجرة)."
        ),
        "alphabet_title": "🔤 الأبجدية العربية (28 حرفًا)",
        "alphabet_footer": "\nاضغط على «رجوع» للعودة إلى القائمة.",
    },
}

# Арабский алфавит: (буква, название буквы, произношение/транслитерация)
ARABIC_ALPHABET = [
    ("ا", "Алиф / Alif / ألف", "a / â"),
    ("ب", "Ба / Bo / باء", "b"),
    ("ت", "Та / To / تاء", "t"),
    ("ث", "Тха / Sa / ثاء", "th (межзубный)"),
    ("ج", "Джим / Jim / جيم", "j / dj"),
    ("ح", "Ха / Ha / حاء", "h (гортанный)"),
    ("خ", "Кха / Xa / خاء", "kh"),
    ("د", "Даль / Dol / دال", "d"),
    ("ذ", "Заль / Zol / ذال", "dh (звонкий th)"),
    ("ر", "Ра / Ro / راء", "r"),
    ("ز", "Зай / Zay / زاي", "z"),
    ("س", "Син / Sin / سين", "s"),
    ("ش", "Шин / Shin / شين", "sh"),
    ("ص", "Сад / Sod / صاد", "s (эмфатический)"),
    ("ض", "Дад / Dod / ضاد", "d (эмфатический)"),
    ("ط", "Та / To' / طاء", "t (эмфатический)"),
    ("ظ", "За / Zo' / ظاء", "z (эмфатический)"),
    ("ع", "Айн / Ayn / عين", "‘ (гортанный звук)"),
    ("غ", "Гайн / G'ayn / غين", "gh (картавое)"),
    ("ف", "Фа / Fa / فاء", "f"),
    ("ق", "Каф / Qof / قاف", "q (глубокое k)"),
    ("ك", "Каф / Kof / كاف", "k"),
    ("ل", "Лям / Lom / لام", "l"),
    ("م", "Мим / Mim / ميم", "m"),
    ("ن", "Нун / Nun / نون", "n"),
    ("ه", "Ха / Ha / هاء", "h"),
    ("و", "Вав / Vav / واو", "w / u"),
    ("ي", "Йа / Ya / ياء", "y / i"),
]


def t(lang: str, key: str) -> str:
    return TEXTS.get(lang, TEXTS["ru"]).get(key, "")


# ==================== КЛАВИАТУРЫ ====================

def language_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        ],
        [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
    ]
    return InlineKeyboardMarkup(keyboard)


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(t(lang, "btn_alphabet"), callback_data="menu_alphabet"),
            InlineKeyboardButton(t(lang, "btn_read_quran"), callback_data="menu_read_quran"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_teachers"), callback_data="menu_teachers"),
            InlineKeyboardButton(t(lang, "btn_history"), callback_data="menu_history"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_online_teacher"), callback_data="menu_online_teacher"),
            InlineKeyboardButton(t(lang, "btn_change_lang"), callback_data="menu_change_lang"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu_back")]]
    )


def read_quran_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📖 alqurankarim.net", url=QURAN_READ_URL)],
            [InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu_back")],
        ]
    )


def teachers_keyboard(lang: str) -> InlineKeyboardMarkup:
    link_buttons = [InlineKeyboardButton(label, url=url) for label, url in TEACHER_LINKS]
    # группируем по 2 кнопки в ряд
    rows = [link_buttons[i:i + 2] for i in range(0, len(link_buttons), 2)]
    rows.append([InlineKeyboardButton(t(lang, "btn_back"), callback_data="menu_back")])
    return InlineKeyboardMarkup(rows)


# ==================== ХЕНДЛЕРЫ ====================

def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "ru")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        TEXTS["ru"]["choose_lang"], reply_markup=language_keyboard()
    )


async def send_main_menu(query_or_message, lang: str, edit: bool = True):
    text = t(lang, "welcome")
    markup = main_menu_keyboard(lang)
    if edit:
        await query_or_message.edit_message_text(text, reply_markup=markup)
    else:
        await query_or_message.reply_text(text, reply_markup=markup)


def build_alphabet_text(lang: str) -> str:
    lines = [t(lang, "alphabet_title"), ""]
    for letter, name, sound in ARABIC_ALPHABET:
        lines.append(f"{letter}  —  {name}  —  [{sound}]")
    lines.append(t(lang, "alphabet_footer"))
    return "\n".join(lines)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- Выбор языка ---
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        context.user_data["lang"] = lang
        await send_main_menu(query, lang, edit=True)
        return

    lang = get_lang(context)

    if data == "menu_back":
        await send_main_menu(query, lang, edit=True)

    elif data == "menu_change_lang":
        await query.edit_message_text(
            TEXTS["ru"]["choose_lang"], reply_markup=language_keyboard()
        )

    elif data == "menu_alphabet":
        await query.edit_message_text(
            build_alphabet_text(lang), reply_markup=back_keyboard(lang)
        )

    elif data == "menu_read_quran":
        await query.edit_message_text(
            t(lang, "read_quran_text"), reply_markup=read_quran_keyboard(lang)
        )

    elif data == "menu_teachers":
        await query.edit_message_text(
            t(lang, "teachers_text"), reply_markup=teachers_keyboard(lang)
        )

    elif data == "menu_history":
        text = f"{t(lang, 'history_title')}\n\n{t(lang, 'history_text')}"
        await query.edit_message_text(text, reply_markup=back_keyboard(lang))

    elif data == "menu_online_teacher":
        await query.edit_message_text(
            t(lang, "online_teacher_text"), reply_markup=back_keyboard(lang)
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ошибка при обработке апдейта:", exc_info=context.error)


def main():
    if BOT_TOKEN == "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН_ОТ_BOTFATHER":
        print(
            "⚠️  Вставьте токен бота в переменную BOT_TOKEN "
            "(или задайте переменную окружения BOT_TOKEN) перед запуском!"
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    print("✅ Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()
