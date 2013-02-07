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
from reportlab.lib.fonts import addMapping

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

    stylesheet.add(ParagraphStyle(name='TableTitle',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=6),
        alias='tabletitle')

    stylesheet.add(ParagraphStyle(name='TableTitleSmall',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=8,
        alignment=TA_CENTER,
        spaceAfter=6),
        alias='tabletitlesmall')

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
        fontSize=7,
#        leading=8.8,
        firstLineIndent=0
#        leftIndent=36
    ))

    return stylesheet


def aix_pdf_generate(AIXSNAP):
    response = HttpResponse(mimetype='application/pdf')
    filename = 'snapreport_' + AIXSNAP['sysparams']['plat_type'] + "-" + AIXSNAP['sysparams']['plat_model'] + "_" + \
               AIXSNAP['sysparams']['plat_serial'] + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', ARIAL_FONT_FILELOCATION))

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, rightMargin=1*cm,leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)

    styles = getReportStyleSheet('Arial')
    ts = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
          ('ALIGN', (1,1), (-1,-1), 'LEFT'),
          ('FONT', (0,0), (-1,-1), 'Arial')]
    errptts = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
          ('ALIGN', (1,1), (-1,-1), 'LEFT'),
          ('FONT', (0,0), (-1,-1), 'Arial'),
          ('FONTSIZE', (0,0), (-1,-1), 10)]
    littlets = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
               ('ALIGN', (1,1), (-1,-1), 'LEFT'),
               ('FONT', (0,0), (-1,-1), 'Arial'),
               ('FONTSIZE', (0,0), (-1,-1), 8)]

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

    # ERRPT INFO
    if AIXSNAP['errors']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('err_info_rep'), styles["Heading2"]))
        data = [[Paragraph(_('err_count_rep'), styles["TableTitle"]), Paragraph(_('err_id_rep'), styles["TableTitle"]),
                 Paragraph(_('err_firstocc_rep'), styles["TableTitle"]),
                 Paragraph(_('err_lastocc_rep'), styles["TableTitle"]),
                 Paragraph(_('err_type_rep'), styles["TableTitle"]),
                 Paragraph(_('err_class_rep'), styles["TableTitle"]),
                 Paragraph(_('err_resource_rep'), styles["TableTitle"]),
                 Paragraph(_('err_desc_rep'), styles["TableTitle"])
                 ]]
        for error in AIXSNAP['errors']:
            data.append([error['errpt_errq'],
                Paragraph(error['errpt_errid'], styles["BodyText"]),
                Paragraph(error['errpt_errdates'], styles["BodyText"]),
                Paragraph(error['errpt_erridatee'], styles["BodyText"]),
                Paragraph(error['errpt_errtype'], styles["BodyText"]),
                Paragraph(error['errpt_class'], styles["BodyText"]),
                Paragraph(error['errpt_errres'], styles["BodyText"]),
                Paragraph(error['errpt_errdesc'], styles["BodyText"])])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    # BOOTINFO
    if AIXSNAP['bootinfo']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('bootinfo_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))
        data = [[_('osloaded_rep'), AIXSNAP['bootinfo']['bootinfo_k'] + _('osbits_rep')]]
        table = Table(data, style=ts, hAlign='LEFT')
        Elements.append(table)

    # SMTINFO
    if AIXSNAP['smt']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('smtinfo_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.1 * cm))
        if AIXSNAP['smt']['smt_threads_count'] == '0':
            Elements.append(Paragraph(_('smt0_threads_rep'), styles["BodyText"]))
        else:
            Elements.append(Paragraph(_('smton_rep') + AIXSNAP['smt']['smt_threads_count'] + _('smt_threades_rep'),
                styles["BodyText"]))

    # TUNABLES INFO
    if AIXSNAP['tunables']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('tun_info_rep'), styles["Heading2"]))
        data = [[ _('tun_name_rep'), _('tun_value_rep') ]]
        for tune in AIXSNAP['tunables']:
            data.append([tune['tun_name'], tune['tun_value'] ])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    # NOYUNABLES INFO
    if AIXSNAP['no_tunables']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('notun_info_rep'), styles["Heading2"]))
        data = [[ _('notun_name_rep'), _('notun_value_rep') ]]
        for tune in AIXSNAP['no_tunables']:
            data.append([tune['tun_name'], tune['tun_value'] ])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    # VOLGROUP INFO
    if AIXSNAP['vgs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('vg_info_rep'), styles["Heading2"]))
        data = [[Paragraph(_('vgname_rep'), styles["TableTitle"]), Paragraph(_('vgstate_rep'), styles["TableTitle"]),
                 Paragraph(_('vgblocksize_rep'), styles["TableTitle"]),
                 Paragraph(_('vgfreesize_rep'), styles["TableTitle"]),
                 Paragraph(_('vgdiskcount_rep'), styles["TableTitle"]),
                 Paragraph(_('vgdiskactive_rep'), styles["TableTitle"]),
                 Paragraph(_('vgautoimport_rep'), styles["TableTitle"])
                ]]
        for vg in AIXSNAP['vgs']:
            data.append([Paragraph(vg['name'], styles["BodyText"]), Paragraph(vg['state'], styles["BodyText"]),
                         Paragraph(vg['pp_size'], styles["BodyText"]), Paragraph(vg['free_size'], styles["BodyText"]),
                         Paragraph(vg['totalpv'], styles["BodyText"]), Paragraph(vg['activepv'], styles["BodyText"]),
                         Paragraph(vg['auto'], styles["BodyText"])])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    # VOLGROUP INFO
    if AIXSNAP['lvs']:
        Elements.append(Paragraph(_('lv_info_rep'), styles["Heading2"]))
        Elements.append(Spacer(0, 0.5 * cm))
        for lv in AIXSNAP['lvs']:
            Elements.append(Paragraph(_('vgtitle_rep') + lv['volgroup'], styles["Heading3"]))
            Elements.append(Spacer(0, 0.1 * cm))
            data = [[Paragraph(_('lvname_rep'), styles["TableTitleSmall"]),
                     Paragraph(_('lvtype_rep'), styles["TableTitleSmall"]),
                     Paragraph(_('lvcopycount_rep'), styles["TableTitleSmall"]),
                     Paragraph(_('lvstate_rep'), styles["TableTitleSmall"]),
                     Paragraph(_('lvmountp_rep'), styles["TableTitleSmall"]),
                     Paragraph(_('lvmounted_rep'), styles["TableTitleSmall"]),
                     Paragraph(_('lvbusy_rep'), styles["TableTitleSmall"]),
                     Paragraph(_('lvinodebusy_rep'), styles["TableTitleSmall"])
                    ]]
            for l in lv['volumes']:
                data.append([Paragraph(l['name'], styles["Code"]), Paragraph(l['type'], styles["Code"]),
                             Paragraph(l['copies'], styles["Code"]), Paragraph(l['state'], styles["Code"]),
                             Paragraph(l['mount'], styles["Code"]), Paragraph(l['mounted'], styles["Code"]),
                             Paragraph(l['used'], styles["Code"]), Paragraph(l['iused'], styles["Code"])])
            table = Table(data, style=littlets, hAlign='CENTRE', repeatRows=1, splitByRow=1)
            Elements.append(table)

    # SWAP INFO
    if AIXSNAP['swaps']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('swap_info_rep'), styles["Heading2"]))
        data = [[ _('swapname_rep'), _('swapactive_rep'), _('swapsize_rep'), _('swapused_rep') ]]
        for swap in AIXSNAP['swaps']:
            data.append([swap['swap_vol'], swap['swap_active'], swap['swap_size'], swap['swap_used']])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    # DNS INFO
    if AIXSNAP['dns']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('dns_info_rep'), styles["Heading2"]))
        data = []
        if 'dns_nameserver_1' in AIXSNAP['dns']:
            data.append([_('dnsname_rep'), AIXSNAP['dns']['dns_nameserver_1']])
        if 'dns_nameserver_2' in AIXSNAP['dns']:
            data.append([ _('dnsname_rep'), AIXSNAP['dns']['dns_nameserver_2']])
        if 'dns_nameserver_3' in AIXSNAP['dns']:
            data.append([ _('dnsname_rep'), AIXSNAP['dns']['dns_nameserver_3']])
        if 'dns_nameserver_4' in AIXSNAP['dns']:
            data.append([ _('dnsname_rep'), AIXSNAP['dns']['dns_nameserver_4']])
        if 'dns_nameserver_5' in AIXSNAP['dns']:
            data.append([ _('dnsname_rep'), AIXSNAP['dns']['dns_nameserver_5']])
        if 'dns_domain' in AIXSNAP['dns']:
            data.append([ _('dnsdomain_rep'), AIXSNAP['dns']['dns_domain']])
        if 'dns_search' in AIXSNAP['dns']:
            data.append([ _('dnssearch_rep'), AIXSNAP['dns']['dns_search']])

        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    # HEQUIV INFO
    if AIXSNAP['hequiv']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('hequiv_info_rep'), styles["Heading2"]))
        for host in AIXSNAP['hequiv']:
            Elements.append(Paragraph[host, styles["BodyText"]])

    # NFS INFO
    if AIXSNAP['nfs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('nfsshares_info_rep'), styles["Heading2"]))
        if len(AIXSNAP['nfs']) > 1:
            for share in AIXSNAP['nfs']:
                Elements.append(Paragraph[share, styles["BodyText"]])
        else:
            if AIXSNAP['nfs'][0] == "exportfs: nothing exported":
                Elements.append(Paragraph(_('nonfsshares_rep'), styles["BodyText"]))
            else:
                Elements.append(Paragraph(AIXSNAP['nfs'][0], styles["BodyText"]))

    #RPMS INFO
    if AIXSNAP['rpms']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('rpms_info_rep'), styles["Heading2"]))
        data = [[ _('rpmnamever_rep')]]
        for rpm in AIXSNAP['rpms']:
            data.append([rpm['rpmname']])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    #VRPSLPPS INFO
    if AIXSNAP['vrtslpps']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('vrtslpps_info_rep'), styles["Heading2"]))
        data = [[ _('vrtslppname_rep'), _('vrtslppver_rep')]]
        for lpp in AIXSNAP['vrtslpps']:
            data.append([lpp['lppname'], lpp['lppver']])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    #SYSPARAMS INFO
    if AIXSNAP['sysparams']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('sys0_info_rep'), styles["Heading2"]))
        data = [[ _('atname_rep'), _('atval_rep')],
                [AIXSNAP['sysparams']['atname_1'],AIXSNAP['sysparams']['atval_1']],
                [AIXSNAP['sysparams']['atname_2'],AIXSNAP['sysparams']['atval_2']]
        ]
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    #limits INFO
    if AIXSNAP['limits']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('limits_info_rep'), styles["Heading2"]))
        for user in AIXSNAP['limits']:
            Elements.append(Paragraph(user['username'], styles["Heading3"]))
            Elements.append(Spacer(0, 0.1 * cm))
            data = [[ _('atname_rep'), _('atval_rep')]]
            for limit in user['limitlist']:
                data.append([limit['limname'], limit['limval']])
            table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
            Elements.append(table)
            Elements.append(Spacer(0, 0.1 * cm))

    # ADAPTERS INFO
    if AIXSNAP['adapters']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('adapters_info_rep'), styles["Heading2"]))
        data = [[ Paragraph(_('adaptername_rep'), styles["TableTitle"]),
                  Paragraph(_('adapterdesc_rep'), styles["TableTitle"]),
                  Paragraph(_('adaptestate_rep'), styles["TableTitle"]),
                  Paragraph(_('adapterloc_rep'), styles["TableTitle"])]
        ]
        for adapter in AIXSNAP['adapters']:
            data.append([Paragraph(adapter['adapter_name'], styles["BodyText"]),
                         Paragraph(adapter['adapter_desc'], styles["BodyText"]),
                         Paragraph(adapter['adapter_state'], styles["BodyText"]),
                         Paragraph(adapter['adapter_loc'], styles["BodyText"])
            ])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    # ENT1G INFO
    if AIXSNAP['ent1g_attrs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('ent1g_info_rep'), styles["Heading2"]))
        for ent in AIXSNAP['ent1g_attrs']:
            Elements.append(Paragraph(ent['name'], styles["Heading3"]))
            Elements.append(Spacer(0, 0.1 * cm))
            data = [
                [ _('atname_rep'), _('atval_rep')],
                [ ent['atname_1'], ent['atval_1']],
                [ ent['atname_2'], ent['atval_2']],
                [ ent['atname_3'], ent['atval_3']],
                [ ent['atname_4'], ent['atval_4']]
            ]
            table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
            Elements.append(table)

    # ENT10G INFO
    if AIXSNAP['ent10g_attrs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('ent10g_info_rep'), styles["Heading2"]))
        for ent in AIXSNAP['ent10g_attrs']:
            Elements.append(Paragraph(ent['name'], styles["Heading3"]))
            Elements.append(Spacer(0, 0.1 * cm))
            data = [
                [ _('atname_rep'), _('atval_rep')],
                [ ent['atname_1'], ent['atval_1']],
                [ ent['atname_2'], ent['atval_2']],
                [ ent['atname_3'], ent['atval_3']]
            ]
            table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
            Elements.append(table)

    # ENTEC INFO
    if AIXSNAP['entec_attrs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('entec_info_rep'), styles["Heading2"]))
        for ent in AIXSNAP['entec_attrs']:
            Elements.append(Paragraph(ent['name'], styles["Heading3"]))
            Elements.append(Spacer(0, 0.1 * cm))
            data = [
                [ _('atname_rep'), _('atval_rep')],
                [ ent['atname_1'], ent['atval_1']],
                [ ent['atname_2'], ent['atval_2']],
                [ ent['atname_3'], ent['atval_3']]
            ]
            table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
            Elements.append(table)

    # FCS INFO
    if AIXSNAP['fcs_attrs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('fcs_info_rep'), styles["Heading2"]))
        for fcs in AIXSNAP['fcs_attrs']:
            Elements.append(Paragraph(fcs['name'], styles["Heading3"]))
            Elements.append(Spacer(0, 0.1 * cm))
            data = [
                [ _('atname_rep'), _('atval_rep')],
                [ fcs['atname_1'], fcs['atval_1']],
                [ fcs['atname_2'], fcs['atval_2']],
                [ fcs['atname_3'], fcs['atval_3']]
            ]
            table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
            Elements.append(table)

    # FSCSI INFO
    if AIXSNAP['fscsi_attrs']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('fscsi_info_rep'), styles["Heading2"]))
        for fscsi in AIXSNAP['fscsi_attrs']:
            Elements.append(Paragraph(fscsi['name'], styles["Heading3"]))
            Elements.append(Spacer(0, 0.1 * cm))
            data = [
                [ _('atname_rep'), _('atval_rep')],
                [ fscsi['atname_1'], fscsi['atval_1']],
                [ fscsi['atname_2'], fscsi['atval_2']],
                [ fscsi['atname_3'], fscsi['atval_3']]
            ]
            table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
            Elements.append(table)

    #HDISKS INFO
    if AIXSNAP['disks']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('hdisk_info_rep'), styles["Heading2"]))
        data = [[ Paragraph(_('hdisktype_rep'), styles["TableTitle"]),
                  Paragraph(_('hdiskcount_rep'), styles["TableTitle"])]]
        for disk in AIXSNAP['disks']:
            data.append([
                Paragraph(disk['hdisk_type'], styles["BodyText"]),
                disk['hdisk_count']
            ])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    #RMTS INFO
    if AIXSNAP['rmts']:
        Elements.append(Spacer(0, 0.5 * cm))
        Elements.append(Paragraph(_('rmts_info_rep'), styles["Heading2"]))
        data = [[ Paragraph(_('rmtname_rep'), styles["TableTitle"]),
                  Paragraph(_('rmtvendor_rep'), styles["TableTitle"]),
                  Paragraph(_('rmttype_rep'), styles["TableTitle"])
                  ]]
        for rmt in AIXSNAP['rmts']:
            data.append([
                Paragraph(rmt['name'], styles["BodyText"]),
                Paragraph(rmt['vendor'], styles["BodyText"]),
                Paragraph(rmt['type'], styles["BodyText"])
            ])
        table = Table(data, style=errptts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)

    doc.build(Elements)

    response.write(buffer.getvalue())
    buffer.close()
    return response