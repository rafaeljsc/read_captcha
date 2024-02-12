from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import easyocr
import time

sitesCategorizados = []
ocr = easyocr.Reader(['en'], verbose=False)
sites = json.load(open('./sites.json', 'r'))['sites']
service = Service('./chromedriver.exe')  
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
url = 'https://sitereview.bluecoat.com/'
driver.get(url)

def verificaCategoria():
    try:
        campoURL = driver.find_element(By.ID, 'txtUrl')           
        campoURL.send_keys(site)
        botaoVerificar = driver.find_element(By.ID, 'btnLookup')
        botaoVerificar.click()
        categoria = driver.find_element(By.CLASS_NAME, 'clickable-category')
        return categoria
    except:
        return None

for site in sites:
    categoria = verificaCategoria()
    if categoria is None:
        while True:
            try:
                time.sleep(2)
                captcha = driver.find_element(By.ID, 'imgCaptcha')
                captcha.screenshot('captcha.png')
                ocrCaptcha = ocr.readtext('./captcha.png')
                
                txtCaptcha = ''
                for t in ocrCaptcha: txtCaptcha += t[1]
                txtCaptcha = txtCaptcha.replace(' ','')

                campoCaptcha = driver.find_element(By.ID, 'txtCaptcha')
                campoCaptcha.send_keys(txtCaptcha)
                time.sleep(1)
                botaoEnviaCaptcha = driver.find_element(By.ID, 'btnCaptcha')
                botaoEnviaCaptcha.click()
            
            except:
                time.sleep(1)
                categoria = verificaCategoria()
                if categoria is not None: break

    sitesCategorizados.append(f"{site}: {categoria.text}")
    driver.back()

driver.quit()