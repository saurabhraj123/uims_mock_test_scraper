# Importing libraries
import os
import re
import urllib
import pandas as pd
import pytesseract
from PIL import Image
from selenium.webdriver.common.by import By

# wait while loading
def waitUntilLoaded():
    loading = (driver.find_element('xpath', '//*[@id="divQuestionOptionsMain_Loading"]').value_of_css_property('display') == 'block')
    while loading == True:
        loading = (driver.find_element('xpath', '//*[@id="divQuestionOptionsMain_Loading"]').value_of_css_property('display') == 'block')

# converts image to text 
def imageToText(location):
    # take screenshot of the image and save it to 'location'
    img = driver.find_element('xpath', '//*[@id="ctl02_imgQuestion"]')
    src = img.get_attribute('src')

    # open a new tab
    driver.execute_script("window.open('about:blank', 'secondtab');")

    # switch to the new tab
    driver.switch_to.window("secondtab")            
    
    # go to the image url
    driver.get(src)
    
    # take screenshot of the image and save it to 'location'
    driver.find_element('xpath', '/html/body/img').screenshot(location)
    
    # switch back to the parent tab
    parent = driver.window_handles[0]
    driver.switch_to.window(parent)
    
    # opening an image from the source path
    img = Image.open(location)
    
    # path where the tesseract module is installed
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR/tesseract.exe'
    
    # converts the image to result and saves it into result variable
    result = pytesseract.image_to_string(img)
    
    return result

# returns if the option is correct 
def isCorrect(option):
    return re.match(r'(?=.*\b(Right)\b)', str(option)) != None

# returns the right answer 
def getAnswer(options):
    for option in options:
        if(isCorrect(option) == True):
            right_answer = option[10:len(option)-7]
            return right_answer

# finds the correct option and submits 
def findAndSelect(right_answer, test_options):
    x = 1
    found = False
    
    for option_text in test_options:
        if option_text.strip() == right_answer.strip():
            driver.find_element('xpath', '(//*[@id="rbopt1"])[' + str(x) + ']').click()
            found = True
            return found
        x += 1
    
    return found

# searches the problem in csv and submit the correct answer 
def searchAndSubmit(df, problem_text):
    # looping through indices in the dataframe
    for i in df.index:
        found = False
        
        # problem statement without spaces and line breaks
        problem_without_spaces = df['Problem Statement'][i].replace(" ", "")
        problem_without_spaces = problem_without_spaces.replace('\n', "")
        
        problem_text = problem_text.replace(' ', '')
        problem_text = problem_text.replace('\n', '')
        
        # if problem is found in the csv file
        if problem_without_spaces == problem_text:
            # split the options from the csv in form of a list 
            options = df['Answer'][i].splitlines()
            
            # correct option 
            right_answer = getAnswer(options)
            
            # options on the test page in form of a list 
            test_options = driver.find_element('xpath', "(//*[@class = 'list-answer-selection'])").text.splitlines()
            
            # finds and submit the right answer 
            findAndSelect(right_answer, test_options)

# the question in image based 
def handleImageQuery(df, file_name, i):
    # file location to save to 
    user = os.path.expanduser('~')
    file_location = user + "\Documents\\" + file_name + '_' + str(i+1) + '.png'
    
    # image to text conversion
    problem = imageToText(file_location)
    
    # searches for the problem and submit it with the right solution
    searchAndSubmit(df, problem)

# the problem is text based 
def handleTextQuery(df, file_name, i):
    while True:
        try:
            # total text and undesired_text insidde the total_text
            problem_total = driver.find_element('xpath', '//*[@id="divQuestionOptions"]').text
            undesired_text = driver.find_element('xpath', '//*[@class="answer-wrap"]').text
            
            # problem statement = problem_total - undesired_text
            problem = problem_total.replace(undesired_text, "")
            
            # print('Problem Statement:', problem)

            # print('Just before Searching')
            # searches for the problem and submit it with the right solution
            searchAndSubmit(df, problem)
            # print('After before Searching')
            
            # if current <p> doesn't have any text, continue
            if problem == '':
                print('problem is empty')
                handleImageQuery(df, file_name, i)
        
            break
        except Exception as e:
            try:
                handleImageQuery(df, file_name, i)
                break
            except Exception as e:
                print(e.args)
                pass
            print(e.args)

# submit answers 
def submitAnswers(question_count, file_name):
    # read the csv file 
    user = os.path.expanduser('~')
    df = pd.read_csv(user + '\Documents\\' + file_name + '.csv')
    
    # looping through each question and answering
    for i in range(0, question_count):
        # click on the question number 
        driver.find_element('xpath', '(//*[@class = "QuestionSel"])[' + str(i+1) + ']').click()
        
        # waits until the question is loaded
        waitUntilLoaded()

        try:
            #handles text based query
            handleTextQuery(df, file_name, i)
        except Exception as e:
            # handles if problem is image based
            print(e)
            print(e.args)
            handleImageQuery(df, file_name, i)

#  ============================ DRIVER CODE ================================
def run(web_driver):
    # creating a global variable driver
    global driver 
    driver = web_driver
    
    # redirecting to mock test page
    print('\nWait while the mock test page is being loaded...')
    driver.get('https://uims.cuchd.in/uims/frmMockTest.aspx')

    # taking other required inputs
    file_name = input('\nEnter file name to read answers: ')
    question_count  = int(input('\nEnter number of questions in the test: '))
    
    print('\nPress ENTER after starting the test')
    enter = input('>> ')
    
    # answering questions
    print('\nPlease wait while your test is being answered...')
    submitAnswers(question_count, file_name)
    
    # printing good bye message
    print('\nYour test submission has been completed. Have a nice day! - Saurabh Raj')

