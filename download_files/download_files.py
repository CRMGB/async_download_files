import requests
import os

class Genie:
    def __init__(self):
        self.full_path = os.path.abspath("genie")
        self.headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
        self.read_text_file()

    def read_text_file(self):
        with open(self.full_path+"/images_to_download.txt") as f:
            lines = f.readlines()

    def download_images(self, lines):
        print("\nPlease input the name of the folder to save the files:")
        down_dir = input()
        directory = self.create_dir(down_dir)
        path = directory +"/"+"image.png"
        for image in lines:
            request_img = requests.get(str(image.rstrip()), headers=self.headers)
            with open(path,'wb') as f:  
                f.write(request_img.content)

init = Genie()
