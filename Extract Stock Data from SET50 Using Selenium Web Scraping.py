#!/usr/bin/env python
# coding: utf-8

# # Project: Scrape Stock Data SET50 by Selenium Web Scraping 

# **Objective** :  รวบรวมข้อมูลงบการเงินของหุ้นในกลุ่ม SET50 จากเว็บไซต์ตลาดหลักทรัพย์ เพื่อใช้ในการวิเคราะห์ทางการเงินและการลงทุน แปลงข้อมูลทั้งหมดเป็น Structure Data ในรูปแบบไฟล์ CSV 

# ### Static Website & Dynamic Website ต่างกันอย่างไร

#     1.1 Static Website 
#         - เป็นเว็บไซต์ที่มีเนื้อหาคงที่ ไม่เปลี่ยนแปลงไปตามผู้ใช้หรือสถานการณ์ต่างๆ
#         - ไม่ต้องรอเว็บโหลดเนื้อหา 
#         - เหมาะสำหรับเว็บที่ไม่ต้องการการเปลี่ยนแปลงบ่อย 
#         - เช่น Wikipedid , Educational Website เป็นต้น
#     
#     1.2 Dynamic Website
#         - เป็นเว็บไซต์ที่มีเนื้อหาเปลี่ยนแปลงได้ตามผู้ใช้หรือสถานการณ์
#         - ต้องรอเว็บโหลดเนื้อหา
#         - เหมาะสำหรับเว็บที่ต้องมีการปรับปรุงเนื้อหาบ่อยๆ 
#         - เช่น ร้านค้าออนไลน์, แอพพลิเคชั่น Facebook, Shopee, Lazada, Tiktok เป็นต้น

# # !!! ลองใช้ read_html กับ Dynamic Website

# นี่คือ website SET50 ที่ต้องการโหลดข้อมูลหุ้น
#         https://www.set.or.th/th/market/index/set50/overview
# 
#     ซึ่งจัดเป็น Dynamic Website จะใช้ read_html ไม่ได้
#     จึงต้องใช้ selenium ในการดึงข้อมูล

# In[961]:


import pandas as pd
pd.read_html("https://www.set.or.th/th/market/index/set50/overview")[1]


# # ดังนั้น : SET50 เป็น dynamic website จึงต้องใช้ selenium ในการดึงข้อมูล
# ทำได้ดังต่อไปนี้

# # 1. ติดตั้ง package และ Library ที่ใช้สำหรับ Web Scraping by Selenium

# In[968]:


# ติดตั้ง selenium 
# ติดตั้ง webdriver-manager
# ติดตั้ง html5lib
get_ipython().system('pip install selenium')
get_ipython().system('pip install webdriver-manager')
get_ipython().system('pip install html5lib')


# In[975]:


#Library ที่ใช้

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 

import html5lib 
import time #หน่วงเวลา 

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()))


# # 2. ใช้ driver.get() ในการดึงข้อมูลจากเว็บไวต์ของ SET มาไว้ที่ web chrome browser 

# In[979]:


driver.get('https://www.set.or.th/th/market/index/set50/overview')


# # 3. ใช้ driver.page_source ในการดึง html 

# In[982]:


SET50_data = driver.page_source 


# # 4. pd.read_html อ่าน html จะได้ list

# In[988]:


data_df = pd.read_html(SET50_data) 


# # 5. แปลง list เก็บไว้ใน dataframe

# In[1001]:


# เก็บไว้ใน data_df
data_df = pd.read_html(SET50_data)[1]  #[1] คือ Tableที่ 1 จาก html
data_df


# # 6. จัดการหัวตาราง 

#     6.1 Clean หัวตาราง ต้องการลบ "  (Click to sort Ascending)" เก็บไว้ในตัวแปร SET50_df
#     6.2 set index เป็นหลักทรัพย์

# In[1005]:


data_df.columns


# In[1010]:


