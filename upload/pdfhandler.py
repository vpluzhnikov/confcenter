# -*- coding: utf-8 -*-
from logging import getLogger
from confcenter.common import whoami, get_client_ip, get_session_key
from confcenter.settings import ARIAL_FONT_FILELOCATION
from django.utils.translation import ugettext as _
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.utils.translation import ugettext as _

from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.rl_config import warnOnMissingFontGlyphs
from reportlab.pdfbase import pdfmetrics


logger = getLogger(__name__)

def aix_pdf_generate(AIXSNAP):
    response = HttpResponse(mimetype='application/pdf')
    filename = 'snapreport_' + AIXSNAP['sysparams']['plat_type'] + "-" + AIXSNAP['sysparams']['plat_model'] + "_" + \
               AIXSNAP['sysparams']['plat_serial'] + ".pdf"
#    print filename
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('Arial', ARIAL_FONT_FILELOCATION))

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, rightMargin=1*cm,leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)


    styles = getSampleStyleSheet()
    Title = Paragraph("AIX Snap Report for " + AIXSNAP['hostname']['hostname'] , styles["Heading1"])
    Subtitle = Paragraph("This info was extracted from snap collected on " + AIXSNAP['sysparams']['plat_type'] + "-" +
                                           AIXSNAP['sysparams']['plat_model'] + " " +
                                           AIXSNAP['sysparams']['plat_serial'], styles["Normal"])
    Abstract = Paragraph("""<font name=Arial> This is a simple example document that illustrates how to put together a basic PDF with a chart.
    I used the PLATYPUS library, which is part of ReportLab, and the charting capabilities built into ReportLab.""", styles["Normal"])

    Elements = [Title, Subtitle, Abstract]

    Elements.append(Spacer(0, 0.5 * cm))
    Title_1 = _('system_params_rep')
    Elements.append(Paragraph('<font name=Arial>' + ' ' + Title_1, styles["Heading2"]))
    Elements.append(Spacer(0, 0.5 * cm))


    data = [['Caves',         'Wumpus Population'],
            ['Deep Ditch',    50],
            ['Death Gully',   5000],
            ['Dire Straits',  600],
            ['Deadly Pit',    5],
            ['Conclusion',    'Run!']]

    # First the top row, with all the text centered and in Times-Bold,
    # and one line above, one line below.
    ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
          ('LINEABOVE', (0,0), (-1,0), 1, colors.purple),
          ('LINEBELOW', (0,0), (-1,0), 1, colors.purple),
          ('FONT', (0,0), (-1,0), 'Times-Bold'),

          # The bottom row has one line above, and three lines below of
          # various colors and spacing.
          ('LINEABOVE', (0,-1), (-1,-1), 1, colors.purple),
          ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.purple,
           1, None, None, 4,1),
          ('LINEBELOW', (0,-1), (-1,-1), 1, colors.red),
          ('FONT', (0,-1), (-1,-1), 'Times-Bold')]

    # Create the table with the necessary style, and add it to the
    # elements list.
    table = Table(data, style=ts)
    Elements.append(table)

    doc.build(Elements)

    response.write(buffer.getvalue())
    buffer.close()
    return response