# -*- coding: utf-8 -*-
from logging import getLogger
from confcenter.common import whoami, get_client_ip, get_session_key
from django.utils.translation import ugettext as _
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

logger = getLogger(__name__)

def aix_pdf_generate(AIXSNAP):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(500, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response