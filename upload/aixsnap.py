__author__ = 'vs'
# -*- coding: utf-8 -*-
from os import access, path, R_OK, lseek, SEEK_SET
import os
from string import lstrip, replace


class AixSnap:
    def __init__(self, CWD):
        """
        __init__ class constructor
        Following class attributes initialized in __init__:
        CWD - Full path to snap root directory
        DUMPDEV_SNAP - File Object fot CWD/general/survdump.settings opened file
        DUMP_SNAP - File Object for CWD/dump/dump.snap opened file
        EMGS_SNAP - File Object for CWD/general/emgr.snap opened file
        ERRPT_SNAP - File Object for CWD/general/errpt.out opened file
        GENERAL_SNAP - File Object for CWD/general/general.snap opened file
        ADAPTER_LIST - File Object for CWD/general/lsdev.adapter opened file
        PROCESSOR_LIST - File Pbject for CWD/general/processor.log opened file
        LIMITS - File Object for CWD/general/limits opened file
        LPAR_SNAP - File Object for CWD/general/lparstat.out opened file
        DISK_LIST - File Object for CWD/general/lsdev.disk opened file
        OSLEVEL_SNAP - File Object for CWD/general/oslevel.info opened file
        HACMP_SNAP - File Object for CWD/hacmp/hacmp.snap opened file
        KERNEL_SNAP - File Object for CWD/kernel/kernel.snap opened file
        NFS_SNAP - File Object for CWD/nfs/nfs.snap opened file
        TCPIP_SNAP - File Object for CWD/tcpip/tcpip.snap opened file
        HEQUIV_SNAP - File Object for CWD/tcpip/hosts.equiv opened file
        LVM_SNAP - File Object for CWD/lvm/lvm.snap opened file
        FS_SNAP - File Object for CWD/filesys/filesys.snap opened file
        """

        self.CWD = CWD
        try:
            self.DUMPDEV_SNAP = open(self.CWD + 'general/survdump.settings')
        except IOError:
            self.DUMPDEV_SNAP = None
        try:
            self.DUMP_SNAP = open(self.CWD + 'dump/dump.snap')
        except IOError:
            self.DUMP_SNAP = None
        try:
            self.EMGR_SNAP = open(self.CWD + 'general/emgr.snap')
        except IOError:
            self.EMGR_SNAP = None
        try:
            self.ERRPT_SNAP = open(self.CWD + 'general/errpt.out')
        except IOError:
            self.ERRPT_SNAP = None
        try:
            self.GENERAL_SNAP = open(self.CWD + 'general/general.snap')
        except IOError:
            self.GENERAL_SNAP = None
        try:
            self.ADAPTER_LIST = open(self.CWD + 'general/lsdev.adapter')
        except IOError:
            self.ADAPTER_LIST = None
        try:
            self.PROCESSOR_LIST = open(self.CWD + 'general/processor.log')
        except IOError:
            self.PROCESSOR_LIST = None
        try:
            self.LIMITS = open(self.CWD + 'general/limits')
        except IOError:
            self.LIMITS = None
        try:
            self.LPAR_SNAP = open(self.CWD + 'general/lparstat.out')
        except IOError:
            self.LPAR_SNAP = None
        try:
            self.DISK_LIST = open(self.CWD + 'general/lsdev.disk')
        except IOError:
            self.DISK_LIST = None
        try:
            self.OSLEVEL_SNAP = open(self.CWD + 'general/oslevel.info')
        except IOError:
            self.OSLEVEL_SNAP = None
        try:
            self.HACMP_SNAP = open(self.CWD + 'hacmp/hacmp.snap')
        except IOError:
            self.HACMP_SNAP = None
        try:
            self.KERNEL_SNAP = open(self.CWD + 'kernel/kernel.snap')
        except IOError:
            self.KERNEL_SNAP = None
        try:
            self.NFS_SNAP = open(self.CWD + 'nfs/nfs.snap')
        except IOError:
            self.NFS_SNAP = None
        try:
            self.TCPIP_SNAP = open(self.CWD + 'tcpip/tcpip.snap')
        except IOError:
            self.TCPIP_SNAP = None
        try:
            self.HEQUIV_SNAP = open(self.CWD + 'tcpip/hosts.equiv')
        except IOError:
            self.HEQUIV_SNAP = None
        try:
            self.LVM_SNAP = open(self.CWD + 'lvm/lvm.snap')
        except IOError:
            self.LVM_SNAP = None
        try:
            self.FS_SNAP = open(self.CWD + 'filesys/filesys.snap')
        except IOError:
            self.FS_SNAP = None

    def dumpdev_params(self):
        """
        Reads DUMPDEV_SNAP and returns DICT with info about dump device config (sysdumpdev -L -v)
        """
        DUMPDEV = {}
        stanza = []
        if self.DUMPDEV_SNAP:
            self.DUMPDEV_SNAP.seek(0)
            conffile = self.DUMPDEV_SNAP
            while True:
                line = conffile.readline()
                if not line:
                    break
                if 'sysdumpdev -l' in line:
                    conffile.readline()
                    nextline = conffile.readline()
                    while ( not '**********' in nextline ) or ( not nextline ):
                        if not nextline.rstrip('\r\n') == '':
                            stanza.append(nextline.rstrip('\r\n'))
                        if not nextline:
                            break
                        nextline = conffile.readline()
                    break
            if stanza == []:
                return None
            else:
                DUMPDEV.update({'dumpdev_primary' : stanza[0].split()[1]})
                DUMPDEV.update({'dumpdev_secondary' : stanza[1].split()[1]})
                DUMPDEV.update({'dumpdev_copypath' : stanza[2].split()[2]})
                return DUMPDEV
        else:
            return None

    def dump_params(self):
        """
        Reads DUMP_SNAP file and returns DICT with info about system dump
        """
        DUMP = {}
        unixz = self.CWD + 'dump/unix.Z'
        dump_date = ''
        dump_state = ''
        if self.DUMP_SNAP:
            for record in self.__snap_stanza_read(self.DUMP_SNAP, 'creation date'):
                dump_date = dump_date + ' ' + record
            for record in self.__snap_stanza_read(self.DUMP_SNAP, 'Status of Dump Copy'):
                dump_state = dump_state + ' ' + record
            DUMP.update({'dump_date' : dump_date.lstrip()})
            DUMP.update({'dump_status' : dump_state.lstrip()})
            DUMP.update({'dump_size' : str(path.getsize(unixz))})
        else:
            return None
        return DUMP

    def emgr_params(self):
        """
        Reads EMGR_SNAP and returns LIST with info about installed ifixes
        """
        EMGR = []
        if self.EMGR_SNAP:
            conffile = self.EMGR_SNAP
            while True:
                line = conffile.readline()
                if 'LABEL:' in line:
                    emgr_label = lstrip(line.split(':')[1].rstrip('\r\n'))
                    conffile.readline()
                    conffile.readline()
                    line = conffile.readline()
                    emgr_status = lstrip(line.split(':')[1].rstrip('\r\n'))
                    conffile.readline()
                    line = conffile.readline()
                    emgr_abstruct = lstrip(line.split(':')[1].rstrip('\r\n'))
                    conffile.readline()
                    conffile.readline()
                    line = conffile.readline()
                    emgr_instdate = lstrip(line.split(':')[1].split()[0].rstrip('\r\n'))
                    EMGR.append({'emgr_label': emgr_label, 'emgr_status': emgr_status,
                                 'emgr_abstruct': emgr_abstruct, 'emgr_instdate': emgr_instdate})
                if not line:
                    break
        else :
            return None
        return EMGR

    def errpt_params(self):
        """
        Reads ERRPT_SNAP and returns LIST with descriptions of errors
        """
        ERRPT = []
        errpt_count = 1
        if self.ERRPT_SNAP:
            conffile = self.ERRPT_SNAP
            while True:
                line = conffile.readline()
                if not line:
                    break
                if '---------------------------------------------------------------------------' in line:
                    line = conffile.readline()
                    error_label = lstrip(line.split(':')[1].rstrip('\r\n'))
                    line = conffile.readline()
                    error_id = lstrip(line.split(':')[1].rstrip('\r\n'))
                    error_exists = False
                    for err in ERRPT:
                        if err['errpt_errid'] == error_id:
                            error_exists = True
                            conffile.readline()
                            line = conffile.readline()
                            err['errpt_errdates'] = lstrip((line.split(':')[1] + ':' + line.split(':')[2] + ':' +
                                                            line.split(':')[3]).rstrip('\r\n'))
                            err['errpt_errq'] += 1
                    if not error_exists:
                        conffile.readline()
                        line = conffile.readline()
                        error_dates = lstrip((line.split(':')[1] + ':' + line.split(':')[2] + ':' +
                                              line.split(':')[3]).rstrip('\r\n'))
                        error_datee = lstrip((line.split(':')[1] + ':' + line.split(':')[2] + ':' +
                                              line.split(':')[3]).rstrip('\r\n'))
                        conffile.readline()
                        conffile.readline()
                        conffile.readline()
                        line = conffile.readline()
                        error_class = lstrip(line.split(':')[1].rstrip('\r\n'))
                        line = conffile.readline()
                        error_errtype = lstrip(line.split(':')[1].rstrip('\r\n'))
                        conffile.readline()
                        line = conffile.readline()
                        error_errres = lstrip(line.split(':')[1].rstrip('\r\n').rstrip())
                        while True:
                            line = conffile.readline()
                            if 'Description' in line:
                                line = conffile.readline()
                                errpt_errdesc = line.rstrip('\r\n')
                                break
                            if not line:
                                break
                        ERRPT.append({'errpt_errid': error_id, 'errpt_errlabel': error_label, 'errpt_errq': 1,
                                      'errpt_errdates': error_dates, 'errpt_erridatee': error_datee,
                                      'errpt_errtype': error_errtype, 'errpt_class': error_class,
                                      'errpt_errres': error_errres, 'errpt_errdesc': errpt_errdesc})
        else:
            return None
        return ERRPT

    def bootinfok_params(self):
        """
        Reads GENERAL_SNAP and returns DICT with system kernel mode
        """
        BIK = {}
        if self.GENERAL_SNAP:
            BIK.update({'bootinfo_k' : self.__snap_stanza_read(self.GENERAL_SNAP, 'bootinfo -K')[0] })
        else:
            return None
        return BIK

    def swap_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with swap parameters
        """
        SWAP = []
        if self.GENERAL_SNAP:
            swaplist = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsps -a')
            if swaplist:
                for i in range(len(swaplist)-1):
                    swapargs = swaplist[i+1].split()
                    SWAP.append({'swap_vol' : swapargs[0], 'swap_size' : swapargs[3], 'swap_used' : swapargs[4],
                                 'swap_active' : swapargs[5]})
        else:
            return None
        return SWAP

    def rpm_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with installed RPM packets list
        """
        RPM = []
        if self.GENERAL_SNAP:
            rpmlist = self.__snap_stanza_read(self.GENERAL_SNAP, 'rpm -qa')
            if rpmlist:
                for rpm in rpmlist:
                    RPM.append({'rpmname' : rpm.split()[0]})
            else:
                return None
        else:
            return None
        return RPM

    def ent1g_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with attributes for Gigabit Ethernet adapters
        """
        ENT_PARAMS = []
        if self.GENERAL_SNAP:
            for ent in self.__snap_adapter_list('1000 Base-TX PCI-Express Adapter'):
                ent_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El ' + ent)
                if ent_params:
                    ENT_PARAMS.append({'name' : ent, 'atname_1' : ent_params[3].split()[0],
                                       'atval_1' : ent_params[3].split()[1], 'atname_2' : ent_params[16].split()[0],
                                       'atval_2' : ent_params[16].split()[1], 'atname_3' : ent_params[19].split()[0],
                                       'atval_3' : ent_params[19].split()[1], 'atname_4' : ent_params[20].split()[0],
                                       'atval_4' : ent_params[20].split()[1]})
        else:
            return None
        return ENT_PARAMS

    def ent10g_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with attributes for 10 Gigabit Ethernet adapters
        """
        ENT10G_PARAMS = []
        if self.GENERAL_SNAP:
            for ent in self.__snap_adapter_list('10 Gigabit Ethernet Adapter'):
                ent_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El ' + ent)
                if ent_params:
                    ENT10G_PARAMS.append({'name' : ent, 'atname_1' : ent_params[1].split()[0],
                                          'atval_1' : ent_params[1].split()[1], 'atname_2' : ent_params[10].split()[0],
                                          'atval_2' : ent_params[10].split()[1], 'atname_3' : ent_params[12].split()[0],
                                          'atval_3' : ent_params[12].split()[1]})
        else:
            return None
        return ENT10G_PARAMS

    def entec_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with attributes for configured EtherChannel devices
        """
        ENTEC_PARAMS = []
        if self.GENERAL_SNAP:
            for ent in self.__snap_adapter_list('EtherChannel'):
                ent_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El ' + ent)
                if ent_params:
                    ENTEC_PARAMS.append({'name' : ent, 'atname_1' : ent_params[0].split()[0],
                                          'atval_1' : ent_params[0].split()[1], 'atname_2' : ent_params[3].split()[0],
                                          'atval_2' : ent_params[3].split()[1], 'atname_3' : ent_params[6].split()[0],
                                          'atval_3' : ent_params[6].split()[1]})
        else:
            return None
        return ENTEC_PARAMS

    def fcs_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with attributes for FibreChannel (fcs) devices
        """
        FCS_PARAMS = []
        if self.GENERAL_SNAP:
            for fcs in self.__snap_adapter_list('fcs'):
                fcs_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El ' + fcs)
                if fcs_params:
                    FCS_PARAMS.append({'name' : fcs, 'atname_1' : fcs_params[5].split()[0],
                                       'atval_1' : fcs_params[5].split()[1], 'atname_2' : fcs_params[9].split()[0],
                                       'atval_2' : fcs_params[9].split()[1], 'atname_3' : fcs_params[10].split()[0],
                                       'atval_3' : fcs_params[10].split()[1]})
        else:
            return None
        return FCS_PARAMS


    def fscsi_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with attributes for FSCSI (fscsi) devices
        """
        FSCSI_PARAMS = []
        if self.GENERAL_SNAP:
            fscsilist = self.__snap_adapter_list('fcs')
            for i in range(len(fscsilist)):
                fscsilist[i] = replace(fscsilist[i], 'fcs', 'fscsi')
            for fscsi in fscsilist:
                fscsi_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El ' + fscsi)
                if fscsi_params:
                    FSCSI_PARAMS.append({'name' : fscsi, 'atname_1' : fscsi_params[0].split()[0],
                                         'atval_1' : fscsi_params[0].split()[1],
                                         'atname_2' : fscsi_params[1].split()[0],
                                         'atval_2' : fscsi_params[1].split()[1],
                                         'atname_3' : fscsi_params[2].split()[0],
                                         'atval_3' : fscsi_params[2].split()[1]})
        else:
            return None
        return FSCSI_PARAMS

    def vrtspack_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with list of Veritas (VRTS) packets and their versions
        """
        VRTS_PACKETS = []
        if self.GENERAL_SNAP:
            packet_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lslpp -lc')
            if packet_params:
                for packet in packet_params:
                    if 'VRTS' in packet:
                        VRTS_PACKETS.append({'lppname' : packet.split(":")[1], 'lppver' : packet.split(":")[2]})
        else:
            return None
        return VRTS_PACKETS

