from lxml import html  
import csv,os,json , re
import requests
from exceptions import ValueError
from time import sleep
import collections
from collections import OrderedDict 
from selenium import webdriver
from pyvirtualdisplay import Display
import time
import MySQLdb
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import ast
import pymongo
import odict
import oset
from bson.objectid import ObjectId
import random
from random import randint
from time import sleep
import schedule
import datetime
from fake_useragent import UserAgent
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.keys import Keys
import pymongo as mng
import subprocess
from selenium.webdriver.chrome.options import Options


class AmazonScraper:
    list1 = []
    check_count = 0

    # def __init__(self):
        # self.chrome_executable_driver = "/home/user/Downloads/chromedriver"
        # chrome_options = Options()
        # us =  UserAgent()
        # userAgent = us.random
        # print(userAgent)
        # chrome_options.add_argument('user-agent={userAgent}')
        # # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # # chrome_options.add_argument('--disable-dev-shm-usage')
        # # display = Display(visible=0, size=(800, 800))
        # # display.start()
        # self.browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=self.chrome_executable_driver)

    def hasXpath(self,xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def hastext(self,text):
        try:
            self.browser.find_element_by_link_text(text)
            return True
        except:
            return False        

    def mongo(self,product_dict):
        a = str(datetime.datetime.now().date())
        b = a.split("-")
        c = ''.join(b)
        db_name = "Amazon{}".format(c)
        csv_name = "Amazon{}".format(c)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[db_name]
        mycol = mydb["allproducts"]
        mydict = product_dict 
        print "First : ",mydict

        for i in xrange(1): 
            mydict['i'] = i 
            mydict['_id'] = ObjectId() 
            mycol.insert_one(mydict)
 
        # connected = False
        # #Open DB connection
        # try:
        #     connection = mng.MongoClient('localhost', 27017)
        #     db = connection['Amazon_sample']
        #     print("I am connected to Mongo DB")
        #     connected = True
        # except:
        #     print("I am not able to connect to Mongo DB")
        subprocess.call("mongoexport --db "+db_name+" --collection allproducts --type=csv --fields ASIN,Brand,'Item Model Number','Item Part Number','Item model number','Item part number',MRP,'Model Name',Price,'Product URL','Selling Price',Title,Date --out /home/user/python_projects/Emails/"+csv_name+".csv", shell = True)
        myclient.close()
    
    
    def get_url_list_from_csv(self):
        filename = "/home/user/python_projects/Amazon/Amazon_PDP_URLs1.csv"
        skus1 = [] 

        with open(filename, 'r') as csvfile: 
            csvreader = csv.reader(csvfile) 
            #fields = csvreader.next() 
            for row in csvreader: 
                skus1.append(row[0]) 
        skus1.pop(0)
        skus1 = list(oset.oset(skus1))
        return skus1

    def write_to_csv(self,attributes): 
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        rows = attributes
        fields = ['URL']
        filename = "/home/user/python_projects/Amazon/sample4.csv"
        with open(filename, 'w+') as csvfile:
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(fields)
            print "fields created"
            # for i in rows:
            #     csvfile.write(i + '\n')
            csvwriter = csv.writer(csvfile)
            for i in rows:
                csvwriter.writerow([i])


    def get_data(self,skus1):
        self.list1 = []
        for i in skus1:
            self.chrome_executable_driver = "/home/user/Downloads/chromedriver"
            chrome_options = Options()
            us =  UserAgent()
            userAgent = us.random
            print(userAgent)
            chrome_options.add_argument('user-agent={userAgent}')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument('--disable-dev-shm-usage')
            # display = Display(visible=0, size=(800, 800))
            # display.start()
            self.browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=self.chrome_executable_driver)

            product_dict = odict.odict()
            self.browser.get(i)
            time_hold = randint(7,20)
            sleep(time_hold)
            print time_hold
            today = str(datetime.datetime.now())
            product_dict["Date"] = today
            #print "aa"
            if self.hasXpath('//*[@id="productTitle"]'):
                product_dict["Product URL"] = i
                try:
                    product_title = self.browser.find_element_by_xpath('//*[@id="productTitle"]')
                    print product_title.text
                    product_dict["Title"] = product_title.text 
                except Exception as e:
                    product_dict["Title"] = ""

                try:
                    product_SP = self.browser.find_element_by_xpath('//*[@id="priceblock_ourprice"]')
                    product_dict["Selling Price"] = product_SP.text  
                except Exception as e:
                    product_dict["Selling Price"]=""

                try:
                    product_MRP = self.browser.find_element_by_xpath('//*[@id="price"]/table/tbody/tr[1]/td[2]/span[1]')
                    product_dict["MRP"] = product_MRP.text  
                except Exception as e:
                    product_dict["MRP"]=""

                try:
                    if self.hasXpath('//*[@id="olp-new"]/span/span'):
                        product_price = self.browser.find_element_by_xpath('//*[@id="olp-new"]/span/span')
                    else:
                        if self.hasXpath('//*[@id="olp-sl-new"]/span/span'):
                            product_price = self.browser.find_element_by_xpath('//*[@id="olp-sl-new"]/span/span')
                    
                    product_dict["Price"] = product_price.text
                except Exception as e:
                    product_dict["Price"]=""    

                try:
                    product_Model = self.browser.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[9]/div[4]/div/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[2]')
                    product_dict["Model Name"] = product_Model.text  
                except Exception as e:
                    product_dict["Model Name"]=""

                # try:
                #     product_Model = self.browser.find_element_by_xpath('//*[@id="prodDetails"]/div/div[1]/div/div[2]/div/div/table/tbody/tr[1]/td[2]')
                #     product_dict["Brand"] = product_Model.text  
                # except Exception as e:
                #     product_dict["Brand"]=""


                if self.hasXpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr/td[1]'):
                    time.sleep(0.1)
                    prod_info_dt3 = []
                    prod_info_dd3 = []
                    print "csv4"
                    prod_info_dt4 = []

                    prod_info_dt3_list = self.browser.find_elements_by_xpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr/td[1]')
                    for curr_prod_dt3_info in prod_info_dt3_list:
                        prod_info_dt3.append(curr_prod_dt3_info.get_attribute('innerHTML').encode('ascii','ignore').strip().replace('/[^\x00-\x7F]/g', '').replace('.','_').replace('<b>','').replace('</b>','').replace('&nbsp;','').replace('</ul>','').replace('/n','').replace(':',''))
                    
                    prod_info_dt_list = self.browser.find_elements_by_xpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr/td[2]')
                    prod_info_list_count2 = len(prod_info_dt_list)
                        
                    for curr_prod_dt_info in prod_info_dt_list:
                        prod_info_dt4.append(curr_prod_dt_info.get_attribute('innerHTML').encode('ascii','ignore').strip().replace('/[^\x00-\x7F]/g', '').replace('.','_').replace('<b>','').replace('</b>','').replace('&nbsp;','').replace('</ul>','').replace('/n',''))
                    for i in prod_info_dt4:
                        a1 = i.split(':')
                        prod_info_dd3.append(a1[-1].replace(' ','').replace('&amp',''))

                    for x in range(prod_info_list_count2):
                
                        product_dict[prod_info_dt3[x]] = prod_info_dd3[x] 
                        if product_dict[prod_info_dt3[x]] == "":
                            product_dict[prod_info_dd3[x]] ="null"  
                        print "a9"

                if self.hasXpath('//*[@id="prodDetails"]/div/div[1]/div/div[2]/div/div/table/tbody/tr/td[1]'):
                    # time.sleep(0.1)
                    prod_info_dt1 = []
                    prod_info_dd1 = []
                    print "csv7"
                    prod_info_dt1_list = self.browser.find_elements_by_xpath('//*[@id="prodDetails"]/div/div[1]/div/div[2]/div/div/table/tbody/tr/td[1]')
                    for curr_prod_dt1_info in prod_info_dt1_list:
                        prod_info_dt1.append(curr_prod_dt1_info.get_attribute('innerHTML').encode('ascii','ignore').strip().replace('/[^\x00-\x7F]/g', ''))
                    prod_info_list_count1 = len(prod_info_dt1)
                    
                    prod_info_dd1_list = self.browser.find_elements_by_xpath('//*[@id="prodDetails"]/div/div[1]/div/div[2]/div/div/table/tbody/tr/td[2]')
                    for curr_prod_dd1_info in prod_info_dd1_list:
                        if curr_prod_dd1_info.get_attribute('innerHTML').encode('ascii','ignore').strip()=='<i class="fi-x"></i>':
                            prod_info_dd1.append("No")
                        elif curr_prod_dd1_info.get_attribute('innerHTML').encode('ascii','ignore').strip()=='<i class="fi-check"></i>':
                            prod_info_dd1.append("Yes")
                        else:
                            prod_info_dd1.append(curr_prod_dd1_info.get_attribute('innerHTML').encode('ascii','ignore').strip().replace('&amp',''))
                    for x in range(prod_info_list_count1):
                        product_dict[prod_info_dt1[x]] = prod_info_dd1[x] 

               

                else:                    
                    if self.hasXpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li'):
                        # time.sleep(0.1)
                        print "sf"
                        prod_info_dt = []
                        prod_info_dd = []
                        prod_info_dt2 = []
                        
                        prod_info_dt3_list = self.browser.find_elements_by_xpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li/b')
                        for curr_prod_dt3_info in prod_info_dt3_list:
                            prod_info_dt.append(curr_prod_dt3_info.get_attribute('innerHTML').encode('ascii','ignore').strip().replace('/[^\x00-\x7F]/g', '').replace('.','_').replace('<b>','').replace('</b>','').replace('&nbsp;','').replace('</ul>','').replace('/n','').replace(':',''))
                        
                        prod_info_dt_list = self.browser.find_elements_by_xpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li')
                        prod_info_list_count2 = len(prod_info_dt_list)
                        
                        for curr_prod_dt_info in prod_info_dt_list:
                            prod_info_dt2.append(curr_prod_dt_info.get_attribute('innerHTML').encode('ascii','ignore').strip().replace('/[^\x00-\x7F]/g', '').replace('.','_').replace('<b>','').replace('</b>','').replace('&nbsp;','').replace('</ul>','').replace('/n',''))
                        for i in prod_info_dt2:
                            a1 = i.split(':')
                            prod_info_dd.append(a1[-1].replace(' ','').replace('&amp','').replace(';',''))

                        for x in range(prod_info_list_count2):
                
                            product_dict[prod_info_dt[x]] = prod_info_dd[x] 
                            if product_dict[prod_info_dt[x]] == "":
                                product_dict[prod_info_dd[x]] ="null"  
                            print "a4"
                self.mongo(product_dict)
                self.browser.close()
            
            elif self.hastext("Click here to go back to the Amazon home page"):
                continue
                self.browser.close()
            
            else:
                self.list1.append(i)
                print self.list1
                self.browser.close()
                # if self.browser.hastext("Try different image"):
                #     print "hg"
                #     self.list1.append(i)
                #     # self.browser.close()
                #     print self.list1
                #     # self.write_to_csv(list1)
                # elif self.browser.find_element_by_link_text("Click here to go back to the Amazon home page"): 
                # # self.browser.find_element_by_link_text("Click here to go back to the Amazon home page")
                #     continue
                # elif self.browser.find_element_by_link_text("Checking the proxy and the firewall"):
                #     print "gg"
                #     self.browser.refresh()
                #     self.list1.append(i)    
                # else:
                #     print "gg"
                #     self.browser.refresh()
                #     time.sleep(2)
                #     self.list1.append(i)


    def check_data(self,data):
        self.check_count += 1
        print self.check_count
        if len(data) > 0:
            self.get_data(data)
        if len(self.list1) > 0:
            if (self.check_count <= 3):
                self.check_data(self.list1)


    def main(self):
        # count = 0
        #wait = WebDriverWait(self.browser, 10)
        skus1 = self.get_url_list_from_csv()
        self.get_data(skus1)
        self.check_data(self.list1)        
        self.browser.quit()
 
 
if __name__ == "__main__":
    scrap_obj = AmazonScraper()
    scrap_obj.main()
    # schedule.every().day.at("22:00").do(scrap_obj.main)

    # while 1:
    #     schedule.run_pending()
    #     time.sleep(30)               
