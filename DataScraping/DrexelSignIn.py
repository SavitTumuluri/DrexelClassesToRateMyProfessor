from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pyotp

def SignIn(driver):
    drexelConnect = "https://connect.drexel.edu/idp/profile/cas/login"
    driver.get(drexelConnect)
    loginbox = driver.find_element(By.ID, "login-box")
    loginbox.find_element(By.NAME, "_eventId_proceed").click()

    time.sleep(5)
    username = driver.find_element(By.ID, "i0116")
    username.send_keys("so546@drexel.edu")
    driver.find_element(By.ID, "idSIButton9").click()


    time.sleep(5)
    password = driver.find_element(By.ID, "i0118")
    password.send_keys("Onyi@drexel.2005")
    driver.find_element(By.ID, "idSIButton9").click()

    time.sleep(2)
    mfa_secret = "7mrx5y2nvvvbrrgk"
    totp = pyotp.TOTP(mfa_secret)
    mfa_code = totp.now()


    mfa_input = driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC")
    mfa_input.send_keys(mfa_code)
    mfa_input.submit()

    time.sleep(5)
    driver.get("https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202415?collCode=CI")
    time.sleep(5)