# 6.1 Clean หัวตาราง ต้องการลบ "  (Click to sort Ascending)" เก็บไว้ในตัวแปร SET50_df
SET50_df = data_df.rename(columns=lambda x: x.replace("  (Click to sort Ascending)",""))
SET50_df.head()


# In[1012]:


# 6.2set index เป็นหลักทรัพย์
SET50_df = SET50_df.set_index("หลักทรัพย์")
SET50_df


# # 7. XD ที่ขึ้นอยู่หลังหุ้น คืออะไร ?

# In[1015]:


SET50_df.index


#   XD หรือว่า Ex-Dividend 
# - ถ้าเราเห็นก็แปลว่า คนที่ซื้อกองทุนรวมหรือหุ้น ณ วันที่ขึ้นสัญญาณนี้ ก็จะไม่ได้รับเงินปันผล
# - โดยปกติแล้วหุ้นหรือกองทุนจะประกาศวันที่ขึ้น XD ออกมาล่วงหน้า แต่ยังไม่ใช่วันที่ได้รับเงินปันผลจริง ๆ แล้วก็จะบอกว่าเงินปันผลที่จะเข้าบัญชีเราจริง ๆ วันไหนอีกที
# 
# ขอบคุณ ข้อมูลจาก : https://www.moneybuffalo.in.th/vocabulary/what-is-xd

# In[1018]:


# ดังนั้น จะลบ "XD" ออกจากชื่อ หลักทรัพย์ทุกตัว
# เช่น AWC XD , WHA XD ให้เหลือเพียง AWC , WHA
SET50_df.index = SET50_df.index.str.replace('  XD','')


# In[1020]:


SET50_df.index


# # 8. ต้องการโหลดข้อมูลงบการเงินของหุ้นทุกตัวใน SET50 จะยก หุ้น "AOT" มาทำเป็นตัวอย่างก่อน

# 8.1 กดเข้าไปดู "งบการเงิน" ของหุ้น AOT

#     https://www.set.or.th/th/market/product/stock/quote/AOT/financial-statement/company-highlights

# 8.2 กำหนดให้ stock_name คือ ชื่อหุ้น

# In[1033]:


stock_name = SET50_df.index[1] 
stock_name


# 8.3 สร้าง link สำหรับไปเก็บข้อมูลหุ้นแต่ละตัว 

# In[1037]:


url = 'https://www.set.or.th/th/market/product/stock/quote/' + stock_name + '/financial-statement/company-highlights'
url


# 8.4 เปิดเว็บที่มีข้อมูลงบการเงินของหุ้นด้วย driver.get

# In[1040]:


driver.get(url)


# 8.5 ใช้ driver.page_source ไปหา html

# In[1043]:


stock_data = driver.page_source


# 8.6 pd.read_html เพื่ออ่านค่าhtml เป็น list

# In[1046]:


pd.read_html(stock_data)


# 8.7 เปลี่ยน list เป็นตาราง dataframe

# In[1055]:


# a_df  คือ ตารางงวดงบการเงิน ณ วันที่
# b_df คือ ค่าสถิติสำคัญ ณ วันที่
a_df = pd.read_html(stock_data)[0]
b_df = pd.read_html(stock_data)[1]


# In[1057]:


a_df


# In[1059]:


b_df


# 8.8 บันทึกตารางลงใน Dictionary โดย key = stock_name

# In[1062]:


all_stock_dict = dict()
all_stock_dict


# In[1065]:


all_stock_dict[stock_name] = [a_df, b_df]


# In[1067]:


all_stock_dict


# # 9. เอาขั้นตอนที่ 8.1-8.8 มารวมกัน  เพื่อทำเป็น for loop วนเก็บค่าของหุ้นให้ครบ 50 ตัว

# In[1074]:


SET50_df.index


# In[1073]:


all_stock_dict = dict() #เอาไว้เก็บหุ้นทุกตัวเมื่อวนครบลูป

