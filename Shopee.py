import nltk
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import csv
import os
import datetime


class Shopee_extract:
    def __init__(self, html_file):
        self.soup = BeautifulSoup(html_file, "html.parser")

    def take_shop_info(self):
        ahop_info = self.soup.find_all("span", class_ = "Cs6w3G")
        all_info = []
        for each in shop_info:
            each_info = each.text.strip()
            all_info.append(each_info)
        Danh_gia = all_info[0]
        Ti_Le_Phan_Hoi_Chat = all_info[1]
        Tham_Gia = all_info[2]
        So_San_Pham = all_info[3]
        Thoi_gian_phan_hoi = all_info[4]
        Nguoi_Theo_Doi = all_info[5]
        return Danh_gia,Ti_Le_Phan_Hoi_Chat,Tham_Gia,So_San_Pham,Thoi_gian_phan_hoi,Nguoi_Theo_Doi
    
    def take_all_product_type(self):
        all_product_type = self.soup.find_all('button', class_='sApkZm SkhBL1 selection-box-unselected')
        all_product = []
        for each in all_product_type:
            product_type = each.get('aria-label')
            all_product.append(product_type)
        return all_product    

    def total_rating_product(self):
        total_rating = self.soup.find('div',class_="F9RHbS dQEiAI")
        total_rating_star = total_rating.text.strip()
        return total_rating_star
    
    def total_review_product(self):
        button_element = self.soup.find_all('button', class_='flex e2p50f')
        for each in button_element:
            total_review = each.find('div',class_= 'F9RHbS')
            total_review_pro = total_review.text.strip()
        return total_review_pro
    
    def all_sales(self):
        all_sale = self.soup.find('div',class_='AcmPRb')
        sales = all_sale.text.strip()
        return sales
    
    def take_price(self):
        price = "none"
        discount_rate= 'none'
        if self.soup.find("div",class_="qg2n76") :
            ori_price = self.soup.find("div",class_="qg2n76")
            price = ori_price.text.strip()
        price_after_discount = self.soup.find('div',class_='G27FPf')
        if self.soup.find('div',class_='o_z7q9'):
            discount = self.soup.find('div',class_='o_z7q9')
            discount_rate = discount.text.strip() 
        return price,price_after_discount.text.strip(), discount_rate
    
    def take_ProductID(self):
        global product_id
        script_tag = self.soup.find_all('script', type='application/ld+json')
        for sctrip in script_tag:
            try:    
                script_content = sctrip.string.strip()
                data = json.loads(script_content)
            except json.JSONDecodeError:
                continue

            if 'productID' in data:
                product_id = data['productID']
        return product_id
    
    def take_Product_name(self):
        product = self.soup.find_all('div', class_='WBVL_7')
        for each in product:
            if each and each.find('span'):
                Product_name = each.text.strip()
                return Product_name
    
    def take_shop_name(self):
        shop = self.soup.find_all('div',class_="fV3TIn")
        for each in shop:
            Shop_Name = each.text.strip() 
            return Shop_Name
        
    def take_customer_name(self):
        Name_cus = []
        Name_1 = self.soup.find_all('div', class_='shopee-product-rating__author-name')
        for name in Name_1:
            Name_cus.append(name.text.strip())
        Name_2 = self.soup.find_all('a', class_='shopee-product-rating__author-name')
        for name in Name_2:
            Name_cus.append(name.text.strip())
        return Name_cus
    
    def take_review(self):
        Time_Cat = []
        Review = []
        each_review = self.soup.find_all('div',class_='shopee-product-rating__time' )
        # review_text = each_review.find_next_sibling('div')
        for review in each_review:
            Time_n_Product = review.text.strip()
            a_review = review.find_next_sibling('div')
            review_text = a_review.text.strip()
            Review.append(review_text)
            Time_Cat.append(Time_n_Product)
        return Review, Time_Cat
    
    def take_Time_Category(self):
        Time = []
        Category = []
        review,Time_Cat = self.take_review()
        for time in Time_Cat:
            time = time.split("|")
            Time.append(time[0])
            Category.append(time[1])
        return Time, Category
    
    def take_rating_star(self):
        Rating_star = []
        stars = self.soup.find_all('div',class_="shopee-product-rating__rating")
        for star in stars:
            count = star.find_all('polygon',fill = 'none')
            star_num = 5 - len(count)
            Rating_star.append(star_num)
        return Rating_star
    
    def take_review_information(self):
        Rating_star = self.take_rating_star()
        Review, __ = self.take_review()
        product_id = self.take_ProductID()
        Shop_name  = self.take_shop_name()
        Product_name = self.take_Product_name()
        Time,Category = self.take_Time_Category()
        Name_cus = self.take_customer_name()
        return Shop_name,Product_name,product_id, Time, Category, Name_cus, Review, Rating_star
    
    def to_csv_shop_info(self):
        So_San_Pham,Nguoi_Theo_Doi,Dang_Theo,Danh_gia,Ti_Le_Phan_Hoi_Chat,Tham_Gia= self.take_shop_information()
        ori_price,price_after_discount, discount = self.take_price()
        Shop_name = self.take_shop_name()
        df = pd.DataFrame(zip(Shop_name, So_San_Pham, Nguoi_Theo_Doi, Dang_Theo, Danh_gia,Ti_Le_Phan_Hoi_Chat,Tham_Gia), columns=['Ten_Shop', 'So_San_Pham', 'Nguoi_Theo_Doi', 'Dang_Theo',"Danh_gia","Ti_Le_Phan_Hoi_Chat",'Tham_Gia'])
    
    def to_csv(self):
        Shop_name,Product_name,product_id ,Time, Category, Name_cus, Review, Rating_star, total_rating_star,total_review_pro,sales,ori_price,price_after_discount,discount = self.take_review_information()
        Danh_gia,Ti_Le_Phan_Hoi_Chat,Tham_Gia,So_San_Pham,Thoi_gian_phan_hoi,Nguoi_Theo_Doi= self.take_shop_information()
        ori_price,price_after_discount, discount = self.take_price()

        
        df = pd.DataFrame(zip(Time, Category, Name_cus, Review, Rating_star,), columns=['Time', 'Mat_Hang', 'Ten_khach_hang', 'Thong_tin_Review',"Sao_danh_gia"])
        # print(df)
        # df = pd.DataFrame( { 'Time' : Time, "Category" : Category,"Name_cus" : Name_cus,"Review" : Review,"Rating" : Rating_star})
        Danh_gia,Ti_Le_Phan_Hoi_Chat,Tham_Gia,So_San_Pham,Thoi_gian_phan_hoi,Nguoi_Theo_Doi
        df1 = pd.DataFrame({"Shop_name" : [Shop_name], "Product_name" : [Product_name], "Product_ID": [product_id],"Total_Rating" : [Danh_gia], "Response_rate" : [Ti_Le_Phan_Hoi_Chat], "Join_from": [Tham_Gia],
                            "Total_Product" : [So_San_Pham], "Response_time" : [Thoi_gian_phan_hoi], "Follower": [Nguoi_Theo_Doi]})
        df = df.assign(Shop_name=Shop_name, Product_name=Product_name, Product_ID=product_id)
        row_to_keep = df1.iloc[0:1]
        merged_df = pd.concat([row_to_keep,df], ignore_index=True)
        x = datetime.datetime.now()
        file_path = Shop_name + 'Output.csv'
        if os.path.exists(file_path):
            df_exist = pd.read_csv(file_path)
            output = pd.concat([df_exist,merged_df],ignore_index= True)
            output.to_csv(file_path, index=False,encoding= "utf-8-sig")
        else:
            merged_df.to_csv(file_path, index=False,encoding = 'utf-8-sig')



