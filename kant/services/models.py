from django.db import models


class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)


class AbstractCompanyModel(AbstractDateTimeModel):
    name = models.CharField("Название", max_length=100, null=False, blank=False)
    logo = models.CharField("Лого компании", max_length=500, null=True, blank=True)
    description = models.TextField("Описание", null=True)

    class Meta:
        abstract = True


class AbstractCompanyBranchModel(AbstractDateTimeModel):
    name = models.CharField("Название отдела", max_length=100, null=False, blank=False, )
    address = models.CharField("Адрес", max_length=1000, null=True, blank=True, )
    phone = models.CharField("Номер телефона", max_length=50, null=True, blank=True, )
    longitude = models.CharField("Долгота", max_length=15, null=False, blank=False)
    latitude = models.CharField("Широта", max_length=15, null=False, blank=False)

    class Meta:
        abstract = True


class AbstractBankContactsModel(models.Model):
    types = (
        ('email', 'Почта'),
        ('web', 'Вэб-сайт'),
        ('phone', 'Номер телефона'),
        ('fax', 'Факс'),
        ('social', 'Социальная страничка')
    )

    type = models.CharField("Тип контакта", choices=types, max_length=6, default='Email', )
    data = models.CharField("Ссылка", max_length=500, null=True, blank=True, )

    class Meta:
        abstract = True


class AbstractCompanyImagesModel(models.Model):
    image = models.CharField("Рисунок", max_length=500, null=True, blank=True, )

    class Meta:
        abstract = True


class Services(models.Model):
    name = models.CharField("Название", max_length=100, null=False, blank=False)
    logo = models.CharField("Лого сервиса", max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class BankModel(AbstractCompanyModel):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='Услуга')

    class Meta:
        verbose_name = ""
        verbose_name_plural = "Изменить/добавить услуги"

    def __str__(self):
        return self.name


class BankBranchModel(AbstractCompanyBranchModel):
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE, verbose_name="Банк")

    class Meta:
        verbose_name = "Отдел финансового учреждения"
        verbose_name_plural = "Отделы финансовых учреждений"

    def __str__(self):
        return "{}".format(self.name)


class BankContactsModel(AbstractBankContactsModel):
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE, verbose_name="Банк")

    class Meta:
        verbose_name = "Контакт финансового учреждения"
        verbose_name_plural = "Контакты финансовых учреждений"

    def __str__(self):
        return "{} - {}".format(self.bank.name, self.type)


class BankImagesModel(AbstractCompanyImagesModel):
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE, verbose_name="Банк")

    class Meta:
        verbose_name = "Фото финансового учреждения"
        verbose_name_plural = "Фотографии финансовых учреждений"

    def __str__(self):
        return "{} {}".format(self.bank.name, self.image)


class Suppliers(models.Model):
    name = models.CharField("Название", max_length=100, null=False, blank=False)
    logo = models.CharField("Лого  поставщика", max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Поставщика"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name


class SupplierTypeModel(AbstractCompanyModel):
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE, verbose_name='Поставщик')

    class Meta:
        verbose_name = "Поствавщика"
        verbose_name_plural = " Изменить/добавить поставщиков"

    def __str__(self):
        return self.name


class SupplierBranchModel(AbstractCompanyBranchModel):
    supplier_type = models.ForeignKey(SupplierTypeModel,
                                      on_delete=models.CASCADE,
                                      verbose_name="Тип поствавщика")

    class Meta:
        verbose_name = "Отдел поставщика"
        verbose_name_plural = "Отделы поставщиков"

    def __str__(self):
        return "{} - {}".format(self.supplier_type.name, self.name)


class SupplierContactsModel(AbstractBankContactsModel):
    supplier_type = models.ForeignKey(SupplierTypeModel,
                                      on_delete=models.CASCADE,
                                      verbose_name="Тип поствавщика")

    class Meta:
        verbose_name = "Контакт поставщика"
        verbose_name_plural = "Контакты поставщиков"

    def __str__(self):
        return "{} - {}".format(self.supplier_type.name, self.type)


class SupplierImagesModel(AbstractCompanyImagesModel):
    supplier_type = models.ForeignKey(SupplierTypeModel,
                                      on_delete=models.CASCADE,
                                      verbose_name="Тип поствавщика")

    class Meta:
        verbose_name = "Фото поставщика"
        verbose_name_plural = "Фотографии поставщиков"

    def __str__(self):
        return "{} {}".format(self.supplier_type.name, self.image)


class TechnologyModel(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    text = models.TextField("Данные Технологий", null=True)

    class Meta:
        verbose_name = "Технлогия"
        verbose_name_plural = "Технологии"

    def __str__(self):
        return self.name


class ContractsModel(models.Model):
    title = models.CharField(max_length=1000, null=True, blank=True,
                             default='', verbose_name='Название')
    text = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = 'Контракт/Договор'
        verbose_name_plural = 'Контракты/Договора'

    def __str__(self):
        return self.title
