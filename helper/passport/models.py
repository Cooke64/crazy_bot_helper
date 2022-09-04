from django.db import models

from users.models import TelegramUsers


class Document(models.Model):
    name = models.CharField('Название', max_length=199)
    description = models.TextField(
        'Краткое описание документа', null=True, blank=True
    )
    update_date = models.DateTimeField(
        'Дата обновления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField('Название', max_length=199, unique=True)
    description = models.TextField(
        'Краткое описание страны', null=True, blank=True
    )
    capital = models.CharField('Столица', max_length=269, null=True,
                               blank=True)
    is_friendly = models.BooleanField('Дружеская ли страна', default=False)
    is_dangerous = models.BooleanField('Есть ли риски', default=False)
    orders = models.ManyToManyField(Document, through='TravelOrder',
                                    verbose_name='Порядок следования',
                                    related_name='countries')
    documents = models.ManyToManyField(Document, through='CountryDocument',
                                       verbose_name='Документы',
                                       related_name='country_doc')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class TravelOrder(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    visa_info = models.TextField('Информация о визовом порядке следования',
                                 null=True, blank=True)

    class Meta:
        verbose_name = 'Порядок пересечения'
        verbose_name_plural = 'Порядок пересечения'

    def __str__(self):
        return f'{self.country.name} следует {self.visa_info}'


class CountryDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    duration = models.PositiveSmallIntegerField('Срок действия документа',
                                                default=0)
    image = models.ImageField('Изображение', upload_to='documents/',
                              blank=True, null=True)
    addition_information = models.TextField('Дополнительная информация')
    is_biometric = models.BooleanField('Биометрия', default=True)

    class Meta:
        verbose_name = 'Документ государства'
        verbose_name_plural = 'Документы государства'

    def __str__(self):
        return f'{self.country.name} with {self.document.name}'


class FavoriteCountryTG(models.Model):
    user = models.ForeignKey(TelegramUsers, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        verbose_name = 'Избранное государство пользователя телеграма'
        verbose_name_plural = 'Избранные государства пользователей телеграма'
        default_related_name = 'favorites_tg'
        ordering = ['-id']

    def __str__(self):
        return f'{self.country.name} is favorite {self.user.username}'

    def save(self, *args, **kwargs):
        self.url = f'http://127.0.0.1:8000/api/country/?name={self.country.name}'
        return super().save(*args, **kwargs)