import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
)

# Настройка логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
(
    START,
    VAGON_1, CHOICE_1,
    A1, A1_1, A1_2, A2,
    B1, B1_1, B1_2, B2,
    VAGON_2, VAGON_3, VAGON_4, VAGON_5, VAGON_6, VAGON_7,
    FINAL
) = map(str, range(18))

# Данные пользователей
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = update.effective_user.id
    user_data[user_id] = {
        "ticket": False,
        "elena": False,
        "help_others": False,
    }

    keyboard = [
        [InlineKeyboardButton("Выйти из купе", callback_data="exit")],
        [InlineKeyboardButton("Остаться в купе", callback_data="stay")]
    ]

    await update.message.reply_text(
        "🚂 *Вы просыпаетесь в старом вагоне советского поезда.*\n\n"
        "За окном мелькают бесконечные просторы. На сиденье вы находите записку с именем «Алексей». "
        "Вдали виднеется таинственная фигура, машущая рукой.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return VAGON_1


async def vagon_1_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()

    if query.data == "exit":
        keyboard = [
            [InlineKeyboardButton("Поговорить с Анной", callback_data="talk")],
            [InlineKeyboardButton("Идти дальше", callback_data="forward")]
        ]
        await query.edit_message_text(
            "🚪 Вы выходите в коридор и встречаете проводницу Анну.\n\n"
            "«Вы не первый, кто забыл здесь себя», - говорит она, поправляя форменную шляпу.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return CHOICE_1
    else:
        keyboard = [
            [InlineKeyboardButton("Сосредоточиться на женщине", callback_data="woman")],
            [InlineKeyboardButton("Сосредоточиться на вокзале", callback_data="station")]
        ]
        await query.edit_message_text(
            "🛋 Вы остаётесь в купе. Постепенно всплывают обрывки воспоминаний: "
            "женщина... вокзал... билет...",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return B1


async def choice_1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "talk":
        text = (
            "👩✈️ Анна улыбается: «Этот поезд путешествует по памяти пассажиров. "
            "Чтобы выбраться, нужно разобраться в своём прошлом»."
        )

        keyboard = [
            [InlineKeyboardButton("Спросить о себе", callback_data="ask_me")],
            [InlineKeyboardButton("Спросить что делать", callback_data="ask_do")],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return A1

    else:
        text = "🚶 Вы проходите в следующий вагон..."
        await query.edit_message_text(text, parse_mode="Markdown")
        return await vagon_2_handler(update, context)

async def a1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "ask_me":
        text = "👩✈️ Анна: «Я видела вас раньше в вагоне №7. Возможно, там есть ответы»."

        keyboard = [
            [InlineKeyboardButton("Идти в вагон №7", callback_data="vagon7")],
            [InlineKeyboardButton("Сначала осмотреть вагоны 2-6", callback_data="vagon2_6")],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return A1_1

    else:
        text = (
            "👩✈️ Анна советует: «Попробуйте зайти в вагон-ресторан (№5). "
            "Там часто собираются другие пассажиры»."
        )

        keyboard = [
            [InlineKeyboardButton("Послушать совет", callback_data="vagon5")],
            [InlineKeyboardButton("Игнорировать", callback_data="vagon7")],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return A1_2

async def b1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "woman":
        text = "👩 Перед глазами возникает образ женщины. Вы слышите голос: «Алексей, не уезжай!»"

        keyboard = [
            [InlineKeyboardButton("Выйти искать ответы", callback_data="exit_search")],
            [InlineKeyboardButton("Продолжить вспоминать", callback_data="remember_more")],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return B1_1

    else:
        text = (
            "🏚 Вспоминается вокзал. Вы спешили на поезд, но забыли билет. "
            "Кажется, билет - ключ к выходу!"
        )

        keyboard = [
            [InlineKeyboardButton("Искать проводницу", callback_data="find_conductor")],
            [InlineKeyboardButton("Исследовать поезд", callback_data="explore")],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return B2

async def b1_1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "exit_search":
        text = (
            "🚪 Выйдя в коридор, вы сталкиваетесь с незнакомцем.\n\n"
            "«Я Николай. Вы знаете Елену?» - говорит он."
        )

        keyboard = [
            [InlineKeyboardButton("Поговорить с Николаем", callback_data="talk_nik")],
            [InlineKeyboardButton("Пройти мимо", callback_data="ignore")],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return B1_2

    else:
        user_data[user_id]['elena'] = True
        text = (
            "💔 Яркое воспоминание: вы ссоритесь с Еленой. "
            "Она плачет: «Ты обещал вернуться!»\n\n"
            "Теперь понятно, почему вы здесь..."
        )

        keyboard = [
            [InlineKeyboardButton("Срочно найти проводницу", callback_data="find_anna")],
            [InlineKeyboardButton("Идти в вагон-ресторан", callback_data="vagon5")],
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return B1_2

async def vagon_2_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    text = (
        "🧸 *Вагон №2: Детские воспоминания*\n\n"
        "Перед вами ваша детская комната. В углу сидит мальчик - вы в детстве."
    )

    keyboard = [
        [InlineKeyboardButton("Поговорить с мальчиком", callback_data="talk_boy")],
        [InlineKeyboardButton("Осмотреть комнату", callback_data="explore_room")],
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return VAGON_2

async def vagon_3_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    text = (
        "💼 *Вагон №3: Работа и ответственность*\n\n"
        "Офисная обстановка. Перед вами стоит ваш бывший начальник."
    )

    keyboard = [
        [InlineKeyboardButton("Спорить с начальником", callback_data="argue")],
        [InlineKeyboardButton("Выполнить поручение", callback_data="work")],
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return VAGON_3

async def vagon_4_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    text = (
        "🌑 *Вагон №4: Одиночество*\n\n"
        "Темный вагон. Вокруг - силуэты людей, которые вас игнорируют."
    )

    keyboard = [
        [InlineKeyboardButton("Попытаться заговорить", callback_data="talk_people")],
        [InlineKeyboardButton("Заплакать от отчаяния", callback_data="cry")],
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return VAGON_4

async def vagon_5_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    text = (
        "☕ *Вагон-ресторан*\n\n"
        "Здесь собрались другие пассажиры: старик в углу и женщина у окна."
    )

    keyboard = [
        [InlineKeyboardButton("Поговорить со стариком", callback_data="old_man")],
        [InlineKeyboardButton("Поговорить с женщиной", callback_data="woman_rest")],
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return VAGON_5

async def vagon_6_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    text = (
        "🚉 *Станция выбора*\n\n"
        "Поезд остановился. На табличке: «Назад — в прошлое. Вперёд — в будущее»."
    )

    keyboard = [
        [InlineKeyboardButton("Сойти на станции", callback_data="past")],
        [InlineKeyboardButton("Остаться в поезде", callback_data="future")],
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return VAGON_6

async def vagon_7_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data[user_id]['ticket'] = True

    text = (
        "🔑 *Вагон №7: Комната истины*\n\n"
        "Перед вами финальное воспоминание: вы уезжаете, оставляя Елену одну в больнице. "
        "На столе лежит билет с надписью «Домой»."
    )

    keyboard = [
        [InlineKeyboardButton("Взять билет", callback_data="take_ticket")],
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return FINAL

async def final_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = user_data.get(user_id, {})

    if data.get('ticket') and data.get('elena'):
        text = (
            "🌟 *Прощение и возвращение*\n\n"
            "Вы стоите на настоящем вокзале, сжимая билет. "
            "Вдали видите Елену, которая машет вам рукой."
        )
    elif data.get('help_others'):
        text = (
            "👩✈️ *Новая проводница*\n\n"
            "Вы остаётесь в поезде, помогая другим пассажирам. "
            "Теперь вы - часть этого вечного путешествия."
        )
    else:
        text = (
            "🌌 *Вечное путешествие*\n\n"
            "Поезд продолжает движение. За окном мелькают бесконечные пейзажи..."
        )

    await query.edit_message_text(text, parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Игра прервана")
    return ConversationHandler.END

# Все остальные обработчики остаются без изменений (как в предыдущей версии)

def main() -> None:
    application = ApplicationBuilder().token("8068795309:AAEJo__h_FPTfYuBZSxBDLszC8aLNblRXsY").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            'VAGON_1': [CallbackQueryHandler(vagon_1_choice)],
            'CHOICE_1': [CallbackQueryHandler(choice_1_handler)],

            'FINAL': [CallbackQueryHandler(final_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=True  # Важное исправление!
    )

    application.add_handler(conv_handler)
    application.run_polling()

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Игра прервана")
    return ConversationHandler.END


def main() -> None:
    application = ApplicationBuilder().token("8068795309:AAEJo__h_FPTfYuBZSxBDLszC8aLNblRXsY").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            VAGON_1: [CallbackQueryHandler(vagon_1_choice)],
            CHOICE_1: [CallbackQueryHandler(choice_1_handler)],
            A1: [CallbackQueryHandler(a1_handler)],
            A1_1: [CallbackQueryHandler(vagon_7_handler)],
            A1_2: [CallbackQueryHandler(vagon_5_handler)],
            B1: [CallbackQueryHandler(b1_handler)],
            B1_1: [CallbackQueryHandler(b1_1_handler)],
            B1_2: [CallbackQueryHandler(vagon_5_handler)],
            B2: [CallbackQueryHandler(vagon_2_handler)],
            VAGON_2: [CallbackQueryHandler(vagon_3_handler)],
            VAGON_3: [CallbackQueryHandler(vagon_4_handler)],
            VAGON_4: [CallbackQueryHandler(vagon_5_handler)],
            VAGON_5: [CallbackQueryHandler(vagon_6_handler)],
            VAGON_6: [CallbackQueryHandler(vagon_7_handler)],
            VAGON_7: [CallbackQueryHandler(final_handler)],
            FINAL: [CallbackQueryHandler(final_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False  # Ключевой параметр!
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
