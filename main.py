from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, datetime
import uuid
from influxdb_client_3 import InfluxDBClient3, Point, flight_client_options
import certifi
import sys

webdriver_path="/usr/local/bin/chromedriver"

session_start_time=datetime.datetime.now()

def parsing(n):
    url="https://3cs.fail/ru/crash"

    def parse(driver, iter_counts):
        for i in range(iter_counts):
            try:
                # Функция поиска даинамически появляющегося элемента
                print(f"\nИщу элеммент") 
                wait=WebDriverWait(driver, timeout=400).until(EC.text_to_be_present_in_element((By.CLASS_NAME,"timer__status"),'КРАШ'))
                
                value=float(driver.find_element(By.CLASS_NAME,"timer__timer").text.replace('x',''))
                return_time=datetime.datetime.now()
                
                info= [div.text for div in driver.find_elements(By.CLASS_NAME,'game__stat')]

                point = Point("koeff").tag('session',session_start_time).field('koeff', value).field('bank', info[0]).field('people_count', info[1])
                client.write(record=point, time=return_time)
                
                print(f"№{i+1} Элемент найден \n{return_time}:{value,info}\n")
                time.sleep(4)
                
            except Exception as e:
                print(f"Элемент не найден. Ошибка: {e}")      
        

    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    #Пути к актуальной версии вебдрайвера и гугл хром
    #o.binary_location = chrome_path
    service=webdriver.chrome.service.Service(webdriver_path) 

    driver = webdriver.Chrome(service=service,options=options)
    
    try: 
        token='qLjKZzGWdMA6KjJen3qrtn-_PejLsU0eIUdbQm4AjKiErgj1kc9Xl5gbtrPW9O3bIh7TwW-LYc_-pZzdTPXhFg=='
        org = "koeff"
        host = "https://us-east-1-1.aws.cloud2.influxdata.com"
        
        base='main'
        
        client = InfluxDBClient3(host=host, database=base, token=token, org=org)
        print("Успешно подключено к бд!")
    except:
        print("Не подключено к бд!")
        
    try:
        driver.get(url)
        time.sleep(0.2)
        print('Успешно подключено!')
        
        parse(driver,n)
        #test(driver)
        
    except Exception as e:
        print('Не удалось подключиться!', e)
    
    #driver.quit()          
    
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = sys.argv[1]
        try:
            n = int(n)
            parsing(n)
        except ValueError:
            print("Аргумент должен быть целым числом.")
    else:
        print("Передайте аргумент в командной строке.")
