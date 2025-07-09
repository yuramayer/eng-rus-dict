"""Methods working with bot's text"""


def create_words_message(
        relevant_words: dict) -> str:
    """Creates pretty text for the message"""

    txt = '📖 Подходящие слова:\n\n'

    for key, value in relevant_words.items():
        txt += f' - <b>{key}</b> - {value}\n'

    return txt


def check_word_message(
        word: str, translation: str) -> str:
    """Creates pretty text for checking the new word"""

    txt = (
        '🔖 Ты сохраняешь новую пару:\n\n'
        f'<b>{word}</b> - <b>{translation}</b>'
        '\n\nВсё верно?'
    )

    return txt


def create_start_message() -> str:
    """Creates start message describing the bot"""

    txt = (
        'Я помогаю хранить и вспоминать иностранные слова 📗\n\n'
        'У меня есть 3 команды:\n'
        '  👉🏻 <b>/add_word</b> - сохрани новую фразу в словарь\n'
        '  👉🏾 <b>/get_word</b> - найди нужную фразу в словарике\n'
        '  👉🏼 Нажми <b>/cancel</b> чтобы отменить любую операцию\n\n'
        'Пока твой словарь пустой, добавь первое слово'
        'с помощью /add_word 😉\n\n'
        'Будут вопросы - обращайся <b>@botrqst</b>'
    )

    return txt


def create_end_message() -> str:
    """Created the message sending in the end of the operations"""

    txt = (
        'Чем ещё могу помочь?\n\n'
        '  👉🏻 <b>/add_word</b> - добавить новое слово\n'
        '  👉🏾 <b>/get_word</b> - найти фразу в словаре\n'
    )

    return txt


def create_all_words_message(
        relevant_words: dict) -> str:
    """Creates pretty text for the message with all the words"""

    txt = '📚 Все твои слова:\n\n'

    for key, value in relevant_words.items():
        txt += f' - <b>{key}</b> - {value}\n'

    return txt


def create_not_admin_message() -> str:
    """Creates the message for non-admin users"""

    github_link = 'https://github.com/yuramayer/lang_dict_tg'
    link_name = 'github.com/yuramayer/lang_dict_tg'

    txt = (
        '📖 Бот-словарик по ивриту\n\n'
        'Бот предназначен для частного использования.\n'
        'Разработчик бота: <b>@botrqst</b> 👨🏻‍💻\n'
        f'Код бота на GitHub: <a href="{github_link}">{link_name}</a>'
    )

    return txt
