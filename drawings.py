import fitz
import os
import io
import sys
from PIL import Image
import time






    


dimlimit = 90  # 100  # each image side must be greater than this
relsize = 0.05  # 0.05  # image : image size ratio must be larger than this (5%)
abssize = 7168  # 2048  # absolute image size limit 2 KB: ignore if smaller
imgdir = "ACLTest"  # found images are stored in this subfolder

if not os.path.exists(imgdir):  # make subfolder if necessary
    os.mkdir(imgdir)

def recoverpix(doc, item):
    xref = item[0]  # xref of PDF image
    smask = item[1]  # xref of its /SMask

    # special case: /SMask exists
    # use Pillow to recover original image
    if smask > 0:
        fpx = io.BytesIO(  # BytesIO object from image binary
            doc.extract_image(xref)["image"],
        )
        fps = io.BytesIO(  # BytesIO object from smask binary
            doc.extract_image(smask)["image"],
        )
        img0 = Image.open(fpx)  # Pillow Image
        mask = Image.open(fps)  # Pillow Image
        img = Image.new("RGBA", img0.size)  # prepare result Image
        img.paste(img0, None, mask)  # fill in base image and mask
        bf = io.BytesIO()
        img.save(bf, "png")  # save to BytesIO
        return {  # create dictionary expected by caller
            "ext": "png",
            "colorspace": 3,
            "image": bf.getvalue(),
        }

    # special case: /ColorSpace definition exists
    # to be sure, we convert these cases to RGB PNG images
    if "/ColorSpace" in doc.xref_object(xref, compressed=True):
        pix1 = fitz.Pixmap(doc, xref)
        pix2 = fitz.Pixmap(fitz.csRGB, pix1)
        return {  # create dictionary expected by caller
            "ext": "png",
            "colorspace": 3,
            "image": pix2.getPNGdata(),#("png"),
        }
    return doc.extract_image(xref)


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

