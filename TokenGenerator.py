from selenium import webdriver
from selenium.common.exceptions import JavascriptException

from threading import Thread
from time import sleep

class TokenGenerator():
    def __init__(self, url, site_key=None, site_key_var=None, action='', retry_interval=3.0, headless=True):
        if not site_key and not site_key_var or site_key and site_key_var:
            raise ValueError("Must pass in a site key or site key variable name") 
        elif site_key:
            site_key_var = '"' + site_key + '"'
    
        self.token = None
        self.running = True
        
        options = webdriver.ChromeOptions()
        options.headless = headless
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
            
        thread = Thread(target=self.run, args=(url,site_key_var,action,retry_interval,))
        thread.daemon = True
        thread.start()     


    def run(self, url, site_key_var, action, retry_interval):
        self.driver.get(url)

        while self.running:
            try:
                self.token = self.driver.execute_async_script(f'var done = arguments[0]; await grecaptcha.execute({site_key_var}, {{action: "{action}"}}).then(function (token) {{done(token)}})')
            except JavascriptException as e:
                pass
            sleep(retry_interval)
        
        
    def has_token(self):
        return self.token != None
        
        
    def get_token(self):
        temp = self.token
        self.token = None
        return temp
        
        
    def stop(self):
        self.running = False
        self.driver.quit()