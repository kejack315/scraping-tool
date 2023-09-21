import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


# Add unlimited frame
def unlimited_frame():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


# get score
def get_score(container):
    Score_bubble = container.find_element(By.CSS_SELECTOR, ".ui_bubble_rating").get_attribute("class")
    Score = Score_bubble.split("_")[3]
    return Score


# get review title
def get_review_title(container):
    Review_title = container.find_element(By.CSS_SELECTOR, "a span").text
    return Review_title


# get review content
def get_review_content(container):
    Review_content = container.find_element(By.CSS_SELECTOR, ".QewHA").text
    return Review_content


# get date
def get_travel_date(container):
    Date_detail = container.find_element(By.CSS_SELECTOR, ".teHYY").text
    Date_of_travel = Date_detail.split("Date of travel:")[1]
    return Date_of_travel


# determine the page to scrape, can use click NEXT button as well
def scrape_tripadvisor_reviews(amount, driver):
    df = pd.DataFrame(columns=['Score', 'Review_title', 'Review_content', 'Date_of_travel', 'Bonus'])
    # amount of data to scrape
    number_loop = (amount + 4) // 5

    for index1 in range(number_loop):
        driver.get(
            "https://www.tripadvisor.com.au/Airline_Review-d8729133-Reviews-or" + str(index1 * 5) + "-Qantas#REVIEWS")
        time.sleep(2)
        # click all the "read more" button
        driver.find_element(By.CSS_SELECTOR, ".Ignyf").click()
        # create individual bonus title, can scrape from the website, but this way increases the run speed
        Bonus_title = ["Legroom: ", "Seat comfort: ", "In-flight Entertainment: ", "Customer service: ",
                       "Value for money: ", "Cleanliness: ", "Check-in and boarding: ", "Food and Beverage: "]
        # 5 comments each page
        for i in range(5):
            container = driver.find_element(By.XPATH,
                                            '//*[@id="component_1"]/div/div[5]/div/div/div/div[2]/div[*]/div[2]/div/div[' + str(
                                                i) + '+3]')
            # Ratings of individual criteria (Bonus)
            List_Bonus = []  # use list to save bonus data
            if i == 0:  # the path of the first comment on each page is different from others, so use 'if' to get different comments
                for j in range(8):
                    try:  # use try and except to avoid null comments error
                        # can't use CSS selector, maybe because of the flex tag
                        Bonus_class = container.find_element(By.XPATH, '//./div[3]/div[3]/div[2]/div[' + str(
                            j + 1) + ']/span[1]/span').get_attribute("class")
                        Bonus = Bonus_class.split("_")[3]
                        List_Bonus.append(Bonus_title[j] + Bonus)
                    except:
                        List_Bonus.append(Bonus_title[j] + "null")
            else:
                for z in range(8):
                    try:  # path can't be shortened, an unreal path maybe
                        Bonus_class = container.find_element(By.XPATH,
                                                             '//*[@id="component_1"]/div/div[5]/div/div/div/div[2]/div[*]/div[2]/div/div[' + str(
                                                                 i + 3) + ']/div[2]/div[3]/div[2]/div[' + str(
                                                                 z + 1) + ']/span[1]/span').get_attribute("class")
                        Bonus = Bonus_class.split("_")[3]
                        List_Bonus.append(Bonus_title[z] + Bonus)
                    except:
                        List_Bonus.append(Bonus_title[z] + "null")
            Str_bonus = " ".join(List_Bonus)
            # save data in dictionary
            my_dic = {
                "Score": get_score(container),
                "Review_title": get_review_title(container),
                "Review_content": get_review_content(container),
                "Date_of_travel": get_travel_date(container),
                "Bonus": Str_bonus
            }
            df = df._append(my_dic, ignore_index=True)
    df.drop(df.tail(len(df) - amount).index, inplace=True)
    df.to_csv(path_or_buf='c:/python/result.csv', encoding='utf_8_sig', index=False)
    df.to_json(path_or_buf='c:/python/result.json')


amount = int(input("number of reviews to scrape:"))
driver = unlimited_frame()
scrape_tripadvisor_reviews(amount, driver)
print("done")
