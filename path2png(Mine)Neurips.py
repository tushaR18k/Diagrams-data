"""
Demo skript: Turn Drawings into PNGs
------------------------------------
Walk through the drawings of a page and join path rectangles, which "touch"
each other.
Create high resolution PNG images for each of the resulting rectangles.

License & Copyright
-------------------
License AGPL 3.0
Copyright (c) 2021, Jorj McKie
"""
import fitz
import os
# page = doc[6]
# for b in page.get_text("blocks"):
#     print(b)

paperdetails = []

def findid(text,fig):
    switcher = {
        0:text.find("we present"),
        1: text.find("as shown in"),    
        2:text.find("is shown in"),
        3:text.find("from"),
        4: text.find("the results are"),
        5: text.find(f"{fig} illustrates"),
        6: text.find(f"{fig} demonstrates"),
        7: text.find(f"{fig} presents the"),
        8: text.find(f"{fig} shows the")
    }

    for i in range(0,9):
        id = switcher.get(i)
        if id!=-1:
            return id
    return -1
os.chdir('../PDFNeurIPS')
papernames = list(os.listdir())
#papernames = ["11","101","20","765","35","589","342","58","1000","5001"]
for papername in papernames:
    papername = papername.split('.')
    papername = papername[0]
    try:
        doc = fitz.open(f"B:\\PDFNeurIPS\\{papername}.pdf")
    except:
        continue
    df = {'Image Location':[],'Fig Caption':[],'Fig Desc.':[]}
    figcapmapper = {}
    textlist = []
    if len(doc) > 30:
        continue
    for page in doc:
        new_rects = []  # resulting rectangles
        pagelist = []

        #page = doc[7]
        #print("Hlelos")
        if len(page.get_drawings())> 200:
            continue
        for p in page.get_drawings():
            #print("Hello")
            #print(p)
            w = p["width"]
            r = p["rect"] + (-w, -w, w, w)  # enlarge each rectangle by width value
            for i in range(len(new_rects)):
                if abs(r & new_rects[i]) > 0:  # touching one of the new rects?
                    new_rects[i] |= r  # enlarge it
                    break
            # now look if contained in one of the new rects
            remainder = [s for s in new_rects if r in s]
            if remainder == []:  # no ==> add this rect to new rects
                new_rects.append(r)
            #print("Loop runing")

        new_rects = list(set(new_rects))  # remove any duplicates
        new_rects.sort(key=lambda r: abs(r), reverse=True)
        remove = []
        # text = page.get_text("text")
        # print(text)
        b = page.get_text("blocks")
        b.sort(key=lambda block: (block[1],block[0]),reverse=True) 
        for blocks in b:
            pagelist.append(blocks)
        # text = page.get_text("text")
        # textlist.append(text)
        for j in range(len(new_rects)):
            for i in range(len(new_rects)):
                if new_rects[j] in new_rects[i] and i != j:
                    remove.append(j)
        remove = list(set(remove))
        #print(new_rects)
        # for i in reversed(remove):
        #     del new_rects[i]
        new_rects.sort(key=lambda r: (r.tl.y, r.tl.x))  # sort by location
        mat = fitz.Matrix(3, 3)  # high resolution matrix
        indexes=[]
        
        for i, r in enumerate(new_rects):
            if r.height <= 90 or r.width <= 90:
                continue  # skip lines and empty rects
            #print(r)
            
            #print(page.number)
            #print(text)
            #print(r.x0)
            #print(r.y0)
            #print(r.x1)
            #print(r.y1)
            idx = -1
            
            #print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJj")
            
            # pix = page.getPixmap(matrix=mat, clip=r)
            # loc = f"./ACLimages/{papername}.png"
            # pix.writePNG(loc)

            prev = -1
            it = 0
            while it < 35:
                it+=1
                #print("While")
                print(page)
                #print("Indexes: ",indexes)
                minVal = 100000
                #print(prev)
                for k in range(len(b)):
                    if k not in indexes:
                        if b[k][1] > (r.y1-2):
                            diff = b[k][1]-r.y1
                            if(diff < minVal):
                                minVal = diff
                                #print(b[k][4])
                                idx = k
                                print(idx)
                print(figcapmapper.keys())
                try:
                    caption = b[idx][4]
                except:
                    break
                #print("Caption:", caption)
                #print("************************************")
                #print(indexes)
                figcapt = caption.split(':')

                if "Fig" not in figcapt[0]:
                    break

                try:
                    if figcapt[0] in figcapmapper.keys():
                        #print(figcapmapper.keys())
                        #print(indexes)
                        continue
                    else:
                        #print(caption)
                        indexes.append(idx)
                        prev = idx
                        figcapmapper[figcapt[0]] = figcapt[1]

                        pix = page.getPixmap(matrix=mat, clip=r)
                        loc = f"B:/Nature_Scraping/NeurIPSimages/{papername}.{figcapt[0]}.png"
                        #print(caption)
                        print(loc)
                        pix.writePNG(loc)
                        df["Image Location"].append(loc)
                        df["Fig Caption"].append(figcapt[1])
                        
                        break
                except:
                    break

                
            

            
            

            # idx=10000
            # ol=-1
            # for i in range(len(text)):
            #     if idx > (r[0]-text[i][0]):
            #         idx = r[0]-text[i][0]
            #         ol = i
            
            # print(text[ol][4])
        textlist.append(pagelist)
            

    #print(df)

    img = df["Image Location"]
    figs=[]
    for i in img:
        s = i.split('/')
        s = s[len(s)-1]
        f = s.split('.')
        f = f[1]
        figs.append(f)

    #print(figs)
    #print(textlist)
    paras = []
    for ep in textlist:
        for i in range(len(ep)):
            l=[]
            text = ep[i][4]
            l.append(text)
            paras.append(l)

    #print("************************Paras*************************")
    #print(paras)

    # for i in range(len(textlist)):
    #     textlist[i] = set(textlist[i])
    imgdesc={}
    # print(textlist)
    for t in paras:
        text = t[0].lower()
        for fig in figs:
            fig = fig.lower()
            idx = findid(text,fig)
            if fig in text:
                if fig in imgdesc.keys():
                    imgdesc[fig]+= text
                else:
                    imgdesc[fig] = text

    # print(imgdesc)

    # print(imgdesc['figure 4'])

    # print(imgdesc['figure 5'])

    l = df["Image Location"]
    for loc in l:
        s = loc.split(".")
        k = s[1]
        k = k.lower()
        desc = imgdesc[k]
        df["Fig Desc."].append(desc)


    #print("Dataframe**********************************************************************************")

    #print(df)

    page1 = doc[0]
    abstract = page1.get_text("blocks")
    paper = {'id':papername,'abstract':'','diagrams':[]}
    #print(abstract)
    for i in range(len(abstract)):
        t = abstract[i][4]
        id = t.find("Abstract")
        try:
            if id!=-1:
                a = abstract[i+1][4]
                paper['abstract']+=a
                paper['diagrams'].append(df)
                break
        except:
            break
        
    paperdetails.append(paper)
    
