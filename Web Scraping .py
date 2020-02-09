#!/usr/bin/env python
# coding: utf-8

# ###  Step 1: Identify the specialties of the NYC doctor
#         

# In[ ]:


import requests,re
import pandas
from bs4 import BeautifulSoup
import time


# In[ ]:


import pandas as pd


# In[ ]:


def identify_specialities(base_url="https://www.ratemds.com/ny/newyork/"):
    l=[]
    specialities=[]
    base_url=base_url
    burl=requests.get(base_url)
    cont=burl.content
    basesoup=BeautifulSoup(cont,"html.parser")
    for ul in basesoup.findAll('ul', class_='nav home-specialties-nav hidden-xs'):
        for link in ul.findAll("li"):
            try:
                ngattr= link.attrs["ng-class"]
                spec = ngattr.split("==")[1].replace('}','').replace("'","")
            except:
                spec=None
            specialities.append(spec)
    specialities.remove(None)
    return(specialities)      


# In[ ]:


specialities=identify_specialities(base_url="https://www.ratemds.com/ny/newyork/")


# In[ ]:


specialities


# In[ ]:


l=[]
pages = [10,10,10,10,10,10,10,10,10,10,10,10,10]
base_url_start="https://www.ratemds.com/best-doctors/ny/new-york/"
base_url_end="/?page="
for speciality,page in zip(specialities, pages):
    for p in range(1, page+1, 1):
        print(base_url_start + speciality + base_url_end + str(p))
        r=requests.get(base_url_start + speciality+base_url_end + str(p))
        c=r.content
        soup=BeautifulSoup(c,"html.parser")
        all=soup.find_all("div",{"class":"search-item doctor-profile"})
        for item in all:
            d={}
            try:
                d["Name"]=item.find("a",{"class":"search-item-doctor-link"}).text.replace("\n","")
            except:
                d["Name"]=None
            try:
                d["Link"]= "ratemds.com" + item.find("a",{"class":"search-item-doctor-link"}).attrs["href"]
            except:
                d["Link"]=None
            try:
                d["Speciality"]=item.find("div",{"class":"search-item-specialty"}).text.replace("\n","")
            except:
                d["Speciality"]=None
            try:
                d["Rating"]=item.find("span",{"class":"star-rating"}).attrs["title"]
            except:
                d["Rating"]=None
            try:
                d["Reviews Count"]=item.find("div",{"class":"star-rating-count"}).text.split()[0]
            except:
                d["Reviews Count"]=None
            try:
                d["Comment"]=item.find("p",{"class":"rating-comment"}).text

            except:
                d["Comment"]=None
            l.append(d)


# In[ ]:


df=pd.DataFrame(l)


# In[ ]:


df_new=df.drop_duplicates()


# In[ ]:


df_new.to_csv("all_specialities.csv")


# In[ ]:


import requests,re
import pandas as pd
from bs4 import BeautifulSoup
import time
import math


# ### Step 2: Create dataframe for doctors that scapped online

# In[ ]:


#Final code to extract list of all reviews in each doctor's page

staff_value = []
punctuality_value = []
helpfulness_value = []
knowledge_value = []
star_rating = []
l = []
links = []
name = []
spec = []
star_rating = []
comment = []
rating_usefulness = []
review_date = []

#you can either read from the csv created from the previous step or use the df directly
#df = pd.read_csv(r'ratemd_all_specialities.csv', encoding='utf8')

rows, col = df_new.shape

base_url_start = str("https://www.")

#Looping each doctor's link in df
for i in range(rows):
    k = i+1
    print('Doctor '+ str(k) +' is getting scraped')
    base_url = str(df.iloc[i]['Link'])
    base_url1 = str("?page=")
    
    reviews = int(df.iloc[i]['Reviews Count'])
#Extracting the number of pages for each doctor based on the number of reviews
    page_no = math.ceil(reviews/10)

    page_no += 1
#Looping over each page of each doctor in the outer loop    
    for j in range(1, page_no):
        base_url2 = str(j)
        doc_url = base_url_start + base_url + base_url1 + base_url2

        durl=requests.get(doc_url)
        dcont=durl.content
        docsoup=BeautifulSoup(dcont,"html.parser")

        alldoc = docsoup.find_all("div", class_="col-sm-7".split())
#Looping over all the div elements of class "col-sm-7" in that particular page        
        for el in alldoc:
            all_rating=el.get_text()
            links.append(doc_url)
            name.append(df.iloc[i]['Name'])
            spec.append(df.iloc[i]['Speciality'])
            try:
                staff_value.append(int(all_rating.split()[0][0]))
            except ValueError:
                staff_value.append(int(0))
            try:
                punctuality_value.append(int(all_rating.split()[1][0]))
            except ValueError:
                punctuality_value.append(int(0))
            try:
                helpfulness_value.append(int(all_rating.split()[2][0]))
            except ValueError:
                helpfulness_value.append(int(0))
            try:
                knowledge_value.append(int(all_rating.split()[3][0]))
            except ValueError:           
                knowledge_value.append(int(0))
#Looping over all the div elements of class "rating" in that particular page 
        all_star_rating=docsoup.find_all("div",{"class":"rating"})
        for item in all_star_rating:
            try:
                star_rating.append(item.find("span",{"class":"star-rating"}).attrs["title"])
            except:
                star_rating.append(0)
            try:
                comment.append(item.find("p",{"itemprop":"reviewBody"}).text)
            except:
                comment.append('NA')
            try:
                rating_usefulness.append(item.find("p",{"class":"rating-comment-votes pull-left"}).text.split()[4:])
            except:
                rating_usefulness.append(0)
            try:
                review_date.append(item.find("p",{"class":"rating-comment-created pull-right"}).text.split()[3:])
            except:
                review_date.append('NA')
        print(len(name), len(spec), len(star_rating), len(staff_value), len(punctuality_value), len(helpfulness_value),len(knowledge_value), len(comment), len(review_date), len(links))

d ={'Name': name, 'Speciality' : spec, 'Star Rating': star_rating, 'Staff': staff_value, 'Punctuality': punctuality_value, 'Helpfulness': helpfulness_value,'Knowledge': knowledge_value, 'comment': comment,'Rating Usefulness' : rating_usefulness, 'Review Date': review_date,'Link': links}


# In[ ]:


d.keys()


# In[ ]:


print(len(d['Name']), len(d['Speciality']), len(d['Star Rating']))


# In[ ]:


### data set for all reviews 
k=list(d.keys())
v=list(d.values())


# In[ ]:


df_all=df = pd.DataFrame(d)


# In[ ]:


df_all.to_csv(r'review_dataset.csv', encoding='utf8')

