Write a Python script that downloads files from the internet and saves them in a download directory.


The list of URLs to download will be provided in a simple text file. URLs are separated by a newline. Assume that the files are small, so downloading them does not require streaming.


Input.txt:

https://cdn-9.motorsport.com/images/mgl/24vA3r46/s500/max-verstappen-red-bull-racing-1.webp

https://cdn-8.motorsport.com/images/mgl/24vA4nA6/s500/daniel-ricciardo-mclaren-1.webp

https://cdn-8.motorsport.com/images/mgl/0L1nLWJ2/s500/lando-norris-mclaren-1.webp


The download directory should be provided as a command line parameter.


Consider the following and implement reasonable solutions for the following problems:


How to handle HTTP 404 errors?
- Try catch performed in the method raise_except_if_not_200() to catch if it's not 200 and displays the status code.

How to make the download process faster?
- Using the asyncronous libraries asyncio, aiohttp and aiofiles mentioned bellow to install. more details: 
https://betterprogramming.pub/asynchronous-programming-in-python-for-making-more-api-calls-faster-419a1d2ee058

How to display the progress of downloads?
- Using asyncio.as_completed inbuilt function from asyncio to display the tasks finished so it optimises the download we are using asynchronously aiohttp.ClientSession instead of using the typical requests library from python.

How to handle cancellation? (i.e., the user presses CTRL+C)
- Just with a try-catch in the download_images() method, I just wanted an easy solution here. Only downside from my perspective? Is that downloading is too fast so you'll be lucky to stop it, maybe you need larger files or a time.sleep() whih I don't like to implement usually.

Optional: How to handle retry in case of intermittent network errors?
- I've implemented a wrapper method to the download_images() method in download_files.py. It is a separated method in a file called: retry_connection.py. It has got doc strings with a description on top.

INSTALLATION:

We assume you've got pip installed and python 3.8 or higher, the SO used is ubuntu but there shoulnd't be any problemns using another SO because of the virtual environment.
    
    To install & setup the virtual environment:
        - pip3 install virtualenv
        - python3.8 -m venv env
        - source env/bin/activate
        - pip list (to check it's working)
    
    Another pip packages once the virtual env is installed:
        - pip install requests
        - pip install aiohttp
        - pip install aiofiles
        - pip install tqdm
        - pip install multidict

Finally you can just run the command: 
    - python download_files/download_files.py
