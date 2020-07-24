from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

WINDOW = "1920,1080"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=%s' %WINDOW)

headless_browsers = []
chrome_instances = 5

for i in range(chrome_instances):
    driver= webdriver.Chrome(chrome_options=chrome_options)
    headless_browsers.append(driver)


class ImageDownloader:
    """
        ImageDownloader class will create chrome brower instances.
        It will load the webpages from the urls list and save a ss in temp folder
    """
    def __init__(self):
        self.urlsMapper = {}
        self.count = 0
        self.mapper = {}

    def addUrl(self, url):
        filename =  datetime.now().isoformat()+".png"
        self.mapper[filename] = False
        self.urlsMapper[filename] = url
        res = self.getImage(filename)
        if(res == "error"):
            return res
        del self.mapper[filename]
        del self.urlsMapper[filename]
        return "/static/temp/"+filename
    
    def getImage(self, filename):
        driver = headless_browsers[self.count % chrome_instances]
        self.count+=1
        current_url = self.urlsMapper[filename]
        if not current_url.startswith('http'):
            return 'error'
        driver.get(current_url)
        driver.save_screenshot(os.path.join('static','temp',filename))
        self.mapper[filename] = True
        return True

    def removeOldFiles(self):
        currentTimeStamp = datetime.now().timestamp()
        with os.scandir('static/temp') as s:
            for file in s:
                lastModified = os.path.getmtime(file)
                diff = currentTimeStamp - lastModified
                if((diff/(24*60*60)) > 1):
                    os.remove(file)
                    print(file)

    def getCount(self):
        return self.count

if __name__=="__main__":
    i = ImageDownloader()
    i.removeOldFiles()
            
