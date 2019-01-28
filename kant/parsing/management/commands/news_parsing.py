from django.core.management import BaseCommand, CommandError

from bs4 import BeautifulSoup
import requests
import datetime

from parsing.models import NewsModel


class News(object):

    def __init__(self, link, data, name, description=''):
        self.link = link
        self.data = data
        self.name = name
        self.description = description

    def __str__(self):
        return "link: " + str(self.link) + "\n" + "data: "\
               + str(self.data) + "\n" + "name: " + str(self.name) +\
               "\n" + "description: " + str(self.description)


class Command(BaseCommand):
    help = 'Parsing news from ROSSAHAR.RU '

    def handle(self, *args, **options):
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)

        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day

        try:
            # datetime.datetime.today().weekday() != 5 and datetime.datetime.today().weekday() != 6:
            source = requests.get(f'http://rossahar.ru/news/{year}/{month}/{day}').text
            self.parse_news(source)
            return self.stdout.write(self.style.SUCCESS('News parsed successfully'))
        except AttributeError:
            return self.stdout.write(self.style.ERROR('This is weekend or holiday'))

    @staticmethod
    def parse_news(source):

        soup = BeautifulSoup(source, 'lxml')

        date_list = []
        news_list = []

        # parsing date of news
        date = soup.find('div', class_='date')
        date_list.append(date.text)

        # parsing all <a> in this div
        for news in soup.find('div', class_='date').find_next_siblings('a'):
            # getting href attr of <a> tag
            link = news['href']
            date = date_list[0]
            name = news.text
            n = NewsModel.objects.create(link=link, data=date, name=name)
            news_list.append(n)

        for news in news_list:
            # Find specific url for every news' description
            des_source = requests.get('http://rossahar.ru' + str(news.link)).text
            soup123 = BeautifulSoup(des_source, 'lxml')

            for paragraph in soup123.find('div', class_='visible').find_all('p'):
                news.description += paragraph.text
                news.description += '\n'

            news.save()

        # for i in news_list:
        #     print(i)
        #     print(i.description)
        #     print('``````````````````````````````````````````````````````')

    # @staticmethod
    # def parse_description(source):
    #     soup = BeautifulSoup(source, 'lxml')




