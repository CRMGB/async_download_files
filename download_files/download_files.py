import os
import asyncio
import aiohttp
import aiofiles
import tqdm
from download_files.retry_connection.retry_connection import retry

class Genie:
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }
        self.file_urls = os.path.abspath("download_files/file_urls/images_to_download.txt")

    def read_text_file(self, file=None):
        """ Simple method to read the file with the urls in them.
        For the purpose of testing we might pass the file it as a parameter.
        """
        try:
            if file != None:
                self.file_urls = file
            with open(self.file_urls) as f:
                lines = f.readlines()
        except ValueError:
            print("Error reading the file.")
        dir = self.create_dir()
        asyncio.run(self.download_images(lines, dir))

    async def download_images(self, lines, dir):
        """Main method to download where aiohttp and asyncio are doing the job.
        we're relying on task for every file we download.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(self.save_images(session, dir, image_url)) 
                for image_url in lines
            ]
            try:
                [
                    await f for f 
                    in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))
                ]
                await asyncio.gather(*tasks)
                print("Download terminated!")
            except KeyboardInterrupt:
                print("Received exit by CTRL+C, exiting")

    @retry(
        aiohttp.ServerDisconnectedError, aiohttp.ClientError,
        aiohttp.ClientHttpProxyError
    )
    async def save_images(self, session, dir, resp_img):
        """ Method which will make the async request. It will call the method 
        raise_except_if_not_200 if the response is not 200 as the name shows.
        """
        path = dir +"/"+f"{resp_img.rsplit('/', 1)[-1]}.png"
        async with session.get(str(resp_img), headers=self.headers) as response:
            await self.raise_except_if_not_200(response)
            f = await aiofiles.open(path, mode='wb')
            await f.write(await response.read())
            await f.close()      

    def create_dir(self):
        """ Sinple method just to create a directory for the user to save the
        files. I would improve it asking to the user for deletion of older 
        folders+files and able to select which file to download.
        """
        print("\nPlease input the name of the folder to save the files to:")
        down_dir = input()        
        if not os.path.exists(down_dir):
            os.mkdir(down_dir)
            print("Directory " , down_dir ,  " Created ")
            return down_dir
        else:
            print(f"INFO: the directory already exists, will write to: {down_dir}")
        return down_dir

    async def raise_except_if_not_200(self, response):
        try:
            if response.status != 200:
                raise ValueError(f"status code: {response.status}")
        except asyncio.CancelledError as e:
            print(f"ERROR! There was a problem trying to download the image: {response.status}")


if __name__ == '__main__':
    init = Genie()
    init.read_text_file()
