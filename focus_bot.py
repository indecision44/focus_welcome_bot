import sys
print("=== БОТ НАЧИНАЕТ ЗАГРУЗКУ ===", flush=True)

from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from aiohttp import web
import random
import datetime
import os
import asyncio

print("=== ИМПОРТЫ ЗАГРУЖЕНЫ ===", flush=True)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
print(f"Токен установлен: {'ДА' if TOKEN else 'НЕТ'}", flush=True)
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set")

# ==================== КОМАНДЫ ДЛЯ PERSISTENT MENU ====================
async def cmd_schedule(update: Update, context):
    # Ссылка на тему "Расписание" в вашей группе
    # Формат: https://t.me/c/ID_ГРУППЫ/ID_ТЕМЫ
    # ID группы без -100 (например, если ID -1001234567890, то берём 1234567890)
    group_id = "1234567890"  # Замените на ID вашей группы (без -100)
    topic_id = "1"  # Замените на ID темы "Расписание"
    schedule_topic_link = f"https://t.me/c/focus_grushevka/307"
    
    keyboard = [[InlineKeyboardButton("📅 Записаться на тренировку", url=schedule_topic_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📅 Расписание находится на вкладке 📅расписание и обновляется каждую неделю! Бегом записываться🏃🏃🏃!!!\n\n"
        "Если после голосования ваши планы изменились и вы не сможете прийти на тренировку, пожалуйста, отмените свой голос в опросе ❌ (или переголосуйте🔄).\n\n"
        "Это поможет тренеру и нам точнее понимать, сколько человек будет. Спасибо за понимание! 🙌\n\n"
        "⚠️ Важно: не сможете прийти — отмените свой голос в опросе ❌",
        reply_markup=reply_markup
    )

async def cmd_what_to_take(update: Update, context):
    await update.message.reply_text(
        "🎒 Что взять на тренировку:\n"
        "✅ полотенце\n"
        "✅ удобная обувь\n"
        "✅ удобная одежда\n"
        "✅ вода / бутылка для воды\n"
        "✅ хорошее настроение"
    )

async def cmd_location(update: Update, context):
    await update.message.reply_text(
        "📍 Адрес: проспект Дзержинского, 19 (вход с ул.Щорса, 2 этаж - над Белинвестбанком)"
    )

async def cmd_news(update: Update, context):
    # Ссылка на тему "Расписание" в вашей группе
    # Формат: https://t.me/c/ID_ГРУППЫ/ID_ТЕМЫ
    # ID группы без -100 (например, если ID -1001234567890, то берём 1234567890)
    group_id = "1234567890"  # Замените на ID вашей группы (без -100)
    topic_id = "1"  # Замените на ID темы "Расписание"
    news_topic_link = f"https://t.me/c/focus_grushevka/1461"
    
    keyboard = [[InlineKeyboardButton("📢 Ознакомиться с предстоящими мероприятиями", url=news_topic_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📅 Фокус не перестает удивлять и регулярно анонсирует новые мероприятия!!!\n"
        "Интересно, что у нас сейчас по плану?).\n\n",
        reply_markup=reply_markup
    )

async def cmd_training_format(update: Update, context):
    await update.message.reply_text(
        "❤️ Кардио-тренировка.\nЭто тренировка, направленная на развитие выносливости и укрепление сердечно-сосудистой системы. В основе — циклические движения в умеренном или высоком темпе: гребля, велосипед, берпи, выпады и т.д. Кардио ускоряет метаболизм, помогает эффективно сжигать калории и снижает уровень стресса\n\n"
        "💪 Силовая тренировка.\nЭто работа с отягощениями (гантели, штанги, тренажёры, собственный вес) для развития мышечной силы, массы и выносливости. Силовые упражнения стимулируют рост мышц, укрепляют костную ткань, ускоряют обмен веществ и формируют подтянутое, сильное тело. Подходят как для новичков, так и для продвинутых атлетов — важно лишь правильно подобрать нагрузку\n\n"
        "🔄 Гибридная тренировка.\n Это комбинация кардио- и силовых элементов в одном занятии. Цель — развить одновременно выносливость, силу и функциональность. Гибридный формат лежит в основе таких дисциплин, как HYROX/CRACE: Идеальный выбор для тех, кто хочет быть сильным, выносливым и готовым к любым физическим вызовам\n\n"
    )

async def cmd_start(update: Update, context):
    await update.message.reply_text(
        "👋 Добро пожаловать в Focus!\n\n"
        "Используй кнопки в меню слева:\n"
        "• /schedule — Расписание\n"
        "• /what_to_take — Что взять\n"
        "• /location — Где находимся\n"
        "• /news — Новости\n"
        "• /training_format — Новости"
    )

# ==================== ТЕСТОВЫЕ КОМАНДЫ ====================
async def test_join(update: Update, context):
    test_name = "ТестовыйНовичок"
    await update.message.reply_text("🧪 **ТЕСТ ВХОДА**\nИмитирую появление нового участника...")
    greeting = random.choice(GREETINGS).format(name=test_name)
    await update.message.reply_text(greeting)
    await update.message.reply_text(MANDATORY_GREETING)
    await update.message.reply_text(f"👋 {test_name}, используй кнопки в меню слева!")

async def test_leave(update: Update, context):
    test_name = "ТестовыйНовичок"
    await update.message.reply_text("🧪 **ТЕСТ ВЫХОДА**\nИмитирую уход участника...")
    farewell = random.choice(FAREWELLS).format(name=test_name)
    await update.message.reply_text(farewell)

# ==================== ПРИВЕТСТВИЯ ====================
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

MANDATORY_GREETING = "📢 Добро пожаловать в чат Focus!🔴🔵⚪️\n\nFocus — это энергичные групповые тренировки по 45 минут с постоянно обновляющимися программами, сочетанием силы, кардио и сильной командной атмосферой. Каждое занятие - новый формат, чтобы тело постоянно прогрессировало.\n\n📎В закреплённых сообщениях — важная информация.\n\nЕсли ты здесь впервые - записывайся на свою первую тренировку (Вкладка «📅Расписание») - и почувствуй наш формат на практике🔥"

FAREWELLS = [
    "👋 {name}, надеюсь, ты вернешься! Тренировки ждут.",
    "😢 {name} покинул зал... Всегда рады видеть снова!",
    "💪 {name} ушел, но сила осталась с нами. Возвращайся!",
    "🏃 {name} убежал дожимать? Ждем обратно с новыми рекордами!",
    "🕐 {name} закончил тренировку. Отличная работа!",
    "👋 {name}, не забывай — зал всегда открыт для тебя.",
    "🤝 {name}, до новых встреч! Пусть мышцы отдыхают.",
    "💪 {name} вышел, но его результаты остаются в чате.",
    "🔥 {name}, хорошего восстановления! Ждем снова.",
    "✅ {name}, тренировка завершена. Молодец!"
]

# ==================== ОТСЛЕЖИВАНИЕ УЧАСТНИКОВ ====================
async def track_gym_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for user in update.message.new_chat_members:
            if not user.is_bot:
                greeting = random.choice(GREETINGS).format(name=user.first_name)
                await update.message.reply_text(greeting)
                await update.message.reply_text(MANDATORY_GREETING)

                bot_username = (await context.bot.get_me()).username
                keyboard = [[InlineKeyboardButton("🔵 Начать общение", url=f"https://t.me/{bot_username}")]]
                await update.message.reply_text(
                    f"👋 {user.first_name}, нажми на кнопку ниже, чтобы открыть чат со мной. Я могу рассказать тебе много интересного!",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
    if update.message and update.message.left_chat_member:
        user = update.message.left_chat_member
        if not user.is_bot:
            farewell = random.choice(FAREWELLS).format(name=user.first_name)
            await update.message.reply_text(farewell)

# ==================== PERSISTENT MENU ====================
async def set_persistent_menu(app):
    commands = [
        BotCommand("schedule", "📅 Расписание"),
        BotCommand("what_to_take", "🎒 Что взять"),
        BotCommand("location", "📍 Где находимся"),
        BotCommand("news", "📢 Новости"),
        BotCommand("training_format", "🏋 Формат тренировок"),
    ]
    await app.bot.set_my_commands(commands)
    print("✅ Persistent menu установлен", flush=True)

# ==================== WEBHOOK ====================
async def webhook(request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot_application.bot)
        asyncio.create_task(bot_application.process_update(update))
        return web.Response(text="OK")
    except Exception as e:
        print(f"Ошибка webhook: {e}")
        return web.Response(text="Error", status=500)

async def health(request):
    return web.Response(text="OK")

bot_application = None

async def main():
    global bot_application
    print("=== ЗАПУСК MAIN ===", flush=True)
    
    bot_application = Application.builder().token(TOKEN).build()
    
    # Устанавливаем persistent menu
    await set_persistent_menu(bot_application)
    
    # Добавляем обработчики
    bot_application.add_handler(MessageHandler(filters.StatusUpdate.ALL, track_gym_members))
    bot_application.add_handler(CommandHandler("test1", test_join))
    bot_application.add_handler(CommandHandler("test2", test_leave))
    bot_application.add_handler(CommandHandler("start", cmd_start))
    bot_application.add_handler(CommandHandler("schedule", cmd_schedule))
    bot_application.add_handler(CommandHandler("what_to_take", cmd_what_to_take))
    bot_application.add_handler(CommandHandler("location", cmd_location))
    bot_application.add_handler(CommandHandler("news", cmd_news))
    bot_application.add_handler(CommandHandler("training_format", cmd_training_format))
    
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

    # 5. Комментарий
    #Закомментировать: Ctrl + K, Ctrl + C (сначала зажать Ctrl+K, затем не отпуская Ctrl, нажать C)
    #Раскомментировать: Ctrl + K, Ctrl + U