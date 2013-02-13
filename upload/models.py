# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class News(models.Model):
    add_date = models.DateField('Дата добавления', auto_now_add=True)
    news_lang = models.CharField('Язык новости', max_length=10, blank=False)
    news_text = models.CharField('Новость', max_length=400, blank=False)
    def __unicode__(self):
        return self.news_text
    class Meta(object):
        verbose_name_plural = "Новости"

class Orgs(models.Model):
    name = models.CharField('Наименование', max_length=135, blank=True)
    fullname = models.CharField('Полное наименование', max_length=750, blank=True)
    address = models.CharField('Адрес', max_length=135, blank=True)
    city = models.CharField('Город', max_length=135, blank=True)
    def __unicode__(self):
        return self.name
    class Meta(object):
        verbose_name_plural = "Организации"

class Contacts(models.Model):
    name = models.CharField('Имя', max_length=135, blank=True) # Field name made lowercase.
    surname = models.CharField('Фамилия', max_length=300, blank=True) # Field name made lowercase.
    sec_name = models.CharField('Отчество', max_length=300, blank=True) # Field name made lowercase.
    orgs = models.ForeignKey(Orgs, verbose_name='Организация') # Field name made lowercase.
    def __unicode__(self):
        return '%s %s %s'  % (self.name, self.sec_name, self.surname)
    class Meta(object):
        verbose_name_plural = "Контактные лица"


class OsTypes(models.Model):
    os_name = models.CharField('Название ОС', max_length=135, blank=True)
    os_vendor = models.CharField('Производитель', max_length=100, blank=True)
    comment = models.CharField('Комментарий', max_length=135, blank=True)
    def __unicode__(self):
        return '%s %s' % (self.os_vendor, self.os_name)
    class Meta(object):
        verbose_name_plural = "Типы операционных систем"

class Oses(models.Model):
    os_level = models.CharField('Уровень обноваления ОС', max_length=135, blank=True)
    ostypes = models.ForeignKey(OsTypes, verbose_name='Тип ОС')
    def __unicode__(self):
        return self.os_level
    class Meta(object):
        verbose_name_plural = "Операционные системы"

class PartRules(models.Model):
    param = models.CharField(max_length=750, blank=True)
    value = models.CharField(max_length=750, blank=True)
    condition = models.IntegerField(null=True, blank=True)

class PlatformTypes(models.Model):
    type_name = models.CharField(max_length=135, blank=True)
    model_name = models.CharField(max_length=135, blank=True)
    vendor_name = models.CharField(max_length=135, blank=True)
    comments = models.CharField(max_length=750, blank=True)
    def __unicode__(self):
        return '%s %s %s' % (self.vendor_name, self.type_name, self.model_name)
    class Meta(object):
        verbose_name_plural = "Типы платформ"

class OsTypesHasPartRules(models.Model):
    os_types = models.ForeignKey(OsTypes)
    part_rules = models.ForeignKey(PartRules)
    platform_types = models.ForeignKey(PlatformTypes)

class Parts(models.Model):
    hostname = models.CharField(max_length=135, blank=True)
    conf_output_name = models.CharField(max_length=765, blank=True)
    orgs = models.ForeignKey(Orgs)
    oses = models.ForeignKey(Oses)
    platform_types = models.ForeignKey(PlatformTypes)

class PartParams(models.Model):
    param = models.CharField(max_length=750, blank=True)
    value = models.CharField(max_length=750, blank=True)
    parts = models.ForeignKey(Parts)