from django.contrib import admin

from users.models import TelegramUsers


@admin.register(TelegramUsers)
class CountryDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'country_last_seen_pk')

