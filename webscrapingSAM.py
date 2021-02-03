from bs4 import BeautifulSoup
import requests
import pandas as pd
import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# --------------------------------------------------------------
url = 'https://scrapartsmusic.com/events'
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
# --------------------------------------------------------------

#testing the conection 
print(page.status_code)  # if answer=200 ->ok

# Searching for a TABLE  with the CLASS....then Find All the tr tags
table = soup.find('table', class_='table-style border-accent').find_all('tr')

# --------------Setting Variables -----------------------------------------
event_date = soup.find_all('span', class_="date")
event_name = soup.find_all('span', class_="name")
event_location = soup.find_all('span', class_="text text-tertiary")

#Creating a List called eventos 
eventos = []

for i in table:
    #getting data from the table
    event_date = i.find_all('span', class_="date")
    event_name = i.find_all('span', class_="text")
    event_location = i.find_all('span', class_="text text-tertiary")

    #if Exist get Text else Set "Not available"
    if event_date:
        event_date_txt = html.unescape(event_date[0].text)
    else:
        event_date_txt = "Not available"
    #if Exist get Text else Set "Not available"
    if event_name:
        event_name_txt = html.unescape(event_name[0].text)
    else:
        event_name_txt = "Not available"
    #if Exist get Text else Set "Not available"
    if event_location:
        event_location_txt = html.unescape(event_location[0].text)
    else:
        event_location_txt = "Not available"

    


    # LINKS -----------------------------------------------------------------
    event_link = soup.find_all('a', class_="event_details no-pjax")
    #print(event_link)
    # print(type(event_link))

    for i in event_link:
        # print all the Href
        event_link_txt= i.get('href', None)
        #print(event_link_txt)

        url = 'https://scrapartsmusic.com/'+event_link_txt
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')


        share_link = soup.find_all('a', class_='button button-tertiary zoogle-share')
        # print(share)

        for i in share_link:
            # print(i.get('href', None), end="\n")
            share_link_txt=i.get('href', None)
            print(share_link_txt)

    eventos.append([event_date_txt, event_name_txt, event_location_txt, share_link_txt])


# Guardamos los datos para el dataframe
df = pd.DataFrame(eventos, columns=["Date", "Event", "Location","Share"])
# print(df.head())

# EXPORTAR >>> a un formato csv
df.to_json('SAM-Events.json', orient="index")