os.chdir('./PDFNatureAntibiotics')
papernames = list(os.listdir())
paperdetails = []
papernames = ["9.pdf"]
for papername in papernames:

    #papername="10001.pdf"
    papername = papername.split('.')
    papername = papername[0]
    pdfpath = f"B:\\Nature_Scraping\\{papername}.pdf"
    print(pdfpath)
    try:
        doc = fitz.open(pdfpath)
    except:
        continue
    
    page_count = doc.page_count  # number of pages
    t0 = time.time()
    xreflist = []
    imglist = []
    df = {'Image Location':[],'Fig Caption':[],'Fig Desc.':[]}
    figcapmapper = {}
    textlist = []
    if len(doc) <= 2:
        continue
    for pno in range(len(doc)):
        #pno = 3
        b = doc[pno].get_text("blocks")
        b.sort(key=lambda block: (block[1],block[0]),reverse=True)
        pagelist = []
        il = doc.get_page_images(pno)
        l = doc[pno].getImageList()
        # print(il)
        # print("***")
        # print(l)
        #print(l[0]["image"])
        imglist.extend([x[0] for x in il])
        indexes = []
        for blocks in b:
            pagelist.append(blocks)
        for img in il:
            #print(img)
            xref = img[0]
            if xref in xreflist:
                continue
            width = img[2]
            height = img[3]
            if min(width, height) <= dimlimit:
                continue
            image = recoverpix(doc, img)
            n = image["colorspace"]
            imgdata = image["image"]

            if len(imgdata) <= abssize:
                continue
            if len(imgdata) / (width * height * n) <= relsize:
                continue
            #box = doc[pno].getImageBbox(img)
            image_blocks = [b for b in doc[pno].getText("dict")["blocks"] if b["type"] == 1]  # image blocks
            img = doc.extract_image(img[0])
            for bi in image_blocks:
                if img["image"] == bi["image"]:
                    box = bi["bbox"]
                    break
            
            #print(box)
            
            
            
            idx=-1
            it=0
            print("Blocks:*********************")
            #print(b)
            while it<35:
                    it+=1
                    #print("While")
                    #print(page)
                    #print("Indexes: ",indexes)
                    minVal = 100000
                    #print(prev)
                    for k in range(len(b)):
                        if k not in indexes:
                            #print(b[k][1])
                            if b[k][1] > (box[3]-2):
                                diff = b[k][1]-box[3]
                                if(diff < minVal):
                                    minVal = diff
                                    #print(b[k][4])
                                    idx = k
                      #              print(idx)
                    #print(figcapmapper.keys())
                    try:
                        caption = b[idx][4]
                    except:
                        break
                    print("Caption:", caption)
                    print("************************************")
                    #print(indexes)
                    split = 0
                    z=0
                    for i in range(len(caption)):
                        if caption[i] == "\xa0":
                            split = i+2
                            z=1
                            break
                        if caption[i] == "\n":
                            split = i
                            break
                    #print("i: ",i)
                    figcapt0 = caption[:split]
                    fig0=""
                    if z==1:
                        z=0
                        for c in figcapt0:
                            if c == "\xa0":
                                continue
                            fig0+=c
                        #print(fig0)
                        ch = fig0[len(fig0)-1]
                        fig0 = list(fig0)
                        fig0[len(fig0)-1] = "\xa0"
                        fig0.append(ch)
                        fig0 = "".join(fig0)
                        figcapt0 = fig0
                    figcapt1 = caption[split+1:]
                    #print(figcapt0)
                    #print(figcapt1)
                    print("###########################################3")
                    #print(figcapt0)
                    #print(figcapt1)
                    # figcapt = caption.split(':')
                    
                    if "Fig" not in figcapt0:
                        
                        break

                    try:
                        if figcapt0 in figcapmapper.keys():
                            #print(figcapmapper.keys())
                            #print(indexes)
                            continue
                        else:
                            #print(caption)
                            indexes.append(idx)
                            prev = idx
                            figcapmapper[figcapt0] = figcapt1

                            imgfile = f"B:/Nature_Scraping/ACLTest/{papername}.{figcapt0}.{image['ext']}"
                            print(imgfile)
                            fout = open(imgfile, "wb")
                            fout.write(imgdata)
                            fout.close()
                            xreflist.append(xref)
                            df["Image Location"].append(imgfile)
                            df["Fig Caption"].append(figcapt1)
                            
                            break
                    except:
                        break
        textlist.append(pagelist)

    img = df["Image Location"]
    try:
        figs1=[]
        for i in img:
            s = i.split('/')
            s = s[len(s)-1]
            f = s.split('.')
            f = f[1]+'.'+f[2]
            figs1.append(f)
        print("figs and textlist")
        #print(figs1)
        #print(textlist)

        figs2=[]
        for i in img:
            s = i.split('/')
            s = s[len(s)-1]
            f = s.split('.')
            f = f[1]
            figs2.append(f)
    except:
        continue
    #print(figs2)

    paras = []
    for ep in textlist:
        for i in range(len(ep)):
            l=[]
            text = ep[i][4]
            l.append(text)
            paras.append(l)

    #print("************************Paras*************************")
    #print(paras)


    imgdesc={}
        # print(textlist)
    #print(paras)
    for t in paras:
        text = t[0].lower()
        for fig in figs1:
            fig = fig.lower()
            st = "fig.\xa0"+fig[len(fig)-1]
            #print(st)
            idx = findid(text,fig)
            if fig in text or st in text:
                if fig in imgdesc.keys():
                    imgdesc[fig]+= text
                else:
                    imgdesc[fig] = text
    try:
        for t in paras:
            text = t[0].lower()
            for fig in figs2:
                fig = fig.lower()
                st = "fig.\xa0"+fig[len(fig)-1]
                idx = findid(text,fig)
                if fig in text or st in text:
                    if fig in imgdesc.keys():
                        imgdesc[fig]+= text
                    else:
                        imgdesc[fig] = text
    except:
        continue

    #print("imgdesc: ",imgdesc)
    #print(imgdesc)
    try:
        l = df["Image Location"]
        for loc in l:
            s = loc.split(".")
            try:
                k = s[1] + '.' + s[2]
                k = k.lower()
                desc = imgdesc[k]
            except:
                k = s[1]
                k = k.lower()
                desc = imgdesc[k]
            df["Fig Desc."].append(desc)
    except:
        continue


    print("Dataframe**********************************************************************************")

    #print(df)

    page1 = doc[0]
    abstract = page1.get_text("blocks")
    paper = {'id':papername,'abstract':'','diagrams':[]}
    #print("Abs")
    #print(abstract)
    absidx = 0
    count=0
    for i in range(len(abstract)):
        id = abstract[i][4].find("image")
        if id !=-1:
            continue
        for c in abstract[i][4]:
            if c == "\n":
                count+=1
        if count == 4:
            absidx = i
            break
    #print(absidx)
    try:
        paper['abstract']+=abstract[absidx+1][4] + abstract[absidx+2][4]
        paper['diagrams'].append(df)

        paperdetails.append(paper)
    except:
        continue

    #print(paperdetails)

    t1 = time.time()
    imglist = list(set(imglist))
    print(len(set(imglist)), "images in total")
    print(len(xreflist), "images extracted")
    print("total time %g sec" % (t1 - t0))
#print(paperdetails)
#print(paperdetails)
# import json
# with open("Naturedata.json",'w') as f:
#     json.dump(paperdetails,f)  