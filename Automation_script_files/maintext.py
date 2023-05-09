from selenium import webdriver

# from appium import webdriver

from selenium.webdriver.common.by import By


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



# Automated Login, please don't abuse it!

def DoLogin(browser, username, password):

    # emailOrPhone - input

    # login-password - input

    # sc-AykKD FullscreenLayout__SubmitButton-sc-1a0qg1-2 bbVTcV - button

    browser.get('https://my.replika.com/login')
    # browser.find_element_by_id("login-email").send_keys(username)
    browser.find_element(By.ID, "login-email").click()
    browser.find_element(By.ID, "login-email").send_keys(username)

    browser.find_element(By.ID, "login-password").click()
    browser.find_element(By.ID, "login-password").send_keys(password)

    browser.find_element(By.CSS_SELECTOR, ".iubenda-cs-accept-btn").click()
    browser.find_element(By.CSS_SELECTOR, ".AuthLayout__SubmitButton-sc-110rp2i-17").click()
    browser.execute_script("window.scrollTo(0,0)")
    # browser.find_element(By.CSS_SELECTOR, ".DialogLayout__StyledCloseIcon-sc-103t4c8-4").click()
    # browser.execute_script("window.scrollTo(0,0)")
    # browser.find_element(By.CSS_SELECTOR, ".DialogLayout__CancelButton-sc-103t4c8-13").click()



    # time.sleep(5)


    # elements = browser.find_elements_by_tag_name('button')

    # elements[len(elements) - 1].click()

    # time.sleep(5)

    # try:

    #     browser.find_element_by_class_name('Buttons__AccentButton-sc-8h2vjq-6 AuthLayout__SubmitButton-sc-110rp2i-17 cwHBsG ddIIRZ').click()

    # except:

    #     pass





# Sends a Message by typing the text by "send_keys"

def SendMessage(browser, text):

    # send-message-textarea

    try:

        time.sleep(2)
        browser.find_element(By.ID, "send-message-textarea").click()
        browser.find_element(By.ID, "send-message-textarea").send_keys(text)

        # browser.find_element(By.ID, "send-message-textarea").send_keys(text)
        browser.find_element(By.ID, "send-message-textarea").send_keys(Keys.ENTER)
    except:

        print("err with sending msg")

        pass


def GetMessages(browser, messages=[]):
    try:
        # MessageGroup__MessageGroupRoot-sc-h4dfhv-0
        time.sleep(8)
        cid = "ChatMessagesList__ChatMessagesListInner-sc-1ajwmer-1"

        # divs = browser.find_element_by_class_name(cid)
        divs = browser.find_element(By.CLASS_NAME,cid)
        # divs = divs.find_elements_by_tag_name("div")
        divs = divs.find_elements(By.TAG_NAME,"div")

        # class_msg = browser.find_elements_by_class_name("bWpZMs")
        class_msg = browser.find_elements(By.CLASS_NAME,"bWpZMs")

        # print("class_msg: ", class_msg)
        for x in class_msg: 
            # spans = x.find_elements_by_tag_name("span")
            spans = x.find_elements(By.TAG_NAME,"span")

            for y in spans:
                message = y.get_attribute('innerHTML')
                # print(message)
                if "<span>" not in message and not (message == "thumb up" or message == "thumb down") and (message != "show more actions"):
                    messages.append(message)
        return messages
    except:
        print("ERROR! GetMessages Failed!")


# Poor Method for getting all Messages out of Selenium Window...

# def GetMessages(browser, messages=[]):

#     try:

#         time.sleep(5)
#         cid = "ChatMessagesList__ChatMessagesListInner-sc-1ajwmer-1"
#         # divs = browser.find_element_by_class_name(cid)
#         divs = browser.find_element(By.CLASS_NAME,cid)
#         print("-----------------> 1")
#         print(divs)
#         divs = divs.find_elements_by_tag_name("div")
#         # divs = browser.find_element(By.TAG_NAME,"div")
#         # print("-----------------> 2")
#         for x in divs:
# # MessageHover__MessageHoverRoot-sc-6lkiln-0 dNlIrv BubbleText__BubbleTextRoot-sc-1bng39n-0 hiwsCy MessageGroup__StyledMessage-sc-h4dfhv-2 bUGZCU
# # MessageHover__MessageHoverRoot-sc-6lkiln-0 dNlIrv BubbleText__BubbleTextRoot-sc-1bng39n-0 hiwsCy MessageGroup__StyledMessage-sc-h4dfhv-2 bUGZCU
# # MessageHover__MessageHoverRoot-sc-6lkiln-0 dNlIrv BubbleText__BubbleTextRoot-sc-1bng39n-0 fJaVvT MessageGroup__StyledMessage-sc-h4dfhv-2 bUGZCU
#             print("-----------------> 3")
#             # "BubbleText__BubbleTextContent-sc-1bng39n-1"
#             print(x.get_attribute("class"))
#             if "hvuwYF" in x.get_attribute("class"):
#                 print("-----------------> 4")
#                 spans = x.find_elements_by_tag_name("span")
#                 print(spans)
#         #         spans = x.find_element(By.TAG_NAME,"span")

#                 for y in spans:
#                     print("-----------------> 5")
#                     message = y.get_attribute('innerHTML')
#                     print(y)
#                     print("-----------------> 6")
#                     print(message)
#         #             if "<span>" not in message and not (message == "thumb up" or message == "thumb down") and (message != "show more actions"):

#         #                 messages.append(message)

#         # return messages

#     except:

#         print("ERROR: GetMessage didn't work!")






# Gets TheLastMessage out of Array messages

def GetLastMessage(browser, messages=[]):

    try:

        return messages[len(messages) - 3] #messages

    except:

        print("ERROR: GetLastMessage didn't work!")


def main():

    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    DoLogin(browser, "farazuddin.m1999@gmail.com", "hussnafarha1")


    data = pd.read_csv('data_text.csv')
    # print(data)
    ss = sentence_similarity()

    pass_cnt = 0

    fail_cnt = 0
    
    r1 = []
    
 
    try:

        for i in range(0, 6):

            print("Input to Replika - ")

            print(data.iloc[i]['Requests'])
            print("Send Text: ")
            # Send message

            SendMessage(browser, data.iloc[i]['Requests'])



            # Getting current Messages (for checking if any new messages)
            # GetMessages(browser)
            r1 = GetMessages(browser)

            print("Output from Replika - ")




            print("--Last msg--")

            last_message = GetLastMessage(browser, r1)

            print(last_message)

            print("Similarity Test - ")

            sample_sentences_list = [s.rstrip(' ').lstrip(' ') for s in list(data.iloc[i]['Responses'][1:-1].split(","))]

            present, most_similar_exp_output, similarity_score = ss._run(sample_sentences_list, last_message)

            if present:

                print('----------PASS-----------\nSimilarity Score = %f'%(similarity_score))

                pass_cnt += 1

            else:

                print('----------FAIL-----------\nSimilarity Score = %f'%(similarity_score))

                fail_cnt += 1
    except:
        print("ERROR: Execution of Main Failed!")



    print("====================SUMMARY=========================")

    print("Number of test cases that passed = {}".format(pass_cnt))

    print("Number of test cases that failed  = {}".format(fail_cnt))

    print("====================================================")

    # browser.close()





if __name__ == '__main__':

    main()

