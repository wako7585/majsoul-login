import random
import sys  
import os
from time import sleep, time  
from datetime import datetime  
from selenium import webdriver  
from selenium.webdriver import ActionChains  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
  
log_path = os.path.join(os.getcwd(), "log.txt")    
action_start_time = time()  

def random_normal_distribution_int(a, b, n=3):
    """
    Generate a normal distribution int within the interval.
    Use the average value of several random numbers to simulate normal distribution.

    Args:
        a (int): The minimum of the interval.
        b (int): The maximum of the interval.
        n (int): The amount of numbers in simulation. Default to 3.

    Returns:
        int
    """
    a = round(a)
    b = round(b)
    if a < b:
        total = 0
        for _ in range(n):
            total += random.randint(a, b)
        return round(total / n)
    else:
        return b

def random_rectangle_point(area, n=3):
    """Choose a random point in an area.

    Args:
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        n (int): The amount of numbers in simulation. Default to 3.

    Returns:
        tuple(int): (x, y)
    """
    x = random_normal_distribution_int(area[0], area[2], n=n)
    y = random_normal_distribution_int(area[1], area[3], n=n)
    return x, y

# move_to_element_with_offset 基於中心點偏移 (495, 279)
def offset_point_from_center(area, origin=(495, 279)): 
    """ 計算相對於指定原點的偏移座標。 

    Args: 
    area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
    origin (tuple): origin point (0,0) defaults to (495, 279).

    Returns: 
    tuple(int): (dx, dy) 
    """ 
    x, y = random_rectangle_point(area, n=3)
    dx = x - origin[0] 
    dy = y - origin[1] 
    return dx, dy

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
        x, y = offset_point_from_center((640, 160, 830, 185))
        ActionChains(driver) \
            .move_to_element_with_offset(screen, x, y) \
            .click() \
            .perform()  
        wait = WebDriverWait(driver, 15)
        screen.screenshot("element1.png")
        email_input = wait.until(EC.presence_of_element_located((By.NAME, 'input')))
        email_input.send_keys(email)  
        print('Input email successfully')  

        # 3. input password  
        x, y = offset_point_from_center((640, 220, 830, 245))
        ActionChains(driver) \
            .move_to_element_with_offset(screen, x, y) \
            .click() \
            .perform()  
        password_input = wait.until(EC.presence_of_element_located((By.NAME, 'input_password')))
        password_input.send_keys(passwd)  
        print('Input password successfully')  

        # 4. Click login button 
        x, y = offset_point_from_center((640, 330, 830, 360))
        ActionChains(driver) \
            .move_to_element_with_offset(screen, x, y) \
            .click() \
            .perform()  
        print('Entering game...')  
        sleep(30)
        print('Login success')  

        # 5. Click mail box button
        x, y = offset_point_from_center((740,30,780,50))
        ActionChains(driver) \
            .move_to_element_with_offset(screen, x, y) \
            .click() \
            .perform()  
        print('Goto  mail box')
        sleep(10)

        # 6. Click receive or delete mail button
        x, y = offset_point_from_center((565,480,630,505))
        ActionChains(driver) \
            .move_to_element_with_offset(screen, x, y) \
            .click() \
            .perform()  
        print('Receive or delete mail')
        sleep(10)
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
