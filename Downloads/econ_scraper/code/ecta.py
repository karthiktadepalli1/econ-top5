import pandas as pd
from bs4 import BeautifulSoup
import requests
from helpers import quickSoup

def getLinksECTA(startYear, endYear):
    """
    Helper that gets a dataframe of links to ECTA articles in the given timeframe.
    startYear: int
        The first year for which ECTA info is requested
    endYear: int
        The last year (inclusive) for which ECTA info is requested
    """
    rootUrl = "https://onlinelibrary.wiley.com/toc/14680262/"
    years = range(startYear, endYear + 1)
    issues = range(1, 7)
    issueMap = {1: '01', 2: '03', 3: '05', 4: '07', 5: '09', 6: '11'}
    linkList = []
    for year in years:
        vol = year - 1932
        for issue in issues:
            url = rootUrl + str(year) + "/" + str(vol) + "/" + str(issue)
            month = issueMap[issue]
            issueDate = str(year) + '-' + month + '-01'
            soup = quickSoup(url)
            all_abs = soup.find_all('a', attrs = {'title': 'Abstract'})
            urls = [a['href'] for a in all_abs]
            dates = [issueDate for i in range(len(urls))]
            compiled = list(zip(dates, urls))
            linkList = linkList + compiled
    ecta_links = pd.DataFrame(linkList, columns = ['Date', 'ArticleURL'])
    ecta_links['ArticleURL'] = ecta_links['ArticleURL'].apply(lambda x: x.replace('/abs/', '/full/'))
    ecta_links['ArticleURL'] = "https://onlinelibrary.wiley.com" + ecta_links['ArticleURL']
    return(ecta_links)



# ECTA pt 2 - abstracts and titles from urls

def getDetailsECTA(url):
    """
    Helper that gets the title and abstract from an ECTA article.
    url: string
        Location of the ECTA article being scraped
    """
    try:
        soup = quickSoup(url)
        abst = soup.find('div', attrs = {'class': 'article-section__content en main'})
        if abst is None:
            return None
        abstText = abst.get_text().strip()
        title = soup.find('h2', attrs = {'class': 'citation__title'}).get_text()
        return (url, title, abstText)
    except Exception as e:
        print(e)
        raise

def getECTA(startYear, endYear):
    """
    Get a dataframe with JPE information in the given time range - specifically all articles with their titles, abstracts, URLs, issue dates.
    startYear: int
        The first year for which JPE info is requested. IMPORTANT: 1988 is the earliest year for which this method successfully returns abstract information.
    endYear: int
        The last year (inclusive) for which JPE info is requested
    """
    ecta_links = getLinksECTA(startYear, endYear)
    details = ecta_links.ArticleURL.apply(getDetailsECTA)
    detsDf = details.apply(pd.Series)
    detsDf.columns = ['ArticleURL', 'Title', 'Abstract']
    ecta = ecta_links.merge(detsDf, on = 'ArticleURL')
    ecta['Journal'] = 'ECTA'
    return(ecta)
