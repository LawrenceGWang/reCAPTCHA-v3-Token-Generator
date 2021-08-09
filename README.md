# **reCAPTCHA v3 Token Generator**

## **Description**
Uses Selenium to mimic a call for a captcha response token without the website's private key.

## **Requirements**
* Python 3.5+
* Selenium (pip install selenium)
* ChromeDriver (https://chromedriver.chromium.org/)

## **Usage**
### **Basic Usage**
Import and create a TokenGenerator object
```python
from TokenGenerator import TokenGenerator

url = 'https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php'
site_key = '6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696'

generator = TokenGenerator(url, site_key=site_key, action='examples/v3scores', retry_interval=3.0)
```
Wait until a valid token has been generated. The retry_Interval determines the duration between calls for a new token in seconds. 
```python
while not generator.has_token():
    time.sleep(1)
token = generator.get_token()
```
Use the token in an API call that requires a captcha token
```python
requests.get(f'https://recaptcha-demo.appspot.com/recaptcha-v3-verify.php?action=examples/v3scores&token={token}')
```
The generator will continue to generate tokens until the stop() function is called
```python
generator.stop()
```
### **Site Keys**
There are two ways to pass in a website's public site key to the generator. 
Some sites have the key embedded in the DOM for example:
```html
<script src="https://www.google.com/recaptcha/api.js?render=6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696"></script>
```
In this case, parse the site key and pass it into the generator constructor with the parameter
```python
site_key = '6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696'
```
Other websites create JavaScript variables to store their site key for example:
```html
<script type="text/javascript">var recaptcha_site_key = '6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696';</script>
```
In this case, create call the generator constructor with the parameter
```python
site_key_var = 'recaptcha_site_key'
```