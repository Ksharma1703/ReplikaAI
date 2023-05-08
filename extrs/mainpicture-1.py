from selenium import webdriver

#from appium import webdriver

from webdriver_manager.microsoft import IEDriverManager

from webdriver_manager.chrome import ChromeDriverManager

from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.keys import Keys

#from selenium.webdriver.firefox.service import Service

#from webdriver_manager.firefox import GeckoDriverManager# from appium import webdriver

import time

import pandas as pd

from sentence_similarity import sentence_similarity

import os

# Automated Login, please don't abuse it!

def DoLogin(browser, username, password):

    # emailOrPhone - input

    # login-password - input

    # sc-AykKD FullscreenLayout__SubmitButton-sc-1a0qg1-2 bbVTcV - button

    browser.get('https://my.replika.ai/login')

    browser.find_element_by_id("emailOrPhone").send_keys(username)

    browser.find_element_by_tag_name("button").click()

    time.sleep(1)

    browser.find_element_by_id("login-password").send_keys(password)

    elements = browser.find_elements_by_tag_name('button')

    elements[len(elements) - 1].click()

    time.sleep(5)

    try:

        browser.find_element_by_class_name('DialogLayout__StyledCloseIcon-sc-103t4c8-2').click()

    except:

        pass





# Sends a Message by typing the text by "send_keys"

def SendMessage(browser, text):

    # send-message-textarea

    try:

        time.sleep(2)

        textarea = browser.find_element_by_id("send-message-textarea")

        textarea.send_keys(text)

        textarea.send_keys(Keys.ENTER)

    except:

        print("err with sending msg")

        pass





# Poor Method for getting all Messages out of Selenium Window...

def GetMessages(browser, messages=[]):

    try:

        time.sleep(2)

        cid = "ChatMessagesList__ChatMessagesListInner-sc-1ajwmer-1"

        divs = browser.find_element_by_class_name(cid)

        divs = divs.find_elements_by_tag_name("div")

        for x in divs:

            if x.get_attribute("class") == "MessageGroup__MessageGroupRoot-h4dfhv-0 xoUuE":

                spans = x.find_elements_by_tag_name("span")

                for y in spans:

                    message = y.get_attribute('innerHTML')

                    if "<span>" not in message and not (message == "thumb up" or message == "thumb down") and (message != "show more actions"):

                        messages.append(message)

        return messages

    except:

        pass





# Gets TheLastMessage out of Array messages

def GetLastMessage(browser, messages=[]):

    try:

        return messages[len(messages) - 3]

    except:

        pass


def main():

    # Defs (Browser "Windows")
    
    #options = Options()
    #options.binary_location = r"C:/Users/prern/AppData/Local/Mozilla Firefox/firefox.exe"
    #browser = webdriver.Firefox(options=options, executable_path=r"C:\Users\prern\Documents\CMPE 287\Deliverable 2\Code\geckodriver-v0.31.0-win64\geckodriver.exe")
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    #browser.get('http://google.com/')

    DoLogin(browser, "prerna.shekarbharadwaj@sjsu.edu", "Prerna@123")

    
    ss = sentence_similarity()

    pass_cnt = 0
    fail_cnt = 0
    
    r1 = []
    
   
    
    print("start processing images:")
    dataPic = pd.read_csv('pic-data.csv')
    try:
        for i in range(0, 3):
            print("Input to Replika - ")
            print(dataPic.iloc[i]['Requests'])
            print("Send image:")
            browser.find_element_by_id("upload-image-to-chat").send_keys(os.getcwd()+"\pic\\"+dataPic.iloc[i]['Requests'])
            r1 = GetMessages(browser)
            print("Output from Replika - ")
            # Getting of each messages array the last message (usually it's the newest)
            last_message = GetLastMessage(browser, r1)
            print(last_message)
            print("Similarity Test - ")
            sample_sentences_list = [s.rstrip(' ').lstrip(' ') for s in list(dataPic.iloc[i]['Responses'][1:-1].split(","))]
            present, most_similar_exp_output, similarity_score = ss._run(sample_sentences_list, last_message)
            if present:
                print('----------PASS-----------\nSimilarity Score = %f'%(similarity_score))
                pass_cnt += 1
            else:
                print('----------FAIL-----------\nSimilarity Score = %f'%(similarity_score))
                fail_cnt += 1
    except:
        pass

    print("================IMAGE SUMMARY=========================")
    print("Number of test cases that passed = {}".format(pass_cnt))
    print("Number of test cases that failed  = {}".format(fail_cnt))
    print("====================================================")

    # pass_cnt = 0
    # fail_cnt = 0
    # data = pd.read_csv('datap.csv')

    # print("start processing Text:")
    # try:
    #     for i in range(0, 8):
    #         print("Input to Replika - ")
    #         print(data.iloc[i]['Requests'])
    #         # Send message
    #         SendMessage(browser, data.iloc[i]['Requests'])
    #         # Getting current Messages (for checking if any new messages)

    #         r1 = GetMessages(browser)
    #         print("Output from Replika - ")
    #         last_message = GetLastMessage(browser, r1)
    #         print(last_message)

    #         print("Similarity Test - ")
    #         sample_sentences_list = [s.rstrip(' ').lstrip(' ') for s in list(data.iloc[i]['Responses'][1:-1].split(","))]
    #         present, most_similar_exp_output, similarity_score = ss._run(sample_sentences_list, last_message)
    #         if present:
    #             print('----------PASS-----------\nSimilarity Score = %f'%(similarity_score))
    #             pass_cnt += 1
    #         else:
    #             print('----------FAIL-----------\nSimilarity Score = %f'%(similarity_score))
    #             fail_cnt += 1
    # except:
    #     pass



    # print("================Text SUMMARY=========================")

    # print("Number of test cases that passed = {}".format(pass_cnt))

    # print("Number of test cases that failed  = {}".format(fail_cnt))

    # print("====================================================")

    browser.close()





if __name__ == '__main__':

    main()

