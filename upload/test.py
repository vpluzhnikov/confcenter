from aixsnap import AixSnap

#snap = AixSnap('/Users/vs/dev/confcenter/confcenter/confuploads/98e6a40e05a8334dd7a43901d08a068e_erie1.snap.pax.Z_AIX/')
#print snap.smt_new()
#print snap.LVM_SNAP.closed
#print snap.FS_SNAP.closed

from django.core.files.uploadhandler import TemporaryFileUploadHandler

#def full_snap_test():
#current_snap = AixSnap('/Users/vs/dev/confcenter/confcenter/confuploads/08fbb839476f26469c6087121133feae_snap_valday2_060712.pax.Z_AIX/')
#current_snap = AixSnap('/Users/vs/dev/confcenter/confcenter/confuploads/dac0b33d7b88a2b27b3ba50d0aa0b1a7_snap_valday2_060712.pax.Z_AIX/')
snap = AixSnap(
    '/Users/vs/dev/confcenter/confcenter/confuploads/d32cb43aca57a20d12e246e262d52b01_snap_dubna-t3.pax.Z_AIX/')
snap.dump_snap_to_json('snap_dubna-t3.pax', 'test.json')
snap.load_snap_from_json('test.json')
xxx = AixSnap('')
DATA = xxx.load_snap_from_json('test.json')
print snap.adapters_params()
print DATA
#print snap.entec_params()
#snap.sys0_params()
#snap.oslevel_params()
#snap.mcodes_params()
#snap.dumpdev_params()
#snap.dump_params()
#snap.emgr_params()
#snap.errpt_params()
#snap.bootinfok_params()
#snap.swap_params()
#snap.rpm_params()
#snap.ent1g_params()
#snap.ent10g_params()
#snap.entec_params()
#snap.fcs_params()
#snap.fscsi_params()
#snap.vrtspack_params()
#print snap.smt_params()
#snap.rmt_params()
#snap.lpar_params()
#snap.hostname_params()
#snap.hdisk_params()
#snap.hacmp_params()
#snap.tunables_params
#snap.nfs_params()
#snap.dns_params()
#snap.no_params()
#snap.hostsequiv_params()
#snap.vg_params()
#snap.lv_params()
#snap.adapters_params()
