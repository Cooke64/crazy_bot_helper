from django.contrib import admin
from . import models


class TravelOrderInline(admin.TabularInline):
    model = models.TravelOrder
    extra = 1
    min_num = 1


class CountryDocumentInline(admin.TabularInline):
    model = models.CountryDocument
    extra = 1
    min_num = 1


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = (CountryDocumentInline, TravelOrderInline)
    list_display = (
        'pk',
        'name',
        'is_friendly',
        'is_dangerous',
    )
    search_fields = ('name',)
    list_editable = ('is_friendly', 'is_dangerous')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'update_date')
    list_filter = ('name',)


@admin.register(models.CountryDocument)
class CountryDocumentAdmin(admin.ModelAdmin):
    list_display = ('country', 'document', 'duration')
    list_filter = ('country', 'document')


@admin.register(models.TravelOrder)
class CountryDocumentAdmin(admin.ModelAdmin):
    list_display = ('country', 'document',)
    list_filter = ('country', 'document')


@admin.register(models.FavoriteCountryTG)
class FavoriteCountryTGAdmin(admin.ModelAdmin):
    list_display = ('country', 'user',)
    list_filter = ('country', 'user')
