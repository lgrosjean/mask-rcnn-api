import os
import sys
import argparse

import urllib.request
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import time
from time import sleep

import json

IMAGES_PATH = "download/"
if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

class ChromeDriver():

    def __init__(self):
        
        if not "chromedriver.exe" in os.listdir("."):
            chromedriver_url = "https://chromedriver.storage.googleapis.com/2.41/chromedriver_win32.zip"
            urllib.request.urlretrieve(chromedriver_url, "./data/chromedriver.exe")

        self.path_to_web_driver = "./data/chromedriver.exe"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        self.driver = webdriver.Chrome(
            executable_path=self.path_to_web_driver,
            chrome_options=self.options)

    def get(self, url):
        self.driver.get(url)

class GoogleImageScraper():

    def __init__(self):
        # We initialize the driver for scraping and get the url data
        self.driver = ChromeDriver()
    
    def fit(self, word, number=200):
        self.word = word
        self.number = number
        
        # Number_of_scrolls * 400 images will be opened in the browser
        number_of_scrolls = int(number / 400 + 1)

        # Create the image downloaded folder : replace space with undescorces
        self.word_ = word.replace(" ", "_")
        self.image_path = os.path.join(IMAGES_PATH, self.word_)

        # The google image generated url with the requested word to search
        url = "https://www.google.co.in/search?q=" + word + "&source=lnms&tbm=isch"
        
        self.driver.get(url)

        # Prepare Google Page
        for _ in range(number_of_scrolls):
            for __ in range(10):
                # Multiple scrolls needed to show all 400 images
                self.driver.driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(0.2)
            # to load next 400 images
            time.sleep(2.5)
            try:
                self.driver.driver.find_element_by_xpath(
                    "//*[@id='smb']").click()

                #driver.driver.find_element_by_xpath(
                #   "//input[@value='Show more results']").click()
                time.sleep(2.5)
            except Exception as e:
                print("Less images found:" + str(e))
                break

        img_list = self.driver.driver.find_elements_by_xpath(
                '//div[contains(@class,"rg_meta")]')

        self.img_list = img_list

    def get_images(self):
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)
            print("{} folder created.".format(self.image_path))
        else:
            print("{} folder already created.".format(self.image_path))
            
        i_downloaded = 0
        for i in range(min(self.number, len(self.img_list))):
            img = self.img_list[i]
            img_name = self.word_ + str(i)
            img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
            img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
            img_path = os.path.join(self.image_path, img_name + "." + img_type)

            try:

                if img_type in ["jpg", "jpeg"]:
                    urllib.request.urlretrieve(img_url, img_path)
                    i_downloaded+=1

            except HTTPError:
                pass

            except URLError:
                pass

            sys.stdout.write("\rDownloading: {}/{}".format(i_downloaded, self.number))
            sys.stdout.flush()
            
    def fit_get(self, word, number=200):
        
        self.fit(word, number)
        self.get_images()

if __name__=="__main__":
    ggscraper = GoogleImageScraper()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--words', nargs='+')

    # for _, value in parser.parse_args()['words']:
    #     if value is not None:
    #         print(value)