from django.db import models


class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class SugarModel(models.Model):
    name = models.CharField(max_length=10)
    date = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    percentage = models.CharField(max_length=10)

    class Meta:
        unique_together = ('name', 'date',)
        verbose_name = "Sugar"
        verbose_name_plural = "Sugar infos"

    def __str__(self):
        return "{} {}".format(str(self.date), self.name)


class JomModel(models.Model):
    name = models.CharField(max_length=10)
    date = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    percentage = models.CharField(max_length=10)

    class Meta:
        unique_together = ('name', 'date',)
        verbose_name = "JOM Info"
        verbose_name_plural = "JOMs info"

    def __str__(self):
        return "{} {}".format(str(self.date), self.name)


class NewsModel(AbstractDateTimeModel):
    link = models.CharField(max_length=50, null=True, unique=True)
    data = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=5000, null=True, )
    description = models.CharField(max_length=5000, null=True, default="")

    class Meta:
        verbose_name = "Новости с Rossahar.ru"
        verbose_name_plural = "Новости с Rossahar.ru"

    def __str__(self):
        return "{}. {}".format(self.pk, self.name)
