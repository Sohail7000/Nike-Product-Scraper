from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
from pymongo import MongoClient
import config

# Now you can access the MongoDB connection URL from the config module
mongo_url = config.MONGO_URL


# creating a chrome webdriver to run automation
driver = webdriver.Chrome()

#going to the link
driver.get("https://www.nike.com/ie/w/mens-shoes-nik1zy7ok")



#extracting the link of all the shoes from the product page and stroring it in a list
shoe_ele = driver.find_elements(
    By.CSS_SELECTOR, '[data-testid="product-card__link-overlay"]')

all_shoe_links = []

for i in range(len(shoe_ele)):
    link = shoe_ele[i].get_attribute("href")
    print(link)
    all_shoe_links.append(link)


# creating an empty list to store the values
product_title_list = []
product_category_list = []
product_price_list = []
product_description_list = []
review_count_list = []
product_rating_list = []

for i in range(len(all_shoe_links)):
    driver.get(all_shoe_links[i])
    time.sleep(3)

    # product title
    product_title = driver.find_elements(
        By.CSS_SELECTOR, '[data-test="product-title"]')[1].text
    product_title_list.append(product_title)
    print(product_title)

    # product category
    product_category = driver.find_elements(
        By.CSS_SELECTOR, '[data-test="product-sub-title"]')[1].text
    product_category_list.append(product_category)
    print(product_category)

    # product_price
    product_price = driver.find_elements(
        By.CSS_SELECTOR, '[data-test="product-price"]')[1].text
    product_price_list.append(product_price)
    print(product_price)

    # product_description
    product_description = driver.find_element(
        By.CSS_SELECTOR, '[class="description-preview body-2 css-1pbvugb"]').text
    product_description_list.append(product_description)
    print(product_description)

    # review_count
    review_count = driver.find_elements(
        By.CSS_SELECTOR, '[class="headline-4"]')[-1].text
    review_count_list.append(review_count)
    print(review_count)

    # product rating
    product_rating_sel = driver.find_element(By.CSS_SELECTOR, '.css-n209rx')

    # Get the value of the aria-label attribute
    product_rating = product_rating_sel.get_attribute("aria-label")

    product_rating_list.append(product_rating)

    # Extract the rating from the aria-label attribute
    print("Rating:", product_rating)
    
    
#creating a Dataframe from the dictonary
product_details = {
    "product_title": product_title_list,
    "product_category": product_category_list,
    "product_price": product_price_list,
    "product_description": product_description_list,
    "review_count": review_count_list,
    "product_rating": product_rating_list
}

df = pd.DataFrame(product_details)

print(df)


""" 
data cleaning using python library called re(regex) to remove the euro sign and other strings to convert the price into float and also extract the value of review_count from reviews
"""

# Extract numeric values from strings and convert to float
df['product_price'] = df['product_price'].str.extract(
    r'(\d+\.\d+)').astype(float)


# Extract numeric values from strings and replace non-matching rows with "Not Applicable"
df['review_count'] = df['review_count'].apply(lambda x: re.findall(
    r'\d+', x)[0] if re.findall(r'\d+', x) else "Not Applicable")



""" 
Sending the dataframe to a NoSQL Database called Mongodb

"""

try:
    # Connect to MongoDB
    client = MongoClient(
        mongo_url)
    db = client['nike_product_scraper']
    collection = db['nike_product_details']

    # Convert DataFrame to dictionary
    data = df.to_dict(orient='records')
    print(data)

    # Insert data into MongoDB collection
    collection.insert_many(data)

    print("Data inserted successfully into MongoDB")

except Exception as e:
    print("Error:", e)

finally:
    # Close connection
    client.close()
