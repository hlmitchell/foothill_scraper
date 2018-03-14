from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import threading

def errorHandlingFunction(functionName):
    print("\nERROR in " + functionName + "\n")
    driver.close()

def goToFootHillWEB(driver): 
    try:
        driver.get("https://myportal.fhda.edu/cp/home/displaylogin")
    except:
        errorHandlingFunction("goToFootHillWeb")

def loginToFootHill(driver):
    try:
        userName = driver.find_element_by_id("user")
        userName.send_keys("*****")

        password = driver.find_element_by_id("pass")
        password.send_keys("*****")

        driver.find_element_by_name("login_btn").click()
    except:
        errorHandlingFunction("loginToFootHill")

def clickRegistrationTab(driver):
    try:
        driver.implicitly_wait(10)
        element = driver.find_element_by_id("tabs_tda")
        element = element.find_elements_by_class_name("taboff")
        element[2].click()
    except:
        errorHandlingFunction("clickRegistrationTab")

def clickAddOrDropClasses(driver):
    try:
        driver.implicitly_wait(10)
        element = driver.find_element_by_id("content")
        element = element.find_element_by_id("channel")
        element = element.find_element_by_id("p_chan_text")
        element = element.find_element_by_class_name("TargetedSelfServiceMenu")
        element = element.find_elements_by_tag_name('a')
        element[3].click()
    except:
        errorHandlingFunction("clickAddOrDropClasses")

def switchFrame(driver, frameName):
    try:
        driver.switch_to_frame(frameName)
        return driver
    except:
        errorHandlingFunction("switchFrame")

def selectSpringFootHillDropDown(driver):
    try:
        submit = driver.find_element_by_class_name("pagebodydiv")
        element = submit.find_element_by_class_name("dataentrytable")
        element = element.find_element_by_name("term_in")
        element.click()
        element = element.find_elements_by_tag_name("option")
        element[1].click()

        submit.find_element_by_tag_name("form").submit()
    except:
        errorHandlingFunction("selectSpringFootHillDropDown")
        
def clickClassSearch(driver):
    try:
        def find(driver):
            element = driver.find_element_by_xpath("//input[@name='REG_BTN' and @value='Class Search']")
            if element:
                return element
            else:
                return False

        element = WebDriverWait(driver, 10).until(find)
        element.click()
    except:
        errorHandlingFunction("clickClassSearch")

def chooseComputerScienceOption(driver):
    try:
        def find(driver):
            element = driver.find_element_by_xpath("//option[@value='C S']")
            if element:
                return element
            else:
                return False

        element = WebDriverWait(driver, 10).until(find)
        element.click()
    except:
        errorHandlingFunction("clickClassSearch")

def clickCourseSearch(driver):
    try:
        element = driver.find_element_by_xpath("//input[@name='SUB_BTN' and @value='Course Search']")
        element.click()
    except:
        errorHandlingFunction("clickCourseSearch")

def clickViewSections(driver):
    try:
        def find(driver):
            element = driver.find_elements_by_class_name("datadisplaytable")
            element = element[1]
            element = element.find_elements_by_tag_name("tr")
            if len(element) > 10:
                return element
            else:
                return False

        element = WebDriverWait(driver, 10).until(find)
    
        #use tabs to select the button
        i = 14  # number of times to press TAB
        tabs = ActionChains(driver) 

        for x in range(i):
            tabs = tabs.send_keys(Keys.TAB)
        tabs = tabs.send_keys(Keys.ENTER)

        tabs.perform()
    except:
        errorHandlingFunction("clickViewSections")

def checkWaitListValues(driver):
    try:
        def find(driver):
            element = driver.find_elements_by_class_name("dddefault")
            if len(element) > 60:
                return element
            else:
                return False

        element = WebDriverWait(driver, 10).until(find)

        WLcapacity = element[55].text   #number of waitlist spots filled
        WLactive = element[56].text     #number of waitlist spots available

        return WLcapacity + WLactive
    except:
        errorHandlingFunction("checkWaitListValues")

def sendEmailToMe():
    try:
        fromaddr = "han.lou.mitchell@gmail.com"
        toaddr = "han.lou.mitchell@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "CS OPENING"
        
        body = "CHECK THE WEBSITE"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "*****")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    except:
        errorHandlingFunction("sendEmailToMe")

def runScraper():
    
    #runs loop every 15 minutes
    threading.Timer(900.0, runScraper).start()
    
    try:
        driver = webdriver.Chrome()

        goToFootHillWEB(driver)
        loginToFootHill(driver)

        clickRegistrationTab(driver)
        clickAddOrDropClasses(driver)

        driver = switchFrame(driver, "content")
        
        selectSpringFootHillDropDown(driver)
        clickClassSearch(driver)
        
        chooseComputerScienceOption(driver)
        clickCourseSearch(driver)

        clickViewSections(driver)

        total = checkWaitListValues(driver)
        print(total)

        #send email if either waitlist variable changes
        if total != "1010": 
            sendEmailToMe()

        driver.close()

    except:
        print("\nERROR in runscraper\n")

if __name__ == "__main__":
    runScraper()
