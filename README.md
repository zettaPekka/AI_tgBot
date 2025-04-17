# Telegram Bot with Mistral AI Integration

## 🤖 Описание бота

Этот телеграм-бот использует мощь нейросети Mistral AI для выполнения различных задач:
- Ответы на вопросы с глубоким контекстом
- Генерация текста по запросам
- Анализ изображений (текст на фото)
- Обработка LaTeX выражений
- Интеллектуальный анализ информации

Бот работает на базе API Mistral AI, что обеспечивает высокое качество и точность ответов.

## ⚙️ Установка и настройка

1. **Создайте виртуальное окружение**:
   ```bash
   python -m venv venv
   ```

2. **Активируйте окружение**:
   - Для Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Для Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```

3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл .env в корне проекта** со следующими переменными:
   ```
   DB_PATH=your_database_path.db
   ADMIN_ID=your_telegram_id
   TG_TOKEN=your_telegram_bot_token
   MISTRAL_API_KEY=your_mistral_api_key
   ```

5. **Запустите бота**:
   ```bash
   python main.py
   ```
