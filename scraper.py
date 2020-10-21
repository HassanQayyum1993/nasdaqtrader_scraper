import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def check_in_file(i_string):
    try:
            global is_new_row
            with open(old_file_name, 'r') as read_obj:
                next(read_obj) #skip header
                # Read all lines in the file one by one
                for line in read_obj:
                    # For each line, check if line contains the string
                    if i_string in line:
                        is_new_row = False
                        break
                else:
                    is_new_row = True

    except Exception as e:
        print('check_in_file(): '+str(e))

def get_each_row(tag_name):

    try:
        count = 0
        col_5_str = ''
        
        global table, heading_list, unique_key_str, is_new_row, count_new_row
        unique_key_str = ''
        
        for row in table.find_elements_by_xpath(tag_name):
            row_dict = {}
            for col_data in row.find_elements_by_xpath('.//td'):
                if count == 5:
                    for a_tag in col_data.find_elements_by_xpath('.//a'):
                        col_5_str += a_tag.text + ' '
                    row_dict[heading_list[count]] = col_5_str
                else:    
                    row_dict[heading_list[count]] = col_data.text
                if count<3:
                    unique_key_str += col_data.text
                    unique_key_str += ','
                
                count+=1

            if row_dict:
                if os.path.isfile(old_file_name):
                    check_in_file(unique_key_str)
                else:
                   is_new_row = True 
                if is_new_row == True:
                    count_new_row += 1
                    row_list.append(row_dict)
    
    except Exception as e:
        print('get_each_row(): '+str(e))

try:

    browser = webdriver.Chrome()
    browser.get('https://nasdaqtrader.com/Trader.aspx?id=TradeHalts')
    browser.implicitly_wait(5)
    heading_list = []
    heading_list_len = 0
    table = browser.find_element_by_class_name("genTable")
    row_list = []
    is_new_row = True
    count_new_row = 0
    row1 = table.find_elements_by_xpath('.//tr[1]')
    old_file_name = "Data/Old_Halts.csv"  
    new_file_name = "Data/New_Halts.csv"
    dir_path = "Data/"
    csv_file = new_file_name
    unique_key_str = ''

    #create Data folder
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    #rename file to Old_Halts.csv
    if os.path.isfile(new_file_name):
        os.rename(new_file_name, old_file_name)
    
    #store headings

    for head_row in row1:
        for col_heading in head_row.find_elements_by_xpath('.//th'):
            heading_list.append(col_heading.text)    
    
    heading_list_len = len(heading_list)

    #store row data

    i = 2
    for row in table.find_elements_by_xpath('.//tr'): 
        if is_new_row == True:
            get_each_row('.//tr['+str(i)+']')
            i+=1


    if count_new_row or not os.listdir('Data'):
        with open(new_file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=heading_list)
            writer.writeheader()
            for data in row_list:
                writer.writerow(data)
    
    #if old and new file both are present delete the old file
    if os.path.isfile(old_file_name) and os.path.isfile(new_file_name):
        os.remove(old_file_name)

    browser.quit()
    sys.exit(0)

except Exception as e:
    sys.exit('main(): '+str(e))

