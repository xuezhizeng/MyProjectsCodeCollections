# Feel free to modify the code in whatever way you like
# 1. The goal is to collect information for all employers and workers (bidders)
# 2. Parse all available information on the webpage, the current identified items may not be complete
# 3. Profile images are very important. Some users may change their profile images. Please also collect their previous images if available
# 4. Save the source code of webpages for future reference, in case that some info are not parsed or incorrectly parsed. 
import requests
import csv
import os
import urllib2
import re
import sys
from bs4 import BeautifulSoup
import time


def read_from_page(uids):
    url = "https://www.freelancer.com/users/"
    f = open('location.csv', mode='w')
    f.writelines('\t'.join(['uid','location'])+'\n')
    #f.writelines('\t'.join(['uid','username','pic','location','membership','user_heading','user_byline','user_desc','verification','top_skills'])+'\n')

    for uid in uids:
        try:
            page = url+uid+".html"
            print(page)
            source_code = requests.get(page)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "lxml")

            username = soup.findAll('div', {'class': 'profile-user-name'})
            # username = username.text
            username = username[0].text
            username = os.linesep.join([s for s in username.strip().splitlines(True) if s.strip("\r\n").strip()])

            location = soup.findAll('span', {'class': 'profile-location-name'})
            location = location[0].text
            location = os.linesep.join([s for s in location.strip().splitlines(True) if s.strip("\r\n").strip()])

            membership = soup.findAll('div', {'class': 'profile-membership-length'})
            membership = membership[0].text
            membership = os.linesep.join([s for s in membership.strip().splitlines(True) if s.strip("\r\n").strip()])
##change

            timeOffset = soup.findAll('span', {'class': 'timeOffset'})
            timeOffset = timeOffset[0].text
            timeOffset = os.linesep.join([s for s in timeOffset.strip().splitlines(True) if s.strip("\r\n").strip()])
            
            primary_language = soup.findAll('span', {'class': 'primary_language'})
            primary_language = primary_language[0].text
            primary_language = os.linesep.join([s for s in primary_language.strip().splitlines(True) if s.strip("\r\n").strip()])

            search_languages = soup.findAll('span', {'class': 'search_languages'})
            search_languages = search_languages[0].text
            search_languages = os.linesep.join([s for s in search_languages.strip().splitlines(True) if s.strip("\r\n").strip()])

            true_location = soup.findAll('span', {'class': 'true_location'})
            true_location = true_location[0].text
            true_location = os.linesep.join([s for s in true_location.strip().splitlines(True) if s.strip("\r\n").strip()])

            city = soup.findAll('span', {'class': 'city'})
            city = city[0].text
            city = os.linesep.join([s for s in city.strip().splitlines(True) if s.strip("\r\n").strip()])

            latitude = soup.findAll('span', {'class': 'latitude'})
            latitude = latitude[0].text
            latitude = os.linesep.join([s for s in latitude.strip().splitlines(True) if s.strip("\r\n").strip()])

            longitude = soup.findAll('span', {'class': 'longitude'})
            longitude = longitude[0].text
            longitude = os.linesep.join([s for s in longitude.strip().splitlines(True) if s.strip("\r\n").strip()])

            vicinity = soup.findAll('span', {'class': 'vicinity'})
            vicinity = vicinity[0].text
            vicinity = os.linesep.join([s for s in vicinity.strip().splitlines(True) if s.strip("\r\n").strip()])
           
            administrative_area = soup.findAll('span', {'class': 'administrative_area'})
            administrative_area = administrative_area[0].text
            administrative_area = os.linesep.join([s for s in administrative_area.strip().splitlines(True) if s.strip("\r\n").strip()])
           
            full_address = soup.findAll('span', {'class': 'full_address'})
            full_address = full_address[0].text
            full_address = os.linesep.join([s for s in full_address.strip().splitlines(True) if s.strip("\r\n").strip()])

            primary_currency = soup.findAll('span', {'class': 'primary_currency'})
            primary_currency = primary_currency[0].text
            primary_currency = os.linesep.join([s for s in primary_currency.strip().splitlines(True) if s.strip("\r\n").strip()])
           

            
###            
            hourly = soup.findAll('span', {'class': 'hourly-rate-value'})
            hourly = hourly[0].text
            hourly = os.linesep.join([s for s in hourly.strip().splitlines(True) if s.strip("\r\n").strip()])

            photo = soup.findAll('img', {'class': 'profile-image-ImageThumbnail-image'})[0]
            photo_url = photo.get('src')
            photo_url = "https:" + photo_url
            if photo_url.find("unknown")==-1:
                photo = requests.get(photo_url)  # read image
                pic = photo.content
            else:
                pic = None

            user_heading = soup.findAll('h1',{'class':'profile-intro-username'})[0].text
            user_heading = os.linesep.join([s for s in user_heading.strip().splitlines(True) if s.strip("\r\n").strip()])

            user_byline = soup.findAll('div',{'class':'profile-user-byline'})[0].text
            user_byline = os.linesep.join([s for s in user_byline.strip().splitlines(True) if s.strip("\r\n").strip()])

            user_desc = soup.findAll('span',{'class':'profile-about-description'})[0].text
            user_desc = os.linesep.join([s for s in user_desc.strip().splitlines(True) if s.strip("\r\n").strip()])

            verificationslist = soup.findAll('li', {'class': 'VerificationsList-item'})
            top_skills = ""
            verifs = []

            for skillrow in verificationslist:
                try:
                    x = skillrow.a.text
                    x = os.linesep.join([s for s in x.strip().splitlines(True) if s.strip("\r\n").strip()])
                    top_skills = x + "," + top_skills
                except:
                    verifs.append(skillrow)
            verification = ""

            for verifrow in verifs:
                check = verifrow.get('class')
                if check[1] == 'is-VerificationsList-verified':
                    temp = verifrow.span.text
                    temp = os.linesep.join([s for s in temp.strip().splitlines(True) if s.strip("\r\n").strip()])
                    verification = temp + "," + verification

            vals = [uid,username,pic,location,membership,user_heading,user_byline,user_desc,verification,top_skills]
            f.writelines('\t'.join([uid, location]) + '\n')
            f.flush()
            time.sleep(1)

        except Exception, e:
            print ("Exception in fetching",e)
            f.flush()
    f.close()


uids = []
with open('user_id00519.csv', 'r') as fr:
    for line in fr: uids.append(line.replace('\n','').replace('\r',''))
read_from_page(uids)







