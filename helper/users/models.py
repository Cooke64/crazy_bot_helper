from django.db import models


class TelegramUsers(models.Model):
    username = models.CharField('Имя пользователя', max_length=199, unique=True)
    chat_id = models.CharField('Айди чата пользователя', max_length=255, unique=True)
    country_last_seen_pk = models.CharField('Номер страны, которую последнюю смотрел', max_length=199, default=0)

    class Meta:
        verbose_name = 'Пользователь телеграмма'

    def __str__(self):
        return self.username


