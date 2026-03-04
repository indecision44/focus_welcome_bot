from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import random
import datetime

TOKEN = '8549484882:AAFr6klJedHwGZJnCeE60fsaccI8cNS7CLQ'

def get_welcome_keyboard():
#Создает клавиатуру с кнопками
    keyboard = [
        [InlineKeyboardButton("📅 Расписание", callback_data='schedule')],
        [InlineKeyboardButton("🎒 Что взять", callback_data='what_to_take')],
        [InlineKeyboardButton("📰 Новости", callback_data='news')],
    ]
    return InlineKeyboardMarkup(keyboard)

######################
#ТЕСТОВЫЕ КОМАНДЫ OPEN
######################

async def test_join(update, context):
    """Имитирует вход нового участника"""
    test_name = "ТестовыйНовичок"
    
    await update.message.reply_text("🧪 **ТЕСТ ВХОДА**\nИмитирую появление нового участника...")
    
    greeting = random.choice(GREETINGS).format(name=test_name)
    await update.message.reply_text(greeting)
    await update.message.reply_text(MANDATORY_GREETING)
    
    await update.message.reply_text(
        f"👋 {test_name}, что тебя интересует?",
        reply_markup=get_welcome_keyboard()
    )
    
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"🧪 [{time_now}] Тест входа от {update.effective_user.first_name}")

async def test_leave(update, context):
    """Имитирует выход участника"""
    test_name = "ТестовыйНовичок"
    
    await update.message.reply_text("🧪 **ТЕСТ ВЫХОДА**\nИмитирую уход участника...")
    
    farewell = random.choice(FAREWELLS).format(name=test_name)
    await update.message.reply_text(farewell)
    
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"🧪 [{time_now}] Тест выхода от {update.effective_user.first_name}")

######################
#ТЕСТОВЫЕ КОМАНДЫ CLOSE
######################

# Приветствия для спортзала
GREETINGS = [
    "💪 Добро пожаловать в зал, {name}! Сегодня день ног?",
    "💪 Привет, {name}! Сегодня день ног или снова грудь?",
    "🔥 {name} в зале! Угадаю — сегодня бицуха?",
    "🏋️ {name} зашел! Опять день груди пропускать будем?",
    "🦵 {name} с нами! Надеюсь, ты не из тех, кто пропускает ноги",
    "💪 О, {name} пришел! Сегодня жать или приседать?",
    "🔥 {name} в строю! День спины или снова грудь?",
    "🏋️ {name} явился! Что качаем? Только честно)",
    "💪 {name} в зале! Протеин уже развели?",
    "🔥 {name} пришел! Лови гантель, пока не улетела",
    "🦾 {name} с нами! Блины не забудь убрать после подходов",
    "⚡ {name} зашел! Футболочку для селфи погладил?",
    "💪 {name} в деле! Сегодня без читинга?",
    "🔥 {name} явился! Вода в бутылке есть — можно трениться",
    "🏋️ {name} в строю! Полотенце взял? А то текут некоторые",
    "🌟 {name} с нами! Сегодня точно будет рекорд",
    "🎯 {name} в зале! Цель вижу — препятствий нет",
    "💫 {name} пришел! Ждем новых достижений",
    "🔥 {name} в игре! Сегодня ты станешь сильнее",
    "⚡ {name} заряжен на тренировку! Покажи всем",
    "🍗 {name} в зале! Читмил был? Отрабатывать пришел?",
    "🥩 {name} пришел! Курица с гречкой уже ждут",
    "😴 {name} явился! Выспался? Тогда вперед",
    "☕ {name} с нами! Кофеин уже в крови — можно трениться",
    "🍌 {name} зашел! Банан съел? Энергия нужна",
    "🏋️ {name} в строю! Жим лежа 100 уже сегодня?",
    "🦵 {name} пришел! Присед со штангой или на тренажере?",
    "💪 {name} в зале! Бицепс 40 см будет?",
    "🔥 {name} с нами! Становая тяга ждет",
    "🎯 {name} явился! Турник свободен, беги"
]

MANDATORY_GREETING = "📢 Добро пожаловать в чат Focus!🔴🔵⚪️\n\nFocus  — это энергичные групповые тренировки по 45 минут с постоянно обновляющимися программами, сочетанием силы, кардио и сильной командной атмосферой.Каждое занятие - новый формат, чтобы тело постоянно прогрессировало.\n\n📎В закреплённых сообщениях — важная информация.\n\nЕсли ты здесь впервые - записывайся на свою первую бесплатную тренировку (Вкладка «📅Расписание») и почувствуй формат на практике🔥"

# Прощальные сообщения
FAREWELLS = [
    "💪 {name} в игре! Разминайся",
    "🔥 {name} зашел на рекорд!",
    "🏋️ {name} с нами! Ждем новых достижений",
    "🦾 {name} в строю! Покажи, на что способен",
    "⚡ {name} заряжен на тренировку!",
    "🌟 {name} с нами! Сегодня точно будет прогресс",
    "🎯 {name} в деле! Цель вижу — препятствий нет",
    "💫 {name} присоединился! Рабочая атмосфера обеспечена",
    "👊 {name} с нами! Жми лежа, не лежа",
    "🏆 {name} в зале! Новые рекорды уже близко"
]

async def track_gym_members(update, context):
    """Отслеживает входы и выходы в спортзале"""
    
    # Новый участник
    if update.message and update.message.new_chat_members:
        for user in update.message.new_chat_members:
            if not user.is_bot:
                # Выбираем случайное приветствие
                greeting = random.choice(GREETINGS).format(name=user.first_name)
                await update.message.reply_text(greeting)
                
                # ОБЯЗАТЕЛЬНОЕ сообщение (ВОТ ЭТО ДОБАВИТЬ!)
                await update.message.reply_text(MANDATORY_GREETING)

                # Пишем в терминал для статистики
                time_now = datetime.datetime.now().strftime("%H:%M")
                print(f"✅ [{time_now}] {user.first_name} зашел в зал")
    
    # Кто-то вышел
    if update.message and update.message.left_chat_member:
        user = update.message.left_chat_member
        if not user.is_bot:
            farewell = random.choice(FAREWELLS).format(name=user.first_name)
            await update.message.reply_text(farewell)
            time_now = datetime.datetime.now().strftime("%H:%M")
            print(f"👋 [{time_now}] {user.first_name} вышел")

if __name__ == '__main__':
    print("🏋️‍♂️ СПОРТИВНЫЙ БОТ ЗАПУЩЕН")
    print("📅 Жду посетителей спортзала...")
    print("="*40)
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, track_gym_members))
    app.add_handler(CommandHandler("test1", test_join))  # имитация входа
    app.run_polling()