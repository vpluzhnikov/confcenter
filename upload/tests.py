"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from aixsnap import AixSnap
from conffiles import detect_filetype


class AixSnapTest(TestCase):
    def setUp(self):
        self.testsnap = \
        AixSnap('/Users/vs/dev/confcenter/upload/testsnap/98e6a40e05a8334dd7a43901d08a068e_erie1.snap.pax.Z_AIX/')
        self.name = '98e6a40e05a8334dd7a43901d08a068e_erie1.snap.pax.Z'
        self.file = open('/Users/vs/dev/confcenter/upload/testsnap/98e6a40e05a8334dd7a43901d08a068e_erie1.snap.pax.Z')

    def test_all_snap(self):
        """
        Full test for snap
        """
        results = detect_filetype(self.file, self.name)
        self.assertEqual(results['filetype'], 'AIX')
        data = self.testsnap.sys0_params()
        self.assertEqual(data['plat_serial'], '0284D5AF6')
        data = self.testsnap.oslevel_params()
        self.assertEqual(data['oslevel'], '7100-00-03-1115')
        data = self.testsnap.mcodes_params()
        self.assertIsNotNone(data, msg='mcodes is None')
        data = self.testsnap.dumpdev_params()
        self.assertIsNotNone(data, msg='dumpdev is None')
        data = self.testsnap.dump_params()
        self.assertIsNotNone(data, msg='dump is None')
        data = self.testsnap.emgr_params()
        self.assertIsNotNone(data, msg='emgris None')
        data = self.testsnap.errpt_params()
        self.assertIsNotNone(data, msg='errptis None')
        data = self.testsnap.swap_params()
        self.assertIsNotNone(data, msg='swap is None')
        data = self.testsnap.rpm_params()
        self.assertIsNotNone(data, msg='rpm is None')
        data = self.testsnap.ent1g_params()
        self.assertIsNotNone(data, msg='ent1g is None')
        data = self.testsnap.ent10g_params()
        self.assertIsNotNone(data, msg='ent10g is None')
        data = self.testsnap.entec_params()
        self.assertIsNotNone(data, msg='entec is None')
        data = self.testsnap.fcs_params()
        self.assertIsNotNone(data, msg='fcs is None')
        data = self.testsnap.fscsi_params()
        self.assertIsNotNone(data, msg='fscsi is None')
        data = self.testsnap.vrtspack_params()
        self.assertIsNotNone(data, msg='vrts is None')
        data = self.testsnap.smt_params()
        self.assertIsNotNone(data, msg='smt is None')
        data = self.testsnap.rmt_params()
        self.assertIsNotNone(data, msg='rmt is None')
        data = self.testsnap.limits_params()
        self.assertIsNotNone(data, msg='limits is None')
        data = self.testsnap.lpar_params()
        self.assertIsNotNone(data, msg='lpar is None')
        data = self.testsnap.hostname_params()
        self.assertEqual(data['hostname'], 'erie1')
        data = self.testsnap.hdisk_params()
        self.assertIsNotNone(data, msg='hdisk is None')
        data = self.testsnap.hacmp_params()
        self.assertIsNotNone(data, msg='hacmp is None')
        data = self.testsnap.tunables_params()
        self.assertIsNotNone(data, msg='tunables is None')
        data = self.testsnap.nfs_params()
        self.assertIsNotNone(data, msg='nfs is None')
        data = self.testsnap.dns_params()
        self.assertIsNotNone(data, msg='dns is None')
        data = self.testsnap.no_params()
        self.assertIsNotNone(data, msg='no is None')
        data = self.testsnap.hostsequiv_params()
        self.assertIsNone(data, msg='hostequiv is None')
        data = self.testsnap.vg_params()
        self.assertIsNotNone(data, msg='vg is None')
        data = self.testsnap.lv_params()
        self.assertIsNotNone(data, msg='lv is None')
        data = self.testsnap.adapters_params()
        self.assertIsNotNone(data, msg='adaoters is None')

