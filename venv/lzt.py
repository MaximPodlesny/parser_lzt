import time
import json
import csv
from random import randint
from os import path, walk
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
# from fake_useragent import UserAgent
from twocaptcha import TwoCaptcha

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
        reader['key_rucaptcha'] = input('Введите ключ rucaptcha: ')
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
        # driver.implicitly_wait(3)
        try:
            driver.find_element(By.CSS_SELECTOR, 'button.btn').click()
        except:
            pass
        driver.find_element(By.CSS_SELECTOR, '#navigation > div.pageContent > nav > div > div > a.button.primary.login-and-signup-btn.OverlayTrigger').click()
        time.sleep(10)
        
        # Считывание данных из файла 
        with open(secret, 'r', encoding='utf-8') as f:
            reader = json.load(f)
            login = reader['login']
            password = reader['password']
            secret_word = reader['secret']
            refresh_time = reader['refresh_time']
            key_rucaptcha = reader['key_rucaptcha']
            # key_rucaptcha = '555b06d2169b354083e34ec2be1bedad'

        # Решение капчи
        input_key = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'cf-turnstile-response')))
        solver = TwoCaptcha(key_rucaptcha)
        token = solver.turnstile(sitekey='0x4AAAAAAADMHhlDN2zO9nrC', url='https://lzt.market/?pget=1')
        
        driver.execute_script('arguments[0].setAttribute("value", arguments[1]);', input_key, token['code'])
        driver.execute_script('arguments[0].dispatchEvent(new Event("input", { bubbles: true }));', input_key)
        driver.execute_script('arguments[0].dispatchEvent(new Event("change", { bubbles: true }));', input_key)

        #  Ввод данных и аутотентификация
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
        
        input('Введите параметры поиска и нажмите Enter')
        
        action = ActionChains(driver)

        global counter
        counter = 0
        #  Зацикленный процесс покупки аккаунтов
        while True:
            try:
                driver.find_element(By.CSS_SELECTOR, 'button.btn').click()
            except:
                pass
            refr = driver.find_element(By.CSS_SELECTOR, '#title > div > span')
            # driver.refresh()
            # driver.execute_script('return arguments[0].scrollIntoView(true);', driver.find_element(By.CSS_SELECTOR, '#content > div > div > div.mainContainer > div > div.categoryLinks'))
            driver.execute_script('return arguments[0].scrollIntoView(true);', refr)
            driver.execute_script('window.scrollBy(0, -100)')
            time.sleep(0.5)
            WebDriverWait(driver, 10).until(EC.visibility_of(refr))
            action.move_to_element(refr).pause(0.5).click().perform()
            time.sleep(2)

            accounts = []
            try:
                accounts = driver.find_element(By.CSS_SELECTOR, 'form.InlineModForm.section').find_elements(By.TAG_NAME, 'li')
            except:
                pass

            if not accounts:
                time.sleep(refresh_time)
                # print(refresh_time)
                continue
            
            # Проходим по собранным аккаунтам
            for i, ac in enumerate(accounts):
                # if i > 5:
                #     driver.quit()
                #     break
                try:
                    driver.find_element(By.CSS_SELECTOR, 'button.btn').click()
                except:
                    pass
                driver.execute_script('return arguments[0].scrollIntoView(true);', ac)
                driver.execute_script('window.scrollBy(0, -100)')
                time.sleep(0.5)
                WebDriverWait(driver, 10).until(EC.visibility_of(ac))

                link = f"https://lzt.market/{driver.find_element(By.CSS_SELECTOR, 'a.marketIndexItem--Title.PopupItemLink').get_attribute('href')}"
                ac_id = ac.get_attribute('id').split('--')[1]
                
                
                    
                ac.find_element(By.CSS_SELECTOR, 'a.marketIndexItem--Title.PopupItemLink').click() # Переход по ссылке купить
                time.sleep(1)
                blanks = driver.window_handles
                driver.switch_to.window(blanks[1])
                time.sleep(0.3)
                try:
                    driver.find_element(By.CSS_SELECTOR, 'button.btn').click()
                except:
                    pass
                title = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div.mainContainer > div > div.market--titleBar.market--spec--titleBar > div.marketItemView--title > h1 > span').text.strip()
                
                # print(i)
                try:
                    # buy = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/div/div[2]/div[3]/div[1]/a[2]').click()
                    buy = driver.find_element(By.CSS_SELECTOR, 'a.button.primary.InlinePurchase.OverlayTrigger.DisableButton.marketViewItem--buyButton').click()
                except:
                    driver.close()
                    driver.switch_to.window(blanks[0])
                    time.sleep(1)
                    continue

                # Ввод секретного кода
                try:
                    WebDriverWait(driver, 2, 0.5).until(EC.element_to_be_clickable((By.NAME, 'secret_answer')))
                    secret_input = driver.find_element(By.NAME, 'secret_answer').send_keys(secret_word)

                    time.sleep(0.5)
                    driver.find_element(By.CSS_SELECTOR, 'div.SA--bottom > input.button.primary.mn-15-0-0.OverlayTrigger').click()
                except:
                    pass
                
                # Проверка на окно пополнени баланса
                # try:
                #     driver.find_element(By.CSS_SELECTOR, 'body > div.modal.fade.in > div > div > h2')
                #     time.sleep(5)
                #     print('Пополните баланс')
                #     driver.quit()
                # except:
                #     pass

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
                    # try:
                    #     driver.find_element(By.CSS_SELECTOR, '#ctrl_record_enabled').click()
                    # except:
                    #     pass
                    time.sleep(3)
                    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#BuyWithoutValidationButton')))
                    WebDriverWait(driver, 2, 0.3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#BuyWithoutValidationButton'))).click()
                    time.sleep(1)

                except:
                    # try:
                    #     driver.find_element(By.CSS_SELECTOR, '#ctrl_record_enabled').click()
                    # except:
                    #     pass

                    #  Покупка с чекбоксом
                    try:
                        time.sleep(3)
                        driver.find_element(By.CSS_SELECTOR, '#ctrl_record_enabled').click()
                        
                        # WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.modal.fade.in > div > div > div > form.MarketItemBuy--confirmBuyForm > div.NoRequireVideoRecording.noRequireVideoRecording > input')))
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modal.fade.in > div > div > div > form.MarketItemBuy--confirmBuyForm > div.NoRequireVideoRecording.noRequireVideoRecording > input'))).click()
                        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctrl_record_enabled_Disabler > input')))
                        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ctrl_record_enabled_Disabler > input'))).click()
                        time.sleep(1)
                    except:
                        

                        # Покупка без чекбокса с проверкой аккаунта
                        try:
                            time.sleep(3)
                            WebDriverWait(driver, 40, 1).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.NoRequireVideoRecording.noRequireVideoRecording > input.button.primary.mn-15-0-0')))
                            # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.NoRequireVideoRecording.noRequireVideoRecording > input')))
                            # action.send_keys(Keys.ENTER).perform()
                            WebDriverWait(driver, 40, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.NoRequireVideoRecording.noRequireVideoRecording > input.button.primary.mn-15-0-0'))).click()
                            time.sleep(2)

                        except:
                            print()
                            print(f"Покупка {[title, link, ac_id]} не состоялась")
                            print()
                            driver.close()
                            driver.switch_to.window(blanks[0])
                            time.sleep(1)
                            continue

                l = [title, link, ac_id]
                
                counter += 1
                print(f"{counter} - Куплен {[title, link, ac_id]}")

                # Запись данных по купленному аккаунту
                with open(path_list_accounts, 'a', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    # writer.writerow(['Title', 'Link', 'Id])
                    writer.writerows(l)
                driver.close()
                driver.switch_to.window(blanks[0])
                time.sleep(1)



if __name__=='__main__':
    with open(secret, 'r', encoding='utf-8') as file:
        reader = json.load(file)
        if 'login' not in reader:
            check_secret()
    try:
        main()
    except KeyboardInterrupt:
        print('Программа остановлена принудительно!')
        print(f'Куплено {counter} аккаунтов.')
    except Exception as e:
        print(f'Произошла ошибка {e}')
        input()
        
    
    
    
