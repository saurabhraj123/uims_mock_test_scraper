################################################################################
# @Creator - Saurabh Raj
################################################################################

# Importing libraries
import os
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# waits until the page is loaded
def waitUntilLoaded():
    # fetching loading screen aria-label
    # until it is set to false, keep looping
    loading_screen_hidden = driver.find_element('xpath', '//*[@id="UpdateProgress1"]').get_attribute('aria-hidden')
    while loading_screen_hidden == 'false':
        loading_screen_hidden = driver.find_element('xpath', '//*[@id="UpdateProgress1"]').get_attribute('aria-hidden')

# function to scrape the data
def dataScraper(test_number, question_count, file_name):
    # creating a data frame to store data in form of a table
    headers = ['Problem Statement', 'Answer']
    df = pd.DataFrame(columns = headers)

    print('\nYour page is being scraped. Please wait.')
    
    # looping through all the questions and scraping data
    for i in range(0, question_count):
        try:
            # clicking on the question
            question = driver.find_element('xpath', '//*[@id="ContentPlaceHolder1_grdQuestion_labquestion_' + str(i) + '"]')
            question.click()
            
            # wait while the page is loaded completely
            waitUntilLoaded()
            
            # fetch the problem and the solution statements
            solution = driver.find_element('xpath', '//*[@id="ContentPlaceHolder1_grd_option"]/tbody').text
            problem  = driver.find_element('xpath', '//*[@id="ContentPlaceHolder1_div_question"]').text
            
            # adding the question to the data frame
            row = [problem, solution]
            length = len(df)
            df.loc[length] = row
        except Exception as e:
            # if the question is a screenshot and not text,
            # it throws exception. In that case, just save the answer to the file
            if e.__class__.__name__ == 'NoSuchElementException':
                row = ['', solution]
                length = len(df)
                df.loc[length] = row
            else:
                # printing error message
                print('\nSomething went wrong while scraping the data.')
                print('Your data up to this point is saved to your file.')
                break

    # saving data to a csv file
    user = os.path.expanduser('~')
    file_location = user + "\Documents\\" + file_name + '.csv'
    df.to_csv(file_location)


# =========================== DRIVER CODE ================================== # 
# loading chrome driver 
driver = webdriver.Chrome(r'C:\Users\Saurabh Raj\Desktop\web scraping\chromedriver.exe')

# Prompting user to login to UIMS
print('Loading UIMS. Please login to UIMS to continue...')

# opening UIMS for user login
driver.get('https://uims.cuchd.in/uims/login.aspx')

print('Press ENTER when logged in')
enter = input('>> ')

# taking user input for the test number to scrape
while True:
    try:
        # redirecting to mock test page
        print('\n---------------------------------------------------')
        print('Wait while the mock test page is being loaded...\n')
        driver.get('https://uims.cuchd.in/uims/frmStuQuestionSolution.aspx')

        # taking input for the test number
        test_number = int(input('Enter the test number to scrape: '))

        # clicking on the required test number
        show_details = driver.find_element('xpath', '//*[@id="ContentPlaceHolder1_grdtest_studentname_'+ str(test_number-1) +'"]')
        show_details.click()

        # taking other required inputs
        question_count  = int(input('Enter number of questions in that test: '))
        file_name = input('Enter file name: ')

        # wait while the page is loaded completely
        waitUntilLoaded()
        
        # calling dataScraper function to scrape the data
        dataScraper(test_number, question_count, file_name)
        
        # printing good bye message
        print('\nYour scraped file is saved in Documents folder.')
        print('Good luck with your mock test and have a nice day! - Saurabh Raj')
        break
    except Exception as ex:
        print(ex.args)


