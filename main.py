from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, datetime
import uuid
from influxdb_client_3 import InfluxDBClient3, Point, flight_client_options
import certifi

webdriver_path="D:/Python/scrap/chromedriver.exe"
chrome_path="C:/Program Files (x86)/chrome-win64/chrome.exe"

#Подключение к бд для windows
#with open(certifi.where(), "r") as fh:
#    cert = fh.read()
#client = InfluxDBClient3(host=host, database=base, token=token, org=org, flight_client_options=flight_client_options(tls_root_certs=cert))

token='qLjKZzGWdMA6KjJen3qrtn-_PejLsU0eIUdbQm4AjKiErgj1kc9Xl5gbtrPW9O3bIh7TwW-LYc_-pZzdTPXhFg=='
org = "koeff"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

base='new'

client = InfluxDBClient3(host=host, database=base, token=token, org=org)


session_start_time=datetime.datetime.now()

def parsing(n):
    url="https://2cs.fail/ru/crash"

    def parse(driver, iter_counts):
        for i in range(iter_counts):
            try:
                # Функция поиска даинамически появляющегося элемента
                print(f"\nИщу элеммент") 
                wait=WebDriverWait(driver, timeout=150).until(EC.text_to_be_present_in_element((By.CLASS_NAME,"timer__status"),'КРАШ'))
                
                value=float(driver.find_element(By.CLASS_NAME,"timer__timer").text.replace('x',''))
                return_time=datetime.datetime.now()
                
                info= [div.text for div in driver.find_elements(By.CLASS_NAME,'game__stat')]

                point = Point("koeff").tag('session',session_start_time).field('koeff', value).field('bank', info[0]).field('people_count', info[1])
                client.write(record=point, time=return_time)
                
                print(f"№{i+1} Элемент найден \n{return_time}:{value,info}\n")
                print(f"")
                time.sleep(4)
                
            except Exception as e:
                print(f"Элемент не найден. Ошибка: {e}")      
        

    o = Options()
    o.headless = True
    #Пути к актуальной версии вебдрайвера и гугл хром
    o.binary_location = chrome_path
    service=webdriver.chrome.service.Service(webdriver_path) 

    driver = webdriver.Chrome(service=service,options=o)

    try:
        driver.get(url)
        time.sleep(0.2)
        print('Успешно подключено!')
        
        parse(driver,n)
        #test(driver)
        
    except Exception as e:
        print('Не удалось подключиться!', e)
    
    driver.quit()          
    
    
if __name__ == "__main__":
    parsing(200)
