import time
import json
import csv
from random import randint
from os import path, walk
# from tkinter import W
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
# from fake_useragent import UserAgent
# from seleniumbase import SB
from twocaptcha import TwoCaptcha

# import pywhatkit.whats as pk

path_list_accounts = path.abspath(path.join(path.dirname(__file__), 'list_accounts_lzt.csv'))
secret = path.abspath(path.join(path.dirname(__file__), 'secret_lzt.json'))
path_driver = path.abspath(path.join(path.dirname(__file__), 'chromedriver.exe'))

# ua = UserAgent()
def check_secret():
    with open(secret, 'w', encoding='utf-8') as file:
        reader['login'] = input('Введите login: ')
        reader['password'] = input('Введите пароль: ')
        reader['secret'] = input('Введите секретное слово: ')
        reader['refresh_time'] = int(input('Введите максимальное время ожидание в секундах: '))
        json.dump(reader, file, ensure_ascii=False, indent=3)


def main():
    serv = Service(executable_path=path_driver)
    dict_arguments = {'source': '''
                adoQpoasnfa76pfcZLmcfl_Array;
                adoQpoasnfa76pfcZLmcfl_Promise;
                adoQpoasnfa76pfcZLmcfl_Symbol;
                '''
            }
    
    option = webdriver.ChromeOptions()
    option.add_argument('start-maximized')
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    

    with webdriver.Chrome(service=serv, options=option) as driver:
        
        url = "https://lzt.market/" 
        driver.get(url)
        driver.implicitly_wait(10)
        try:
            driver.find_element(By.CSS_SELECTOR, 'button.btn').click()
        except:
            pass
        driver.find_element(By.CSS_SELECTOR, '#navigation > div.pageContent > nav > div > div > a.button.primary.login-and-signup-btn.OverlayTrigger').click()
        # blancks = driver.window_handles
        time.sleep(10)
       
        # print(WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="Виджет, содержащий вызов безопасности Cloudflare"]'))))

        input_key = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'cf-turnstile-response')))
        
        solver = TwoCaptcha('555b06d2169b354083e34ec2be1bedad')
        token = solver.turnstile(sitekey='0x4AAAAAAADMHhlDN2zO9nrC', url='https://lzt.market/?pget=1')
        
        driver.execute_script('arguments[0].setAttribute("value", arguments[1]);', input_key, token['code'])
        driver.execute_script('arguments[0].dispatchEvent(new Event("input", { bubbles: true }));', input_key)
        driver.execute_script('arguments[0].dispatchEvent(new Event("change", { bubbles: true }));', input_key)
        with open(secret, 'r', encoding='utf-8') as f:
            reader = json.load(f)
            login = reader['login']
            password = reader['password']
            secret_word = reader['secret']
            refresh_time = reader['refresh_time']
        driver.find_element(By.NAME, 'login').clear
        driver.find_element(By.NAME, 'login').send_keys(login[:len(login)//2])
        time.sleep(0.2)
        driver.find_element(By.NAME, 'login').send_keys(login[len(login)//2:])
        time.sleep(1)
        driver.find_element(By.NAME, 'login').clear
        driver.find_element(By.NAME, 'password').send_keys(password)
        time.sleep(0.5)
        button_log = driver.find_element(By.CSS_SELECTOR, '#pageLogin > div.loginForm--bottomBar > input')
        driver.execute_script('return arguments[0].scrollIntoView(true);', button_log)
        button_log.click()
        
        time.sleep(3)
        input('Введите параметры поиска и нажмите Enter')
        # driver.find_element(By.NAME, 'pmax').send_keys(10)
        # driver.find_element(By.NAME, 'pmax').send_keys(Keys.ENTER)
        # time.sleep(0.4)
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#SubmitSearchButton'))).click()
        # time.sleep(2)
        # driver.execute_script('window.scrollBy(0, 100)')
        action = ActionChains(driver)
        while True:
            refr = driver.find_element(By.CSS_SELECTOR, '#title > div > span')
            driver.execute_script('return arguments[0].scrollIntoView(true);', driver.find_element(By.CSS_SELECTOR, '#content > div > div > div.mainContainer > div > div.categoryLinks'))
            action.move_to_element(refr).pause(0.5).click().perform()
            time.sleep(3)

            try:
                accounts = driver.find_element(By.CSS_SELECTOR, 'form.InlineModForm.section').find_elements(By.TAG_NAME, 'li')[:10]
            except:
                time.sleep(randint(2, refresh_time))
                continue
            with open(path_list_accounts, 'r', encoding='utf-8') as file:
                reader = list(csv.reader(file))[1:]
                
                if reader[0]:
                    reader = [i[2] for i in reader]
                
                
                for i, ac in enumerate(accounts):
                    if i > 5:
                        driver.quit()
                        break
                    WebDriverWait(driver, 10).until(EC.visibility_of(ac))

                    link = f"https://lzt.market/{driver.find_element(By.CSS_SELECTOR, 'a.marketIndexItem--Title.PopupItemLink').get_attribute('href')}"
                    ac_id = ac.get_attribute('id').split('--')[1]
                    
                    if ac_id not in reader:
                        
                        ac.find_element(By.CSS_SELECTOR, 'a.marketIndexItem--Title.PopupItemLink').click() # Переход по ссылке купить
                        time.sleep(5)
                        blanks = driver.window_handles
                        driver.switch_to.window(blanks[1])
                        time.sleep(1)
                        title = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div.mainContainer > div > div.market--titleBar.market--spec--titleBar > div.marketItemView--title > h1 > span').text.strip()
                        
                        
                        try:
                            # buy = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/div/div[2]/div[3]/div[1]/a[2]').click()
                            buy = driver.find_element(By.CSS_SELECTOR, 'a.button.primary.InlinePurchase.OverlayTrigger.DisableButton.marketViewItem--buyButton').click()
                        except:
                            driver.close()
                            driver.switch_to.window(blanks[0])
                            time.sleep(1)
                            continue

                        # Проверка на окно пополнени баланса
                        try:
                            driver.find_element(By.XPATH, '//*[@id="XenForo"]/body/div[9]/div/div/h2')
                            print('Пополните баланс')
                            break
                        except:
                            pass

                        # Ввод секретного кода
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'secret_answer')))
                        secret_input = driver.find_element(By.NAME, 'secret_answer').send_keys(secret_word)

                        time.sleep(0.5)
                        driver.find_element(By.CSS_SELECTOR, 'div.SA--bottom > input.button.primary.mn-15-0-0.OverlayTrigger').click()

                        # Проверка валидности кода
                        try:
                            driver.find_element(By.LINK_TEXT, 'Вы ввели неправильный ответ на секретный вопрос')
                            print('Вы ввели неправильный ответ на секретный вопрос')
                            check_secret()
                        except:
                            pass

                        # Покупка
                        try:
                            # Проверка наличия чекбокса
                            try:
                                driver.find_element(By.CSS_SELECTOR, '#ctrl_record_enabled').click()
                            except:
                                pass
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#BuyWithoutValidationButton')))
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#BuyWithoutValidationButton'))).click()
                            print('Без проверки')

                        except:
                            pass
                        try:
                            try:
                                driver.find_element(By.CSS_SELECTOR, '#ctrl_record_enabled').click()
                            except:
                                pass
                            # WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.modal.fade.in > div > div > div > form.MarketItemBuy--confirmBuyForm > div.NoRequireVideoRecording.noRequireVideoRecording > input')))
                            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modal.fade.in > div > div > div > form.MarketItemBuy--confirmBuyForm > div.NoRequireVideoRecording.noRequireVideoRecording > input'))).click()
                            WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctrl_record_enabled_Disabler > input')))
                            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ctrl_record_enabled_Disabler > input'))).click()
                            print('С записью')
                        except:
                            pass
                        try:
                            action.send_keys(Keys.ENTER).perform()
                            # WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.NoRequireVideoRecording.noRequireVideoRecording > input')))
                            # WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.NoRequireVideoRecording.noRequireVideoRecording > input'))).click()
                        except:
                            print(f"Покупка {[title, link, ac_id]} не состоялась")
                            driver.close()
                            driver.switch_to.window(blanks[0])
                            time.sleep(1)
                            continue

                        l = [title, link, ac_id]
                        print(f"Куплен {[title, link, ac_id]}")
                        with open(path_list_accounts, 'a', encoding='utf-8', newline='') as file:
                            writer = csv.writer(file)
                            # writer.writerow(['Title', 'Link', 'Id])
                            writer.writerows(l)
                        time.sleep(2)
                        driver.close()
                        driver.switch_to.window(blanks[0])
                        time.sleep(2)



        # if new_list_jobs:              
        #     count = 0
        #     for data in new_list_jobs:
        #         message = '\n'.join(data)
        #         try:
        #                 pk.sendwhatmsg_instantly('+79898198015', message=message,\
        #                                                     wait_time=60, tab_close=True)
        #         except:
        #             pass
        #         count += 1
        #     try:
        #         pk.sendwhatmsg_instantly('+79898198015', message=f'Новых заказов: {count}',\
        #                                                 wait_time=60, tab_close=True)
        #     except:
        #         pass

        
    
    

if __name__=='__main__':
    with open(secret, 'r', encoding='utf-8') as file:
        reader = json.load(file)
        if 'login' not in reader:
            check_secret()
    try:
        main()
    except:
        pass
