# Скачивание книг

Программа предназначена для настройки умного чатбота для Telegram и VK.

Список скриптов:
- train_dialogflow.py: обучение бота
- tg_bot.py: запуск telegram-бота
- vk_bot.py: запуск vk-бота

![image](https://github.com/Boltasov/dvmn_speech_bot/blob/master/demo.gif)

## Как установить

Должны быть предустановлены Python 3 и pip.

Скачайте код с помощью команды в командной строке
```
git clone https://github.com/Boltasov/dvmn_speech_bot
```
Перейдите в папку с проектом
```
cd dvmn_speech_bot
```
Установите необходимые библиотеки командой
```
python pip install -r requirements.txt
```
Далее:
1. Настройте DialogFlow (инструкция ниже)
2. Создайте Telegram-бота и получите его API-токен
3. Создайте паблик VK и создайте API-токен с разрешением на отправку сообщений.

### Настройка DialogFlow для обработки текста
1. Создать аккаунт DialogFlow - https://dialogflow.cloud.google.com/#/login
2. Создать проект в DialogFolw и сохранить его идентификатор - https://cloud.google.com/dialogflow/docs/quick/setup
3. Создать "умного агента" в DialogFlow - https://cloud.google.com/dialogflow/docs/quick/build-agent. Используйте при создании идентификатор проекта из предыдущего шага.
4. Включить доступ к API в DialogFlow - https://cloud.google.com/dialogflow/es/docs/quick/setup#api
5. Получить файл с ключами от вашего Google-аккаунта, `credentials.json` с помощью консольной утилиты [gcloud](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)
6. Создать токен для доступа к DialogFlow - https://cloud.google.com/docs/authentication/api-keys
7. Заполнить `.env` 

Заполнить `.env`:
```
TG_BOT_KEY=<ВАШ_КЛЮЧ_TELEGRAM_БОТА>
PROJECT_ID=<ВАШ_ID_ПРОЕКТА_DIALOGFLOW>
DIALOGFLOW_KEY=<ВАШ_API_КЛЮЧ_DIALOGFLOW>
GOOGLE_APPLICATION_CREDENTIALS=<ПУТЬ К ФАЙЛУ credentials.json>
GOOGLE_API_KEY=<ВАШ_GOOGLE_API_KEY>
VK_KEY=<ВАШ_КЛЮЧ_VK>
LOG_BOT_KEY=<ВАШ_КЛЮЧ_TELEGRAM_БОТА_ДЛЯ_ЛОГГИРОВАНИЯ>
CHAT_ID=<ВАШ_CHAT_ID_В_ТЕЛЕГРАМ_ДЛЯ_ЛОГОВ>
```

## Запуск
Для работы ботов сначала нужно натренировать dialogflow:
- вручную на сайте;
- с помощью скрипта `train_dialogflow.py`.

### Использование `train_dialogflow.py`
1. Подготовьте набор intents для dialogflow на примере файла `example_questions.json`
2. Запустите скрипт, подставив свой путь к файлу при необходимости:
```commandline
python train_dialogflow.py --filepath=example_questions.json
```

### Запустить tg-бот
```commandline
python tg_bot.py
```

### Запустить VK-бот
```commandline
python vk_bot.py
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
