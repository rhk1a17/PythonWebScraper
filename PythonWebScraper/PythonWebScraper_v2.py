from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup # library used export data from web content
import time
from datetime import datetime
from PIL import Image
import numpy



output_list = []

def LoginSunnyPortal():
    ###########################################################
    global browser
    #enter the link to the website you want to automate login.
    website_link_true="https://www.sunnyportal.com/Templates/Start.aspx?logout=true"
    #enter your login username
    username_true="monitoring@ers.my"
    #enter your login password
    password_true="ers12345"

    ###########################################################

    #enter the element for username input field
    element_for_username="ctl00$ContentPlaceHolder1$Logincontrol1$txtUserName"
    #enter the element for password input field
    element_for_password="ctl00$ContentPlaceHolder1$Logincontrol1$txtPassword"
    #enter the element for submit button
    element_for_submit="ctl00$ContentPlaceHolder1$Logincontrol1$LoginBtn"

    ###########################################################

    browser = webdriver.Chrome("C:/Users/ersenergy/Desktop/Khee_Intern/chromedriver.exe")
    #browser = webdriver.PhantomJS("C:/Users/ersenergy/Desktop/Khee_Intern/PythonWebScraper/PythonWebScraper/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    browser.get((website_link_true))

    username = browser.find_element_by_name(element_for_username)
    username.send_keys(username_true)		
    password  = browser.find_element_by_name(element_for_password)
    password.send_keys(password_true)
    signInButton = browser.find_element_by_name(element_for_submit)
    signInButton.click()

    