#    def smt_params_old(self):
#        """
#        Reads GENERAL_SNAP and returns DICT with smt threads count on system
#        """
#        SMT = {}
#        global_smt = True
#        temp_smt_active = ''
#        temp_smt_threads = ''
#        if self.GENERAL_SNAP:
#            for proc in self.__snap_proc_list():
#                proc_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El ' + proc)
#                if proc_params:
#                    if temp_smt_active == '':
#                        temp_smt_active = proc_params[1].split()[1]
#                        temp_smt_threads = proc_params[2].split()[1]
#                    else:
#                        if ( not temp_smt_active == proc_params[1].split()[1] ) or ( not temp_smt_threads ==
#                                                                                         proc_params[2].split()[1] ):
#                            global_smt = False
#            if global_smt:
#                if temp_smt_active == 'true':
#                    SMT.update({'smt_threads_count' : temp_smt_threads})
#                else:
#                    SMT.update({'smt_threads_count' : '0'})
#        else:
#            return None
#        return SMT

    def rmt_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with attributes of Tape Devices (rmt)
        """
        RMT = []
        if self.GENERAL_SNAP:
            lscfg_out = self.__snap_stanza_read(self.GENERAL_SNAP, 'lscfg -pv')
            if lscfg_out:
                for line in range(len(lscfg_out)):
                    if 'rmt' in lscfg_out[line]:
                        RMT.append({'name' : lstrip(lscfg_out[line].split()[0]),
                                    'vendor' : lstrip(lscfg_out[line+1].split('................')[1]),
                                    'type' : lstrip(lscfg_out[line+2].split('......')[1])})
        else:
            return None
        return RMT

    def sys0_params(self):
        """
        Reads GENERAL_SNAP and returns DICT with attributes for platform (sys0)
        """
        SYS0 = {}
        if self.GENERAL_SNAP:
            sys0_out = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El sys0')
            if sys0_out:
                SYS0.update({'plat_type' : sys0_out[27].split()[1].split(',')[1].split('-')[0]})
                SYS0.update({'plat_model' : sys0_out[27].split()[1].split(',')[1].split('-')[1]})
                SYS0.update({'plat_serial' : sys0_out[36].split()[1].split(',')[1]})
                SYS0.update({'atname_1' : sys0_out[24].split()[0]})
                SYS0.update({'atname_2' : sys0_out[28].split()[0]})
                SYS0.update({'atval_1' : sys0_out[24].split()[1]})
                SYS0.update({'atval_2' : sys0_out[28].split()[1]})
            else:
                return None
        else:
            return None
        return SYS0

    def mcodes_params(self):
        """
        Reads GENERAL_SNAP and returns LIST with microcode levels (lsmcode -A) for every physical device in system
        """
        MCODE = []
        if self.GENERAL_SNAP:
            mcode_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsmcode -A')
            if mcode_params:
                for mcode in range(len(mcode_params)):
                    if mcode_params[mcode].split('!')[0] == 'sys0':
                        MCODE.append({'mcode_devname' : mcode_params[mcode].split('!')[0], 'mcode_level' :
                            mcode_params[mcode].split(':')[1].split()[0]})
                    else:
                        MCODE.append({'mcode_devname' : mcode_params[mcode].split('!')[0], 'mcode_level' :
                            mcode_params[mcode].split('!')[1].split('.')[1]})
            else:
                return None
        else:
            return None
        return MCODE

    def limits_params(self):
        """
        Reads LIMITS and returns LIST for three type stanzas (default, root, oracle)
        """
        LIMITS = []
        if self.LIMITS:
            for user in ['default', 'root', 'oracle']:
                limits_stanza = self.__limits_stanza_read(self.LIMITS, user + ':')
                if limits_stanza:
                    curlimits = []
                    for limit in range(len(limits_stanza)):
                        curlimits.append({'limname' :  limits_stanza[limit].split()[0],
                            'limval' : limits_stanza[limit].split()[2]})
                    LIMITS.append({'username' : user, 'limitlist' : curlimits})
        else:
            return None
        return LIMITS

    def lpar_params(self):
        """
        Reads LPAR_SNAP and returns DICT with attributes for LPAR
        """
        LPAR = {}
        if self.LPAR_SNAP:
            conffile = self.LPAR_SNAP
            conffile.seek(0)
            LPAR.update({'lpar_nodename': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_name': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_number': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_type': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_mode': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_capacity': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            for i in range(3):
                conffile.readline()
            LPAR.update({'lpar_max_cpu': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_min_cpu': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            conffile.readline()
            LPAR.update({'lpar_max_mem': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_min_mem': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            for i in range(22):
                conffile.readline()
            LPAR.update({'lpar_des_cpu': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
            LPAR.update({'lpar_des_mem': conffile.readline().split(':')[1].lstrip().rstrip('\r\n')})
        else:
            return None
        return LPAR

    def adapters_params(self):
        """
        Reads ADAPTER_LIST and returns LIST with attributes for adapters (state, location code and description)
        """
        ADAPTERS = []
        a_count = 1
        if self.ADAPTER_LIST:
            conffile = self.ADAPTER_LIST
            conffile.seek(0)
            for line in conffile:
                ADAPTER = {}
                ADAPTER.update({'adapter_name': line.split()[0]})
                ADAPTER.update({'adapter_state': line.split()[1]})
                if ('EtherChannel' in line):
                    ADAPTER.update({'adapter_loc': ''})
                    descr = ''
                    for i in range(2, len(line.split())):
                        descr = descr + ' ' + line.split()[i]
                        ADAPTER.update({'adapter_desc': lstrip(descr)})
                else:
                    if ('Virtual' in line):
                        ADAPTER.update({'adapter_loc': line.split()[2]})
                        descr = ''
                        for i in range(3, len(line.split())):
                            descr = descr + ' ' + line.split()[i]
                            ADAPTER.update({'adapter_desc': lstrip(descr)})
                    else:
                        ADAPTER.update({'adapter_loc': line.split()[3]})
                        descr = ''
                        for i in range(4, len(line.split())):
                            descr = descr + ' ' + line.split()[i]
                            ADAPTER.update({'adapter_desc': lstrip(descr)})
                ADAPTERS.append(ADAPTER)
        else:
            return None
        return ADAPTERS

    def hdisk_params(self):
        """
        Reads DISK_LIST and returns LIST with hdisk types and total numbers of hdisks
        """
        DISKS = {}
        DISKS_WEB = []
        d_count = 1
        if self.DISK_LIST:
            conffile = self.DISK_LIST
            conffile.seek(0)
            for line in conffile:
                if DISKS == {}:
                    descr = ''
                    for i in range(4, len(line.split())):
                        descr = descr + ' ' + line.split()[i]
                    DISKS.update({'hdisk_type_' + str(d_count): lstrip(descr)})
                    DISKS.update({'hdisk_count_' + str(d_count): 1})
                    d_count += 1
                else:
                    disk_exists = False
                    descr = ''
                    for i in range(4, len(line.split())):
                        descr = descr + ' ' + line.split()[i]
                    for i in range(len(DISKS) / 2):
                        if  lstrip(descr) == DISKS['hdisk_type_' + str(i + 1)]:
                            DISKS['hdisk_count_' + str(i + 1)] += 1
                            disk_exists = True
                    if not disk_exists:
                        DISKS.update({'hdisk_type_' + str(d_count): lstrip(descr)})
                        DISKS.update({'hdisk_count_' + str(d_count): 1})
                        d_count += 1
        else:
            return None
        for i in range(d_count-1):
            DISKS_WEB.append({'hdisk_type' : DISKS['hdisk_type_'+str(i+1)],
                              'hdisk_count' : DISKS['hdisk_count_'+str(i+1)]})
        return DISKS_WEB

    def oslevel_params(self):
        """
        Reads OSLEVEL_SNAP and returns DICT with oslevel of system
        """
        OSLEVEL = {}
        if self.OSLEVEL_SNAP:
            self.OSLEVEL_SNAP.seek(0)
            self.OSLEVEL_SNAP.readline()
            line = self.OSLEVEL_SNAP.readline()
            OSLEVEL = {'oslevel': line.rstrip('\r\n')}
        else:
            return None
        return OSLEVEL

    def hacmp_params(self):
        """
        Reads HACMP_SNAP and retuns DICT with hacmp_used key
        """
        HACMP = {}
        if self.HACMP_SNAP:
            HACMP.update({'hacmp_used' : 1})
        else:
            HACMP.update({'hacmp_used' : 0})
        return HACMP

    def hostname_params(self):
        """
        Reads GENERAL_SNAP and returns DICT with hostname key
        """
        HOSTNAME = {}
        if self.GENERAL_SNAP:
            hostname_params = self.__snap_stanza_read(self.GENERAL_SNAP, 'lsattr -El inet0')
            if hostname_params:
                for record in hostname_params:
                    if 'hostname' in record:
                        HOSTNAME.update({'hostname' : record.split()[1]})
        else:
            return None
        return HOSTNAME

    def tunables_params(self):
        """
        Reads KERNEL_SNAP and returns LIST with non-default tunables from vmo,ioo,schedo sections (and some
        additional tunables like maxclient% etc.)
        """
        TUNABLES = []
        if self.KERNEL_SNAP:
            for tunname in ['vmo', 'ioo', 'schedo']:
                tun_params = self.__snap_stanza_read(self.KERNEL_SNAP, tunname + ' -FL')
                if tun_params:
                    tunable = False
                    for param in range(len(tun_params)):
                        if tunable:
                            if 'maxclient%' in tun_params[param]:
                                TUNABLES.append({'tun_name' : 'vmo_maxclient%',
                                                 'tun_value' : tun_params[param].split()[1]})
                            if (not 'n/a' in tun_params[param]) and (not 'Restricted' in tun_params[param])\
                            and (not 'maxclient%' in tun_params[param]):
                                if (len(tun_params[param].split()) > 1):
                                    if not tun_params[param].split()[1] == tun_params[param].split()[2]:
                                    #                                if 'maxclient%' in tun_params[param].split()[0]:
                                    #                                    TUNABLES.update({'tun_maxclient%' : tun_params[param].split()[1]})
                                        TUNABLES.append({'tun_name' : tun_params[param].split()[0],
                                                         'tun_value' : tun_params[param].split()[1]})
                                else:
                                    if not tun_params[param + 1].split()[0] == tun_params[param + 1].split()[1]:
                                        TUNABLES.append({'tun_name' : tun_params[param].split()[0],
                                                         'tun_value' : tun_params[param + 1].split()[0]})
                            tunable = False
                        if tun_params[param] ==\
                           '--------------------------------------------------------------------------------':
                            tunable = True
            vmstat_v = self.__snap_stanza_read(self.KERNEL_SNAP, 'vmstat -v')
            if vmstat_v:
                for record in vmstat_v:
                    if 'client filesystem I/Os blocked with no fsbuf' in record:
                        TUNABLES.append({'tun_name' : 'client_blocked_fsbufs',
                                         'tun_value' : lstrip(record).split()[0] })
                    else:
                        if ( 'filesystem I/Os blocked with no fsbuf' in record) and not ('external' in record):
                            TUNABLES.append({'tun_name' : 'fs_blocked_fsbufs',
                                             'tun_value' : lstrip(record).split()[0] })
        else:
            return None
        return TUNABLES

    def nfs_params(self):
        """
        Reads NFS_SNAP and returns LIST with list of all exported filesystems
        """
        NFS = []
        if self.NFS_SNAP:
            nfs_params = self.__snap_stanza_read(self.NFS_SNAP, 'exportfs')
            if nfs_params:
                for nfs_share in nfs_params:
                    NFS.append({'exportedfs' : nfs_share })
            else:
                return None
        else:
            return None
        return NFS

    def dns_params(self):
        """
        Read TCPIP_SNAP and returns DICT with DNS configuration
        """
        DNS = {}
        dns_serv_count = 1
        if self.TCPIP_SNAP:
            dns_params = self.__snap_stanza_read(self.TCPIP_SNAP, 'Name Server')
            if dns_params:
                for record in dns_params:
                    if 'nameserver' in record:
                        DNS.update({'dns_nameserver_' + str(dns_serv_count) : record.split()[1]})
                        dns_serv_count += 1
                    if 'domain' in record:
                        DNS.update({'dns_domain' : record.split()[1]})
                    if 'search' in record:
                        DNS.update({'dns_search' : record.split()[1]})
            else:
                return None
        else:
            return None
        return DNS

    def no_params(self):
        """
        Read TCPIP_SNAP and returns LIST with some of "no" parameters
        """
        NO = []
        if self.TCPIP_SNAP:
            no_params = self.__snap_stanza_read(self.TCPIP_SNAP, 'no -a')
            if no_params:
                for record in no_params:
                    if 'somaxconn' in record:
                        NO.append({'tun_name' : 'somaxconn', 'tun_value' : record.split('=')[1].lstrip()})
                    if 'sb_max' in record:
                        NO.append({'tun_name' : 'sb_max', 'tun_value'  : record.split('=')[1].lstrip()})
                    if 'tcp_ephemeral_high' in record:
                        NO.append({'tun_name' : 'tcp_ephemeral_high', 'tun_value' : record.split('=')[1].lstrip()})
                    if 'tcp_ephemeral_low' in record:
                        NO.append({'tun_name' : 'tcp_ephemeral_low', 'tun_value' : record.split('=')[1].lstrip()})
                    if 'udp_ephemeral_high' in record:
                        NO.append({'tun_name' : 'udp_ephemeral_high', 'tun_value' : record.split('=')[1].lstrip()})
                    if 'udp_ephemeral_low' in record:
                        NO.append({'tun_name' : 'udp_ephemeral_low', 'tun_value' : record.split('=')[1].lstrip()})
                    if 'tcp_recvspace' in record:
                        NO.append({'tun_name' : 'tcp_recvspace', 'tun_value' : record.split('=')[1].lstrip()})
                    if 'tcp_sendspace' in record:
                        NO.append({'tun_name' : 'tcp_sendspace', 'tun_value' : record.split('=')[1].lstrip()})
            else:
                return None
        else:
            return None
        return NO

    def hostsequiv_params(self):
        """
        Reads HEQUIV_SNAP and returns LIST with all equiv hosts
        """
        HOSTS_EQUIV = []
        if self.HEQUIV_SNAP:
            self.HEQUIV_SNAP.seek(0)
            for line in self.HEQUIV_SNAP:
                if not ( '#' in line):
                    HOSTS_EQUIV.append(line.rstrip('\r\n'))
        else:
            return None
        if HOSTS_EQUIV:
            return HOSTS_EQUIV

    def vg_params(self):
        """
        Reads LVM_SNAP and returns LIST with attributes for all volume groups
        """
        LVM = []
        if self.LVM_SNAP:
            vglist = self.__snap_stanza_read(self.LVM_SNAP, 'lsvg -o')
            if vglist:
                for vg in vglist:
                    VG = {}
                    tempfile = self.CWD + 'lvm/' + vg + '.snap'
                    if access(tempfile, R_OK):
                        vg_params = self.__snap_stanza_read(open(tempfile), 'lsvg ' + vg)
                        if vg_params:
                            for record in vg_params:
                                if 'VOLUME GROUP' in record:
                                    VG.update({'name' : record.split()[2]})
                                if 'VG STATE' in record:
                                    VG.update({'state' : record.split()[2]})
                                    VG.update({'pp_size' : record.split()[5] + ' ' + record.split()[6]})
                                if 'FREE PPs' in record:
                                    VG.update({'free_size' : record.split()[5]})
                                if 'TOTAL PVs' in record:
                                    VG.update({'totalpv' : record.split()[2]})
                                if 'AUTO ON' in record:
                                    VG.update({'activepv' : record.split()[2]})
                                    VG.update({'auto' : record.split()[5]})
                            LVM.append(VG)
                    else:
                        print "cannot access vg - " + vg
            else:
                return None
        else:
            return None
        return LVM

    def lv_params(self):
        """
        Reads LVM_SNAP and FS_SNAP and returns LIST with attributes for all logical volumes
        """
        ALLLV = []
        if self.LVM_SNAP:
            vglist = self.__snap_stanza_read(self.LVM_SNAP, 'lsvg -o')
            if vglist:
                for vg in vglist:
                    LVS = []
                    tempfile = self.CWD + 'lvm/' + vg + '.snap'
                    if access(tempfile, R_OK):
                        lv_params = self.__snap_stanza_read(open(tempfile), 'lsvg -l ' + vg)
                        if lv_params:
                            for record in lv_params:
                                LV = {}
                                if not ('LV NAME' in record) and not (vg+':' in record):
                                    LV.update({'name' : record.split()[0]})
                                    LV.update({'type' : record.split()[1]})
                                    if record.split()[2] == record.split()[3]:
                                        LV.update({'copies' : '1'})
                                    else:
                                        if (int(record.split()[3])/int(record.split()[2])) == 2:
                                            LV.update({'copies' : '2'})
                                        else:
                                            LV.update({'copies' : 'N/A'})
                                    LV.update({'state' : record.split()[5]})
                                    LV.update({'mount' : record.split()[6]})
                                    LVS.append(LV)
                            ALLLV.append({'volgroup' : vg , 'volumes' : LVS})
                    else:
                        print "cannot access vg - " + vg
            else:
                return None
        else:
            return None
        if self.FS_SNAP:
            df_params = self.__snap_stanza_read(self.FS_SNAP, 'df -k')
            if df_params:
                for vg in ALLLV:
                    for lv in vg['volumes']:
                        lv.update({'mounted' : 'No', 'used' : 'N/A', 'iused' : 'N/A'})
                for vg in ALLLV:
                    for lv in vg['volumes']:
                        for record in df_params:
                            if '/dev/'+lv['name'] in record:
                                lv.update({'mounted' : 'Yes', 'used' : record.split()[3], 'iused' : record.split()[5]})
        return ALLLV

    def smt_params(self):
        """
        Reads GENERAL_SNAP and returns DICT with smt threads count on system
        """
        cpucount = 0
        SMTLIST = []
        SMT = {}
        if self.GENERAL_SNAP:
            self.GENERAL_SNAP.seek(0)
            while True:
                CUR_SMT = {}
                line = self.GENERAL_SNAP.readline()
                if not line:
                    break
                if 'smt_enabled' in line:
                    CUR_SMT.update({'smt_enabled' : line.split()[1]})
                    line = self.GENERAL_SNAP.readline()
                    CUR_SMT.update({'smt_threads' : line.split()[1]})
                    if len(SMTLIST) > 0:
                        for item in SMTLIST:
                            if not(item == CUR_SMT):
                                SMTLIST.append(CUR_SMT)
                    else:
                        SMTLIST.append(CUR_SMT)
                    cpucount += 1
            if (cpucount == len(self.__snap_proc_list())) and (len(SMTLIST) == 1):
                if SMTLIST[0]['smt_enabled'] == True:
                    SMT.update({'smt_threads_count' : SMTLIST[0]['smt_threads']})
                else:
                    SMT.update({'smt_threads_count' : '0'})
        else:
            return None
        return SMT

    def __snap_stanza_read(self, conffile, key):
        """
        Reads stanza of data with specific conditions to snap output and returns LIST of lines
        """
        stanza = []
        conffile.seek(0)
        while True:
            line = conffile.readline()
            if not line:
                break
            if key in line:
                conffile.readline()
                nextline = conffile.readline()
                while ( not '.....\n' == nextline ) or ( not nextline ):
                    if not nextline.rstrip('\r\n') == '':
                        stanza.append(nextline.rstrip('\r\n'))
                    if not nextline:
                        break
                    nextline = conffile.readline()
                break
        if stanza == []:
                return None
        else:
            return stanza

    def __snap_adapter_list(self, adapter):
        """
        Reads ADAPTER_LIST and returns LIST with adapter = adapter
        """
        ADAPTERS = []
        if self.ADAPTER_LIST:
            self.ADAPTER_LIST.seek(0)
            for line in self.ADAPTER_LIST:
                if adapter in line:
                    ADAPTERS.append(line.split()[0])
            return ADAPTERS
        else:
            return None


    def __snap_proc_list(self):
        """
        Reads PROCESSOR_LIST and returns LIST with procs
        """
        PROCESSORS = []
        if self.PROCESSOR_LIST:
            self.PROCESSOR_LIST.seek(0)
            for line in self.PROCESSOR_LIST:
                if 'proc' in line:
                    if not 'The available' in line:
                        PROCESSORS.append(line.split()[0])
            return PROCESSORS
        else:
            return None


    def __limits_stanza_read(self, conffile, user):
        """
        Reads stanza of limits output and returns LIST with lines
        """
        stanza = []
        conffile.seek(0)
        while True:
            line = conffile.readline()
            if not line:
                break
            if user in line:
                nextline = conffile.readline()
                while ( not ':' in nextline ) or ( not nextline ):
                    if not nextline.rstrip('\r\n').lstrip('\t') == '':
                        stanza.append(nextline.rstrip('\r\n').lstrip('\t'))
                    if not nextline:
                        break
                    nextline = conffile.readline()
                break
        if stanza == []:
            return None
        else:
            return stanza