from doctest import Example
import requests
import os
import asyncio
import time

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
        self.download_images(lines)

    def download_images(self, lines):
        print("\nPlease input the name of the folder to save the files:")
        down_dir = input()
        directory = self.create_dir(down_dir)
        for image in lines:
            path = directory +"/"+f"{image.rsplit('/', 1)[-1]}.png"
            request_img = requests.get(str(image), headers=self.headers)
            try:
                if request_img.status_code != 200:
                    raise ValueError(f"status code: {request_img.status_code}")
            except ValueError as err:
                print(f"There was a problem trying to download the image, {err}")
            self.save_images(path, request_img)
    
    def save_images(self, path, request_img):
        with open(path,'wb') as f:  
            f.write(request_img.content)


    def create_dir(self, down_dir):
        if not os.path.exists(down_dir):
            os.mkdir(down_dir)
            print("Directory " , down_dir ,  " Created ")
            return down_dir
        else:    
            print("Directory " , down_dir ,  " already exists")

init = Genie()