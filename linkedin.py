import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
s = Service('D:\CSE Software\Chrome Driver 106\chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)


#logging in to LinkedIn using email and password
def logging_linkedIn():
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com')

    # WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.XPATH, '//a[@data-tracking-control-name="homepage-basic_intl-segments-login"]')))

    # sign_in_button = driver.find_element(by=By.XPATH, value='//a[@data-tracking-control-name="homepage-basic_intl-segments-login"]')
    # sign_in_button.click()

    # sleep(3)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//button[@class="sign-in-form__submit-button"]')))

    # locate email form by_class_name
    username = driver.find_element('id', 'session_key')
    # send_keys() to simulate key strokes
    username.send_keys(parameters.linkedin_username) #replace your email

    # locate password form by_class_name
    password = driver.find_element('id', 'session_password') 
    # send_keys() to simulate key strokes
    password.send_keys(parameters.linkedin_password) #replace your password

    # locate submit button by_class_name
    log_in_button = driver.find_element(
        'class name', 'sign-in-form__submit-button')
    # .click() to mimic button click
    sleep(3)
    log_in_button.click()

    # sleep(5)

    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # sleep(4)

    # skip_button = driver.find_element(
    #     'class name', 'secondary-action-new')
    # skip_button.click()
    # sleep(2)


    # about_extraction()
    # people_extraction()
    post_extraction()


#Extract data from About part of desired site
def about_extraction():
    driver.get('https://www.linkedin.com/company/myjobsmyanmar/about/') #link of 'About' of desired site on linkedIn
    sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(4)
    overview = driver.find_element(by=By.XPATH, value='//section[@class="artdeco-card p5 mb4"]//p[@class="break-words white-space-pre-wrap mb5 text-body-small t-black--light"]')
    overview_text = overview.text


    elements = driver.find_elements(by=By.XPATH, value='//section[@class="artdeco-card p5 mb4"]//dl[@class="overflow-hidden"]//dd')
    weblink = elements[0].text
    industry = elements[1].text
    company_size = elements[2].text
    employees_on_linkedIn = elements[3].text
    headquarters = elements[4].text
    speciality = elements[5].text

    df = pd.DataFrame({'Overview': overview_text, 'Website': weblink, 'Industry': industry, 'Company Size': company_size + " "+  employees_on_linkedIn, 'Headquarters': headquarters, 'Specialities': speciality}, index=[0])
    df.to_csv('linkedIn.csv')
    print(df)


#Extract data from People part of desired site
def people_extraction():
    driver.get('https://www.linkedin.com/company/myjobsmyanmar/people/')
    employees_on_linkedIn = driver.find_element(by=By.XPATH, value='//div[@class="artdeco-card pb2"]//h2[@class="t-20 t-black t-bold"]')
    print(employees_on_linkedIn.text)

    driver.execute_script("window.scrollBy(0,810)")
    # sleep(4)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="org-people__show-more-button t-16 t-16--open t-black--light t-bold"]')))
    showMore_button = driver.find_element(by=By.XPATH, value='//button[@class="org-people__show-more-button t-16 t-16--open t-black--light t-bold"]')
    showMore_button.click()

    country, university, industry, major, skill, connection = ([] for i in range(6))  
    i = 1 
    incr = 1 #represent each category
    while i <= 3: # 3 pages in People tab to be scraped
        for k in range(2): # 2 categories in a page
            sleep(2)
            # path = '(//div[@class="artdeco-carousel__content"]//li)['+str(incr)+']//span'
            path = '(//div[@class="artdeco-carousel__content"]//li)['+str(incr)+']//button//div[@class="org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"]//span'
            category = driver.find_elements(by=By.XPATH, value=path)
            category_list = [category[j].text for j in range(len(category))]

            sleep(2)
            # path = '(//div[@class="artdeco-carousel__content"]//li)['+str(i)+']//button//div[@class="org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"]//strong'
            path = '(//div[@class="artdeco-carousel__content"]//li)['+str(incr)+']//strong'
            count = driver.find_elements(by=By.XPATH, value=path)
            count_list = [count[j].text for j in range(len(count))]

            incr += 1

            if i == 1 and k == 0:
                country.extend((f'{count_list[j]} | {category_list[j]}' for j in range(len(category_list))))
            elif i == 1 and k == 1:
                university.extend((f'{count_list[j]} | {category_list[j]}' for j in range(len(category_list))))
            elif i == 2 and k == 0:
                industry.extend((f'{count_list[j]} | {category_list[j]}' for j in range(len(category_list))))
            elif i == 2 and k == 1:
                major.extend((f'{count_list[j]} | {category_list[j]}' for j in range(len(category_list))))
            elif i == 3 and k == 0:
                skill.extend((f'{count_list[j]} | {category_list[j]}' for j in range(len(category_list))))
            elif i == 3 and k == 1:
                connection.extend((f'{count_list[j]} | {category_list[j]}' for j in range(len(category_list))))
        i += 1 

        sleep(2)
        target = driver.find_element(by=By.XPATH, value='//button[@aria-label="Next"]')   
        driver.execute_script('arguments[0].scrollIntoView(true);', target)
        driver.execute_script("arguments[0].click();", target)


    # print('Where they live: ', country, '\n\nWhere they studied: ', university, '\n\n What they do: ', industry, '\n\n What they studied: ', major, '\n\n What they are skilled at: ', skill, '\n\n How you are connected: ', connection)
    
    
    mydict = {'Where They Live': country, 'Where They Studied': university, 'What They Do': industry,'What They Studied': major, 'What They are Skilled at': skill, 'How You are Connected': connection}
    dict_df = pd.DataFrame({ key:pd.Series(value) for key, value in mydict.items() })
    dict_df.to_csv('linkedIn_people.csv')
    print(dict_df)

    
    
#Extract description, number of comments and reactions, texts of comments from each post
def post_extraction():
    # driver.get("https://www.linkedin.com/company/myjobsmyanmar/posts/")
    driver.get("https://www.linkedin.com/company/shopee/posts/")

    # driver.get("https://www.linkedin.com/company/google-ai/posts/")

    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(4)

    scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

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

        if i > 20: #scroll time
            break
    
    time = driver.find_elements(by=By.XPATH, value='//div[@class="ember-view  occludable-update "]//span[@class="visually-hidden"][contains(text(),"ago")]')
    # print("Time : ", len(time))
    time_list = [time[i].text for i in range(len(time))]
    
    description = driver.find_elements(by=By.XPATH, value='//div[@class="ember-view  occludable-update "]//span[@class="break-words"]//span[@dir="ltr"]')
    # print("Desc : ", len(description))
    description_list = [description[i].text for i in range(len(description))]

    temp_list = driver.find_elements(by=By.XPATH, value='//button[@aria-label="Comment"]')
    button_list = [i.get_attribute('id') for i in temp_list]
    print(button_list)

    reaction_list = []
    comment_list = []
    comment_count = []
    description_link = []
    for i in range(len(button_list)):
        target = driver.find_element(by=By.ID, value=button_list[i])
        driver.execute_script('arguments[0].scrollIntoView(true);', target)
        print("scroll")

        path = '(//div[@class="ember-view  occludable-update "]//div[@class="feed-shared-update-v2__description-wrapper"])['+str(i+1)+']//span[@class="break-words"]//span[@dir="ltr"]//a'
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, path)))
        except:
            pass
        
        links = driver.find_elements(by=By.XPATH, value=path)
        specific_link = [links[j].get_attribute("href") for j in range(len(links))]
        description_link.append(specific_link)
        # print('description done')

        #click comment button
        sleep(1)
        comment_button = driver.find_element(by=By.XPATH,value=f'(//button[@id="{button_list[i]}"])')
        driver.execute_script("arguments[0].click();", comment_button)
        # print('cmt button clicked')

        #reaction
        sleep(1)
        path = '(//div[@class="social-details-social-activity update-v2-social-activity"])['+str(i+1)+']//span[@class="social-details-social-counts__reactions-count"]'
        try:
            reaction = driver.find_element(by=By.XPATH, value=path)
            reaction_list.append(reaction.text)
        except:
            reaction_list.append('0')
        # print('got reaction')

        
        path = '(//div[@class="social-details-social-activity update-v2-social-activity"])['+str(i+1)+']//span[@class="display-flex align-items-center t-black--light t-bold"]'
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, path)))
        except:
            pass

        try: 
            #click comment options button 
            comment_options = driver.find_element(by=By.XPATH, value=path)
            driver.execute_script("arguments[0].click();", comment_options)
            # print('click cmt option')

            #choose Most Recent to see all comments
            path = '//div[@aria-label="Most recent. See all comments, the most recent comments are first"]//h5'
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, path)))
            except:
                pass
            
            most_recent = driver.find_element(by=By.XPATH, value=path)
            driver.execute_script("arguments[0].click();", most_recent)
            # print('most recent')

            # load more comments
            more_comments = ''
            while more_comments is not None:
                path = '//button[@class="comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]//span[@class="artdeco-button__text"]'
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
                path = '//button[@class="button show-prev-replies t-12 t-black t-normal hoverable-link-text"]'
                try:
                    WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, path)))
                except:
                    pass

                more_replies = driver.find_elements(by=By.XPATH, value=path)
                for j in range(len(more_replies)):
                    driver.execute_script("arguments[0].click();", more_replies[j])
            # print('more replies')

            #get all comments for a post
            path = '(//div[@class="social-details-social-activity update-v2-social-activity"])['+str(i+1)+']//span[@class="comments-comment-item__main-content feed-shared-main-content--comment t-14 t-black t-normal"]//span[@dir="ltr"]'
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, path)))
            except:
                pass
            
            comments = driver.find_elements(by=By.XPATH, value=path)
            specific_comment = [comments[j].text for j in range(len(comments))]
            comment_list.append(specific_comment)
            
            comment_count.append(len(comment_list[i]))

        except:
            comment_list.append([])
            comment_count.append(0)
        
        
        
    print(len(button_list))
    # for i in range(len(button_list)):
    #     print(f"Post {i}: {time_list[i]}, {description_list[i]}, Reaction Count: {reaction_list[i]}, Comment Count: {comment_count[i]} \n, Comments: {comment_list[i]}")

    df = pd.DataFrame({'Timeline': time_list, 'Description': description_list, 'Links': description_link,'Reaction Count': reaction_list, 'Comment Count': comment_count, 'Comments': comment_list})
    df.to_csv('linkedIn_shopee.csv')
    print(df)
    


    

logging_linkedIn()
#driver.quit()

