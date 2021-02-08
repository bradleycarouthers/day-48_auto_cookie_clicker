from selenium import webdriver
import time

chrome_driver_path = "C:/Development/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element_by_id("cookie")

# Store items
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]


# Time limits
timeout = time.time() + 5
five_min = time.time() + 5 * 60


# Start loop
while True:
    cookie.click()

    # After 5 seconds
    if time.time() > timeout:

        # Find prices and make list
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []

        # Get cost
        for price in all_prices:
            element_text = price.text
            try:
                if element_text != "":
                    cost = int(element_text.split("-")[1].replace(",", ""))
                    item_prices.append(cost)
            except AttributeError:
                print("Cost is 0")

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        cookie_count = driver.find_element_by_id("money").text
        money = int(cookie_count.replace(",", ""))

        # Find affordable upgrades
        right_panel = driver.find_element_by_id("rightPanel")
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if money > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        driver.find_element_by_id(to_purchase_id).click()

        timeout = time.time() + 5

    # After 5 minutes stop the bot and check cookies p/s
    if time.time() > five_min:
        print(driver.find_element_by_id("cps").text)
        break
