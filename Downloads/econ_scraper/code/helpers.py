

def quickSoup(url):
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = requests.get(url, headers=header, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')
        return(soup)
    except Exception as e:
        print(e)
        return(None)

def quickDriver():
    chrome_opts = Options()
    chrome_opts.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_opts)
    return(driver)
