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

from forms import ConfUploadForm
from conffiles import handle_uploaded_file
from aixsnap import AixSnap
from confcenter.common import whoami, get_client_ip, get_session_key
from django.utils.translation import ugettext as _
from io import BytesIO
from reportlab.pdfgen import canvas



logger = getLogger(__name__)

def anal_acc(request):
    #return HttpResponse('OK - ' + request.session['filename'] + ' - ' + str(request.session['filesize']) +
    #                    ' ' + request.session['filetype'] + ' -  ' + request.session['archpath'] )
    snap = AixSnap(request.session['archpath'])
    AIXSNAP = {"snapname": request.session['filename'],
           "sysparams" : snap.sys0_params(),
           "oslevel" : snap.oslevel_params(),
           "mcodes" : snap.mcodes_params(),
           "dumpdev" : snap.dumpdev_params(),
           "dump" : snap.dump_params(),
           "emgrs" : snap.emgr_params(),
           "errors" : snap.errpt_params(),
           "bootinfo" : snap.bootinfok_params(),
           "swaps" : snap.swap_params(),
           "rpms" : snap.rpm_params(),
           "ent1g_attrs" : snap.ent1g_params(),
           "ent10g_attrs" : snap.ent10g_params(),
           "entec_attrs" : snap.entec_params(),
           "fcs_attrs" : snap.fcs_params(),
           "fscsi_attrs" : snap.fscsi_params(),
           "vrtslpps" : snap.vrtspack_params(),
           "smt" : snap.smt_params(),
           "rmts" : snap.rmt_params(),
           "sys0" : snap.sys0_params(),
           "limits" : snap.limits_params(),
           "lparinfo" : snap.lpar_params(),
           "hostname" : snap.hostname_params(),
           "disks" : snap.hdisk_params(),
           "hacmp" : snap.hacmp_params(),
           "tunables" : snap.tunables_params(),
           "nfs" : snap.nfs_params(),
           "dns" : snap.dns_params(),
           "no_tunables" : snap.no_params(),
           "hequv" : snap.hostsequiv_params(),
           "vgs" : snap.vg_params(),
           "lvs" : snap.lv_params(),
           "adapters" : snap.adapters_params(),}

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
#        context = { "snapname": request.session['filename'],
#                   "sysparams" : snap.sys0_params(),
#                   "oslevel" : snap.oslevel_params(),
#                   "mcodes" : snap.mcodes_params(),
#                   "dumpdev" : snap.dumpdev_params(),
#                   "dump" : snap.dump_params(),
#                   "emgrs" : snap.emgr_params(),
#                   "errors" : snap.errpt_params(),
#                   "bootinfo" : snap.bootinfok_params(),
#                   "swaps" : snap.swap_params(),
#                   "rpms" : snap.rpm_params(),
#                   "ent1g_attrs" : snap.ent1g_params(),
#                   "ent10g_attrs" : snap.ent10g_params(),
#                   "entec_attrs" : snap.entec_params(),
#                   "fcs_attrs" : snap.fcs_params(),
#                   "fscsi_attrs" : snap.fscsi_params(),
#                   "vrtslpps" : snap.vrtspack_params(),
#                   "smt" : snap.smt_params(),
#                   "rmts" : snap.rmt_params(),
#                   "sys0" : snap.sys0_params(),
#                   "limits" : snap.limits_params(),
#                   "lparinfo" : snap.lpar_params(),
#                   "hostname" : snap.hostname_params(),
#                   "disks" : snap.hdisk_params(),
#                   "hacmp" : snap.hacmp_params(),
#                   "tunables" : snap.tunables_params,
#                   "nfs" : snap.nfs_params(),
#                   "dns" : snap.dns_params(),
#                   "no_tunables" : snap.no_params(),
#                   "hequv" : snap.hostsequiv_params(),
#                   "vgs" : snap.vg_params(),
#                   "lvs" : snap.lv_params(),
#                   "adapters" : snap.adapters_params(),
#                   }
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
#                return HttpResponse('OK - ' + request.FILES['file'].name + ' - ' + str(request.FILES['file'].size) +
#                                    ' ' + fileattr['filetype'] + ' -  ' + fileattr['archpath'] )
                request.session['filename'] = request.FILES['file'].name
                request.session['filesize'] = request.FILES['file'].size
                request.session['archpath'] = fileattr['archpath']
                request.session['filetype'] = fileattr['filetype']
                logger.info("Sucsessfully handeled file  %s in %s" % (request.FILES['file'].name, whoami()))
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
            return HttpResponse(simplejson.dumps({'length': 0, 'uploaded' : 0}))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

def list_values(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))