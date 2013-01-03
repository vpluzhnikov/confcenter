__author__ = 'vss'
# -*- coding: utf-8 -*-
from django import forms
from upload.models import OsTypes, Oses
from django.utils.translation import ugettext as _



class ConfUploadForm(forms.Form):

    OS_TYPES = []
    AllOsTypes = OsTypes.objects.all()

    OS_TYPES.append((_(u'Auto-detect'), [(0, _('Auto-detect'))]))

    for type in AllOsTypes:
        AllOsVers = Oses.objects.filter(ostypes=type)
        OSES_LIST = []
        for ver in AllOsVers:
            OSES_LIST.append((ver.id, type.os_vendor + ' ' + type.os_name + ' ' + ver.os_level))
        OS_TYPES.append((type.os_vendor + ' ' + type.os_name, (OSES_LIST)))

    ostype = forms.ChoiceField(choices=OS_TYPES, label=_(u'choose_ostype_upload'))
    file  = forms.FileField(label=_(u'choose_file_upload'))
