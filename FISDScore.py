from selenium import webdriver
import time
import os
import sys
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas

import requests

driver = webdriver.Firefox()
driver.get("https://hac.friscoisd.org/homeaccess/")
element = driver.find_element_by_id("LogOnDetails_UserName")
element.send_keys("Yang.C2")
element = driver.find_element_by_id("LogOnDetails_Password")
element.send_keys("5X598IB3")
element.submit()
time.sleep(5)
element = driver.find_element_by_id("hac-Classes")
element.click()
time.sleep(5)

#Request again for HTML embeded in iframe
#Currenting hard coded URL for score table
driver.get("https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx")

page = driver.page_source

soup = BeautifulSoup(page,"html.parser")

all = soup.findAll("div",{"class":"AssignmentClass"})

subject_list = []

for item in all:
    subject = item.find("a",{"class":"sg-header-heading"})
    print(subject.text.strip())
    subject_list.append(subject.text.strip())

l=[]
for n in range(8):
    if n == 3 or n == 4:
        continue
    else:
        #Find table and skip the hinden table
        sub = "plnMain_rptAssigmnetsByCourse_dgCourseAssignments_" + str(n)
        table = soup.find("table",{"id":sub})
        assignment = table.findAll("tr",{"class":"sg-asp-table-data-row"})
        index = 0
        for number in assignment:
            d={}
            d["Subject Class"] = subject_list[n]

            for i in range(6):
                if i == 1:
                    continue
                try:
                    if i == 0:
                        d["Date"] = number.findAll("td")[i].text.strip().strip('*').replace("\n","")
                    elif i == 2:
                        d["Assignment"] = number.findAll("td")[i].text.strip().strip('*').replace("\n","")
                    elif i == 3:
                        d["Category"] = number.findAll("td")[i].text.strip().strip('*').replace("\n","")
                    elif i == 4:
                        d["Score"] = number.findAll("td")[i].text.strip().strip('*').replace("\n","")
                    else:
                        d["Total Point"] = number.findAll("td")[i].text.strip().strip('*').replace("\n","")
                except:
                    print(None)
            l.append(d)
print(l)
driver.close()
df=pandas.DataFrame(l)

#manually re-order the columns as python dictionary does not preserve the order of its keys
df = df[["Subject Class","Date","Assignment","Category","Score","Total Point"]]
df.to_csv("Output.csv")
