import pyautogui
import time
import math
import random
import os
import sys
import requests
import wmi
import imaplib
import email
from email.header import decode_header
import webbrowser
import threading
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
from os import listdir
from os.path import isfile, join
import concurrent.futures
from datetime import datetime
import selenium
import urllib.request
import urllib
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time,string,zipfile,os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
import multiprocessing
from selenium import webdriver
def randkeys(element, keys, driver):
    for myi in keys:
        element.send_keys(myi)
        time.sleep(random.uniform(0.05, 0.25))

def press_key(key, driver):
    actions = ActionChains(driver)
    actions.send_keys(key)
    actions.perform()

def initdriver(proxy):
    chrome_options = webdriver.ChromeOptions()
    #mobile_emulation = {

        #"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

    #"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }

    #chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    chrome_options.add_argument(str('--proxy-server=http://'+str(proxy)))
    #chrome_options.add_argument("--headless")   
    driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
    driver.set_page_load_timeout(45)
    #driver.set_window_position(0, -2000, windowHandle='current')
    driver.delete_all_cookies()
    return driver


def startallthreads(threadnum):
    threads = []
    allproxies = ['proxylist']
    thist = 0
    for i in range(threadnum):
        
        if thist >= int(len(allproxies) - 1):
            thist = 0
        else:
            thist += 1
        thread = threading.Thread(target=fullprocess, args=(allproxies[thist],i))
        threads.append(thread)
    for thread in threads:
        thread.start()
        time.sleep(0.5)
    for thread in threads:
        thread.join()


def fullprocess(proxy, thread):
    driver = initdriver(proxy)
    thisi = 0
    file = open("allniches.txt","r")
    niches = file.readlines()
    file.close()
    states = listdir("states/")
    
    for state in states:
        state = state.strip().replace("\r","").replace("\n","")
        while True:
            thisi += 1
            nichenum = int(int(thread + 1) * thisi)
            searchterm = niches[nichenum]
            if nichenum >= int(len(niches) - 1):
                print(str("Thread "+str(thread)+": Hit end of niches, moving on to next state"))
                break
            searchterm = searchterm.strip().replace("\r","").replace("\n","")
            page = 0
            while True:
                try:
                    page += 1
                    if page > 100:
                        print(str("Thread "+str(thread)+": hit end of page, breaking"))
                        break

                    print(str("Thread "+str(thread)+": Scraping page number "+str(page)))
                    
                    try:
                        try:
                            driver.get(str("https://www.yellowpages.com/search?search_terms="+str(searchterm)+"&page="+str(page)+"&geo_location_terms="+str(state)))
                        except Exception as EEEE:
                            print(str("Thread "+str(thread)+": Couldn't load page fully, trying to get data anyway: "+str(EEEE)))
                        time.sleep(4)
                        try:
                            if driver.find_element_by_xpath('//*[@id="no-results"]/div[2]') != None:
                                break
                        except:
                            print(str("Thread "+str(thread)+": Found results"))
                        for _ in range(5):
                            press_key(Keys.SPACE, driver)
                        time.sleep(1)
                        try:
                            if driver.find_element_by_xpath(str('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div')) != None:
                                print(str("Thread "+str(thread)+": Listings still here, scraping"))
                        except:
                            try:
                                if driver.find_element_by_xpath(str('/html/body/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div')) != None:
                                    print(str("Thread "+str(thread)+": Listings still here, scraping"))
                            except:
                                print(str("Thread "+str(thread)+": no more listings. Killing this tab"))
                                break


                        
                        for index in range(1,30):
                                                
                            try:
                                website = "NAN"
                                street = "NAN"
                                locality = "NAN"
                                name = "NAN"
                                
                                try:
                                    phone = driver.find_element_by_xpath(str('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[2]/div[1]')).text 
                                except:
                                    print(str("Thread "+str(thread)+": Error finding phone, trying second xpath"))
                                    phone = driver.find_element_by_xpath(str('/html/body/div[3]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[2]/div[1]')).text 
                                 
                                try:
                                    street = driver.find_element_by_xpath(str('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[2]/div[2]')).text 
                                except:
                                    print(str("Thread "+str(thread)+": error finding street"))
                                    try:
                                        street = driver.find_element_by_xpath(str('/html/body/div[3]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[2]/div[2]')).text 
                                    except:
                                        print(str("Thread "+str(thread)+": error finding street"))


                                    
                                try:
                                    locality = driver.find_element_by_xpath(str('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[2]/div[3]')).text 
                                except:
                                    print(str("Thread "+str(thread)+": error getting locality"))
                                    try:
                                        locality = driver.find_element_by_xpath(str('/html/body/div[3]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[2]/div[3]')).text 
                                    except:
                                        print(str("Thread "+str(thread)+": error getting locality"))

                                try:
                                    name = driver.find_element_by_xpath(str('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/h2/a/span')).text 
                                except:
                                    print(str("Thread "+str(thread)+": error getting name"))
                                    try:
                                        name = driver.find_element_by_xpath(str('/html/body/div[3]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/h2/a/span')).text 
                                    except:
                                        print(str("Thread "+str(thread)+": error getting name"))

                                try:
                                    websitetemp = driver.find_element_by_xpath(str('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[1]/div[4]/a[1]'))
                                    if "Website" in websitetemp.text:
                                        website = websitetemp.get_attribute('href')
                                except:
                                    print(str("Thread "+str(thread)+": error getting website"))
                                    try:
                                        websitetemp = driver.find_element_by_xpath(str('/html/body/div[3]/div/div[1]/div[1]/div[2]/div[2]/div['+str(index)+']/div/div/div[2]/div[1]/div[4]/a[1]'))
                                        if "Website" in websitetemp.text:
                                            website = websitetemp.get_attribute('href')
                                    except:
                                        print(str("Thread "+str(thread)+": error getting website"))
                                    
                                try:
                                    file = open(str("data/"+str(searchterm)+str(state).strip().replace("\n","").replace("\r","")+".txt"),"r")
                                    entries = file.readlines()
                                    file.close()
                                    if str(phone.strip().replace("\n","").replace("\r","")) not in str(entries) and str(name.strip().replace("\n","").replace("\r","")) not in str(entries):
                                        
                                        file = open(str("data/"+str(searchterm)+str(state).strip().replace("\n","").replace("\r","")+".txt"),"a")
                                        file.write(str( str(name)+":"+str(phone)+":"+str(street)+":"+str(locality)+":"+str(website)+"\n"))
                                        file.close()
                                        
                                except Exception as EEE:
                                    print(str("Thread "+str(thread)+": No data file for city yet. Making one: "+str(EEE)))
                                    file = open(str("data/"+str(searchterm)+str(state).strip().replace("\n","").replace("\r","")+".txt"),"w")
                                    file.write(str( str(name)+":"+str(phone)+":"+str(street)+":"+str(locality)+":"+str(website)+"\n" ))
                                    file.close()
                            except Exception as EE:
                                print(str("Thread "+str(thread)+": Looking for next data point: "+str(EE)))
                            
                                
                    except Exception as E:
                        print(str("Thread "+str(thread)+": Error: "+str(E)))
                except Exception as EEr:
                    print(str("Thread "+str(thread)+": Big error: "+str(EEr)))
    try:
        driver.close()
        driver.quit()
    except:
        print(str("Thread "+str(thread)+": Error closing driver"))
    
            
startallthreads(25)


