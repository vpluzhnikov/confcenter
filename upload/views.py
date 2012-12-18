# Create your views here.
# -*- coding: utf-8 -*-

from django.http import  HttpResponse
from django.shortcuts import render_to_response, redirect

from forms import ConfUploadForm
from conffiles import handle_uploaded_file
from aixsnap import AixSnap


def anal_acc(request):
    #return HttpResponse('OK - ' + request.session['filename'] + ' - ' + str(request.session['filesize']) +
    #                    ' ' + request.session['filetype'] + ' -  ' + request.session['archpath'] )
    snap = AixSnap(request.session['archpath'])
    context = {"snapname": request.session['filename'],
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
               "tunables" : snap.tunables_params,
               "nfs" : snap.nfs_params(),
               "dns" : snap.dns_params(),
               "no_tunables" : snap.no_params(),
               "hequv" : snap.hostsequiv_params(),
               "vgs" : snap.vg_params(),
               "lvs" : snap.lv_params(),
               "adapters" : snap.adapters_params(),
               }
    return render_to_response("snapreport_form.html", context)

def upload_file(request):
    """
        Function upload_file starts form for confupload_form.html
    """
    if request.method == 'POST':
        form = ConfUploadForm(request.POST, request.FILES)
        if form.is_valid():
            UF_FORM  = form.cleaned_data
            if request.session.session_key:
                key = request.session.session_key
            else:
                key = 'None'
            fileattr = handle_uploaded_file(request.FILES['file'], key + '_' +
                                                                    request.FILES['file'].name, UF_FORM['ostype'])
            if not ( fileattr == None ):
                #return HttpResponse('OK - ' + request.FILES['file'].name + ' - ' + str(request.FILES['file'].size) +
                #                    ' ' + fileattr['filetype'] + ' -  ' + fileattr['archpath'] )
                request.session['filename'] = request.FILES['file'].name
                request.session['filesize'] = request.FILES['file'].size
                request.session['archpath'] = fileattr['archpath']
                request.session['filetype'] = fileattr['filetype']
                return redirect('anal_acc/')
            else:
                return HttpResponse('Bad file type or file corrupted')
    else:
        form = ConfUploadForm() # A empty, unbound form
    return render_to_response('confupload_form.html', {'form': form})

def list_values(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))