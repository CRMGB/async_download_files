import os
import asyncio
import aiohttp
import aiofiles
import sys

class Genie:
    def __init__(self):
        self.full_path = os.path.abspath("download_files")
        self.headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
        self.read_text_file()

    def read_text_file(self):
        try:
            with open(self.full_path+"/images_to_download.txt") as f:
                lines = f.readlines()
        except ValueError:
            print("Error reading the file.")
        asyncio.run(self.download_images(lines))

    async def download_images(self, lines):
        directory = self.create_dir()
        async with aiohttp.ClientSession() as session:
            for image in lines:
                # Handle when a directory already e
                path = directory +"/"+f"{image.rsplit('/', 1)[-1]}.png"
                async with session.get(str(image), headers=self.headers) as response:
                    print("response---> ", response)
                    self.raise_except_if_not_200(response)
                    await self.save_images(path, response)
    
    async def save_images(self, path, request_img):
        f = await aiofiles.open(path, mode='wb')
        await f.write(await request_img.read())
        await f.close()

    def create_dir(self):
        print("\nPlease input the name of the folder to save the files:")
        down_dir = input()        
        if not os.path.exists(down_dir):
            os.mkdir(down_dir)
            print("Directory " , down_dir ,  " Created ")
            return down_dir
        else:
            print(f"INFO: the directory already exists, will write to: {down_dir}")
        return down_dir

    def raise_except_if_not_200(self, response):
        try:
            if response.status != 200:
                raise ValueError(f"status code: {response.status}")
        except ValueError as err:
            print(f"ERROR! There was a problem trying to download the image, {err}")

init = Genie()