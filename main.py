import datetime
import json
import os
import re
import requests
from bs4 import BeautifulSoup

from models.category import Category
from models.foods import FoodItem
from models.subcategory import Subcategory

# Define the target URL
url = 'https://www.sklavenitis.gr/sitemap/'
test_url = 'https://www.sklavenitis.gr/freska-froyta-lachanika/'
api_url = 'http://127.0.0.1:8000/items/'

# Send a GET request
response = requests.get(url)
test_response = requests.get(test_url)


def main():
    getCategories()
    getFood(test_response)
    
# Check if the request was successful
def getCategories():
    categories_list = []
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the main sitemap div
        sitemap_div = soup.find('div', class_='row sitemap')
        
        # Extract the categories
        categories = sitemap_div.find_all('div', class_='sect')
        
        for category_div in categories:
            # Extract category title
            category_title = category_div.find('h5').text.strip()
            category = Category(title=category_title)
            
            # Extract subcategories
            subcategories = category_div.find_all('a')
            
            for subcategory in subcategories:
                subcategory_title = subcategory.text.strip()
                subcategory_link = subcategory['href']
                subcategory_obj = Subcategory(title=subcategory_title, link=subcategory_link)
                category.add_subcategory(subcategory_obj)
            
            categories_list.append(category)
    else:
        print('Failed to retrieve the webpage')
    
    for category in categories_list:
        print(category)
    return

def post_to_api(food_item):
    # Convert the FoodItem object to a dictionary
    data = food_item.to_dict()
    print(f"Posting data: {data}")
    # Send POST request to FastAPI API
    response = requests.post(api_url, json=data)
    
    if response.status_code == 200:
        print(f"Successfully added {food_item.name}")
    else:
        print(f"Failed to add {food_item.name}, status code: {response.status_code}")

def getFood(repsonse):
    food_items = []
    food_items_api = []

    soup = BeautifulSoup(repsonse.text, 'html.parser')
    # product_number= soup.find('div', class_='page').find('span', class_='current-page').text.strip().split()[3]
    # category_pages = int(product_number) // 24 + 1 if int(product_number) % 24 > 0 else ""
    # if category_pages > 1:
    #     for i in range(1, category_pages):
    #         url = f'{response}/?pg={i}'
    #         test_response = requests.get(url)
    #         getFoodItems(test_response, food_items)
    # else:
    #     getFoodItems(test_response, food_items)
        
    if test_response.status_code == 200:
        product_list = soup.find('section', class_='productList list-items-container')

        if product_list:
            # Find all food items
            products = product_list.find_all('div', re.compile(r'product prGa.*'))

            for product in products:
                name = product.find('h4', class_='product__title').text.strip() if product.find('h4', class_='product__title') else 'No Name'
                
                # Extract product SKU from data-item attribute
                data_item = product.get('data-item')
                if data_item:
                    product_data = json.loads(data_item)
                    product_sku = product_data.get('ProductSKU', 'No SKU')
                else:
                    product_sku = 'No SKU'
                
                deleted_price_per_kilo = None
                price_per_kilo = None
                deleted_main_price = None
                main_price = None
                food_id = None
                food_desc = None
                has_kilo_price = None
                has_piece_price = None
                food_photo = None
                
                
                product_inner_btm = product.find('div', class_='product_innerBtm')
                if product_inner_btm:
                    price_kil_div = product_inner_btm.find('div', class_='priceKil')
                    ekptosi = price_kil_div.find('div', class_='deleted')
                    main_price_div = product_inner_btm.find('div', class_='main-price')
                    image_tag = product.find('div', class_='product_innerTop').find('img')
                    image_path = image_tag['src'] if image_tag else None
                    food_photo = download_image(image_path, product_sku) if image_path else None
                    if ekptosi:
                        if price_kil_div:
                            deleted_price_per_kilo = price_kil_div.find('div', class_='deleted__price').text.strip() if price_kil_div.find('div', class_='deleted__price') else None
                            price_per_kilo = price_kil_div.find('div', class_='hightlight').text.strip().split()[0] if price_kil_div.find('div', class_='hightlight') else None
                            price_per_kilo = price_per_kilo.replace(',', '.') if price_per_kilo else None
                            price_per_kilo = extract_price(price_per_kilo) if price_per_kilo else None
                        
                        if main_price_div:
                            deleted_main_price = main_price_div.find('div', class_='deleted__price').text.strip() if main_price_div.find('div', class_='deleted__price') else None
                            main_price = main_price_div.find('div', class_='price').text.strip().split()[0] if main_price_div.find('div', class_='price') else None
                            main_price = main_price.replace(',', '.')
                            main_price = extract_price(main_price) 
                    else:
                        price_per_kilo = price_kil_div.text.strip() if price_kil_div else None
                        main_price = main_price_div.find('div', class_='price').text.strip().split()[0] if main_price_div.find('div', class_='price') else None
                        main_price = main_price.replace(',', '.')
                        price_per_kilo = price_per_kilo.replace(',', '.') if price_per_kilo else None
                        price_per_kilo = extract_price(price_per_kilo) if price_per_kilo else None
                
                
                food_item = FoodItem(name=name, deleted_price_per_kilo=deleted_price_per_kilo, price_per_kilo=price_per_kilo, deleted_main_price=deleted_main_price, main_price=main_price, food_id= food_id, food_desc=food_desc, has_kilo_price=has_kilo_price, has_piece_price=has_piece_price, food_photo=food_photo)
                food_items.append(food_item)
                
                # Add the food item to the list
                food_items_api.append(food_item)
                
                # Post to API
                post_to_api(food_item)

        else:
            print('Product list not found')
    else:
        print('Failed to retrieve the webpage')

    # Print the extracted food items
    for item in food_items:
        print(item)

def download_image(image_url, image_name, save_folder='images'):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    image_path = os.path.join(save_folder,image_name + '.jpg')
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    return image_path

def extract_price(price_str):
    # Use regex to extract the first occurrence of a numeric value (with or without a decimal point)
    match = re.search(r'\d+(\.\d+)?', price_str)
    if match:
        return float(match.group())  # Convert to float for correct data type
    return None
main()