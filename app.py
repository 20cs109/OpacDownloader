from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

code = input("Enter member code: ")
password = input("Enter password: ")
dept = input("Enter department(CSE, ECE, etc): ")
subject = input("Enter subject name: ")

with webdriver.Chrome() as driver:
    original_window = driver.current_window_handle

    driver.get("http://opac.cit.edu.in/member/login")

    inputElement = driver.find_element(By.NAME,"member_code")
    inputElement.send_keys(code)

    inputElement = driver.find_element(By.NAME,"password")
    inputElement.send_keys(password)

    inputElement.send_keys(Keys.ENTER)

    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, "btn-group"))
    qBankBtn = driver.find_element(By.XPATH, "//*[contains(text(), 'Question Bank')]")
    qBankBtn.click()
    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.ID, "course_name"))
    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.ID, "dept_name"))
    select_element = driver.find_element(By.ID, 'dept_name')
    select = Select(select_element)
    time.sleep(1)
    select.select_by_visible_text(dept)

    dept_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter any SubjectName"]')
    dept_field.send_keys(subject)

    searchBtn = driver.find_element(By.XPATH, "//button[contains(text(), 'Search ')]")
    searchBtn.click()

    WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.CLASS_NAME, "page-link"))

    pages = driver.find_elements(By.CLASS_NAME, "page-link")
    names = driver.find_elements(By.CSS_SELECTOR, 'small[class="pl-2 pt-4 pb-4 pr-2 ng-star-inserted"]')

    pdfList = []
    pageCount = 0
    for page in pages:
        if(page.text.isdigit()):
            pageCount+=1
    currPage = 1

    print(pageCount)
    while(currPage<=pageCount):
        page = driver.find_element(By.XPATH, "//a[contains(text(), '"+ str(currPage) + "')]")
        page.click()
        WebDriverWait(driver, timeout=3).until(lambda d: d.find_elements(By.CLASS_NAME, "page-link"))
        names = driver.find_elements(By.CSS_SELECTOR, 'small[class="pl-2 pt-4 pb-4 pr-2 ng-star-inserted"]')
        for name in names:
            ayo = name.find_element(By.TAG_NAME, 'title')
            pdfList.append(ayo.text)
        currPage += 1


    for x in pdfList:
        x = x.strip("Download")
        x = x.strip()

        driver.switch_to.new_window('tab')
        link = "http://opac.cit.edu.in/autolib-api/download/"+x+"/qb"
        driver.get(link)

        driver.close()
        driver.switch_to.window(original_window)
        print(x)
    time.sleep(5)
