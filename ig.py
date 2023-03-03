from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, urllib.request
# import requests
import parameters
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#reference source about instagram scraping: https://python.plainenglish.io/scrape-everythings-from-instagram-using-python-39b5a8baf2e5

s=Service("D:\CSE Software\Chrome Driver 107\chromedriver")
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--disable-extensions")

# # Pass the argument 1 to allow and 2 to block
# chrome_options.add_experimental_option(
#     "prefs", {"profile.default_content_setting_values.notifications": 1}
# )

# driver = webdriver.Chrome(options=chrome_options, service=s)


driver = webdriver.Chrome(service=s)


url="https://www.instagram.com/"
driver.get(url)

#logging in to instagram with email and password
def logged_in():
    #login
    time.sleep(5)
    import parameters

    username = driver.find_element("css selector", "input[name='username']")
    password =driver.find_element("css selector", "input[name='password']")
    wait = WebDriverWait(driver, 10)

    username.clear()
    password.clear()
    username.send_keys(parameters.ig_username)
    password.send_keys(parameters.ig_password)

    login=driver.find_element("css selector", "button[type='submit']").click()

    # #save your login info?
    time.sleep(10)

    #to learn more about xpath : https://www.browserstack.com/guide/find-element-by-xpath-in-selenium#:~:text=Go%20to%20the%20First%20name,locate%20the%20first%20name%20field.
#     notnow = driver.find_element("xpath","//button[contains(text(), 'Not Now')]")
#     driver.execute_script("arguments[0].click();", notnow)

    #turn on notif
#     time.sleep(10)
#     notnow2 = driver.find_element("xpath","//button[contains(text(), 'Not Now')]")
#     driver.execute_script("arguments[0].click();", notnow2)

    post_extraction()





#get number of following, followers and total posts from the page and extract description, comments, like number and date posted from each post  
def post_extraction():
        #Attach desired website link here
        driver.get("https://www.instagram.com/docdoc.app/?hl=en")

        # link to learn more about https://www.softwaretestingmaterial.com/webdriverwait-selenium-webdriver/
        try:
                WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '(//header[@class="x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"]//span[@class="_ac2a"])[1]')))
        except:
                pass

        #actual website path to extract data from
        posts = driver.find_element("xpath",'(//header[@class="x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"]//span[@class="_ac2a"])[1]') 
        total_posts = posts.text
        print("Total Posts",total_posts)

        WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'(//header[@class="x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"]//span[@class="_ac2a"])[2]')))
        followers = driver.find_element("xpath",'(//header[@class="x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"]//span[@class="_ac2a"])[2]')
        total_followers = followers.text
        print("Total Followrs",total_followers)

        WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'(//header[@class="x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"]//span[@class="_ac2a"])[3]')))
        followings = driver.find_element("xpath",'(//header[@class="x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"]//span[@class="_ac2a"])[3]')
        
        total_followings = followings.text
        print("Total Followings",total_followings)
        
        #clicking the first post in instagram
        WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'(//div[@class="_aagw"])[1]')))
        driver.find_element("xpath",'(//div[@class="_aagw"])[1]').click()

        i=0
        

        descriptions, cmt,likes,days = ([] for i in range(4))
        while i < 40: #sample size of number of posts extracted
                comments = []
                WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH,'(//span[@class="_aacl _aaco _aacu _aacx _aad7 _aade"])[1]')))
                
                #Description extraction
                des = driver.find_element("xpath",'(//span[@class="_aacl _aaco _aacu _aacx _aad7 _aade"])[1]')
                description = des.text
                #     print("Description",description)

                #Comment extraction
                try:
                        # load more comments
                        more_comments = ''
                        while more_comments is not None:
                                path = '//li//div[@class="_ab8w  _ab94 _ab99 _ab9h _ab9m _ab9p  _abcj _abcm"]//button[@class="_abl-"]'
                                try:
                                        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, path)))
                                except:
                                        pass

                                try: 
                                        more_comments = driver.find_element(by=By.XPATH, value=path)
                                        driver.execute_script("arguments[0].click();", more_comments)
                                except:
                                        more_comments = None
                        # print('more cmts')

                        
                        #load more replies
                        more_replies = ['']
                        while len(more_replies) != 0 :
                                path = '//button[@class="_acan _acao _acas"]//span[contains(text(), "View replies")]'
                                try:
                                        WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, path)))
                                except:
                                        pass

                                more_replies = driver.find_elements(by=By.XPATH, value=path)
                                for j in range(len(more_replies)):
                                        driver.execute_script("arguments[0].click();", more_replies[j])

                        try:
                                WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH,'//span[@class="_aacl _aaco _aacu _aacx _aad7 _aade"]')))
                        except:
                                pass
                        cmts= driver.find_elements("xpath",'//span[@class="_aacl _aaco _aacu _aacx _aad7 _aade"]')
                        
                        for j in range(len(cmts)):
                                comments.append(cmts[j].text)
                                
                        #     j=1
                        #     while j <len(cmts):
                        #         comments.append(cmts[j].text)
                        #         # print(cmts[j].text)
                        #     j+=1
                        #     print("Comments",comments)
                except:
                        # pass
                        #     comment=0
                                comments=0


                # Like extraction
                try:
                        WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH,'//div[@class="_aacl _aaco _aacw _aacx _aada _aade"][contains(text(),"like")]')))
                        lk = driver.find_element("xpath",'//div[@class="_aacl _aaco _aacw _aacx _aada _aade"][contains(text(),"like")]')
                        like = lk.text
                        # print("Likes",like)

                except:
                        like = 0
                        # pass

                #Time extraction      
                WebDriverWait(driver, 30).until(
                        EC.visibility_of_element_located((By.XPATH,'//div[@class="_aacl _aacm _aacu _aacy _aad6"]//time')))
                d = driver.find_element("xpath",'//div[@class="_aacl _aacm _aacu _aacy _aad6"]//time')
                day=d.text
                # print("Time",day)

                descriptions.append(description)
                likes.append(like)
                days.append(day)
                cmt.append(comments[1:])
                time.sleep(1)
                i+=1

        #             # go to next posts after the first post in instagram by clicking of right button
                WebDriverWait(driver, 30).until(
                        EC.visibility_of_element_located((By.XPATH,'//div[@class=" _aaqg _aaqh"]//button[@class="_abl-"]')))
                driver.find_element("xpath",'//div[@class=" _aaqg _aaqh"]//button[@class="_abl-"]').click()
                #     print("comment",cmt[1:])

        #add the results to dataframe
        #link to learn more about https://sparkbyexamples.com/pandas/pandas-write-dataframe-to-csv-file/
        df = pd.DataFrame({'Total Posts': total_posts, 'Total followers':total_followers,'Total followings':total_followings,
                        'Descriptions': descriptions, 'Reactions': likes,'Comments': cmt, 'Time': days})
        df.to_csv('ig.csv')

logged_in()