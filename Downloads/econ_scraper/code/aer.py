import pandas as pd
import requests
from bs4 import BeautifulSoup
from helpers import quickSoup
import time
from datetime import datetime, date

def getLinksAER():
    """
    Helper to get the links for AER articles.
    """
    rootUrl = "https://www.aeaweb.org/journals/aer/issues"
    rootSoup = quickSoup(rootUrl)
    issues = rootSoup.find_all('div', attrs = {'style': 'margin-top:5px;'})
    bigList = []
    for issue in issues:
        littleList = []
        year = int(issue.get_text().split(" ")[1])
        monthName = issue.get_text().split(" ")[0]
        monthName = monthName[1:]
        monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        monthNum = monthList.index(monthName) + 1
        mmyy = date(year = year, month = monthNum, day = 1)
        littleList.append(mmyy)
        href = issue.find('a')['href']
        littleList.append("https://www.aeaweb.org" + href)
        bigList.append(littleList)

    rootDf = pd.DataFrame(bigList, columns = ['Date', 'ArticleURL'])
    return(rootDf)

def getAbstractAER(url):
    """
    Helper to get the abstract given a URL.
    """
    page = quickSoup(url)
    abst = page.find("section", attrs = {"class": "article-information abstract"})
    if abst is not None:
        cleanedAbs = abst.get_text().strip().replace("Abstract", "").strip()
        return cleanedAbs

def getAER():
    """
    Get a dataframe with all recent AER articles with their titles, abstracts, URLs, issue dates.
    """
    rootDf = getLinksAER()
    aerList = []
    def getArticles(row):
        issueSoup = quickSoup(row['URL'])
        articles = issueSoup.find_all('h3')
        for art in articles:
            if art.find('a') is not None:
                artUrl = "https://www.aeaweb.org" + art.find('a')['href']
                artTitle = art.find('a').get_text()
                newRow = [row['Date'], artUrl, artTitle]
                aerList.append(newRow)
    rootDf.apply(getArticles, axis = 1)
    aer = pd.DataFrame(aerList, columns = ['Date', 'ArticleURL', 'Title'])
    aer = aer.loc[aer['Title'] != "Front Matter"]
    aer['Date'] = pd.to_datetime(aer['Date'])
    aer['Abstract'] = aer['ArticleURL'].apply(getAbstractAER)
    aer['Journal'] = 'AER'
    aer.dropna(inplace=True)
    return(aer)
