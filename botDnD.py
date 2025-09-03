import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler, filters,
                          ContextTypes, ConversationHandler, CallbackQueryHandler)
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv("config.env")
TOKEN = os.getenv("TELEGRAM_TOKEN")
client = Groq(
    api_key=os.getenv("GROC_TOKEN"),
)
# States for conversation
CHARACTER_NAME, PLAYER_NAME, CHARACTER_LEVEL, CHARACTER_CLASS, CHARACTER_RACE, CHARACTER_BACKGROUND, CHARACTER_ALIGNMENT, END = range(8)
#сохранение истории диалога
dialog_history = [
    {
        "role": "system",
        "user_id": "system",
        "content": "Пиши на русском!",
        }
]
character_history = [
    {
        "user_id": "system",
        "content": ""
    }
]

white_list = [
    # тут будут описаны привелегии, чтоб добавить команды классные
]

# Inline keyboard options
class_options = [
    ["Воин", "Бард", "Варвар", "Волшебник"],
    ["Друид", "Жрец", "Изобретатель", "Колдун"],
    ["Монах", "Паладин", "Плут", "Следопыт"],
    ["Чародей"]
]
alignment_options = [
    ["Хаотично-нейтральное", "Законно-злое", "Нейтрально-злое"],
    ["Нейтральное", "Нейтрально-доброе", "Законно-доброе"],
    ["Законно-нейтральное", "Хаотично-доброе"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the bot and displays the menu."""
    keyboard = [
        ["Создать персонажа D&D", "Информация о классах D&D"],
        ["Информация о расах D&D", "Бестиарий D&D"],
        ["Пообщаться с ботом", "Бот в качестве GameMaster'а (неробит)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Выберите опцию:", reply_markup=reply_markup)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stops the bot."""
    await update.message.reply_text("Бот остановлен. До встречи!")
    await context.application.stop()

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the current conversation."""
    await update.message.reply_text("Процесс отменён.")
    return ConversationHandler.END

async def create_character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiates character creation."""
    await update.message.reply_text("Введите имя вашего персонажа:")
    return CHARACTER_NAME

async def character_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["character_name"] = update.message.text
    await update.message.reply_text("Введите имя игрока:")
    return PLAYER_NAME

async def player_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["player_name"] = update.message.text
    await update.message.reply_text("Введите уровень персонажа (от 1 до 20):")
    
    return CHARACTER_LEVEL

async def character_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level = update.message.text
    if not level.isdigit() or not (1 <= int(level) <= 20):
        await update.message.reply_text("Уровень должен быть числом от 1 до 20. Попробуйте снова:")
        return CHARACTER_LEVEL

    context.user_data["character_level"] = int(level)
    keyboard = [[InlineKeyboardButton(option, callback_data=option) for option in row] for row in class_options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите класс персонажа:", reply_markup=reply_markup)
    return CHARACTER_CLASS

async def character_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["character_class"] = query.data
    await query.edit_message_text("Введите расу персонажа:")
    return CHARACTER_RACE

async def character_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["character_race"] = update.message.text
    await update.message.reply_text("Напишите предысторию персонажа:")
    return CHARACTER_BACKGROUND

async def character_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["character_background"] = update.message.text
    keyboard = [[InlineKeyboardButton(option, callback_data=option) for option in row] for row in alignment_options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите мировоззрение персонажа:", reply_markup=reply_markup)
    return CHARACTER_ALIGNMENT

async def character_alignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["character_alignment"] = query.data
    user_id = query.message.from_user.id  # Используем query.message вместо update.message

    # Finalize character creation
    character = context.user_data
    summary = (f"Персонаж создан!\n\n"
               f"Имя персонажа: {character['character_name']}\n"
               f"Имя игрока: {character['player_name']}\n"
               f"Уровень: {character['character_level']}\n"
               f"Класс: {character['character_class']}\n"
               f"Раса: {character['character_race']}\n"
               f"Предыстория: {character['character_background']}\n"
               f"Мировоззрение: {character['character_alignment']}"
               "Напиши все что не достает персонажу для полного заполнения листа персонажа (https://longstoryshort.app/characters/builder/6777beb2eaf80d45d829699a)"
               "Выбери конкретное оружие и броню, подходящее персонажу, список обычного оружия: https://dnd.su/articles/inventory/147-armor-arms-equipment-tools/"
               "для того чтобы распределить характеристики используй сайт: https://longstoryshort.app/long/character-creation/"
               "для добавления заклинаний воспользуйся этим сайтом: https://dnd.su/spells/, но заклинания ты можешь давать только те, которые подходят персонажу"
               "А так же до думай предисторию которую написал выше"
               "Пиши в таком формате:"
               '''Внешность - 
воспользуйся сайтом: https://longstoryshort.app/srd
Класс - 
Раса -
Архетип - попроси у пользователя архетип если уровень персонажа равен или выше 3
Уровень - 
Имя игрока - 
Имя персонажа - 
Мировозрение - 
Предыстория - этот пункт добавляй, если выбрана какая-то готовая предыстория с сайта: https://dnd.su/backgrounds/
Личность - раздели этот пункт на: Черты, Идеалы, Привязанности, Слабости
Полная предыстория - 
Владение языками - 
Оружие - пиши сколько кубиков надо кидать и какой урон на носит и свойства оружия (пример:Копье 1к6 колющий Свойства: Метательное (дис. 20/60), универсальное (1к8)). 
Броня - У брони указывай класс защиты и щиты тоже дают класс доспеха и счтиаются броней (Колечный КЗ:13) 
Характеристики: указывай значение характеристики а потом модификатор (пример Сила: 8 (-1))
Заклинания - раздели этот пункт на: заговоры, заклинания 1 уровня, 2 уровня (всего уровней заклинаний 9). Для заклинаний n-го уровня так же напиши количество ячеек. Даже если заклинаний n-го уровня нету, но есть ячейки, то напиши это
Умения и способности - здесь должны быть пассивные умения и способности которые дает расса
Владение навыками - 
Материальное имущество - 
Вконце Напиши следующее сообщение: Если у вас 3 уровень или выше, то вам доступны архитипы, перейдите на сайт: https://dnd.su/class/ и сами посмотрите что надо добавить
В тексте не должно быть иноязычных символов, только русские
'''
               )
    character_history.append({
        "user_id": user_id,
        "content": summary
    })
    await generate_text(update, context, summary)


    return ConversationHandler.END

async def generate_text(update: Update, context, character_description=None):
    user_id = update.callback_query.message.from_user.id  # Используем update.callback_query.message

    if character_description:
        # Добавляем описание персонажа в историю диалога
        dialog_history.append({
            "role": "user",
            "user_id": user_id,
            "content": character_description,
        })
    else:
        # Добавляем сообщение пользователя в историю диалога
        dialog_history.append({
            "role": "user",
            "user_id": user_id,
            "content": update.message.text,
        })

    # Фильтрация сообщений для выбранного пользователя
    filtered_dialog_history = [
        message for message in dialog_history if message["user_id"] == user_id or message["user_id"] == "system"
    ]

    # я так понял мы выбираем модель
    models = ["gemma-7b-it", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]
    chat_completion = client.chat.completions.create(
        messages=[{"role": message["role"], "content": message["content"]} for message in filtered_dialog_history],
        model=models[1],
    )

    # тут наша языковая модель выдает ответ
    response = chat_completion.choices[0].message.content

    # Проверяем, что response не пустой
    if not response:
        response = "Извините, я не смог сгенерировать ответ."

    # соответственно добавляем ответ нашей языковой модели в историю диалога
    dialog_history.append({
        "role": "assistant",
        "user_id": user_id,
        "content": response,
    })
    
    # вывод сообщения для пользователя
    await update.callback_query.message.reply_text(response)



async def chat_with_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts chatting with the language model."""
    user_id = update.message.from_user.id
    await update.message.reply_text("Вы начали диалог с ботом. Пишите, и я отвечу.")

    # Переходим в состояние общения с моделью
    context.user_data["in_chat_with_bot"] = True
    return "CHAT"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    """Handles messages while chatting with the bot."""
    if context.user_data.get("in_chat_with_bot"):
        user_message = update.message.text
        # Добавляем пользовательское сообщение в историю диалога
        dialog_history.append({
            "role": "user",
            "user_id": user_id,
            "content": user_message,
        })

        filtered_dialog_history = [
        message for message in dialog_history if message["user_id"] == user_id or message["user_id"] == "system"
        ]

        # Получаем ответ от языковой модели
        chat_completion = client.chat.completions.create(
            messages=[{"role": message["role"], "content": message["content"]} for message in filtered_dialog_history],
            model="llama3-70b-8192",  # Выбираем модель для общения
        )

        response = chat_completion.choices[0].message.content


        # Добавляем ответ модели в историю диалога
        dialog_history.append({
            "role": "assistant",
            "user_id": user_id,
            "content": response,
        })

        # Отправляем ответ пользователю
        await update.message.reply_text(response)
        return "CHAT"

async def cancel_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the chat with the bot."""
    context.user_data["in_chat_with_bot"] = False
    await update.message.reply_text("Вы прекратили общение с ботом.")
    return ConversationHandler.END

async def info_classes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Информация о классах D&D:\n"
        "- Воин: Боец, мастер оружия и тактики.\n"
        "- Бард: Магия музыки и слова.\n"
        "- Волшебник: Использует заклинания для атаки и защиты.\n"
        "- Друид: Хранитель природы, способный менять облик.\n"
        "... и другие. Полный список классов можно найти здесь: https://dnd.su/class/"
    )
    await update.message.reply_text(text)

async def info_races(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Информация о расах D&D:\n"
        "- Человек: Универсальный и гибкий.\n"
        "- Эльф: Ловкий и магический.\n"
        "- Гном: Устойчивый и трудолюбивый.\n"
        "- Полурослик: Маленький, но смелый.\n"
        "... и другие. Полный список рас можно найти здесь: https://dnd.su/race/"
    )
    await update.message.reply_text(text)

async def info_bestiary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Бестиарий D&D:\n"
        "- Гоблин: Мелкий и злой гуманоид.\n"
        "- Дракон: Могущественное и древнее существо.\n"
        "- Бехолдер: Ужасный монстр с множеством глаз.\n"
        "... и другие. Полный список существ можно найти здесь: https://dnd.su/bestiary/"
    )
    await update.message.reply_text(text)

def main():

    CHAT = range(8, 9)

    application = Application.builder().token(TOKEN).build()

    # Conversation handler for character creation
   
    conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Создать персонажа D&D"), create_character),
                  MessageHandler(filters.Regex("Пообщаться с ботом"), chat_with_bot)],  # Добавляем новый entry point
    states={
        CHARACTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, character_name)],
        PLAYER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, player_name)],
        CHARACTER_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, character_level)],
        CHARACTER_CLASS: [CallbackQueryHandler(character_class)],
        CHARACTER_RACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, character_race)],
        CHARACTER_BACKGROUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, character_background)],
        CHARACTER_ALIGNMENT: [CallbackQueryHandler(character_alignment)],
        "CHAT": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],  # Добавляем состояние общения
    },
    fallbacks=[CommandHandler("cancel", cancel_chat)]  # Новый fallback для завершения общения
)
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex("Информация о классах D&D"), info_classes))
    application.add_handler(MessageHandler(filters.Regex("Информация о расах D&D"), info_races))
    application.add_handler(MessageHandler(filters.Regex("Бестиарий D&D"), info_bestiary))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
