import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from helpers import quickDriver

def getDetailsJPE(url, driver, issueDate):
    """
    Helper function that returns the details for a JPE issue on a given page.
    url: string
        The url with information about all articles in the issue
    driver: selenium.webdriver
        A selenium webdriver instance that will fetch from the url
    issueDate: string
        what month/year is the issue in YYYY-MM-DD
    """
    driver.get(url)
    buttons = driver.find_elements_by_xpath("//a[@class='listSign']")
    for i in range(len(buttons)):
        driver.execute_script("arguments[0].scrollIntoView();", buttons[i])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", buttons[i])
        time.sleep(1)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_absts = soup.find_all('a', attrs = {'class': 'ref nowrap'})
    links = [a['href'] for a in all_absts if "Abstract" in a.get_text()]
    titles = [t.get_text().strip() for t in soup.find_all('span', attrs = {'class': 'art_title'})]
    absts = [a.get_text().strip() for a in soup.find_all('p', attrs = {'class': 'abstractSection'})]
    dates = [issueDate for i in range(len(titles))]
    compiled = list(zip(dates, links, titles, absts))
    return(compiled)

def getJPE(startYear, endYear):
    """
    Get a dataframe with JPE information in the given time range - specifically all articles with their titles, abstracts, URLs, issue dates.
    startYear: int
        The first year for which JPE info is requested. IMPORTANT: 1988 is the earliest year for which this method successfully returns abstract information.
    endYear: int
        The last year (inclusive) for which JPE info is requested
    """
    rootUrl = "https://www.journals.uchicago.edu/toc/jpe/"
    years = range(startYear, endYear + 1)
    issues = range(1, 7)
    issueMap = {1: '02', 2: '04', 3: '06', 4: '08', 5: '10', 6: '12'}
    linkList = []
    driver = quickDriver()
    for year in years:
        vol = year - 1892
        for issue in issues:
            url = rootUrl + str(year) + "/" + str(vol) + "/" + str(issue)
            month = issueMap[issue]
            issueDate = str(year) + '-' + month + '-01'
            compiled = getDetailsJPE(url, driver, issueDate)
            linkList = linkList + compiled
    jpe = pd.DataFrame(linkList, columns = ['Date', 'ArticleURL', 'Title', 'Abstract'])
    jpe['ArticleURL'] = "https://www.journals.uchicago.edu" + jpe['ArticleURL']
    jpe['Journal'] = 'JPE'
    return(jpe)
