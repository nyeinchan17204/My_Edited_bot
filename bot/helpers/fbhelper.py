from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from urllib.error import HTTPError
from pySmartDL import SmartDL
from tqdm import tqdm
import sys
import requests
import time
import os
import wget


def dlink_finder(url):
    op = webdriver.ChromeOptions()
    op.headless = True
    driver_link = Service("C:/Users/Moe Nya/Documents/New_folder/chromedriver.exe")
    fb_link = url
    result = ""
    driver = webdriver.Chrome(service=driver_link)
    driver.get("https://fdown.net/")
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='URLz']"))
    )

    search_box.clear()
    search_box.send_keys(fb_link)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)
    try:
        sd_link = driver.find_element(By.XPATH, '//*[@id="sdlink"]')
        sd_link = sd_link.get_attribute("href")
    except NoSuchElementException:
        sd_link = ""
    print(len(sd_link) > 0)

    try:
        hd_link = driver.find_element(By.XPATH, '//*[@id="hdlink"]')
        hd_link = hd_link.get_attribute("href")
    except NoSuchElementException:
        hd_link = ""
    print(len(hd_link) > 0)

    driver.close()
    if len(hd_link) > 1:
        result = sd_link
        return result
    elif len(sd_link) > 1:
        result = sd_link
        return result
    else:
        result = "Link is Not Downloadable!!"
        return result


def download_fb(url, dl_path):
    try:
        filename = wget.download(url, dl_path)
        return True, os.path.join(f"{dl_path}/{filename}")
    except HTTPError as error:
        return False, error


def download_file(url, dl_path):
    try:
        dl = SmartDL(url, dl_path, progress_bar=True)
        dl.start()
        return True, dl.get_dest()
    except HTTPError as error:
        return False, error
    except Exception as error:
        try:
            filename = wget.download(url, dl_path)
            return True, os.path.join(f"{dl_path}/{filename}")
        except HTTPError:
            return False, error


def download_witprogress(url, dl_path):
    chunk_size = 1024
    r = requests.get(url, stream=True)
    total_size = int(r.headers["content-length"])
    with open(dl_path, "wb") as f:
        for data in tqdm(
            iterable=r.iter_content(chunk_size=chunk_size),
            total=total_size / chunk_size,
            unit="KB",
        ):
            f.write(data)
    print("Download Completed!")
