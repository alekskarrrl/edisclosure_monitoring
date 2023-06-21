from bs4 import BeautifulSoup
import requests
import json
import re


class DisclosureEvent:

    def __init__(self, event_date, public_date, event_title, doc_link):
        self.__event_date = event_date
        self.__public_date = public_date
        self.__event_title = event_title
        self.__doc_link = doc_link

    @property
    def event_date(self):
        return self.__event_date

    @property
    def public_date(self):
        return self.__public_date

    @property
    def event_title(self):
        return self.__event_title

    @property
    def doc_link(self):
        return self.__doc_link

    def __eq__(self, other):
        if other is not None:
            if (self.__event_date == other.event_date) \
                    and (self.__public_date == other.public_date)\
                    and (self.__event_title == other.event_title)\
                    and (self.__doc_link == other.doc_link):
                return True
            else:
                return False
        else:
            if self is None:
                return True
            else:
                return False

    def __str__(self):
        return f"event_date: {self.__event_date}\npublic_date: {self.__public_date}\n" \
               f"event_title: {self.__event_title}\ndoc_link: {self.__doc_link}"

    @staticmethod
    def get_last_disclosure(company_id, year):
        url = f"https://e-disclosure.ru/Event/Page?companyId={company_id}&year={year}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        # send request
        response = requests.get(url, headers=headers)
        content = response.text
        # clean table content
        # разберем блок style и найдем селекторы для исключения строк таблицы
        soup = BeautifulSoup(content, 'html.parser').find('style')
        style_params = soup.text
        pattern = re.compile(r"tr:nth-child\([0-9]+\)")
        selectors = pattern.findall(style_params)
        selectors_str = ", ".join(selectors)
        # находим тег table и удаляем элементы по селектору
        soup = BeautifulSoup(content, 'html.parser')
        tag_table = soup.find('table')
        tr_to_remove = tag_table.select(selectors_str)
        for item in tr_to_remove:
            item.extract()

        # find table -> tr tags / limit=2  - headers + first row
        soup = tag_table.find_all('tr', limit=2)
        event = soup[1]
        event_row = event.find_all('td')
        # read event table row and clean text
        event_params = [item.text.strip('\n').replace('\xa0', ' ') for item in event_row]
        # append href to event_params list
        event_params.append(event_row[-1].a.get('href').strip('\n').replace('\xa0', ' '))
        event_date, public_date, event_title, doc_link = event_params

        # create DisclosureEvent object
        disclosure_event = DisclosureEvent(event_date, public_date, event_title, doc_link)

        return disclosure_event

