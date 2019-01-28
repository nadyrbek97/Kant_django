from django.core.management import BaseCommand, CommandError

from bs4 import BeautifulSoup
import requests

from parsing.models import (SugarModel,
                            NewsModel,
                            JomModel)


class Command(BaseCommand):
    help = ' Parsing from rossahar.ru '

    def handle(self, *args, **options):
        source1 = requests.get('http://rossahar.ru/informs/rf_1221.html?SimG=ufo').text
        source2 = requests.get('http://rossahar.ru/informs/rf_1221.html?SimG=cfo').text
        source3 = requests.get('http://rossahar.ru/informs/jom_524.html?SimG=ufo').text
        source4 = requests.get('http://rossahar.ru/informs/jom_524.html?SimG=cfo').text

        # self.parse_sugar_ufo(source1)
        # self.stdout.write(self.style.SUCCESS('Successfully parsed Sugar UFO'))
        self.parse_sugar_cfo(source2)
        self.stdout.write(self.style.SUCCESS('Successfully parsed Sugar CFO'))
        self.parse_jom_ufo(source3)
        self.stdout.write(self.style.SUCCESS('Successfully parsed JOM UFO'))
        self.parse_jom_cfo(source4)
        self.stdout.write(self.style.SUCCESS('Successfully parsed JOM CFO'))

    @staticmethod
    def parse_sugar_ufo(source):
        soup = BeautifulSoup(source, 'lxml')
        # table = soup.find('table', class_='chartDiv')
        table_list = []
        for td in soup.find('table', class_='chartDiv').find_all('td'):
            t = td.text
            table_list.append(t)

        s = SugarModel.objects.create(name='UFO', date=table_list[0], price=table_list[1],
                                      percentage=table_list[2])

    @staticmethod
    def parse_sugar_cfo(source):
        soup = BeautifulSoup(source, 'lxml')

        table_list = []
        for td in soup.find('table', class_='chartDiv').find_all('td'):
            t = td.text
            table_list.append(t)

        s = SugarModel.objects.create(name='CFO', date=table_list[0], price=table_list[1],
                                      percentage=table_list[2])

    @staticmethod
    def parse_jom_ufo(source):
        soup = BeautifulSoup(source, 'lxml')

        table_list = []
        for td in soup.find('table', class_='chartDiv').find_all('td'):
            t = td.text
            table_list.append(t)

        s = JomModel.objects.create(name='UFO', date=table_list[0], price=table_list[1],
                                    percentage=table_list[2])

    @staticmethod
    def parse_jom_cfo(source):
        soup = BeautifulSoup(source, 'lxml')

        table_list = []
        for td in soup.find('table', class_='chartDiv').find_all('td'):
            t = td.text
            table_list.append(t)

        s = JomModel.objects.create(name='CFO', date=table_list[0], price=table_list[1],
                                    percentage=table_list[2])
