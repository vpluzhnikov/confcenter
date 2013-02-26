# Create your views here.
# -*- coding: utf-8 -*-

from django.http import  HttpResponse, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.core.cache import cache
from django.template import RequestContext
from django.utils import simplejson
from confcenter.settings import MEDIA_URL
from logging import getLogger
from pdfhandler import aix_pdf_generate
from models import News

from forms import ConfUploadForm
from conffiles import handle_uploaded_file
from aixsnap import AixSnap
from confcenter.common import whoami, get_client_ip, get_session_key
from django.utils.translation import ugettext as _
from django.utils.translation import get_language



logger = getLogger(__name__)

def anal_acc(request):
    AIXSNAP = request.session['AIXSNAP']

    if request.method == 'POST':
        if 'pdf_save' in request.POST:
            logger.info("PDF generation requested for %s in %s" % (request.session['archpath'], whoami()))
            return aix_pdf_generate(AIXSNAP)

    if 'db_save'in request.POST:
            logger.info("Saving in DB requester for %s in %s" % (request.session['archpath'], whoami()))
            raise Http404
    else:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], request.session['X-Progress-ID'])
        cache.delete(cache_key)
        logger.info("Snap object analyzed for %s and output generated in %s" % (request.session['archpath'], whoami()))
        return render_to_response("snapreport_form.html", AIXSNAP)

def upload_file(request):
    """
        Function upload_file starts form for confupload_form.html
    """
    if request.method == 'POST':
        form = ConfUploadForm(request.POST, request.FILES)
        if form.is_valid():
            UF_FORM = form.cleaned_data
            if 'X-Progress-ID' in request.GET:
                request.session['X-Progress-ID'] = request.GET['X-Progress-ID']
            logger.info("Starting file  %s proccessing in %s for user from %s" % (request.FILES['file'].name, whoami(),
                                                                               get_client_ip(request)))
            fileattr = handle_uploaded_file(request.FILES['file'], get_session_key(request) + '_' +
                                                                    request.FILES['file'].name, UF_FORM['ostype'])
            if not ( fileattr == None ):
                request.session['archpath'] = fileattr['archpath']
                logger.info("Sucsessfully handeled file  %s in %s" % (request.FILES['file'].name, whoami()))
                snap = AixSnap(fileattr['archpath'])
                AIXSNAP = snap.snap_analyze(request.FILES['file'].name)
                snap.dump_snap_to_json(request.FILES['file'].name, fileattr['dumpfilename'])
                snap.snap_destroy()
                request.session['AIXSNAP'] = AIXSNAP
                return redirect('/upload/anal_acc/')
            else:
                logger.info("File type %s is not good, reported from %s" % (request.FILES['file'].name, whoami()))
                return HttpResponse(_('Bad file type or file corrupted'))

    else:
        logger.info("Empty upload form prepared from %s for user from %s, "
                    "session id %s" % (whoami(), get_client_ip(request), get_session_key(request)))
        form = ConfUploadForm() # A empty, unbound form

    return render_to_response('confupload_form.html', {'form': form, 'MEDIA_URL' : MEDIA_URL},
        context_instance=RequestContext(request))

def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    logger.debug("JSON recieved in %s value %s" % (whoami(),request.GET))
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        logger.debug('Searching for cache key %s in %s' % (cache_key, whoami()))
        data = cache.get(cache_key)
        logger.debug('Data retrieved %s', (data))
        if data:
            return HttpResponse(simplejson.dumps(data))
        else:
            return HttpResponse(simplejson.dumps({'size': 0, 'received' : 0}))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

def list_values(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def headpiece(request):
    """
       Function headpiece prints background
    """
    AllNews= News.objects.filter(news_lang=request.LANGUAGE_CODE).order_by("-add_date")[0:5]
    NEWS = []
    print get_language()
    for news in AllNews:
        NEWS.append({'date' : news.add_date, 'text' : news.news_text})
    return render_to_response('headpiece.html', {'news' : NEWS, 'MEDIA_URL' : MEDIA_URL})

def dummy(request):

    return render_to_response('dummy.html')

def projects(request):
    lang = get_language()
    if lang not in ['en', 'ru']:
        lang = 'en'
    return render_to_response('projects_'+lang+'.html')

def plans(request):
    lang = get_language()
    if lang not in ['en', 'ru']:
        lang = 'en'
    return render_to_response('plans_'+lang+'.html')
