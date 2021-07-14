import requests
from bs4 import BeautifulSoup
import os
link = "https://www.aclweb.org/anthology/"
f = requests.get(link,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
html_parse = BeautifulSoup(f.text,'html.parser')
print(len(html_parse.find_all('table')))
table = html_parse.find_all('table')
table = table[0]
print(len(table.contents))
#print(table.contents[1])
table = table.contents[1]
# print(table.contents[2].find_all('td'))
# td = table.contents[1].find_all('td')
# for t in td:
#     if t.a is not None:
#         print(t.a['href'])
parent_link = "https://www.aclweb.org"
count = 0
for i in range(len(table.contents)-1):
    tds = table.contents[i].find_all('td')
    links = []
    for t in tds:
        if t.a is not None:
            links.append(parent_link+t.a['href'])
            
    for l in links:
        inner_page = requests.get(l,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        html = BeautifulSoup(inner_page.text,'html.parser')
        main_container = html.find('div',id='main-container')
        o = main_container.find_all('span',{"class":'d-block'})
        pdfs = []
        for span in o:
            pdf = span.find_all('a',{'title':"Open PDF"})
            pdfs.append(pdf)
        print(len(pdfs))
        pdfsfinal = []
        for p in pdfs:
            if len(p) != 0:
                pdfsfinal.append(p[0])
        #print(pdfsfinal)
        print(pdfsfinal[0]['href'])
        
        for i in range(len(pdfsfinal)):
            download = pdfsfinal[i]['href']
            splt = download.split('/')
            os.system('cmd /c "curl {} --output ./AllPDF/{}.pdf"'.format(download,count))
            count+=1 


        # pdflinks = []
        # for span in o:
        #     print(span.a.text)
        #     if str(span.a.text) == "pdf":
        #         pdflinks.appen(span.a)
        # print(pdflinks)
        # print(o[])
        #for i in range(2,len)
