# -*- coding: utf-8 -*-
from logging import getLogger
from confcenter.common import whoami, get_client_ip, get_session_key
from confcenter.settings import ARIAL_FONT_FILELOCATION
from django.utils.translation import ugettext as _
from io import BytesIO
from reportlab.lib.units import cm
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab import rl_config

from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER


logger = getLogger(__name__)

def getReportStyleSheet(font):
    """Returns a stylesheet object"""
    stylesheet = StyleSheet1()

#    styles.add(ParagraphStyle(name='hhh2',
#        fontName = 'Arial',
#        fontSize=14,
#        leading=18,
#        spaceBefore=12,
#        spaceAfter=6))

    stylesheet.add(ParagraphStyle(name='Normal',
        fontName=font,
        fontSize=10,
        leading=12)
    )

    stylesheet.add(ParagraphStyle(name='BodyText',
        parent=stylesheet['Normal'],
        spaceBefore=6)
    )
    stylesheet.add(ParagraphStyle(name='Italic',
        parent=stylesheet['BodyText'],
        fontName = font)
    )

    stylesheet.add(ParagraphStyle(name='Heading1',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=18,
        leading=22,
        spaceAfter=6),
        alias='h1')

    stylesheet.add(ParagraphStyle(name='Title',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=6),
        alias='title')

    stylesheet.add(ParagraphStyle(name='Heading2',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6),
        alias='h2')

    stylesheet.add(ParagraphStyle(name='Heading3',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=12,
        leading=14,
        spaceBefore=12,
        spaceAfter=6),
        alias='h3')

    stylesheet.add(ParagraphStyle(name='Heading4',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=10,
        leading=12,
        spaceBefore=10,
        spaceAfter=4),
        alias='h4')

    stylesheet.add(ParagraphStyle(name='Heading5',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=9,
        leading=10.8,
        spaceBefore=8,
        spaceAfter=4),
        alias='h5')

    stylesheet.add(ParagraphStyle(name='Heading6',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2),
        alias='h6')

    stylesheet.add(ParagraphStyle(name='Bullet',
        parent=stylesheet['Normal'],
        firstLineIndent=0,
        spaceBefore=3),
        alias='bu')

    stylesheet.add(ParagraphStyle(name='Definition',
        parent=stylesheet['Normal'],
        firstLineIndent=0,
        leftIndent=36,
        bulletIndent=0,
        spaceBefore=6,
        bulletFontName=font),
        alias='df')

    stylesheet.add(ParagraphStyle(name='Code',
        parent=stylesheet['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=8.8,
        firstLineIndent=0,
        leftIndent=36))

    return stylesheet


def aix_pdf_generate(AIXSNAP):
    response = HttpResponse(mimetype='application/pdf')
    filename = 'snapreport_' + AIXSNAP['sysparams']['plat_type'] + "-" + AIXSNAP['sysparams']['plat_model'] + "_" + \
               AIXSNAP['sysparams']['plat_serial'] + ".pdf"
#    print filename
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', ARIAL_FONT_FILELOCATION))

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, rightMargin=1*cm,leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)

    styles = getReportStyleSheet('Arial')
    ts = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
          ('ALIGN', (1,1), (-1,-1), 'LEFT'),
          ('FONT', (0,0), (-1,-1), 'Arial')]

    #REPORT TITLE
    Title = Paragraph(_('pdf_main_title') + AIXSNAP['hostname']['hostname'], styles["Heading1"])
    Subtitle = Paragraph(_('pdf_main_subtitle') + AIXSNAP['sysparams']['plat_type'] + "-" +
                                           AIXSNAP['sysparams']['plat_model'] + " " +
                                           AIXSNAP['sysparams']['plat_serial'], styles["Normal"])

    Elements = [Title, Subtitle]

    # SYTEM PARAMETERS
    if AIXSNAP['sysparams']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('system_params_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))


        data = [[ _('server_type_model_rep'), AIXSNAP['sysparams']['plat_type'] + "-" + AIXSNAP['sysparams']['plat_model']],
                [_('server_serial_rep'), AIXSNAP['sysparams']['plat_serial']],
                [_('server_lparname_rep'), AIXSNAP['hostname']['hostname']]]
        if AIXSNAP['hacmp']:
            if AIXSNAP['hacmp']['hacmp_used'] == 0:
                data.append([_('hacmp_notused_rep')])
            else:
                data.append([_('hacmp_used_rep')])
        else:
            data.append([_('hacmp_notdetected_rep')])
        table = Table(data, style=ts, hAlign='LEFT')
        Elements.append(table)

    # LPAR PARAMTERS
    if AIXSNAP['lparinfo']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('lpar_conf_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))
        data = [[ _('lpar_hmcnum_rep'), AIXSNAP['lparinfo']['lpar_number']],
                [_('lpar_hmcname_rep'), AIXSNAP['lparinfo']['lpar_name']],
                [_('lpar_type_rep'), AIXSNAP['lparinfo']['lpar_type']],
                [_('lpar_mode_rep'), AIXSNAP['lparinfo']['lpar_mode']],
                [_('lpar_capacity_rep'), AIXSNAP['lparinfo']['lpar_capacity']],
                [_('lpar_mincpu_rep'), AIXSNAP['lparinfo']['lpar_min_cpu']],
                [_('lpar_descpu_rep'), AIXSNAP['lparinfo']['lpar_des_cpu']],
                [_('lpar_maxcpu_rep'), AIXSNAP['lparinfo']['lpar_max_cpu']],
                [_('lpar_minmem_rep'), AIXSNAP['lparinfo']['lpar_min_mem']],
                [_('lpar_desmem_rep'), AIXSNAP['lparinfo']['lpar_des_mem']],
                [_('lpar_maxmem_rep'), AIXSNAP['lparinfo']['lpar_max_mem']]
                ]
        table = Table(data, style=ts, hAlign='LEFT')
        Elements.append(table)


    # DEVICES MICROCODES
    if AIXSNAP['mcodes']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('mcode_levels_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))
        data = []
        for mcode in AIXSNAP['mcodes']:
            data.append([_('mcode_dev_rep')+" "+mcode['mcode_devname'],mcode['mcode_level']])
        table = Table(data, style=ts, hAlign='LEFT')
        Elements.append(table)

    # SYSTEM OSLEVEL
    if AIXSNAP['oslevel']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('oslevel_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))
        data = [[_('oslevel_rep'), AIXSNAP['oslevel']['oslevel']]]
        table = Table(data, style=ts, hAlign='LEFT')
        Elements.append(table)

    # DUMP DEVICE
    if AIXSNAP['dumpdev']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('dumpdev_conf_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))
        data = [[_('primary_dumpdev_rep'), AIXSNAP['dumpdev']['dumpdev_primary']],
                [_('secondary_dumpdev_rep'), AIXSNAP['dumpdev']['dumpdev_secondary']],
                [_('dumpdev_copypath'), AIXSNAP['dumpdev']['dumpdev_copypath']]
                ]
        table = Table(data, style=ts, hAlign='LEFT')
        Elements.append(table)

    # SAVED SYSTEM DUMP
    if AIXSNAP['dump']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('sysdump_prp_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))
        data = [[_('sysdump_date_rep'), AIXSNAP['dump']['dump_date']],
                [_('sysdump_status_rep'), AIXSNAP['dump']['dump_status']],
                [_('sysdump_size_rep'), AIXSNAP['dump']['dump_size'] + " bytes"]
        ]
        table = Table(data, style=ts, hAlign='LEFT')
        Elements.append(table)

    # IFIXES INFO
    if AIXSNAP['emgrs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('emgr_info_rep'), styles["Heading2"]))
        for emgr in AIXSNAP['emgrs']:
            Elements.append(Spacer(0, 0.1 * cm))
            data = [[_('emgr_label_rep'), emgr['emgr_label']],
                    [_('emgr_instdate_rep'), emgr['emgr_instdate']],
                    [_('emgr_abstruct_rep'), emgr['emgr_abstruct']],
                    [_('emgr_status_rep'), emgr['emgr_status']]
            ]
            table = Table(data, style=ts, hAlign='LEFT')
            Elements.append(table)

    doc.build(Elements)

    response.write(buffer.getvalue())
    buffer.close()
    return response