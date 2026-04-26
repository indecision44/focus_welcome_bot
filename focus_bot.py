from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from aiohttp import web
import random
import datetime
import os
import sys
import asyncio

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set")

def get_welcome_keyboard():
    keyboard = [
        [InlineKeyboardButton("📅 Расписание", callback_data='schedule')],
        [InlineKeyboardButton("🎒 Что взять", callback_data='what_to_take')],
        [InlineKeyboardButton("📍 Где находимся", callback_data='news')],
    ]
    return InlineKeyboardMarkup(keyboard)

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

MANDATORY_GREETING = "📢 Добро пожаловать в чат Focus!🔴🔵⚪️\n\nFocus — это энергичные групповые тренировки по 45 минут с постоянно обновляющимися программами, сочетанием силы, кардио и сильной командной атмосферой. Каждое занятие - новый формат, чтобы тело постоянно прогрессировало.\n\n📎В закреплённых сообщениях — важная информация.\n\nЕсли ты здесь впервые - записывайся на свою первую бесплатную тренировку (Вкладка «📅Расписание») и почувствуй формат на практике🔥"

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

async def track_gym_members(update: Update, context):
    if update.message and update.message.new_chat_members:
        for user in update.message.new_chat_members:
            if not user.is_bot:
                greeting = random.choice(GREETINGS).format(name=user.first_name)
                await update.message.reply_text(greeting)
                await update.message.reply_text(MANDATORY_GREETING)
    if update.message and update.message.left_chat_member:
        user = update.message.left_chat_member
        if not user.is_bot:
            farewell = random.choice(FAREWELLS).format(name=user.first_name)
            await update.message.reply_text(farewell)

async def test_join(update: Update, context):
    test_name = "ТестовыйНовичок"
    await update.message.reply_text("🧪 **ТЕСТ ВХОДА**\nИмитирую появление нового участника...")
    greeting = random.choice(GREETINGS).format(name=test_name)
    await update.message.reply_text(greeting)
    await update.message.reply_text(MANDATORY_GREETING)
    await update.message.reply_text(f"👋 {test_name}, что тебя интересует?", reply_markup=get_welcome_keyboard())

async def test_leave(update: Update, context):
    test_name = "ТестовыйНовичок"
    await update.message.reply_text("🧪 **ТЕСТ ВЫХОДА**\nИмитирую уход участника...")
    farewell = random.choice(FAREWELLS).format(name=test_name)
    await update.message.reply_text(farewell)

# ========== Webhook обработчик для aiohttp ==========
async def webhook(request):
    """Принимает JSON от Telegram и передаёт в приложение бота"""
    try:
        data = await request.json()
        # Создаём объект Update из JSON
        update = Update.de_json(data, bot_application.bot)
        # Ставим задачу на обработку в фоне (чтобы не блокировать ответ)
        asyncio.create_task(bot_application.process_update(update))
        return web.Response(text="OK")
    except Exception as e:
        print(f"Ошибка webhook: {e}")
        return web.Response(text="Error", status=500)

async def health(request):
    return web.Response(text="OK")

# Глобальная переменная для приложения бота
bot_application = None

async def main():
    global bot_application
    bot_application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    bot_application.add_handler(MessageHandler(filters.StatusUpdate.ALL, track_gym_members))
    bot_application.add_handler(CommandHandler("test1", test_join))
    bot_application.add_handler(CommandHandler("test2", test_leave))
    
    await bot_application.initialize()
    await bot_application.start()
    
    # Устанавливаем webhook
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "https://focus-welcome-bot.onrender.com")
    webhook_url = f"{render_url}/webhook/{TOKEN}"
    await bot_application.bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")
    
    # Запускаем aiohttp сервер
    app = web.Application()
    app.router.add_post(f"/webhook/{TOKEN}", webhook)
    app.router.add_get("/health", health)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8080)))
    await site.start()
    print("🚀 Бот запущен и слушает webhook")
    
    # Держим сервер запущенным
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

    
    # 1. Проверить, какие файлы изменились/добавились
    #git status

    # 2. Добавить все файлы в отслеживаемые
    #git add .

    # Или только конкретные файлы:
    #git add focus_bot.py requirements.txt Dockerfile

    # 3. Создать коммит с описанием изменений
    #git commit -m "Добавил Dockerfile и обновил бота"

    # 4. Отправить на GitHub
    #git push