def scrapeSunnyPortal(url):

    browser.get(url) #redirect dashboard URL depends on target
    time.sleep(2); #delay for webpage to load fully
    res = browser.execute_script("return document.documentElement.outerHTML")    
    
    # parser the web content
    soup = BeautifulSoup(res, 'html.parser')
    #data_list = soup.find_all('div',{'class':'mainValue'})
    data_list = soup.find_all('div',{'id':'TabSwitchDeviceSelectionContent2'})
    data_list_string = ""
    for string in data_list:
        data_list_string += str(string)
    data_list_string = data_list_string.split("'")
    final_string = ""
    for ele in data_list_string:
        final_string += ele + "''"
    
    ##TIMESTAMP
    timestamp = final_string.split("data-timestamp")
    timestamp = str(timestamp[1])
    timestamp = timestamp.split('"')
    timestamp = timestamp[1]

    #TITLE
    title_list = soup.find_all('span', {'id':'ctl00_ContentPlaceHolder1_lblPlantOverview'})
    title = str(title_list[0]).split("|")
    title = str(title[1]).split("<")
    title = str(title[0])[1:]

    #CURRENT PV POWER
    powerList = final_string.split("data-timestamp")
    powerList = powerList[1].split(">")
    powerList = powerList[1].split("<")
    power = powerList[0]
    #CURRENT PV POWER UNIT
    powerListUnit = final_string.split("class=\"mainValueUnit\">")
    powerListUnit = powerListUnit[1].split("<")
    powerUnit = powerListUnit[0]

    #PV Energy Today
    pvToday = final_string.split("ctl00_ContentPlaceHolder1_UserControlShowDashboard1_energyYieldWidget_energyYieldValue")
    pvToday = pvToday[1].split("<")
    pvToday = pvToday[0][2:]
    #PV Energy Today Unit
    pvTodayUnit = final_string.split("id=\"ctl00_ContentPlaceHolder1_UserControlShowDashboard1_energyYieldWidget_energyYieldUnit\">")
    pvTodayUnit = pvTodayUnit[1].split("<")
    pvTodayUnit = pvTodayUnit[0]

    #TOTAL ENERGY GENERATED
    totalEnergy = final_string.split("id=\"ctl00_ContentPlaceHolder1_UserControlShowDashboard1_energyYieldWidget_energyYieldTotalValue\">")
    totalEnergy = totalEnergy[1].split("<")
    totalEnergy = totalEnergy[0]
    #TOTALENERGY UNIT
    totalEnergyUnit = final_string.split("id=\"ctl00_ContentPlaceHolder1_UserControlShowDashboard1_energyYieldWidget_energyYieldTotalUnit\">")
    totalEnergyUnit = totalEnergyUnit[1].split("<")
    totalEnergyUnit = totalEnergyUnit[0]

    #CO2 Avoided today
    co2today = final_string.split("ctl00_ContentPlaceHolder1_UserControlShowDashboard1_carbonWidget_carbonReductionValue")
    co2today = co2today[1].split("<")
    co2today = co2today[0][2:]
    #CO2 UNIT
    co2todayUnit = final_string.split("ctl00_ContentPlaceHolder1_UserControlShowDashboard1_carbonWidget_carbonReductionUnit")
    co2todayUnit = co2todayUnit[1].split("<")
    co2todayUnit = co2todayUnit[0][2:]

    #CURRENT DATETIME
    #FORMAT 2019-08-08T10:00:00
    now = datetime.now()
    real_datetime = now.strftime("%Y-%m-%dT%H:%M:%S")

    #CAPACITY
    cap_list = soup.find_all('div', {'data-name':'plantInfo'})
    cap = str(cap_list[0]).split("<strong>")
    cap = (str(cap[1]).split('<'))[0]

    #GRAPH URL 
    graph_list = soup.find_all('img', {'id':'ctl00$ContentPlaceHolder1$UserControlShowDashboard1$UserControlShowEnergyAndPower1$_diagram'})
    graph = str(graph_list[0]).split("src=\"")
    graph = graph[1].split('"')
    graph = graph[0]

    #GRAPH
    filename_datetime = now.strftime("%Y-%m-%dT%H%M%S") #FILENAME FOR GRAPH
    browser.get("https://www.sunnyportal.com" + str(graph))
    for element in browser.find_elements_by_tag_name('img'):
        filename = "C:/Users/ersenergy/Desktop/Khee_Intern/Scraped_Graph/" + str(filename_datetime)+'.png'
        with open(filename, 'wb') as file:
            file.write(element.screenshot_as_png)

    connection_string = "INSERT INTO SUNNY_PORTAL_STRING (_datetime, title, current_power, power_unit, energy_today, energy_unit,total_energy, total_energy_unit, co2today, co2_unit, real_datetime, capacity) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %  (timestamp, title, power, powerUnit, pvToday, pvTodayUnit,totalEnergy,totalEnergyUnit, co2today, co2todayUnit, real_datetime, cap)
    output_list.append(connection_string)
    time.sleep(2);


def SemsLogin():
    ###########################################################
    global browser
    #enter the link to the website you want to automate login.
    website_link_true="https://semsportal.com/home/login"
    #enter your login username
    username_true="monitoring@ers.my"
    #enter your login password
    password_true="ersmy123"

    ###########################################################

    #enter the element for username input field
    element_for_username="username"
    #enter the element for password input field
    element_for_password="password"
    #enter the element for submit button
    element_for_submit="btnLogin"

    ###########################################################

    browser = webdriver.Chrome("C:/Users/ersenergy/Desktop/Khee_Intern/chromedriver.exe")
    browser.get((website_link_true))

    username = browser.find_element_by_name(element_for_username)
    username.send_keys(username_true)		
    password  = browser.find_element_by_name(element_for_password)
    password.send_keys(password_true)
    signInButton = browser.find_element_by_id(element_for_submit)
    signInButton.click()
    time.sleep(2)
    
