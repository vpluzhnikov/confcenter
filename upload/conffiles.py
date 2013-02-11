__author__ = 'vs'

from upload.models import Oses, OsTypes
from subprocess import Popen
from os import mkdir, access, R_OK, listdir
from confcenter.settings import UPLOAD_DIR, AIX_ARCHIVER, AIX_ARCHIVER_ARGS, SOLARIS_ARCHIVER, SOLARIS_ARCHIVER_ARGS
from logging import getLogger
from confcenter.common import whoami
from os import remove

logger = getLogger(__name__)

def handle_uploaded_file(file, name, ostype):
    """
        Function handle_uploaded_file(f, name, ostype) saves file f to UPLOAD_DIR and returns DICT(filetype, archpath, filename)
    """
    logger.info("Starting handling of a file %s in %s" % (name, whoami()))
    with open( UPLOAD_DIR + name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    if (ostype == '0'):
        fileattrs = detect_filetype(file, name)
        if not fileattrs == None:
            logger.info("File type %s is detected as %s" % (name, fileattrs['filetype']))
            fileattrs.update({'filename':name})
            fileattrs.update({'dumpfilename' : UPLOAD_DIR + name + "." + fileattrs['filetype'] + ".confdump"})
            remove(UPLOAD_DIR + name)
            return fileattrs
        else:
            logger.info("File type %s is not valid" % (name))
            remove(UPLOAD_DIR + name)
            return fileattrs
    else:
        fileattrs = validate_filetype(f, name, ostype)
        if not fileattrs == None:
            logger.info("File type %s is validated as %s" % (name, fileattrs['filetype']))
            fileattrs.update({'filename':name})
            remove(UPLOAD_DIR + name)
            return fileattrs
        else:
            logger.info("File type %s is not valid" % (name))
            remove(UPLOAD_DIR + name)
            return fileattrs


def detect_filetype(f, name):
    """
        Function detect_filetype(f, name) tries to detect file type and returns DICT(filetype, archpath)
    """
    SysType = is_Solaris(f, name)
    if not SysType == None:
        return {'filetype' : 'Solaris', 'archpath' : SysType}
    else:
        SysType = is_AIX(f, name)
        if not SysType == None:
            return {'filetype' : 'AIX', 'archpath' : SysType}
        else:
            return None


def validate_filetype(f, name, ostype):
    """
        Function validate_filetype(f, name, ostype) tries to validate if file f is correct configuration
        output for selected type and returns DICT(filetype, archpath)
    """
    Os = Oses.objects.get(id = int(ostype))
    if ( 'Solaris' in Os.ostypes.os_name ):
        SysType = is_Solaris(f, name)
        if  SysType == None:
            return None
        else:
            return {'filetype' : 'Solaris', 'archpath' : SysType}
    else:
        if ( 'AIX' in Os.ostypes.os_name ):
            SysType = is_AIX(f, name)
            if SysType == None:
                return None
            else:
                return {'filetype' : 'AIX', 'archpath' : SysType}
        else:
            print 'This OS not supported yet'
            return None


def is_Solaris(f, name):
    """
        Function is_Solaris(f, name) tries to validate if file f is Solaris configuration
        output and returns CWD for archive
    """
    if ( 'explorer' in name) or ( 'tar.gz' in name ):
        return try_unpack_file(f, 'Solaris', name)
    else:
        return None


def is_AIX(f, name):
    """
        Function is_AIX(f, name) tries to validate if file f is AIX configuration
        output and returns CWD for archive
    """
    if ( 'snap' in name) or ( 'pax' in name ):
        return try_unpack_file(f, 'AIX', name)
    else:
        return None


def try_unpack_file(f, type, name):
    """
        Function try_unpack_file(f, type, name) tries to unpack file f, test output and returns archive CWD
    """
    CWD = UPLOAD_DIR + name + "_" + type + "/"
    try:
        mkdir(CWD)
    except OSError:
        print "Directory is already exists"
    if ( type == 'Solaris' ):
        tarlist = Popen([SOLARIS_ARCHIVER, SOLARIS_ARCHIVER_ARGS, UPLOAD_DIR + name], cwd=CWD, stdout=0, stderr=0)
        if not tarlist.wait():
            sollist = listdir(CWD)
            if ('explorer' in sollist[0] ):
                CWD = CWD + sollist[0] + '/'
                if access(CWD + 'README', R_OK):
                    return CWD
                else:
                    return None
            else:
                return None
    if ( type == 'AIX' ):
        tarlist = Popen([AIX_ARCHIVER, AIX_ARCHIVER_ARGS, UPLOAD_DIR + name], cwd=CWD, stdout=0, stderr=0)
        if not tarlist.wait():
            if access(CWD + '/general/general.snap', R_OK):
                return CWD
            else:
                return None
        else:
            return None