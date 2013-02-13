from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache
from logging import getLogger
from common import whoami
from time import sleep

class UploadProgressCachedHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, 'X-Progress-ID'
    which should contain a unique string to identify the upload to be tracked.
    """

    def __init__(self, request=None):
        super(UploadProgressCachedHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None
        self.logger = getLogger(__name__)

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        if 'X-Progress-ID' in self.request.GET:
            self.logger.debug("Starting proccessing file with ID = %s in %s" % (self.request.GET['X-Progress-ID'],
                                                                                whoami()) )
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET:
            self.progress_id = self.request.GET['X-Progress-ID']
            self.logger.debug('X-Progress-ID exists and equals = %s' % (self.progress_id))
        elif 'X-Progress-ID' in self.request.META:
            self.progress_id = self.request.META['X-Progress-ID']
            self.logger.debug('X-Progress-ID exists and equals = %s' % (self.progress_id))
        if self.progress_id:
            self.cache_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], self.progress_id )
            cache.set(self.cache_key, {
                'length': self.content_length,
                'uploaded' : 0
            })
            self.logger.debug('Cache key is set to %s and data uploaded 0', self.cache_key)

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        if self.cache_key:
            sleep(0.003)
            data = cache.get(self.cache_key)
            data['uploaded'] += self.chunk_size
            cache.set(self.cache_key, data)
#            self.logger.info('Data is now equals %s' % (data_new['uploaded']))
        return raw_data

    def file_complete(self, file_size):
        pass

    def upload_complete(self):
        self.logger.debug('Upload complete')
#        if self.cache_key:
        #            cache.delete(self.cache_key)
#            self.logger.info('Cache key is deleted')