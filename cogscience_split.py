# import PyPDF2

# f = open("C:\\Users\\TushaR\\Downloads\\cogsci20_proceedings_final.pdf",'rb')
# pdfReader = PyPDF2.PdfFileReader(f,strict=False)
# print(pdfReader.numPages)
# page = pdfReader.getPage(16)
# print(page.extractText())

import fitz
#d = fitz.open('./0.pdf')
doc = fitz.open("C:\\Users\\TushaR\\Downloads\\cogsci_23.pdf")
# page = doc[16]
print(len(doc))
# text = page.getText("text")
# s = text.split()

pagenumbers= []
for i in range(14,28): #4,55   #content extraction
    print("Page: ",i+1)
    contentpage = doc[i]
    contenttext = contentpage.getText("text")
    s = contenttext.split()
    for w in s:
        if w.isnumeric():
            pagenumbers.append(int(w))

print(pagenumbers)
from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("C:\\Users\\TushaR\\Downloads\\cogsci_23.pdf", "rb"))
# p = inputpdf.getPage(16)
# #print(p.extractText())
# output = PdfFileWriter()
# output.addPage(inputpdf.getPage(16))
# with open("1.pdf", "wb") as outputStream:
#     output.write(outputStream)
count=8168
for i in range(len(pagenumbers)-1):
    print("hello")
    output = PdfFileWriter()
    startpage = pagenumbers[i]-1+28
    endpage = pagenumbers[i+1]-2+28
    if(endpage < startpage):
        print("*********************************************")
        continue
    try:
        for pagerange in range(startpage,endpage+1):
            output.addPage(inputpdf.getPage(pagerange))
        with open(f"./CogScience/{count}.pdf", "wb") as outputStream:
            output.write(outputStream)
            count+=1
    except:
        continue

# for i in range(inputpdf.numPages):
#     output = PdfFileWriter()
#     output.addPage(inputpdf.getPage(i))
#     with open("document-page%s.pdf" % i, "wb") as outputStream:
#         output.write(outputStream)


# for i in range(len(pagenumbers)-1):
#     startpage = pagenumbers[i]-1
#     endpage = pagenumbers[i+1]-2
#     pdffile = open("0.pdf", "w")
#     pdffile = fitz.open("./0.pdf")
#     pdffile.insertPDF(doc, from_page = startpage, to_page = endpage, start_at = 0)
#     break
    #doc2.save("new-doc-4.pdf")





# print(text)
# for i in range(len(s)-1):
#     w =s[i]
#     if w.isnumeric():
#         pagenum = int(w)
#         startPage = doc[pagenum+71]
#         # page = page2.getText("text")
#         break