def SemsPortalScrape(url):
    browser.get(url) #redirect dashboard URL depends on target
    time.sleep(2); #delay for webpage to load fully
    res = browser.execute_script("return document.documentElement.outerHTML")

    # parser the web content
    soup = BeautifulSoup(res, 'html.parser')

    #TITLE
    title_list = soup.find_all('div', {'class':'station-title'})
    title = str(title_list[0]).split("station-title\">\n")
    title = title[1].split("\n")
    title = title[0][8:]

    #CURRENT PV POWER
    currentPV_list = soup.find_all('ul', {'class':'table-list left-list'})
    currentPV_list = str(currentPV_list[0]).split("Power")
    currentPV_list = str(currentPV_list[1][15:]).split("</")
    currentPV = str(currentPV_list[0])
    #CURRENT PV UNIT
    pv_unit = str(currentPV_list[1]).split("<em>")
    pv_unit = str(pv_unit[1])

    #POWER TODAY
    power_today_list = soup.find_all('div', {'class':'today-power-center'})
    power_today_list = str(power_today_list[0]).split("Today Generation")
    power_today = str(power_today_list[0]).split("<p>")
    power_today = str(power_today[1]).split("</p>")
    power_today = str(power_today[0])
    #POWER TODAY UNIT
    power_today_unit = str(power_today_list[0]).split("<span>")
    power_today_unit = str(power_today_unit[1]).split("</span>")
    power_today_unit = str(power_today_unit[0])

    #TOTAL GENERATED POWER WITH UNIT
    total_power_list = soup.find_all('div', {'class':'total-list left-total-list'})
    total_power = str(total_power_list[0]).split("<p>")
    total_power = str(total_power[1]).split("</p>")
    total_power = str(total_power[0])

    #CONDITION
    condition_list = soup.find_all('div', {'class':'device-status'})
    condition = str(condition_list[0]).split(">")
    condition = str(condition[1]).split("</")
    condition = str(condition[0])

    #CURRENT DATETIME
    #FORMAT 2019-08-08T10:00:00
    now = datetime.now()
    datetime_now = now.strftime("%Y-%m-%dT%H:%M:%S")

    connection_string = "INSERT INTO SEMS_STRING (_datetime, title, current_power, power_unit, energy_today, energy_unit, total_energy, condition) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %  (datetime_now, title, currentPV, pv_unit, power_today, power_today_unit, total_power, condition)
    output_list.append(connection_string)
    time.sleep(2);
    

    #GRAPH
    #filename_datetime = now.strftime("%Y-%m-%dT%H%M%S") #FILENAME FOR GRAPH
    #for element in browser.find_elements_by_tag_name('canvas'):
    #    filename = "C:/Users/ersenergy/Desktop/Khee_Intern/Scraped_Graph/" + str(filename_datetime)+'.png'
    #    with open(filename, 'wb') as file:
    #        file.write(element.screenshot_as_png)



#======================================SUNNY PORTAL SCRAPE START====================================
LoginSunnyPortal()

scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/50f57782-7818-40b9-8455-72d2a96ae8ea")#TCMA 1MWp
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/f3dc9332-e74e-466c-b687-b3c242ecb270")#NK Energy 0.99MWp Solar Farm
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/178d8475-a9f3-4d2c-aef5-ec31ecd7025e")#Maran Road Sawmill - 500kWp
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/f26889bb-d497-46bf-9d68-a5a786a5fb22")#Maran Road Sawmill NEM
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/3f17f707-e670-4963-884c-7282e141e197")#Toyo Tires Manufacturing (M)
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/89a6e79c-9bd1-41b4-8100-57026f970ca6")#Choo Lay Khuan 5kWp
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/36480a1e-ea06-46a4-bb51-076de928dec3")#Nasharuddin 2017
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/d0b93bd9-63b8-4e91-9f1d-a6134d80a10a")#ChuaChinPeng
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/f0482b76-eeda-497e-98f3-5f059725562c")#tingchenhunt
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/2a6c0b9a-0a7f-46f7-8734-b9f4f0577c9c")#Mohamad Shahrir
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/dfb8bbe6-1fd7-43b9-abfe-c697ecd2fdb1")#Loh Kiat Yoong
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/2a3a16db-c26c-419f-9022-69c4ff026578")#Krishna
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/005b27eb-83c5-403b-b776-5feddf925b21")#Affandi
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/f650a5ef-f23a-46b5-a3f4-a0ce6aa44ad1")#Lee Szed Kee
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/25d8e6d2-d14f-42e4-a255-71b9025a03c0")#Ooi Lee Kean
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/87f2131c-29e3-45f5-8609-94bdcbb78320")#SS15
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/831669dc-76a8-4bec-9ae6-61419faeca1d")#Soo Kai Soon
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/9f9454cc-e63d-4e3a-921b-af8dd9b4342a")#Chua Eng Hin
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/c8a4eaf8-7f80-46ff-984c-c8725d09a095")#Ooi Hoon Kong
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/4f3e3986-7a08-47cb-a65c-753f114e5790")#William Lin Kee Wai
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/8af92b18-fe49-4f15-8d2c-2ad4173c54a2")#CP Wong
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/8c1e17ff-b005-4457-8da0-6bcf039f1c09")#Ng Wei Xin
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/6c0df447-1ed7-4439-ac76-9cac44a7c377")#secret-garden 6.3kWp Solar PV
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/718697cb-db6b-468d-8a38-3233d9d2dc6e")#Kuvendran
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/80c11e4c-0845-419e-b0e2-b6ea1dd419c5")#Jack Ong Seng Leong
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/a303e292-2e5a-4866-ad5a-2324dc6e717d")#Tan Chun Weng
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/ebb7685b-bdf8-4cdb-8b19-c157391d5824")#Yim Kien Wai 11.925kWP
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/ef1ae391-ebb6-4e73-bc8b-45b0797ac47e")#Lau Ken Poh
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/99b5a8b8-46c3-45b7-add0-841a99f3e43f")#Lee Khek Mui
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/bf2b3def-7f19-4ddc-bb02-2648f8904581")#CM Yee
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/46658bc7-14da-41ff-a993-a5e0442ac168")#Jerome Heah
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/2d1feb1c-65ec-456e-ab18-6dabaa40a1e6")#ChocoPOW
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/bc90caad-d6a1-4b2c-892c-ff79794227b3")#ChengPK 22 S.Tropika U13/20B
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/d49d4876-f7b8-4b9b-b756-ff568ee90aeb")#Klang Presbyterian Church
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/5fbb81bd-1fff-4d3d-aee2-9680fe779151")#1773 Aviva Green
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/0a3acb4d-0d7f-49b7-acbc-140f5ddbede6")#Tan Yu Wea
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/8d2138db-1d09-4c2f-903d-959ba47190e4")#Fresh Fishery 132kWp
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/69dbe0e5-68e5-440a-968d-04b9796e8a23")#River Of Life
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/aa3b0301-99d6-4cdb-b59e-d4cd2cf99b06")#Kraiburg-TPE
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/cf0de763-cb7f-4f86-9184-9a8c3b82c7c1")#Hercules F2
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/438ac8e9-ce6a-4ad5-878f-07722beddf6e")#SSL 180kwp
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/ddd896c2-8640-4871-8264-bded1a88ee84")#Shea Fatt Hardware (M) Sdn Bhd
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/6d2acb59-e06b-4d14-a373-524fbf78934d")#SYW INDUSTRY
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/9d8f80d3-111a-43fb-aad4-478c436cfcf2")#ICP Ulu Choh
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/3fd8671b-c738-45d7-9bb0-2c3fa424be77")#Thumbprints Utd Sdn Bhd
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/ccf19d37-c685-487f-8544-280e6dff824d")#TR Energy 0.99MWp
scrapeSunnyPortal("https://www.sunnyportal.com/RedirectToPlant/7c22e670-5bd3-4f3c-9a8b-4f1e64bb77c6")#FIRMA ODESI 1MW
browser.quit()
#======================================SUNNY PORTAL SCRAPE END====================================

