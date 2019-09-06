import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from helpers import quickDriver

def getDetailsOUP(url, driver, issueDate):
    """
    Helper function that returns the details for an issue on a given page of the OUP website (home to both QJE and REStud)
    url: string
        The url with information about all articles in the issue
    driver: selenium.webdriver
        A selenium webdriver instance that will fetch from the url
    issueDate: string
        what month/year is the issue in YYYY-MM-DD
    """
    driver.get(url)
    buttons = driver.find_elements_by_xpath('//a[@class="showAbstractLink"]')
    for i in range(len(buttons)):
        driver.execute_script("arguments[0].scrollIntoView();", buttons[i])
        driver.execute_script("arguments[0].click();", buttons[i])
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ts = [t.get_text().strip() for t in soup.find_all('h5', attrs = {'class': 'customLink item-title'})]
    ls = [piece.replace("Abstract", "").strip() for piece in soup.get_text().split(" ") if "//doi.org/" in piece]
    absts = [abst.get_text().replace("Abstract", "").strip() for abst in soup.find_all('section', attrs = {'class': 'abstract'})]
    dates = [issueDate for i in range(len(ts))]
    compiled = list(zip(dates, ls, ts, absts))
    return(compiled)

def getQJE(startYear, endYear):
    """
    Get a dataframe with QJE information in the given time range - specifically all articles with their titles, abstracts, URLs, issue dates.
    startYear: int
        The first year for which QJE info is requested. IMPORTANT: This method stops returning abstract information around the 1940s
    endYear: int
        The last year (inclusive) for which QJE info is requested
    """
    rootUrl = "https://academic.oup.com/qje/issue/"
    years = range(startYear, endYear + 1)
    quarters = range(1, 5)
    quarterMap = {1: '02', 2: '05', 3: '08', 4: '11'}
    driver = quickDriver()
    linkList = []
    for year in years:
        for quarter in quarters:
            issue = year - 1885
            month = quarterMap[quarter]
            url = rootUrl + str(issue) + "/" + str(quarter) + "/"
            issueDate = str(year) + '-' + month + '-01'
            compiled = getDetailsOUP(url, driver, issueDate)
            linkList = linkList + compiled
    qje = pd.DataFrame(linkList, columns = ['Date', 'ArticleURL', 'Title', 'Abstract'])
    qje['Journal'] = 'QJE'
    return(qje)

def getREStud(startYear, endYear):
    """
    Get a dataframe with REStud information in the given time range - specifically all articles with their titles, abstracts, URLs, issue dates.
    startYear: int
        The first year for which REStud info is requested
    endYear: int
        The last year (inclusive) for which REStud info is requested
    """
    rootUrl = "https://academic.oup.com/restud/issue/"
    years = range(startYear, endYear+1)
    quarters = range(1, 5)
    quarterMap = {1: '01', 2: '04', 3: '07', 4: '10'}
    driver = quickDriver()
    linkList = []
    for year in years:
        for quarter in quarters:
            issue = year - 1933
            month = quarterMap[quarter]
            url = rootUrl + str(issue) + "/" + str(quarter) + "/"
            issueDate = str(year) + '-' + month + '-01'
            compiled = getDetailsOUP(url, driver, issueDate)
            linkList = linkList + compiled
    restud = pd.DataFrame(linkList, columns = ['Date', 'ArticleURL', 'Title', 'Abstract'])
    restud['Journal'] = 'REStud'
    return(restud)
