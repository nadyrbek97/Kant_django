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
        source3 = requests.get('http://rossahar.ru/informs/jom_489.html?SimG=ufo').text
        source4 = requests.get('http://rossahar.ru/informs/jom_489.html?SimG=ufo').text

        self.parse_sugar_ufo(source1)
        self.stdout.write(self.style.SUCCESS('Successfully parsed Sugar UFO'))

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

