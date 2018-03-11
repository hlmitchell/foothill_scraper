from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import threading

#runs scraper every 15 minutes
def runScraper():
    threading.Timer(900.0, runScraper).start()

    #go to website
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get("https://myportal.fhda.edu/cp/home/displaylogin")


    try:
        assert "MyPortal" in driver.title
    except:
        print("Wrong website probably")

    #login
    userName = driver.find_element_by_id("user")
    userName.send_keys("********")
    password = driver.find_element_by_id("pass")
    password.send_keys("*************")

    login = driver.find_element_by_name("login_btn").click()

    #navigate to registration tab
    driver.implicitly_wait(10)
    allTabs = driver.find_element_by_id("tabs_tda")
    offTabs = allTabs.find_elements_by_class_name("taboff")
    offTabs[2].click()

    #click add or drop classes
    driver.implicitly_wait(5)
    placeHolder = driver.find_element_by_id("content")
    placeHolder = placeHolder.find_element_by_id("channel")
    placeHolder = placeHolder.find_element_by_id("p_chan_text")
    placeHolder = placeHolder.find_element_by_class_name("TargetedSelfServiceMenu")
    tabs = placeHolder.find_elements_by_tag_name('a')
    tabs[3].click()

    #change drop down option and submit
    driver.implicitly_wait(10)

    driver.switch_to_frame("content")

    element = driver.find_element_by_class_name("pagebodydiv")
    placeHolder = element.find_element_by_class_name("dataentrytable")
    placeHolder = placeHolder.find_element_by_name("term_in")
    placeHolder.click()
    placeHolder = placeHolder.find_elements_by_tag_name("option")
    placeHolder[1].click()

    element = element.find_element_by_tag_name("form").submit()

    #click class search

    def find1(driver):
        element = driver.find_element_by_xpath("//input[@name='REG_BTN' and @value='Class Search']")
        if element:
            return element
        else:
            return False

    element = WebDriverWait(driver, 10).until(find1)
    element.click()

    #choose computer science

    def find2(driver):
        element = driver.find_element_by_xpath("//option[@value='C S']")
        if element:
            return element
        else:
            return False

    element = WebDriverWait(driver, 10).until(find2)
    element.click()

    #click course search
    element = driver.find_element_by_xpath("//input[@name='SUB_BTN' and @value='Course Search']")
    element.click()

    #click view sections

        #check that the right button has loaded

    def find3(driver):
        element = driver.find_elements_by_class_name("datadisplaytable")
        element = element[1]
        element = element.find_elements_by_tag_name("tr")
        if len(element) > 10:
            return element
        else:
            return False

    element = WebDriverWait(driver, 10).until(find3)

        #use tabs to select the button

    i = 14  # number of times to press TAB

    tabs = ActionChains(driver) 

    for x in range(i):
        tabs = tabs.send_keys(Keys.TAB)
    tabs = tabs.send_keys(Keys.ENTER)

    tabs.perform()


    #check values of waitlisted classes
    def find4(driver):
        element = driver.find_elements_by_class_name("dddefault")
        if len(element) > 60:
            return element
        else:
            return False

    element = WebDriverWait(driver, 10).until(find4)

    WLcapacity = element[55].text
    WLactive = element[56].text

    print(WLcapacity)
    print(WLactive)
    print('\n')

    if WLactive != "10" or WLcapacity != "10": 
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
        server.login(fromaddr, "*********************")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    driver.close()

#runs file
runScraper()
