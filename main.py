from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

categoriesList = ["PatelsFreshKitchen", "Produce", "DairyEggs", "Bakery", "Beverages", "NutsDryFruits", "Snacks", "Spices", "PicklesCondiments", "OilsGhee", "Pantry", "ReadyToEat", "RiceDal", "FryumsNoodles", "Frozen", "HealthBeauty", "HouseholdReligious"]
base_url = 'https://shop.patelbros.com/shop/'

def scroll_down(driver):
    """A method for scrolling the page."""
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_category(url, category):
    driver.get(url)
    # Wait for 5 seconds to ensure the page loads completely
    time.sleep(5)
    products = []
    try:
        # Wait until the h4 elements are present
        wait = WebDriverWait(driver, 10)
        h4_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4.mtopbot0.text-500.text-uppercase.text-secondary")))
        count = 0
        for h4_element in h4_elements:
            count += 1
            if count == 3:
                try:
                    select_button = h4_element.find_element(By.CSS_SELECTOR, "a.btn.location-selected-button.btn-xs.mleft5.ng-scope")
                    select_button.click()
                    print("Clicked the 'Select This Location' button")
                    break
                except Exception as e:
                    print(f"Error clicking the 'Select This Location' button: {e}")
        # Wait for 5 seconds after clicking the first button
        time.sleep(5)
        # Wait until the li elements are present
        li_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.price-list-item.ng-scope")))
        for li_element in li_elements:
            try:
                grocery_button = li_element.find_element(By.CSS_SELECTOR, "h5.mtopbot5.ng-binding")
                if grocery_button and grocery_button.text.strip() == "Groceries":
                    li_element.click()
                    print("Clicked the 'Groceries' button")
                    break
            except Exception as e:
                print(f"Error finding or clicking the groceries button: {e}")
        # Wait for 5 seconds to ensure the page loads completely after clicking the "Groceries" button
        time.sleep(5)
        # Scroll down the page to load all products
        scroll_down(driver)
        # Find all ul elements
        ul_elements = driver.find_elements(By.CSS_SELECTOR, "ul.list-unstyled.row.flex-product-grid.mleftright0.mbot0")
        for ul_element in ul_elements:
            li_elements = ul_element.find_elements(By.CSS_SELECTOR, "li")
            for li_element in li_elements:
                try:
                    # Check if the product is out of stock
                    out_of_stock = li_element.find_elements(By.CSS_SELECTOR, "div.out-of-stock-container span.text")
                    if out_of_stock and "Out of stock!" in out_of_stock[0].text:
                        print(f"Ignoring out of stock product")
                        continue

                    # Extract the product name
                    product_name = li_element.find_element(By.CSS_SELECTOR, "p.text-left.display-name.ng-binding").text.strip()
                except Exception as e:
                    print(f"Error extracting product name: {e}")
                    product_name = "N/A"
                try:
                    # Extract the price
                    price = li_element.find_element(By.CSS_SELECTOR, "span.ng-binding.price").text.strip()
                except Exception as e:
                    print(f"Error extracting price: {e}")
                    price = "N/A"
                if product_name != "N/A" and price != "N/A":
                    print(f"Product: {product_name}, Price: {price}, Category: {category}")
                    products.append((product_name, price, category))
        # Wait for 5 seconds before navigating to the new URL
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
    return products

all_products = []
for category in categoriesList:
    url = base_url + category
    print(f"Scraping URL: {url}")
    products = scrape_category(url, category)
    all_products.extend(products)

# Save data to Excel
df = pd.DataFrame(all_products, columns=["Product Name", "Price", "Category"])
df.to_excel("/Users/lakshminarayanakakumanu/Documents/products.xlsx", index=False)

# Close the WebDriver
driver.quit()
