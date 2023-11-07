from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


USR_COMMANDS = (
    ("translate", "Переклад"),
    ("voice", "Голосове"),
    ("help", "Інструкція"),
)

ADM_COMMANDS = USR_COMMANDS + (
    ('settings', 'Налаштування'),
    ('calendar', 'Календар'),
    ("id", "Ваш ІД"),
)

LAYOUTS = {
    'QWERTY': dict(zip(map(ord, "qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./`"
                                'QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?~'
                                "!@#$%^&*()_+’"),
                       "йцукенгшщзхїʼфівапролджєячсмитьбю.ґ"
                       'ЙЦУКЕНГШЩЗХЇ₴ФІВАПРОЛДЖЄЯЧСМИТЬБЮ,Ґ'
                       '!"№;%:?*()_+є'))
}

START = r'Привіт\! Я бот\-транслітератор\. Переглянь *інструкцію \(/help\)* перед використанням\.'

command_list = "\n".join([f'*\- {comm[0]}*' for comm in USR_COMMANDS[:-1]])
HELP = (
    'Тут ви можете отримати інформацію про всі команди\n\n'
    '*Зараз доступні такі команди:*\n'
    f'{command_list}\n\n'
    'Про яку команду тобі розповісти?'
)

INSTRUCTION_TRANSLATE = (
    '*Інструкція "translate":*📝\n\n'
    '*1\.* Ти забув переключити мову і написав щось на кшталт *"Ghbdsn? lhe;t\!"*\n'
    '*2\.1\.* Відповідаєш на те повідомлення командою *"/translate"*\n'
    '*2\.2\.* Зразу після повідомлення пишеш *"/translate"* і підтверджуєш переклад\n'
    '*3\.* Я відповідаю перекладеним повідомленням *||"Привіт, друже\!"||*\.'
)


INSTRUCTION_VOICE = (
    '*Інструкція "voice":*📝\n\n'
    '*1\.* Хтось надіслав голосове, але тобі не зручно його послухати\n'
    '*2\.1\.* Відповідаєш на те повідомлення командою *"/voice"*\n'
    '*2\.2\.* Зразу після повідомлення пишеш *"/voice"* і підтверджуєш читання\n'
    '*3\.* Я відповідаю прочитаним повідомленням\.'
)

THIS_MESSAGE = 'Перекласти це повідомлення?'
THIS_AUDIO = 'Прочитати це голосове?'

KB_TEXT = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Перекласти', callback_data='text')]])
KB_AUDIO = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Прочитати', callback_data='speach')]])
KB_HELP = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=command[0], callback_data=command[1]) for command in USR_COMMANDS[:-1]]]
)
KB_SETTINGS = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Змінити мову', callback_data='language')]
])

LANGUAGES = {'uk': 'українська', 'en': 'english'}
DG_OPTIONS = {'punctuate': True, 'utt_split': 600.0, 'language': 'uk'}

VOICE_404 = 'Не вдалось розпізнати'
