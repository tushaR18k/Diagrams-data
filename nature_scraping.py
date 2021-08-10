from bs4.element import PageElement
import requests
from bs4 import BeautifulSoup
import os
import wget
#print(requests.getproxies())

counts = {}
link = "https://www.nature.com/siteindex"
cookies = {"CONTENT_USAGE_SESSIONID":"utterlyidle:v1:MzcwNmJhNGItOTFlMS00NGFjLThlYTctZmI3ZDUxOGEwZTQ3",
          "idp_marker":"1935f168-1e6d-4913-9789-b980ba51b30f","idp_session":"sVERSION_1fdf0b6e3-a32a-4e15-9c7b-461b4795b168",
          "idp_session_http":"hVERSION_114ed3258-3dfe-424a-b13a-5752140407a7","nature-briefing-banner_dismissed":"true",
          "OptanonAlertBoxClosed":"2021-02-14T15:04:25.637Z","OptanonConsent":"isIABGlobal=false&datestamp=Fri+Jul+09+2021+12%3A32%3A30+GMT-0400+(Eastern+Daylight+Time)&version=6.12.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0008%3A1%2CC0009%3A1%2CC0005%3A0%2Cgad%3A0&geolocation=%3B&AwaitingReconsent=false"}
f = requests.get(link,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"},cookies=cookies)
siteindex = BeautifulSoup(f.text,'html.parser')
journals = siteindex.find_all('div',{'class':'border-bottom-1'})
count=19401
for j in range(1):#journals:
    #journalsLink = j.find_all('a')
    for l in range(1):#journalsLink:
    #print(journalsLink)
        l = "/palcomms"
        browseLink = "https://www.nature.com"+l+"/articles"
        print(browseLink)
        #browseLink = "https://www.nature.com/aps/articles?searchType=journalSearch&sort=PubDate&page=167"
        while True:
            
            browseRequest = requests.get(browseLink,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"},cookies=cookies)
            #print(f"link: {browseLink}")
            html_parse = BeautifulSoup(browseRequest.text,'html.parser')
            articles = html_parse.find_all('li',{'class':'app-article-list-row__item'})
            for article in articles:
                pprLink = article.find('a',{'c-card__link'})
                openAccess = article.find('span',{'class':'u-color-open-access'})
                print(openAccess)
                if openAccess and openAccess.text == "Open Access":
                    articleLink = "https://www.nature.com"+pprLink['href']
                    articlerequest = requests.get(articleLink,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"},cookies=cookies)
                    article_parse = BeautifulSoup(articlerequest.text,'html.parser')
                    downloadDiv = article_parse.find('div',{'class':'c-pdf-download'})
                    downloadLink = "https://www.nature.com"+downloadDiv.a['href']
                    
                    try:
                        wget.download(downloadLink,f'./PDFNatureAntibiotics/{count}.pdf')

                    except:
                        continue
                    # pdfdwnld = requests.get(downloadLink,allow_redirects=True)
                    # with open(f'./PDFNatureAntibiotics/{count}.pdf', 'wb') as f:
                    #     f.write(pdfdwnld.content)
                    #os.system('cmd /c "curl {} --output ./PDFNatureAntibiotics/{}.pdf"'.format(downloadLink,count))
                    if l in counts.keys():
                        counts[l] += 1
                    else:
                        counts[l] = 1
                    count+=1
            print(counts)
            nextpage = html_parse.find_all('a',{'class':'c-pagination__link'})
            currentPage = html_parse.find('span',{'class':'c-pagination__link--active'})
            lis = html_parse.find_all('li','c-pagination__item')
            li = lis[len(lis)-2]
            span = li.find('span',{'class':'c-pagination__link--active'})
            last=""
            s = str(currentPage.text)
            s =s.split()
            
            if span:
                last = str(span.text)
                last = last.split()
                #print("Last: {}".format(last))
                #print(last[1])
                #print(int(s[1])== int(last[1]))
                if int(s[1]) == int(last[1]):
                    print("Next Journal: **********************************")
                    break
            nextpageLink = nextpage[len(nextpage)-1]
            #print(nextpageLink)
            browseLink =  "https://www.nature.com"+nextpageLink['href']
            print("Next Page")
            print(browseLink)

print(counts)

