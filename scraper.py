# importing libraries
import os
import pandas as pd
import pytesseract
from PIL import Image

# waits until the page is loaded
def waitUntilLoaded():
    # fetching loading screen aria-label
    # until it is set to false, keep looping
    loading_screen_hidden = driver.find_element('xpath', '//*[@id="UpdateProgress1"]').get_attribute('aria-hidden')
    while loading_screen_hidden == 'false':
        loading_screen_hidden = driver.find_element('xpath', '//*[@id="UpdateProgress1"]').get_attribute('aria-hidden')

# creates and returns a dataframe
def getDataFrame():
    headers = ['Problem Statement', 'Answer']
    df = pd.DataFrame(columns = headers)
    return df

# clicks on specified web element
def click(id_type, location):
    driver.find_element(id_type, location).click()
    
# converts image to text 
def imageToText(location):
    # take screenshot of the image and save it to 'location'
    driver.find_element('xpath', '//*[@id="ContentPlaceHolder1_imgquestion"]').screenshot(location)
    
    # opening an image from the source path
    img = Image.open(location)
    
    # path where the tesseract module is installed
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR/tesseract.exe'
    
    # converts the image to result and saves it into result variable
    result = pytesseract.image_to_string(img)
    
    return result

# save the scraped data to csv file 
def save(df, file_name):
    # saving data to a csv file
    user = os.path.expanduser('~')
    file_location = user + "\Documents\\" + file_name + '.csv'
    df.to_csv(file_location)

# function to scrape the answers
def scrape(question_count, output_file_name):
    # data frame
    df = getDataFrame()
    
    print('\nYour page is being scraped. Please wait...')
    
    # looping through all the questions and scraping data
    for i in range(0, question_count):
        try:
            # clicking on the question
            click('xpath', '//*[@id="ContentPlaceHolder1_grdQuestion_labquestion_' + str(i) + '"]')
           
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
                # file location to save to 
                user = os.path.expanduser('~')
                file_location = user + "\Documents\\" + output_file_name + '_' + str(i+1) + '.png'
                
                # converting image to text
                problem_text = imageToText(file_location)
                
                # adding the new problem to the data frame
                row = [problem_text, solution]
                length = len(df)
                df.loc[length] = row
            else:
                # printing error message
                print('\nSomething went wrong while scraping the data.')
                print('Your data up to this point is saved to your file.')
                break
    
    # save data 
    save(df, output_file_name)

# ============================ DRIVER CODE =====================================
def run(web_driver):
    # creating a global variable driver
    global driver
    driver = web_driver
    
    # redirecting to mock test page
    print('\nWait while the mock test page is being loaded...\n')
    driver.get('https://uims.cuchd.in/uims/frmStuQuestionSolution.aspx')
    
    # taking input for the test number
    test_number = int(input('Enter the test number to scrape: '))
    
    # clicking on the required test number
    click('xpath', '//*[@id="ContentPlaceHolder1_grdtest_studentname_'+ str(test_number-1) +'"]')
    
    # taking other required inputs
    question_count  = int(input('Enter number of questions in that test: '))
    file_name = input('Enter output file name: ')
    
    # calling dataScraper function to scrape the data
    scrape(question_count, file_name)
    
    # printing good bye message
    print('\nYour scraped file is saved in Documents folder.')
    print('Good luck with your mock test and have a nice day! - Saurabh Raj\n')
