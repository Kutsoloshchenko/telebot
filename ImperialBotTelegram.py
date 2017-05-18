import telebot
from small_functions import *
from imagehandler import ImageHandlerTelebot
import os

token = "328839472:AAFsBuJYibYpR-Q1YqzLYlM4ifKoOEz4GCA"
bot = telebot.TeleBot(token)


class ImperialTeleg():
    def __init__(self, bot):
        self.bot = bot
        self.help = self._get_help()
        self.faces= self._get_faces()
        self.imagehandler = ImageHandlerTelebot(self.bot)
        self.responce_to_wish = [u'Можно',u'Нельзя',
                                 u'Не лезь блядь, дебил сука ебаный, она тебя сожрет',
                                 u'Может ты еще хочешь что бы тебя орально удовлетворили? А, петушок?',
                                 u'И я так хочу', u'Ну если за Императора, то можно!']
        self.personal_opinion = [u'Норм',
                                 u'Мне не нравится',
                                 u'Лучше умереть за Императора, чем эта фигня',
                                 u'У меня нету четкого мнения по этому поводу',
                                 u'Гавно собачье, жопа',
                                 u'Отлично, и это до поправочки пивчанским',
                                 u'Ну такое, ночем',
                                 u'https://image.ibb.co/c8KnNa/15.jpg']

    @staticmethod
    def _get_faces():
        with open("faceslinks", 'r', encoding="UTF-8") as links:
            faces = links.read().split('\n')
            links.close()
        return faces

    @staticmethod
    def _get_help():
        with open('help', 'r', encoding='UTF-8') as file:
            file_read = file.read()
            file.close()
        return file_read

    def send_help(self, message):
        self.bot.send_message(message.chat.id, self.help)

    def send_to_chat(self, message, text, reply=False, attachment=False):
        if reply:
            self.bot.send_message(chat_id=message.chat.id, text=text, reply_to_message_id=message.message_id)
        elif attachment:
            self.bot.send_photo(chat_id=message.chat.id, caption=text, photo=attachment)
        else:
            self.bot.send_message(chat_id=message.chat.id, text=text)

    def face(self, message):
        text = message.text.lower()
        text, attachment = your_face_telebot(text), choice(self.faces)
        self.send_to_chat(message, text, attachment=attachment)

    def personal_opinion_chose(self):
        token = choice(range(2))
        if token:
            return '%d/10' % choice(range(11))
        else:
            return choice(self.personal_opinion)

    def comic(self, message):
        text = message.text.lower()
        token = None
        if u'биртато' in text:
            token = 2
        elif u'ваха' in text:
            token = 1
        elif u'циан' in text:
            token = 3
        output = self.imagehandler.get_comic(token)
        text = "%s (%s)" % (output[0], output[1])
        attachment = output[2]
        self.send_to_chat(message, text=text, attachment=attachment)

    def search(self, message):
        text = message.text.lower()

        if "вероятность" in text or "инфа" in text:
            self.send_to_chat(message, info(), reply=True)
        elif "привет" in text:
            self.send_to_chat(message, "Под этим солнцем и небом мы тепло преветствуем тебя!", reply=True)
        elif "лицо" in text:
            self.face(message)
        elif "доброе утро" in text:
            self.send_to_chat(message, "Доброе утро! Говорите свободно!", reply=True)
        elif "спасибо" in text:
            self.send_to_chat(message, "Ваша благодарность - высшая награда", reply=True)
        elif "спокойной ночи" in text:
            self.send_to_chat(message, "Пускай АЛЬМСИВИ охраняют твой сон!", reply=True)
        elif "извинися" in text:
            self.send_to_chat(message, "Я прошу прощения за свои слова", reply=True)
        elif "комикс" in text:
            self.comic(message)



TeleBot = ImperialTeleg(bot)


@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    try:
        TeleBot.send_help(message)
    except:
        TeleBot.send_to_chat(message, "Што то пошло не так. Лично я виню в этом тебя")

@bot.message_handler(commands=['comic'])
def send_help(message):
    try:
        TeleBot.comic(message)
    except:
        TeleBot.send_to_chat(message, "Што то пошло не так. Лично я виню в этом тебя")

@bot.message_handler(regexp="Имперец")
def search(message):
    try:
        TeleBot.search(message)
    except:
        TeleBot.send_to_chat(message, "Што то пошло не так. Лично я виню в этом тебя")

@bot.message_handler(content_types=['photo','video'])
def personal_opinion(message):
    try:
        TeleBot.send_to_chat(message, text=TeleBot.personal_opinion_chose(), reply=True)
    except:
        TeleBot.send_to_chat(message, "Што то пошло не так. Лично я виню в этом тебя")

@bot.message_handler(regexp=" или ")
def Or(message):
    try:
        TeleBot.send_to_chat(message, choose_or(message.text))
    except:
        TeleBot.send_to_chat(message, "Што то пошло не так. Лично я виню в этом тебя")

@bot.message_handler(content_types= ["text"])
def want(message):
    try:
        for i in [u'хочу',u'хотел',u'хотелось',u'желаю',u'мечтаю']:
            if i in message.text.lower():
                text = choice(TeleBot.responce_to_wish)
                TeleBot.send_to_chat(message, text=text, reply=True)
                break
    except:
        TeleBot.send_to_chat(message, "Што то пошло не так. Лично я виню в этом тебя")


if __name__ == "__main__":

    while True:
        bot.polling(none_stop=True)
