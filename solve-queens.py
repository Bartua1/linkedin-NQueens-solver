from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC
import time
import matplotlib.pyplot as plt
import numpy as np
from password_reinas import password
from bs4 import BeautifulSoup
from board_solver import backtracking_solver 

PATH = "./chromedriver.exe"
options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

first_time = False # Set to True if it is the first time you play the game

driver = webdriver.Chrome(PATH, options=options)

def queensToNumpy(queens):
    # queens is a bs4 element with the queens grid
    queens_cells = queens.find_all("div", class_="queens-cell")

    # The default is 81 cells
    n_cells = len(queens_cells)

    # Find the shape of the board
    i = 1
    valid = False
    while not valid:
        if n_cells == i*i:
            shape = (i, i)
            valid = True
        i += 1
    board = np.zeros(shape)
    
    row = 0
    col = 0
    board = []
    for cell in queens_cells:
        color = cell["class"][1].split("-")[2]
        board.append(int(color))
    return np.asarray(board).reshape(shape)

if __name__ == "__main__":
    driver.get("https://www.linkedin.com/games/queens/")
    driver.implicitly_wait(10)

    passwd = password().get_password()
    username = password().get_username()
    input_username = driver.find_element(By.ID, "username")
    input_username.send_keys(username)

    input_password = driver.find_element(By.ID, "password")
    input_password.send_keys(passwd)

    # Sign in btn is a btn with data-litms-control-urn = login-submit
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[data-litms-control-urn='login-submit']")
    sign_in_btn.click()
    

    try:
        start_btn = driver.find_element(By.CSS_SELECTOR, "button.launch-footer__btn--start")
        start_btn.click()
    except:
        pass

    if (first_time):
        try:
            # the skip is artdeco-modal__dismiss
            skip_btn = driver.find_element(By.CSS_SELECTOR, "button.artdeco-modal__dismiss")
            skip_btn.click()
        except:
            pass

    time.sleep(1)
    queens_grid = driver.find_element(By.ID, "queens-grid")
    soup = BeautifulSoup(queens_grid.get_attribute("outerHTML"), "html.parser")

    driver.quit()

    board = queensToNumpy(soup)

    solver = backtracking_solver(board, board.shape)
    sol = solver.solve()

    print("Board:\n", board)
    print("Solucion:\n", sol)

    # Obtaining the queens positions and transforming them to the format requested by the game
    indexes = np.argwhere(sol == 1)
    print("Indices de reinas:\n", indexes)
    queens = [ queen[0] * board.shape[0] + queen[1] for queen in indexes]
    print("Queens Indexes:\n", queens)

    driver = webdriver.Chrome(PATH, options=options)
    driver.get("https://www.linkedin.com/games/queens/")
    driver.implicitly_wait(10)

    input_username = driver.find_element(By.ID, "username")
    input_username.send_keys(username)
    
    input_password = driver.find_element(By.ID, "password")
    input_password.send_keys(passwd)

    # Sign in btn is a btn with data-litms-control-urn = login-submit
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[data-litms-control-urn='login-submit']")
    sign_in_btn.click()

    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.launch-footer__btn--start")))
    start_btn = driver.find_element(By.CSS_SELECTOR, "button.launch-footer__btn--start")
    start_btn.click()
    time.sleep(0.5)

    if (first_time):
        try:
            # the skip is artdeco-modal__dismiss
            skip_btn = driver.find_element(By.CSS_SELECTOR, "button.artdeco-modal__dismiss")
            skip_btn.click()
            time.sleep(0.8)
        except:
            pass

    # Now we play the game
    for queen in queens:
        queen_pos = driver.find_element(By.CSS_SELECTOR, f"div[data-cell-idx='{queen}']")
        queen_pos.click()
        time.sleep(0.1)
        queen_pos.click()
        time.sleep(0.1)
        

    time.sleep(10)
    driver.quit()

    print(board)