#======================================SEMS PORTAL SCRAPE START====================================
#SemsLogin()
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/47c2c36d-4314-47fe-984f-e38cea938d86")#Andrew Ho Kin Peng
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/f6a2f38b-9272-4812-af76-58a0854a23a8")#Ang Beng Hooi
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/ce31b853-d9fc-4969-9fc8-d4e3740d85ac")#Anna Kum
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/2396cd53-010d-4013-a6cc-5ab9828590fd")#BEYOND CONTROL SDN BHD - DAVID DZULKIFLI
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/4d1974ce-9fd3-41ba-939c-95507c2b14ee")#Bon Sian Son 6.36kWp NEM
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/3c395d6b-8f27-46f1-bbec-f56b6fac98ff")#Chooi Yok Kuoi
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/f5393d23-6ede-483d-95ec-34e5ee3c6952")#Chua Solar 12kwp
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/d61e13d1-6c5a-4558-b638-dc552b22b6fc")#Datuk Mazlan Bin Zakaria
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/392d2217-3807-499f-8e56-acd364d1d768")#David Low Chong Ming
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/03962d31-d259-4d23-93c7-8fe701a18f3a")#Edward Leong 9-1
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/e59e0e09-540a-48d1-a8b3-2991eb6517e8")#Edward Leong 9-2
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/2aaa3e4f-06c0-4f4d-bb54-bb00f157328e")#Edward Leong 9-G
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/0bce87ce-22fd-4d3a-8eba-1e9cccb6f913")#Francis Solar
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/e05a7a6e-18d0-4a8a-ae78-2b8db9fa6946")#Lai Hun Lean
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/38097bcc-16e0-4800-857f-a11100ce9908")#Li Thiam Hing
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/88e62a18-f9cb-499b-8d3a-b4fe8e69495b")#Loo Lai Chin
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/901828db-096b-4a17-a6f5-e149d7b3a423")#Low Kok Wai
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/9a3dee9f-365d-4190-b6e1-2e672dfac7b7")#Mohamad Hazri Bin Abdul Hamid
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/115f9599-f601-4063-a718-f3f67dbcb6d5")#Mohd Hazim Hassan
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/92948371-6747-4153-b64e-5e22aad54522")#Mohd Sharifuddin Ahmad
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/7b0e5c33-ef3a-458b-ba41-30d670cd7805")#Moneyboy
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/61a98e68-d600-4b3e-bfe2-1dbb32cf9476")#NCT HQ Solar PV
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/91a6f719-b44c-4957-9e55-05cde99b8631")#Nam Solar System
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/d07b296b-5743-42f9-8134-88e06ae8cdbd")#Nazim Bin Masrom
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/d4e83fab-b0ec-4948-8826-bd58d3ee374e")#Ngo Bao Mey
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/59f013c3-fd60-4502-b5c0-d51266b8e70e")#Pv plant Lai Wai Sum
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/ea7f280b-f6f1-4005-b265-3155249a5d04")#S P MUTHU VELOO
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/d11879f0-9c76-495d-9bab-a56df756940a")#Serdang PV
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/880b406e-7bb2-4a64-a0d4-6a517be22f6f")#So Beng Kwang
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/85c09c3b-c00f-44ed-9d91-29fe35a0975f")#So Lay Hoon
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/333bcf1b-ed07-40ab-8aee-3d9f77e939ff")#Soong Wai Leng
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/1115f83d-85a4-4d02-9258-d312b592aae9")#Tan Guan Song
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/92d019c9-ac2a-44dd-985b-062963a8c088")#Tan Hong Siang
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/7e34acfa-f6e7-4631-a25d-ef77c461fb88")#Tan Kien Meng
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/96777ca1-b879-493a-a7f6-cf07a21733b5")#Tin Kim Ang
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/82bb49b1-2ccc-4832-96c3-f99b19e493a4")#Wong Quai Chin
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/64c0dd87-aebd-4c61-b2c4-1b7958021bac")#Yap Say Moi
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/b1aa02e6-a9b7-4045-b749-944900f21d75")#Yong Lin Kok - Hybrid 5048
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/4c01bf85-6a7c-4dd6-a9db-ab0cc7a92bad")#chansolar
#SemsPortalScrape("https://semsportal.com/powerstation/PowerStatusSnMin/434bd127-985f-44a7-849e-3ba204f5cbb7")#zulkefli nem 20.14kwp
#browser.quit()

#======================================SEMS PORTAL SCRAPE END====================================
#print (output_list)
