import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Specify the path to the ChromeDriver executable
# Update this path
driver_path = "C://Users/Boya RamaKrishna/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"

# Set up Selenium WebDriver with the manually specified path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

url = 'https://www.flipkart.com/search?q=nothing+phone+2a&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_8_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_8_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=nothing+phone+2a%7CMobiles&requestId=1c2fd76c-63b8-43f5-be29-af59f36a13e7&as-searchtext=nothing%20'
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Extract product names
try:
    product_name_elements = driver.find_elements(
        By.XPATH, '//div[@class="KzDlHZ"]')
    productli = [elem.text.strip()
                 for elem in product_name_elements if elem.text.strip()]
    print(f"Product Names: {productli}")
except Exception as e:
    print(f"Error extracting product names: {e}")

# Extract product prices
try:
    product_price_elements = driver.find_elements(
        By.XPATH, '//div[@class="Nx9bqj _4b5DiR"]')
    priceli = [elem.text.strip()
               for elem in product_price_elements if elem.text.strip()]
    print(f"Product Prices: {priceli}")
except Exception as e:
    print(f"Error extracting product prices: {e}")

# Extract Product Reviews and Ratings
try:
    # Find all ratings & reviews elements
    ratings_reviews_elements = driver.find_elements(
        By.XPATH, '//span[@class="Wphh3N"]')
    ratesrevs = []

    for elem in ratings_reviews_elements:
        ratings_reviews_text = elem.text.strip()

        # Extract numbers that may include commas
        numbers = re.findall(r'\d{1,3}(?:,\d{3})*', ratings_reviews_text)

        # Combine and remove commas for the final output
        combined_result = ' & '.join([num.replace(',', '') for num in numbers])
        ratesrevs.append(combined_result)

    print(f"Ratings & Reviews: {ratesrevs}")
except Exception as e:
    print(f"Error extracting ratings and reviews: {e}")


driver.quit()


# Ensure the lists are of the same length
if len(productli) != len(priceli):
    print("Error: The lengths of product names and prices lists do not match.")
else:
    # Write the lists to a CSV file
    with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product Name', 'Product Price', 'Ratings&Reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, price, raterew in zip(productli, priceli, ratesrevs):
            writer.writerow(
                {'Product Name': name, 'Product Price': price, 'Ratings&Reviews': raterew})

    print("CSV file has been created successfully.")
