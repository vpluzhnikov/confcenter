__author__ = 'vs'
# -*- coding: utf-8 -*-

from django.contrib import admin
from upload.models import Orgs, Contacts, OsTypes, Oses, PlatformTypes, News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('add_date', 'news_lang', 'news_text')
    search_fields = ('add_date', 'news_lang', 'news_text')
    ordering = ('add_date',)

class OrgsAdmin(admin.ModelAdmin):
    list_display = ('name', 'fullname', 'city')
    search_fields = ('name', 'fullname', 'city')
    ordering = ('name',)


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'sec_name')
    search_fields = ('surname', 'name', 'sec_name')
    ordering = ('surname',)


class OsTypesAdmin(admin.ModelAdmin):
    list_display = ('os_vendor', 'os_name')
    search_fields = ('os_vendor', 'os_name')
    list_filter = ('os_vendor',)
    ordering = ('os_vendor',)


class OsesAdmin(admin.ModelAdmin):
    list_display = ('ostypes', 'os_level')
    search_fields = ('ostypes', 'os_level')
    list_filter = ('ostypes',)
    ordering = ('ostypes',)


class OsPlatformTypes(admin.ModelAdmin):
    list_display = ('vendor_name', 'type_name', 'model_name')
    search_fields = ('vendor_name', 'type_name', 'model_name')

admin.site.register(News, NewsAdmin)
admin.site.register(Orgs, OrgsAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(OsTypes, OsTypesAdmin)
admin.site.register(Oses, OsesAdmin)
admin.site.register(PlatformTypes, OsPlatformTypes)