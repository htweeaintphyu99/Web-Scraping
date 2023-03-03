from selenium import webdriver
import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service
import pandas as pd
import parameters
# from webdriver_manager.chrome import ChromeDriverManager

#Connect with chrome using chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" #location of chrome.exe

chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)


#download chromedriver version which is matched with chrome version and insert its path
s=Service('D:\CSE Software\Chrome Driver 106\chromedriver') 

# driver = webdriver.Chrome(service=s)
driver = webdriver.Chrome(options=chrome_options, service=s)



#Logging in to facebook using email and password
def logged_in():

    url="https://www.facebook.com/"
    driver.get(url)

    #login
    sleep(1)
    username = driver.find_element("id","email")
    password = driver.find_element("id","pass")
    submit   = driver.find_element("name","login")
    username.send_keys(parameters.fb_username)
    password.send_keys(parameters.fb_password)
    submit.click()

    sleep(3)
    post_extraction()



#click 'See More' button to see each full comment
def seeMore_comment():
    path = '//div[@class="xv55zj0 x1vvkbs x1rg5ohu xxymvpz"]//div//div[@dir="auto"]//div[@role="button"][contains(text(), "See more")]'
    sleep(3)
    see_more = driver.find_elements(by=By.XPATH, value=path)
    if len(see_more) > 0:    
        count = 0
        for i in see_more:
            driver.execute_script("arguments[0].click();", i)
        sleep(1)
    else:
        pass


#extracting descriptions, reactions number and comments from posts
def desc_and_comment_extraction(postNum):
     
    description_list = []
    reaction_list = []
    comment_count = []
    comment_list = []
    
    i = postNum-1
   
    while i >= 0:

        #scroll into each post
        post_div = driver.find_element(by=By.XPATH, value='(//div[@class="x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a"])['+str(i+1)+']')
        driver.execute_script('arguments[0].scrollIntoView(true);',post_div)

        #reaction
        path = '(//div[@class="x10wlt62 x6ikm8r x9jhf4c x30kzoy x13lgxp2 x168nmei"])['+str(i+1)+']//span[@class="xt0b8zv x1jx94hy xrbpyxo xl423tq"]'
        try:
            reaction = driver.find_element(by=By.XPATH, value=path)
            reaction_list.append(reaction.text)
        except:
            reaction_list.append('0')

        sleep(1)
        
        #find see more button of description and click
        path = '(//div[@class="x1iorvi4 x1pi30zi x1l90r2v x1swvt13"]//div[@class="x78zum5 xdt5ytf xz62fqu x16ldp7u"])['+str(i+1)+']//div[@role="button"][contains(text(),"See more")]'
        
        try: 
            desc_seeMore = driver.find_element(by=By.XPATH, value=path)
            driver.execute_script("arguments[0].click();", desc_seeMore)

        except:
            pass

        #get descriptions of each post
        path = '(//div[@class="x1iorvi4 x1pi30zi x1l90r2v x1swvt13"])['+str(i+1)+']//div[@dir="auto"]' 
        description = driver.find_elements(by=By.XPATH, value=path)
        desc_list = [description[j].text for j in range(len(description))]

        desc_string = ''
        for j in range(len(desc_list)):
            desc_string += desc_list[j]
        description_list.append(desc_string)



        sleep(2)
        #find comment options button and click
        path = '(//div[@class="x10wlt62 x6ikm8r x9jhf4c x30kzoy x13lgxp2 x168nmei"])['+str(i+1)+']//div[@class="x6s0dn4 x78zum5 xdj266r x11i5rnm xat24cr x1mh8g0r xe0p6wg"]//div[@role="button"]'
        try:   
            comment_options = driver.find_element(by=By.XPATH, value=path)
            driver.execute_script("arguments[0].click();", comment_options)
        except:
            pass

        sleep(1) 
        #choose All Comments in comment options
        path = '//div[@class="x4k7w5x x1h91t0o x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1n2onr6 x1qrby5j x1jfb8zj"]//span[@dir="auto"][contains(text(),"All comments")]'
        try:
            all_comments = driver.find_element(by=By.XPATH, value=path)
            driver.execute_script("arguments[0].click();", all_comments)
        except:
            pass
          
        #click 'View more comments' button if it exists
        sleep(1)
        path = '(//div[@class="x10wlt62 x6ikm8r x9jhf4c x30kzoy x13lgxp2 x168nmei"])['+str(i+1)+']//span[@class="x78zum5 x1w0mnb xeuugli"]//span[@dir="auto"]'   
        try:
            # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, path)))
            more_comments = driver.find_element(by=By.XPATH, value=path)
            driver.execute_script("arguments[0].click();", more_comments)
        except:
            pass
        
        
        
        sleep(2)
        path = '(//div[@class="x10wlt62 x6ikm8r x9jhf4c x30kzoy x13lgxp2 x168nmei"])['+str(i+1)+']//div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]'
        
        # WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(By.XPATH,path))
        numberOfComments = driver.find_elements(by=By.XPATH, value=path)
        comment_count.append(len(numberOfComments))
        print(len(numberOfComments))
        

        #find See More button for each comment and click them
        seeMore_comment()

        comment_list_for_one = []
        for j in range(len(numberOfComments)): #loop through the comments of each post
            specific_comment = ''
            sleep(2)

            # each comment path
            path = '((//div[@class="x10wlt62 x6ikm8r x9jhf4c x30kzoy x13lgxp2 x168nmei"])['+str(i+1)+']//ul//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"])['+str(j+1)+']//div[@dir="auto"]'
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, path)))
            except:
                pass
            comment = driver.find_elements(by=By.XPATH, value=path)
            
            for k in range(len(comment)):
                specific_comment += ' '+ comment[k].text
            comment_list_for_one.append(specific_comment)
        comment_list.append(comment_list_for_one)
            
        i -= 1

    # print('Desc list is : ', description_list , len(description_list))
    # print('Reaction list: ', reaction_list)
    # print('Comment count: ', comment_count)
    # print('Comment list: ',  comment_list)

    #Scrolled the desired number of times and scraped first the data from the last post where the scroll stops in this algorithm. Reverse the lists to order the latest posts first
    description_list.reverse()
    reaction_list.reverse()
    comment_count.reverse()
    comment_list.reverse()

    #create dataframe for the result lists and save as a csv file
    mydict = {'Description': description_list, 'Reaction Count': reaction_list, 'Comment Count': comment_count, 'Comments': comment_list}
    dict_df = pd.DataFrame({ key:pd.Series(value) for key, value in mydict.items() })
    dict_df.to_csv('facebook.csv')
    print(dict_df)
   

#extract posts from 'My Jobs Myanmar' page
def post_extraction():
    driver.get("https://www.facebook.com/MyJobsMyanmar/")

    sleep(1)
    #scroll many times as you want
    scroll_pause_time = 3 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1 #number of scroll time

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  

        # Break the loop when the height we need to scroll to is larger than the total scroll height
        # if (screen_height) * i > scroll_height:
        #     break 

        if i > 13: 
            break

    # time = driver.find_elements(by=By.XPATH, value='//a[@class="qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq jxuftiz4 cxfqmxzd tes86rjd"]')
    # # print("Time : ", len(time))
    # time_list = [time[i].text for i in range(len(time))]
    # print(time_list)


    #Number of posts collected
    numberOfPosts = driver.find_elements(by=By.XPATH, value='//div[@class="x1iorvi4 x1pi30zi x1l90r2v x1swvt13"]')
    print(len(numberOfPosts))
    desc_and_comment_extraction(len(numberOfPosts))
    

logged_in()