print(os.getcwd())
#print(paperdetails)
import json
with open("Neuripsdata.json",'w') as f:
    json.dump(paperdetails,f)  
    
# for text in textlist:
    
#     if type(text)!= list:
#         text = text.lower()
#         for fig in figs:
#             fig = fig.lower()
#             s=""
#             idx =  findid(text,fig)  #text.find("as shown in")
#             print("IDX: ",idx)
#             if  idx != -1:
#                 txtContains = text[idx:]
#                 print(fig)
#                 print(txtContains)
#                 if fig in txtContains:
#                     print("Hello")
#                     fullstop = 0
#                     for j in range(len(txtContains)):
#                         s+= txtContains[j]
#                         print(s)
#                         if txtContains[j] == '.':
#                             fullstop+=1
#                         if fullstop > 1:
#                             break
#                 imgdesc[fig] = s
#             print("******************************************************************************")
#             #break
# print(imgdesc)


        
# import re
# figdesc = {'figure 1':''}
# for p in textlist:
#     for i in range(len(p)):
#         str = p[i].lower()
#         if 'we present' in str and 'figure 1' in str:
#             while(i < len(p)):
#                 figdesc['figure 1'] += p[i].lower()
#                 i+=1
            





# for fig in figs:
    
#     for i in range(len(doc)):
#         page = doc[i]
#         b = page.get_text("blocks")
#         for block in b:




