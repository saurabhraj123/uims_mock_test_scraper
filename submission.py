# Importing libraries
import os
import re
import pandas as pd
import pytesseract
from PIL import Image

# wait while loading
def waitUntilLoaded():
    loading = (driver.find_element('xpath', '//*[@id="divQuestionOptionsMain_Loading"]').value_of_css_property('display') == 'block')
    while loading == True:
        loading = (driver.find_element('xpath', '//*[@id="divQuestionOptionsMain_Loading"]').value_of_css_property('display') == 'block')

# converts image to text 
def imageToText(location):
    # take screenshot of the image and save it to 'location'
    driver.find_element('xpath', '//*[@id="ctl02_imgQuestion"]').screenshot(location)
    
    # opening an image from the source path
    img = Image.open(location)
    
    # path where the tesseract module is installed
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR/tesseract.exe'
    
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
        
        # if problem is found in the csv file
        if df['Problem Statement'][i].strip() == problem_text.strip():
            # split the options from the csv in form of a list 
            options = df['Answer'][i].splitlines()
            
            # correct option 
            right_answer = getAnswer(options)
            
            # options on the test page in form of a list 
            test_options = driver.find_elements_by_class_name('list-answer-selection')[0].text.splitlines()
            
            # finds and submit the right answer 
            findAndSelect(right_answer, test_options)

# the question in image based 
def handleImageQuery(df, file_name, i):
    # print('Before file location')
    # file location to save to 
    user = os.path.expanduser('~')
    file_location = user + "\Documents\\" + file_name + '_' + str(i+1) + '.png'
    # print('After file location')
    
    # print('Before image text')
    # image to text conversion
    problem = imageToText(file_location)
    # print('After image text')
    # print('[Image Problem]:', problem)
    
    # searches for the problem and submit it with the right solution
    searchAndSubmit(df, problem)

# the problem is text based 
def handleTextQuery(df, file_name, i):
    count = 1
    while True:
        try:
            # print('Inside loop. Count:', count)
            problem = driver.find_element('xpath', '//*[@id="divQuestionOptions"]/p[' + str(count) + ']').text
        
            # print('Problem Statement:', problem)
            
            # if current <p> doesn't have any text, continue
            if problem == '':
                # print('problem is empty')
                count += 1
                continue
        
            # print('Just before Searching')
            # searches for the problem and submit it with the right solution
            searchAndSubmit(df, problem)
            # print('After before Searching')
            break
        except Exception as e:
            count += 1
            if count % 5 == 0:
                try:
                    handleImageQuery(df, file_name, i)
                    break
                except Exception as e:
                    print(e.args)
            print(e.args)

# submit answers 
def submitAnswers(question_count, file_name):
    # read the csv file 
    user = os.path.expanduser('~')
    df = pd.read_csv(user + '\Documents\\' + file_name + '.csv')
    
    # looping through each question and answering
    for i in range(0, question_count):
        # click on the question number 
        driver.find_elements_by_class_name('QuestionSel')[i].click()
        
        # waits until the question is loaded
        waitUntilLoaded()
        
        try:
            # checking if the problem is image based
            try:
                # handles if problem is image based
                handleImageQuery(df, file_name, i)
            # if the problem is text based
            except Exception as e:
                print('Image error:', e.args)
                
                #handles text based query
                handleTextQuery(df, file_name, i)
        except Exception as e:
            print(e.args)

#  ============================ DRIVER CODE ================================
def run(web_driver):
    # creating a global variable driver
    global driver 
    driver = web_driver
    
    # redirecting to mock test page
    print('\nWait while the mock test page is being loaded...')
    driver.get('https://uims.cuchd.in/uims/frmMockTest.aspx')

    
    # taking other required inputs
    file_name = input('Enter file name: ')
    print('Press ENTER after starting the test')
    enter = input('>> ')
    question_count  = int(input('\nEnter number of questions in the test: '))
    
    # answering questions
    print('\nPlease wait while your test is being answered...')
    submitAnswers(question_count, file_name)
    
    # printing good bye message
    print('\nYour test submission has been completed. Have a nice day! - Saurabh Raj')

