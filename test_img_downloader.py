import os
import unittest
from image_downloader import get_path_and_filename_from_url, download_image

URL_VALID = 'http://www.digimouth.com/news/media/2011/09/google-logo.jpg?abc=asdsad&sads=asdsa'
URL_VALID_WO_PARAMS = 'http://docs.python.org/3/_static/py.png'
URL_INVALID = 'http://asadad'
URL_INVALID_WO_HTTP = 'helloworld'
URL_EMPTY = ''


class TestImage(unittest.TestCase):
    def test_path_from_url(self):
        valid_path = 'www.digimouth.com/news/media/2011/09/'.replace('/', os.path.sep)
        valid_wo_http = 'docs.python.org/3/_static/'.replace('/', os.path.sep)

        self.assertEqual(get_path_and_filename_from_url(URL_VALID), (valid_path, 'google-logo.jpg'))
        self.assertEqual(get_path_and_filename_from_url(URL_VALID_WO_PARAMS), (valid_wo_http, 'py.png'))
        self.assertEqual(get_path_and_filename_from_url(URL_INVALID), (os.path.sep, 'asadad'))
        self.assertEqual(get_path_and_filename_from_url(URL_EMPTY), ('', ''))

    def test_download_image(self):
        self.assertEqual(download_image(URL_VALID, 'google-logo.jpg'), True)
        self.assertEqual(download_image(URL_VALID_WO_PARAMS, 'py.png'), True)
        self.assertEqual(download_image(URL_INVALID, ''), False)
        self.assertEqual(download_image(URL_INVALID_WO_HTTP, ''), False)
        self.assertEqual(download_image(URL_EMPTY, ''), False)


if __name__ == '__main__':
    unittest.main()
