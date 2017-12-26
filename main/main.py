'''
Created on 27 Mar 2017
Edited on 25 Dec 2017

@author: Ethan Prentice
'''
import os
import re
import inspect
import requests
from selenium import webdriver
import selenium.common.exceptions


# Initiates driver with args
def get_driver(c_dir: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    return webdriver.Chrome(executable_path=c_dir + '/chromedriver.exe', chrome_options=chrome_options)


# Scrapes the web page to get the URL of the raw .mp4 file
def get_video_url(url: str, driver: webdriver.Chrome) -> str:
    try:
        print("Fetching HTML")
        driver.get(url)
        print("Fetching iFrame data")
        driver.switch_to.frame(driver.find_elements_by_xpath('//*[@id="body"]/iframe')[0])
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="video"]/iframe'))
        script_text = driver.find_element_by_xpath('/html/body/script[4]').get_attribute("innerHTML")

        mp4_url = re.findall("https://[^\"]*.mp4[^\"]*", script_text)[0]

        return mp4_url

    except selenium.common.exceptions.WebDriverException:
        print(f"Error connecting to webpage {url}")
        return ""
    except IndexError:
        print(f"No MP4 for this URL was found {url}")
        return ""
    except Exception as e:
        print(f"An unknown error occured, {e}")
        return ""


def download_file(url, download_dir):
    print("\nDownloading File...")

    # Downloads video to directory in 1 megabyte chunks
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(download_dir, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    print(f"MP4 Downloaded to {download_dir}", end='\n\n')


# Asks user for directory to save the videos to
def get_save_directory(directory):
    save_name = input("File Name: ")
    if not re.match(".*.mp4", save_name, re.I):
        save_name += ".mp4"
    return directory + "/" + save_name


# Checks if the filesystem contains the given save directory
def does_dir_exist(directory):
    if os.path.isdir(directory):
        return True
    else:
        create_dir = input("Directory does not exist. Create directory? (y/n): ")
        if create_dir is not 'y':
            return False
        else:
            os.makedirs(directory)
            print("Directory Created.")
            return True


def main():
    os.system('cls')
    print("Loading Drivers")
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    driver = get_driver(current_dir)

    # Gets recommended download directory
    recommended_dir = str(os.path.expanduser('~/Videos') + "/4917").replace("\\", "/")
    print(f"Example Directory: {recommended_dir}")
    base_dir = input("Save Directory: ")

    if not does_dir_exist(base_dir):
        exit(-1)

    finished = False
    while not finished:
        os.system('cls')
        print(f"Current Directory: {base_dir}")
        file_dir = get_save_directory(base_dir)

        base_url = input("URL: ")

        mp4_url = get_video_url(url=base_url, driver=driver)
        if mp4_url is not False:
            download_file(url=mp4_url, download_dir=file_dir)

        finished_input = input("More URLs? (y/n): ")
        if finished_input != 'y':
            finished = True

    print("\nExiting Application")
    driver.quit()


main()
