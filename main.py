from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from format_products_to_table import write_data

driver = webdriver.Chrome()
driver.get("https://www.avito.ru")

sleep(1)

def change_region():
    change_region_btn = driver.find_element(By.CLASS_NAME, 'main-richTitleWrapper__content-WLi_V')
    change_region_btn.click()
    driver.implicitly_wait(2)
    clear_input_btn = driver.find_element(By.CLASS_NAME, 'suggest-icon-qI_yN')
    clear_input_btn.click()
    change_region_input = driver.find_element(By.CLASS_NAME, 'suggest-suggest-cVJJq')
    change_region_input.find_element(By.CLASS_NAME, 'suggest-input-rORJM').send_keys('Все регионы')
    sleep(2)
    change_region_input.find_element(By.TAG_NAME, 'li').click()
    submit_btn = driver.find_element(By.CLASS_NAME, 'popup-buttons-WICnh').find_element(By.CLASS_NAME, 'button-button-CmK9a')
    submit_btn.click()

change_region()

product_to_search = input('what do you want to search?\n> ')
keywords = input('write keywords for search spreading by space or leave this field blank to search without keywords\n> ')
negative_prompts = input('write negative prompts to search spreading by space or leave this field blank to search without keywords\n> ')
search_input = driver.find_element(By.CLASS_NAME, 'input-input-Zpzc1')
search_button = driver.find_element(By.CLASS_NAME, 'desktop-9uhrzn')
only_with_delivery = input('do you want search products only with enabled delivery?(y/n)\n> ')
search_input.send_keys(product_to_search)
search_button.click()

sleep(1)

def select_category(number):
    driver.get(f'{webdriver_categories[number].get_attribute("href")}')

def get_categories():
    global webdriver_categories
    global categories
    webdriver_categories = driver.find_elements(By.CLASS_NAME, 'rubricator-list-item-link-uPiO2')
    categories = [i.get_attribute('title') for i in webdriver_categories]
    for category_number, category in enumerate(categories):
        print(f'({category_number}) {category}')

get_categories()

while True:
    global find_in_category
    find_in_category = -1
    try:
        find_in_category = int(input('> ')) 
        if len(categories) > find_in_category >= 0:
            select_category(find_in_category)
            break
        else:
            print('no category for this number')
    except TypeError:
        print('please, write a number')
    except:
        print('sorry, service has an error')
        quit()

if only_with_delivery == 'y':
    current_url = driver.current_url
    driver.get(f'{current_url}&d=1')

enable_price_filter = input('enable price filter?(y/n)\n> ')

left_border, right_border = [-10000, 1e10]

if enable_price_filter == 'y':
    price_limit_range = input('enter price limit range(bottom line-top line)\n> ')
    left_border, right_border = price_limit_range.split('-')

current_url = driver.current_url
products_list = []
get_pagination = driver.find_element(By.CLASS_NAME, 'pagination-root-Ntd_O').find_elements(By.TAG_NAME, 'span')
pages_numbers = [i.text for i in get_pagination]
products_amount = driver.find_element(By.CLASS_NAME, 'page-title-count-wQ7pG').text.replace(' ', '')
print(f'found {products_amount} products, this may take some time...')
for i in range(2, int(pages_numbers[-2]) + 1):
    driver.get(current_url + f'&p={i}')
    sleep(1)
    products = driver.find_elements(By.CLASS_NAME, 'iva-item-content-rejJg')
    for product in products:
        product_title = product.find_element(By.CLASS_NAME, 'iva-item-titleStep-pdebR').text
        product_price = product.find_element(By.CLASS_NAME, 'price-text-_YGDY').text
        try:
            product_description = product.find_element(By.CLASS_NAME, 'iva-item-descriptionStep-C0ty1').find_element(By.CLASS_NAME, 'iva-item-text-Ge6dR').text
        except:
            product_description = "no description"
        product_link = product.find_element(By.CLASS_NAME, 'link-link-MbQDP ').get_attribute('href')
        if ((keywords == '' or any(keyword.lower() in product_title.lower() for keyword in keywords.split(' '))) and\
                (negative_prompts == '' or all(prompt.lower() not in product_title.lower() for prompt in negative_prompts.split()))) and\
                (not ('бесплат' in product_price.lower()) and (('цена не указана' == product_price.lower()) or\
                (int(left_border) <= int(product_price[:-2].replace(' ', '')) <= int(right_border)))):
            products_list.append([product_title, product_price, product_description, product_link])

write_data(products_list[::-1])

driver.quit()
