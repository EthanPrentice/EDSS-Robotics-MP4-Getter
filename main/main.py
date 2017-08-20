'''
Created on 27 Mar 2017
Edited on 18 Aug 2017

@author: Ethan Prentice
'''
import os,re,inspect
import urllib
from selenium import webdriver

def get_driver(current_dir):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless");
    return webdriver.Chrome(executable_path=current_dir+'/chromedriver.exe',chrome_options=chrome_options)

def get_video_url(url, driver):
    try:
        print "Fetching HTML"
        driver.get(url)
        print "Fetching iFrame data"
        driver.switch_to.frame(driver.find_elements_by_xpath('//*[@id="body"]/iframe')[0])
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="video"]/iframe'))
        script_text = driver.find_element_by_xpath('/html/body/script[4]').get_attribute("innerHTML")
        
        mp4_url = re.findall("https://[^\"]*.mp4[^\"]*", script_text)[0]
        
        return mp4_url
    
    except Exception:
        print "No MP4 for this URL was found %s" % url
        return False
        
def download_file(url, file_dir):
    print "\nDownloading File..."
    testfile = urllib.URLopener()
    testfile.retrieve(url, file_dir)
    print "MP4 Downloaded to %s\n" % file_dir
    
def get_save_directory(base_dir):
    save_name=raw_input("File Name: ")
    if not re.match(".*.mp4", save_name, re.I):
        save_name+=(".mp4")
    return base_dir+"/"+save_name

def does_dir_exist(base_dir):
    if os.path.isdir(base_dir):
        return True
    else:
        create_dir = raw_input("Directory does not exist. Create directory? (y/n): ")
        if create_dir is not 'y':
            return False
        else:
            os.makedirs(base_dir)
            print "Directory Created."
            return True

os.system('cls')
print "Loading Drivers."
current_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
driver = get_driver(current_dir)

recommended_dir=str(os.path.expanduser('~/Videos')+"/4917").replace("\\","/")
print "Example Directory: %s" % recommended_dir
base_dir=raw_input("Save Directory: ")

if not does_dir_exist(base_dir):
    exit(0)

finished=False
while not finished:
    os.system('cls')
    print "Current Directory: %s" % base_dir
    file_dir=get_save_directory(base_dir)
    
    base_url=raw_input("URL: ")
    
    mp4_url = get_video_url(url=base_url, driver=driver)
    if mp4_url is not False:
        download_file(url=mp4_url, file_dir=file_dir)
    
    finished_input=raw_input("More URLs? (y/n): ")
    if finished_input != 'y':
        finished=True
    
print "\nExiting Application"
driver.quit()
