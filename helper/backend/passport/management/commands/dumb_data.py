import json

from django.core.management.base import BaseCommand
from passport import models
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


PASSPORTS = {
    "0": "Государство",
    "1": "Дипломатический паспорт",
    "2": "Служебный паспорт",
    "3": "Служебный паспорт",
    "4": "Общегражданский паспорт"
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(dir_path + '/' + 'data.json', 'rb') as f:
            try:
                data = json.load(f)
                for val in data:
                    country = val.pop('0')
                    models.Country.objects.get_or_create(name=country)
                    get_country = models.Country.objects.get(name=country)
                    for item in PASSPORTS:
                        if item != "0":
                            get_document = models.Document.objects.get(name=PASSPORTS[item])
                            models.TravelOrder.objects.get_or_create(
                                document=get_document,
                                country=get_country,
                                visa_info=val[item]
                            )
                print("готово")

            except ValueError as e:
                raise e

