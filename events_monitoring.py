import json
import os
from dotenv import load_dotenv
from DisclosureEvent import DisclosureEvent
from TelegramBot import TelegramBot
import time

load_dotenv()

def do_check(company_id, company_tiker, year, tlg_bot):
    # получим последнее опубликованное событие
    disclosure_event = DisclosureEvent.get_last_disclosure(company_id, year)
    print(disclosure_event)

    # проверим последнее сохраненное событие по компании
    # read last event from file
    err_msg = ""
    try:
        with open(f"data/{company_tiker}.json", 'r', encoding='utf-8') as f:
            last_event = json.loads(f.read())

        event_date, public_date, event_title, doc_link = last_event['event_date'], \
                                                         last_event['public_date'], \
                                                         last_event['event_title'], \
                                                         last_event['doc_link']
        saved_event = DisclosureEvent(event_date, public_date, event_title, doc_link)
    except FileNotFoundError as e:
        saved_event = None
    except KeyError as e:
        err_msg = f"KeyError - {e}"
        print(err_msg)
        saved_event = None
        # send err_msg to telegram
        tlg_bot.telegram_bot_sendtext(f"{company_tiker}\n\n{err_msg}")

    except json.decoder.JSONDecodeError as e:
        err_msg = f"json.decoder.JSONDecodeError - {e}"
        print(err_msg)
        saved_event = None
        # send err_msg to telegram
        tlg_bot.telegram_bot_sendtext(f"{company_tiker}\n\n{err_msg}")

    print(saved_event)

    if disclosure_event != saved_event:
        # запишем это событие в соответствующий файл
        event_json = {"event_date": disclosure_event.event_date,
                      "public_date": disclosure_event.public_date,
                      "event_title": disclosure_event.event_title,
                      "doc_link": disclosure_event.doc_link
                      }
        with open(f"data/{company_tiker}.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(event_json, indent=4, ensure_ascii=False))
        event_msg = str(disclosure_event)

        # send event_msg to telegram
        tlg_bot.telegram_bot_sendtext(f"%23{company_tiker}\n\n{event_msg}")


def main():
    # company_tiker = "TRNF"
    year = "2023"

    TLG_BOT_TOKEN = os.getenv("TLG_BOT_TOKEN")
    BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")

    bot = TelegramBot(TLG_BOT_TOKEN, BOT_CHAT_ID)

    while True:
        # открыть файл "look_up", прочитать json и забрать нужный id
        with open("look_up.json", 'r') as f:
            companies = json.loads(f.read())

        for ticker in companies:
            company_tiker = ticker
            company_id = companies[ticker]

            do_check(company_id, company_tiker, year, bot)

        time.sleep(60*15)






if __name__ == '__main__':
    main()
