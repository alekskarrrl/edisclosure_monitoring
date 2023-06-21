import requests


class TelegramBot:
    api_base_url = "https://api.telegram.org/bot"

    def __init__(self, token, chat_id, api_base_url=api_base_url):
        self.__token = token
        self.__chat_id = chat_id
        self.__api_base_url = api_base_url

    @property
    def token(self):
        return self.__token

    @property
    def chat_id(self):
        return self.__chat_id

    @property
    def api_base_url(self):
        return self.__api_base_url

    def telegram_bot_sendtext(self, text):
        request_url = "".join([self.__api_base_url,
                               self.__token,
                               '/sendMessage?chat_id=',
                               self.__chat_id,
                               '&parse_mode=None&text=',
                               text])
        try:
            response = requests.get(request_url).json()
            return response
        except requests.exceptions.RequestException as e:
            print(e)

