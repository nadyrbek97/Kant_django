from django.db import models


class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class WeatherModel(models.Model):
    pass


class CurrencyModel():
    pass


class SugarModel(models.Model):
    name = models.CharField("Название", max_length=10)
    date = models.CharField("Дата", max_length=20)
    price = models.CharField("Цена", max_length=10)
    percentage = models.CharField("Рост(в процентах)", max_length=10)

    class Meta:
        unique_together = ('name', 'date',)
        verbose_name = "Сахар"
        verbose_name_plural = "Сахар"

    def __str__(self):
        return "{} {}".format(str(self.date), self.name)


class JomModel(models.Model):
    name = models.CharField("Название", max_length=10)
    date = models.CharField("Дата", max_length=20)
    price = models.CharField("Цена", max_length=10)
    percentage = models.CharField("Рост(в процентах)", max_length=10)

    class Meta:
        unique_together = ('name', 'date',)
        verbose_name = "Жом"
        verbose_name_plural = "Жом"

    def __str__(self):
        return "{} {}".format(str(self.date), self.name)


class NewsModel(AbstractDateTimeModel):
    link = models.CharField("Ссылка на новость", max_length=50, null=True, unique=True, )
    data = models.CharField("Дата", max_length=20, null=True)
    name = models.CharField("Название", max_length=5000, null=True, )
    description = models.CharField("Описание", max_length=20000, null=True, default="")

    class Meta:
        verbose_name = "Новость Rossahar.ru"
        verbose_name_plural = "Новости Rossahar.ru"

    def __str__(self):
        return "{}. {}".format(self.pk, self.name)
