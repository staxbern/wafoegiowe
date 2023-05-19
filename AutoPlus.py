import requests
from loguru import logger
import telebot
from time import sleep
from json import load

with open('config.json') as file:
    config = load(file)
    if config['forum_id'] == '' or config['telegrambot'] == '' or config['message'] == '':
        logger.error('Ошибка, заполните config.json')
        input()
        raise SystemExit()

if config["telegrambot"]:
    bot = telebot.TeleBot(config["tokenBot"], parse_mode=None)
else:
    logger.info("Функция Логирования в телеграмм бота отключена!")

class AutoPlusn:
    def __init__(self, token: str, baseUrl="https://api.zelenka.guru/"):
        self.token = token
        self.session = requests.session()
        self.baseUrl = baseUrl
        self.session.headers = {'Authorization': f'Bearer {self.token}'}
        self.array = [1]

    def get(self, url, params={}):
        return self.session.get(self.baseUrl + url, params=params).json()

    def post(self, url, data={}):
        return self.session.post(self.baseUrl + url, data=data).json()

    def LastTheme(self):
        return self.session.get(self.baseUrl + f"threads?forum_id={config['forum_id']}&order=thread_update_date_reverse").json()

    def PlusPost(self, thread_id: int, post_body: str):
        data = {'thread_id': f"{thread_id}", 'post_body': f"{post_body}"}
        return self.session.post(self.baseUrl + f"/posts", data=data)

    def AutoPlusWhile(self):
        while True:
            try:
                last = self.LastTheme()
                last_id = last['threads'][0]['thread_id']
                last_author = last['threads'][0]['creator_username']
                sleep(4)
                if last_id in self.array:
                    logger.warning("повторка")
                else:
                    if config["hide"]:
                        hidemess = f"[USERS={last_author}]" + str(config["message"]) + "[/USERS]"
                        request = (self.PlusPost(last_id, hidemess))
                        self.array.append(last_id)
                    else:
                        request = (self.PlusPost(last_id, config["message"]))
                        self.array.append(last_id)
                    if config["telegrambot"]:
                        bot.send_message(config["user_id"], " 🐹 " + str(last['threads'][0]['thread_title']) + " | 🌊Ссылка на тему -> zelenka.guru/threads/" + str(last_id))
                    else:
                        logger.success("Вы написали плюс в тему | " + str(last['threads'][0]['thread_title']) + " | Перейти в тему -> zelenka.guru/threads/" + str(last_id))
            except Exception as e:
                print(e)
            sleep(4)


if __name__ == '__main__':
    p = AutoPlusn(config["tokenLolz"])
    p.AutoPlusWhile()
    if config["telegrambot"] == True:
        bot.infinity_polling()