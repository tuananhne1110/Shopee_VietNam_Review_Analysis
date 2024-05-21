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
    
    def to_csv(self):
        Shop_name,Product_name,product_id ,Time, Category, Name_cus, Review, Rating_star = self.take_review_information()
        
        df = pd.DataFrame(zip(Time, Category, Name_cus, Review, Rating_star), columns=['Time', 'Mat_Hang', 'Ten_khach_hang', 'Thong_tin_Review',"Sao_danh_gia"])
        df1 = pd.DataFrame({"Shop_name" : [Shop_name], "Product_name" : [Product_name], "Product_ID": [product_id]})
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



