from bs4.element import PageElement
import requests
from bs4 import BeautifulSoup
import os

link = "https://proceedings.neurips.cc/"
f = requests.get(link,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
html_parse = BeautifulSoup(f.text,'html.parser')
linkscontainer = html_parse.find('div',{'class':'col-sm'})
proceedingslinks = linkscontainer.find_all('a')
count=0
for proceeding in proceedingslinks:
    prolink = "https://proceedings.neurips.cc"+proceeding['href']
    r = requests.get(prolink,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
    proceeding_parse = BeautifulSoup(r.text,'html.parser')
    paper_container = proceeding_parse.find('div',{'class':'col'})
    paper_links = paper_container.find_all('a')
    for paper_link in paper_links:
        print(paper_link)
        paperpagelink = "https://proceedings.neurips.cc"+paper_link['href']
        pagerequest = requests.get(paperpagelink,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        paper_parse = BeautifulSoup(pagerequest.text,'html.parser')
        btnlinks = paper_parse.find_all('a',{'class':'btn'})
        
        for btn in btnlinks:
            print(btn.text)
            if btn.text == "Paper »":
                pdfdownloadlink = "https://proceedings.neurips.cc"+btn['href']
                pdfdwnld = requests.get(pdfdownloadlink)
                with open(f'./PDFNeurIPS/{count}.pdf', 'wb') as f:
                    f.write(pdfdwnld.content)
                count+=1