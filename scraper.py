import time
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_driver = "/Users/olegpash/Developer/work/alexander-auto/chromedriver"


def main(args, res, indx):
    res[indx] = {'res': False, 'time': ''}
    start_time = time.time()
    login, password, article, mode = map(str, args)
    res[indx]['lot'] = article
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path=chrome_driver, options=options)
    driver.get('https://auction.cebank.ru/')
    time.sleep(5)
    driver.find_element(By.XPATH, '//input[@name="P101_PHONE"]').send_keys(login)
    driver.find_element(By.XPATH, '//input[@name="P101_PASSWORD"]').send_keys(password)
    time.sleep(3)
    driver.find_elements(By.XPATH, '//button')[-1].click()
    soup = bs4.BeautifulSoup(driver.page_source, features='lxml')
    elements = soup.find_all('div', {'class': 'row'})[3].find_all('div', {'class': 'col col-4'})
    for i, element in enumerate(elements):
        element_article = element.find('p', {'class': 'p2'})
        element_price = element.find('p', {'class': 'p12'})
        if '</strong>  - </p>' in str(element_price):
            element_price = element.find('p', {'class': 'p11'}).text.split('Минимальная цена')[1].split('руб.')[0].strip()
        else:
            element_price = element_price.text.split('Максимальная ставка')[1].split('руб.')[0].strip()
        new_element_price = ''
        for pointer in range(len(element_price)):
            if element_price[pointer] != ' ':
                new_element_price += element_price[pointer]
        element_price = int(new_element_price) + 5000

        if element_article.text == 'Аукцион № ' + article or mode == 'test-time':
            btn = driver.find_elements(By.XPATH, "//div[@class='row']")[3].find_elements(By.XPATH, "//a[@class='btn']")[i]
            btn.click()
            time.sleep(1)
            iframe = driver.find_element(By.XPATH, "//iframe[@title='Ставка']")
            driver.switch_to.frame(iframe)
            driver.find_element(By.XPATH, '//input[@id="P2_PRICE"]').send_keys(str(element_price))
            if mode == 'test-time':
                break

            driver.find_element(By.XPATH, '//button[@class="t-Button t-Button--hot "]').click()
            time.sleep(1)
            if 'error has occurred' in driver.page_source:
                break
            if 'Ваша ставка успешно принята' in driver.page_source:
                res[indx]['res'] = True
            break
    driver.close()
    res[indx]['time'] = time.time() - start_time