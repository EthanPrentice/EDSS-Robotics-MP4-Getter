'''
Created on 27 Mar 2017

@author: Ethan
'''
from selenium import webdriver

while True:
    try:
        url = raw_input("URL: ")
        driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        
        print("Fetching HTML...")

        driver.get(url)
    
        driver.switch_to.frame(driver.find_elements_by_xpath('//*[@id="body"]/iframe')[0])
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="video"]/iframe'))
    
        output=""
    
        print("Scraping Data...")
    
        scriptText = driver.find_element_by_xpath('/html/body/script[4]').get_attribute("innerHTML")
        for c in range(0, len(scriptText)):
            if scriptText[c]==(".") and scriptText[c+1]==("m") and scriptText[c+2]==("p") and scriptText[c+3]==("4"):
                while scriptText[c]!=('"'):
                    c-=1
                c+=1
                while scriptText[c]!=('"'):
                    output+=str(scriptText[c])
                    c+=1
                print("MP4 File: " + output)
                print("(close browser to enter another URL)")
                driver.get(output)
                break  
    
    except Exception, e:
        print("ERROR: " + repr(e))

