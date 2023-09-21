1.	Use Selenium to scrape all the reviews on the Tripadvisor 

-Install Selenium and Pandas libraries, Set the path to the web driver in the code.

-Use Selenium to navigate to the website and find the required elements using CSS selectors and Xpath.

-To accessary the process speed. I used a loop to click all the "read more" button and creat a bonus_title, otherwise python has to scrap this content each time.

-Use try-except to handle empty reviews. The website might respond nothing for empty reviews which will cause error, so I add a condition to handle this.

-check the outpute path if occurs error



2.	Using the Producthunt API, find all the featured products in the last 7 days

-setup pandas and requests at first

-When prompted, enter the Developer Token obtained from ProductHunt API in the designated "your API token" field.

-Although the test request only 7 days data. I tried and accomplished selecting data by either number or date. Now The program can scrap arbitrary number of records according to the amount or days you want and store the data in a CSV file. The data points number can be changed but no more than 6250.

-Please be aware that the ProductHunt API has a quota limit of 6250 complexity points for every 15 minutes. If occur TypeError:"'NoneType' object is not subscriptable", might because over the quota limit.
