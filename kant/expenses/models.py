from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)


class AbstractExpensesModel(AbstractDateTimeModel):
    name = models.CharField(max_length=5000, null=True, verbose_name="Наименование")
    price = models.FloatField(default=0, verbose_name="Цена")
    amount = models.FloatField(default=0, verbose_name="Количество")

    class Meta:
        abstract = True


class Expenses(AbstractExpensesModel):

    class Meta:
        verbose_name = 'Затрата'
        verbose_name_plural = 'Затраты'

    def __str__(self):
        return self.name


class CommodityModel(AbstractDateTimeModel):
    name = models.CharField(max_length=50, null=True, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True, default=timezone.now)
    district = models.CharField(max_length=30, null=True, blank=True, default="BKK")
    price = models.FloatField(null=False, blank=False)
    flow = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name + ' ' + str(self.date)


class SugarBeetPointModel(AbstractDateTimeModel):
    name = models.CharField(verbose_name='Название', max_length=500, null=False, blank=False)

    class Meta:
        verbose_name = "Свеклоприёмный пункт"
        verbose_name_plural = "Свеклоприёмные пункты"

    def __str__(self):
        return self.name


class FieldsModel(AbstractDateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Телефон')
    beet_point = models.ForeignKey(SugarBeetPointModel, on_delete=models.CASCADE,
                                   verbose_name='Свеклопртемный пункт', default=1)
    year = models.IntegerField('Год', default=2011)
    field_id = models.CharField("Идентификационный номер поля", max_length=100, blank=True, default="")
    average_harvest = models.FloatField(verbose_name='Сред. урожай', default=1.0)
    hectares = models.FloatField(verbose_name='Площадь(Га)')

    class Meta:
        verbose_name = "Поле"
        verbose_name_plural = "Поля"

    def __str__(self):
        return self.user.username + ' ' + str(self.year)


class FieldExpenses(AbstractExpensesModel):
    field = models.ForeignKey(FieldsModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Затраты поля"
        verbose_name_plural = "Затраты поля"

    def __str__(self):
        return self.name


class CoordinatesModel(models.Model):
    field = models.ForeignKey(FieldsModel, on_delete=models.CASCADE, verbose_name='Поле')
    longitude = models.CharField(max_length=30, null=False, blank=False, verbose_name='Долгота')
    latitude = models.FloatField(max_length=30, null=False, blank=False, verbose_name='Широта')
    number = models.IntegerField(verbose_name='Номер порядка')

    class Meta:
        verbose_name = 'Коодинаты поля'
        verbose_name_plural = 'Координаты полей'

    def __str__(self):
        return str(self.field.year) + " " + str(self.number)



