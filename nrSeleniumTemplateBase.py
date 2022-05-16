from multiprocessing.pool import RUN
import profile
from pydoc import Doc
from time import sleep
import re
from cv2 import accumulate

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

import atexit
import threading
import random

class nrSeleniumTemplateBase:
    def __init__(self):
        self.SAVE_MODE = True
        self.RUNNING = True
        self.TARGETED_ACCOUNTS = []

        self.TIMEOUT_DURATION  = 3
        self.IGURL = 'https://www.instagram.com/'


        edge_options = EdgeOptions()
        edge_options.use_chromium = True

        user_data_dir = r"C:\Users\jasbi\AppData\Local\Microsoft\Edge\User Data\Selenium Dev"
        edge_options.add_argument("user-data-dir={}".format(user_data_dir)); 

        edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        driver_location = r"D:\FILES\Desktop\other\IGTools\msedgedriver.exe"

 
        self.browser = Edge(executable_path=driver_location, options=edge_options)

        self.browser.get(self.IGURL)

        self.IG_REQUEST_BUFFER_DURATION = 120


        listener_thread = threading.Thread(target=self.ListenForCommands)
        listener_thread.setDaemon(True)
        listener_thread.start()

        
    def ScrollOnElement(self, element, element_css_selector, sleep_duration = 0):
        JS_injection = '''
        var fDialog = document.querySelector('{}');
        fDialog.scrollTop = fDialog.scrollHeight
            '''.format(element_css_selector)

        self.browser.execute_script(JS_injection)
        if sleep_duration != 0:
            sleep(sleep_duration)


    def Useful(self):
        pop_up_box = None
        ActionChains(self.browser).move_to_element(pop_up_box).click().send_keys(Keys.PAGE_DOWN).perform()
        WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,popup_box_link_xpath))).click()
    
    def ListenForCommands(self):
        while True:
            command = input("ENTER COMMAND:")
            if command.upper() == "SAVE":
                self.SaveChanges()
                print("SAVED CHANGES")
            
            if command.upper() == "EXIT":
                self.RUNNING = False
                self.SaveChanges()
                print("EXITING APPLICATION")
