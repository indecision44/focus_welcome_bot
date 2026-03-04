from telegram.ext import Application, MessageHandler, filters, CommandHandler
import random
import datetime

TOKEN = '8549484882:AAFr6klJedHwGZJnCeE60fsaccI8cNS7CLQ'

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
    "🏋️ {name} в строю! Ждем новых рекордов!",
    "🔥 Еще один боец в строю! Привет, {name}!",
    "🦾 {name} зашел! Разминайся, начинаем!",
    "🌟 {name} с нами! Цель вижу - препятствий нет!",
    "⚡ {name} на месте! Пот будет!",
    "🎯 Привет, {name}! Твои мышцы уже ждут тренировки!"
]

MANDATORY_GREETING = "📢 Добро пожаловать в чат Фокус!🔴🔵⚪️\n\nФокус  — это энергичные групповые тренировки по 45 минут с постоянно обновляющимися программами, сочетанием силы, кардио и сильной командной атмосферой.Каждое занятие - новый формат, чтобы тело постоянно прогрессировало.\n\n📎В закреплённых сообщениях — важная информация.\n\nЕсли ты здесь впервые - записывайся на свою первую бесплатную тренировку (Вкладка «📅Расписание») и почувствуй формат на практике🔥"

# Прощальные сообщения
FAREWELLS = [
    "👋 {name} покинул зал. До следующей тренировки!",
    "🏃 {name} убежал. Завтра ждем обратно!",
    "💨 {name} слился... Шучу, до встречи!",
    "😢 Без {name} зал опустел... Ладно, тренируемся дальше!"
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
                
                # 2. ОБЯЗАТЕЛЬНОЕ сообщение (ВОТ ЭТО ДОБАВИТЬ!)
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