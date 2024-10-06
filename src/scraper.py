# < 20 lines
from bs4 import BeautifulSoup
import requests
import re
import json 

def get_first_paragraph(wikipedia_url, session):
    print(wikipedia_url)

    #return new soup html for each url
    soup = get_text(wikipedia_url, session)
    paragraphs = soup.find_all("p")
    
    pattern = '<b>(.*)</b>'
    rege = re.compile(pattern)
    for para in paragraphs:
        match = rege.search(str(para))
        if match is not None:
            first_paragaraph = para.text
            break
    print (first_paragaraph)


def get_text(url, session):
   
    r = session.get(url)    
    soup = BeautifulSoup( r.content, "html")    
    #print(soup.prettify())
    return soup


# get_leaders for each country
def get_leaders():
    url = "https://country-leaders.onrender.com"
    status_url = f"{url}/status"
    cookie_url = f"{url}/cookie"
    countries_url = f"{url}/countries"
    leaders_url = f"{url}/leaders"
  
    #create a `Session` object to call all the wikipedia pages
    session = requests.Session()
    
    #get cookie
    req = session.get(cookie_url)
    cookies= req.cookies
   
    #get countries
    req = session.get(countries_url,cookies=cookies)
    countries=req.json()

    
    #Loop in each country and get leaders
    leaders_per_country = {} 
    for country in countries:
        country_param = {'country': f'{country}'}
        req = session.get(leaders_url, params=country_param, cookies=cookies)
        leaders = []
        leaders = req.json() 

        #save leasers for each country into dictionary
        #leaders_per_country = {}
        leaders_per_country[country] = leaders
    
        for leader in leaders:
            try:
                wikipedia_url = leader.get('wikipedia_url')               
                first_paragaraph = get_first_paragraph(wikipedia_url, session)
            except:
                 #get cookie
                req = requests.get(cookie_url)
                cookies= req.cookies
                continue
            print(first_paragaraph)
        
        
    return leaders_per_country


# Call get leaders
leaders_per_country = get_leaders()

for key, value in leaders_per_country.items():
    print(f"{key}: {value}")



def save(leaders_per_country):
    with open("src/leaders.json", 'w') as file:
        json.dump(leaders_per_country, file)

# Call save fn to save all returnd leaders
save(leaders_per_country)