for i in range(len(SET50_df.index)):
    stock_name = SET50_df.index[i]
    url = 'https://www.set.or.th/th/market/product/stock/quote/' + stock_name + '/financial-statement/company-highlights'
    driver.get(url) #เปิด browser url
    time.sleep(5) # หน่วงเวลา 5 วินาที
    
    stock_data = driver.page_source #ดึง html
    a_df = pd.read_html(stock_data)[0] #งวดงบการเงิน ณ วันที่
    b_df = pd.read_html(stock_data)[1] #ค่าสถิติสำคัญ ณ วันที่
    all_stock_dict[stock_name] = [a_df, b_df] #เก็บค่าตารางทั้งสองส่วนไว้ในรูปแบบ Dictionary 


# In[1079]:


# แสดงข้อมูลของหุ้น SET 50 ตัวที่โหลดมาไว้ในรูปแบบ Dictionary 
all_stock_dict


# # 10.เรียกดูหุ้น ตามชื่อหลักทรัพย์ ยกตัวอย่างหุ้นที่ชื่อว่า "AOT"

# In[1090]:


all_stock_dict["AOT"][0] #ตาราง งวดงบการเงิน ณ วันที่ ของหุ้น AOT


# In[1094]:


all_stock_dict["AOT"][1]  #ตาราง ค่าสถิติสำคัญ ณ วันที่ ของหุ้น AOT


# # 11. แปลงข้อมูลเป็น Dataframe

# In[1097]:


all_stock_dict["AOT"][0]


# In[1101]:


# ตาราง งวดงบการเงิน ณ วันที่ ของหุ้น AOT
# Transpose ตาราง
A = all_stock_dict["AOT"][0] 
A = A.T
A


# In[1103]:


#กำหนดให้ แถวแรกเป็นชื่อ column
A.columns = A.iloc[0]
A = A.iloc[1:] 
A


# In[1105]:


#เพิ่ม column ชื่อของหุ้น
A.insert(0, "stock_name", "AOT")
A


# # ใช้ For loop แปลงข้อมูลหุ้นทุกตัวเป็น Dataframe

# In[1115]:


all_stock_dict.keys()


# # 11.1 แปลง dictionary งวดงบการเงิน ณ วันที่ ของหุ้น เป็น Dataframe

# In[1121]:


result_list_A = []

for key in all_stock_dict.keys(): #ชื่อหุ้น
    A = all_stock_dict[key][0] # ตารางงวดงบการเงิน ณ วันที่ ของหุ้น
    A = A.T #Transpose ตาราง
    A.columns = A.iloc[0] #กำหนดให้ แถวแรกเป็นชื่อ column
    A = A.iloc[1:]
    A.insert(0, "stock_name", key) #เพิ่ม column ชื่อของหุ้น
    result_list_A.append(A) #เก็บไว้ใน list result_list_A


# In[1127]:


#แปลง list เก็บไว้ใน dataframe result_df_A
result_df_A = pd.concat(result_list_A, ignore_index=False) 
result_df_A


# In[1129]:


#  Reset index 
# เปลี่ยนชื่อ column 
result_df_A.reset_index(drop=False,inplace =True)
result_df_A.rename(columns={'index': 'งวดงบการเงิน ณ วันที่'}, inplace = True)


# In[1133]:


# ได้ตาราง งวดงบการเงิน ณ วันที่ ของหุ้น เป็น Dataframe 
result_df_A


# # 11.2  แปลง dictionary ตารางค่าสถิติสำคัญ ณ วันที่ เป็น Dataframe

# In[1141]:


result_list_B = []

for key in all_stock_dict.keys():
    B = all_stock_dict[key][1]
    B = B.T
    B.columns = B.iloc[0]
    B = B.iloc[1:]
    B.insert(0, "stock_name", key)
    result_list_B.append(B)


# In[1143]:


result_df_B = pd.concat(result_list_B, ignore_index=False)
result_df_B


# In[1145]:


result_df_B.reset_index(drop=False,inplace =True)
result_df_B.rename(columns={'index': 'ค่าสถิติสำคัญ ณ วันที่'}, inplace = True)


# In[1147]:


