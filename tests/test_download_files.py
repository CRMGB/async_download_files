import asyncio
import os
import unittest
import sys
import warnings
from download_files.download_files import Genie
from aiohttp.client import ClientSession
from mock import patch


class DownloadFilesTests(unittest.TestCase):
    def setUp(self):
        if not sys.warnoptions:
            warnings.simplefilter("ignore")        
        self.full_path = os.path.abspath("images_to_download")
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.run = self.loop.run_until_complete
        self.init_genie = Genie()

    async def call_asyncio(self, dir, resp_img):        
        session = ClientSession(
            headers=[("h1", "header1"),
                     ("h2", "header2"),
                     ("h3", "header3")],
            loop=self.loop)        
        await self.init_genie.save_images(session, dir, resp_img)
        await session.close()

    def test_read_file_is_not_present(self):
        """ Test it will raise an error if the directory is not valid"""
        file = os.path.abspath("tests/test_folder/no_file")
        with self.assertRaises(IsADirectoryError):
            self.init_genie.read_text_file(file)

    @patch('download_files.retry_connection.retry_connection')
    async def test_status_200_calling_save_images_method(self, MockRetry):
        """ Test the save_images() method works perfectly. 
            After a successfull 200 response will use the same line as 
            the one in the save_images method to determine the file exists.
        """
        dir = os.path.abspath("tests/test_folder")
        resp_img = "https://cdn-8.motorsport.com/images/mgl/0L1nLWJ2/s500/lando-norris-mclaren-1.webp"
        
        await self.loop.run_until_complete(self.call_asyncio(dir, resp_img))
        path = dir +"/"+f"{resp_img.rsplit('/', 1)[-1]}.png"
        self.assertTrue(os.path.exists(path))

    @patch('download_files.retry_connection.retry_connection')
    async def test_status_403_and_exception_when_file_name_is_worng_calling_save_images_method(self, MockRetry):
        """ We force the method save_images() to return 403 when the url is incorrect"""
        dir = os.path.abspath("test_folder")
        resp_img = "https://cdn-9.motorsport.com/images/mgl/24vA3r46/s500/test_1"
        with self.assertRaises(ValueError):
            await self.loop.run_until_complete(self.call_asyncio(dir, resp_img))
