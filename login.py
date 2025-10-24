import sys  
import os
from time import sleep, time  
from datetime import datetime  
from selenium import webdriver  
from selenium.webdriver import ActionChains  
from selenium.webdriver.common.by import By  
  
log_path = os.path.join(os.getcwd(), "log.txt")    
action_start_time = time()  

try:  
    acccounts = int(len(sys.argv[1:]) / 2)  
    print(f'Config {acccounts} accounts')  
    for i in range(acccounts):  
        email = sys.argv[1 + i]  
        passwd = sys.argv[1 + i + acccounts]  
        print('----------------------------')  

        # 1. Open chrome and load majsoul  
        options = webdriver.ChromeOptions()  
        options.add_argument("--headless=new")  
        driver = webdriver.Chrome(options=options)  
        driver.set_window_size(1000, 720)  
        driver.get("https://game.maj-soul.com/1/")  
        print(f'Account {i + 1} loading game...')  
        sleep(20)  

        # 2. Input email  
        screen = driver.find_element(By.ID, 'layaCanvas')  
        ActionChains(driver) \
            .move_to_element_with_offset(screen, 250, -100) \
            .click() \
            .perform()  
        driver.find_element(By.NAME, 'input').send_keys(email)  
        print('Input email successfully')  

        # 3. input password  
        ActionChains(driver) \
            .move_to_element_with_offset(screen, 250, -50) \
            .click() \
            .perform()  
        driver.find_element(By.NAME, 'input_password').send_keys(passwd)  
        print('Input password successfully')  

        # 4. Click login button  
        ActionChains(driver) \
            .move_to_element_with_offset(screen, 250, 50) \
            .click() \
            .perform()  
        print('Entering game...')  
        sleep(30)
        print('Login success')  
        driver.quit()  

    # no error : login success  
    is_success = True  

except Exception as e:  
    # error : login fail
    is_success = False  
    print(f'Error occurred: {e}')  

finally:  
    action_end_time = time()   
    execution_time = action_end_time - action_start_time   
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  

    # add login info to log.txt
    with open("log.txt", "a", encoding="utf-8") as log_file:  
        log_file.write(f"{current_time}-{'Success' if is_success else 'Failed'}-{execution_time:.2f}s\n")