# ได้ตาราง "ค่าสถิติสำคัญ ณ วันที่" ของหุ้น เป็น Dataframe
result_df_B


# # 12. ทำการรวมตาราง result_df_A และ result_df_B

#     Concept : 
#         12.1 สร้าง column ใหม่ให้กับทั้งสองตาราง เพื่อใช้ merge table
#         12.2 column ใหม่ ชื่อว่า "stock_name_Year"
#         12.3 "stock_name_Year" มีรูปแบบเอาชื่อ stock_name และ year มาต่อ string กัน ยกตัวอย่าง เช่น ADVANC-2563, AOT-2566 
#         12.4 ดังนั้น จะสร้าง column "Year" ในทั้ง result_df_A และ result_df_B

# # result_df_A สร้าง column "stock_name_Year"

# In[1157]:


result_df_A.head(4)


# In[1159]:


result_df_A["งวดงบการเงิน ณ วันที่"].value_counts()


# In[1163]:


#สกัดเอาเฉพาะปีออกมาใส่ column ใหม่ ที่ตั้งชื่อว่า Year
result_df_A["Year"] = result_df_A["งวดงบการเงิน ณ วันที่"].str.split().str[-1]


# In[1165]:


result_df_A.head()


# In[1167]:


#เอา Stockname มาต่อกัน กับ yearเข้าไปตัดเอาปี
result_df_A["stock_name_Year"] = result_df_A['stock_name'] + "-" + result_df_A["Year"]


# In[1171]:


#ผลลัพธ์
result_df_A


# # result_df_B สร้าง column "stock_name_Year" 

# In[846]:


result_df_B.head(4)


# In[1174]:


result_df_B["ค่าสถิติสำคัญ ณ วันที่"].value_counts()


# In[1176]:


#สกัดเอาเฉพาะปีออกมาใส่ column ใหม่ ที่ตั้งชื่อว่า Year
result_df_B["Year"] = result_df_B["ค่าสถิติสำคัญ ณ วันที่"].str.split().str[-1]


# In[1178]:


result_df_B.head()


# In[1180]:


#เอา Stockname มาต่อกัน กับ year
result_df_B["stock_name_Year"] = result_df_B['stock_name'] + "-" + result_df_B["Year"]


# In[1182]:


#ผลลัพธ์
result_df_B


# # รวมตาราง result_df_A และ result_df_B ด้วยฟังก์ชั่น pd.merge()

# In[1211]:


merged_df = pd.merge(result_df_A, result_df_B, on= "stock_name_Year", how='left' )

# how='left' เพราะอยากให้หุ้นทุกตัวแสดงข้อมูลทั้งหมดที่มี หากไม่มีแสดงเป็นช่องว่าง
# left table คือ result_df_A งวดงบการเงิน ณ วันที่ จะปรากฎข้อมูลหุ้นครบทุกปี
# ในขณะที่ right table คือ result_df_B ค่าสถิติสำคัญ ณ วันที่ บางปีอาจจะไม่มีข้อมูลเลย เช่น หุ้น OR ปี 2563 ซึ่งเป็นปีแรกของหุ้นตัวนี้


# In[1188]:


merged_df


# In[1191]:


merged_df.columns


# In[1193]:


#ลบ column ที่ไม่จำเป็น
merged_df.drop(columns = ['Year_x', 'stock_name_y', 'บัญชีทางการเงินที่สำคัญ'], axis =1 ,inplace = True)


# In[1195]:


merged_df.columns


# In[1197]:


#เปลี่ยนชื่อ column
merged_df.rename(columns = {'stock_name_x' : 'หลักทรัพย์', 
                           'stock_name_Year' : 'หลักทรัพย์-ปี',
                           'Year_y' : 'ปี'}, inplace = True)


# In[1199]:


merged_df.columns


# In[1202]:


merged_df


# #  บันทึกหุ้น SET 50 ทุกตัวเป็น CSV เพื่อนำไปใช้ประโยชน์ต่อไป

# In[1207]:


merged_df.to_csv("SET50_stock.csv")

