# importing libraries
from selenium import webdriver
import scraper
import submission as submit

# prints menu
def menu():
    print('================ Select an option: ================')
    print('1. Scrape Answer')
    print('2. Submit Answer')
    print('3. Exit')

# validates input 
def isValidInput():
    return selection >= 1 and selection <= 3
    
# login prompt
def loginPrompt():
    # Prompting user to login to UIMS
    print('\nLoading UIMS. Please login to UIMS to continue...')
    
    # opening UIMS for user login
    driver.get('https://uims.cuchd.in/uims/login.aspx')
    
    print('Press ENTER when logged in')
    enter = input('>> ')
    print()

# starting point of execution
if __name__ == '__main__':
    # loading chrome driver 
    driver = webdriver.Chrome(r'C:\Users\Saurabh Raj\Downloads\Programs\chromedriver.exe')
    
    # login prompt
    loginPrompt()
    
    # user menu
    while True:
        try:
            # print menu
            menu()
            
            # user choice
            selection = int(input('>> '))
            
            # validating input
            if(isValidInput() == False):
                print('\nInvalid selection. Try again.\n')
                continue
            
            # appropriate operation based on user choice
            if selection == 1:
                scraper.run(driver)
            elif selection == 2:
                submit.run(driver)
            else:
                print('\nThank you for using the app.\n- Saurabh Raj')
                break
            
            # line break
            print()
        except Exception as e:
            print(e.args, '\n')
