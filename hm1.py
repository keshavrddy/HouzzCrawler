from bs4 import BeautifulSoup
import uuid
import json
import os
import boto3
from boto3.s3.transfer import S3Transfer
import requests
import wget
import ssl
from functools import wraps

def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar
ssl.wrap_socket = sslwrap(ssl.wrap_socket)

proxies = {
    'http': 'socks5://localhost:10003',
    'https': 'socks5://localhost:10003'
}
client = boto3.client(
    's3',
    aws_access_key_id='AWS_ACCESS_KEY',
    aws_secret_access_key='AWS_SECRET'
)

transfer = S3Transfer(client)
ssl._create_default_https_context = ssl._create_unverified_context
os.chdir("/Users/keshavreddy/PersonalProjects/Data/tmp/")
w = open("/Users/keshavreddy/PersonalProjects/Data/HM_Urls/61.txt", "r")
urls = []
w = w.readlines()
headers = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    'upgrade-insecure-requests': "1",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'dnt': "1",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
    'cookie': "v=1511609533_23fe2c3f-9c64-4f05-89b7-b3abff649dbb_db8233aacd464ab06f54d4e43e13875e; prf=listStyle%7C%7D; documentWidth=1280; documentHeight=676; xauth=1511609534; v2=1511609534_2a2c6391-b174-4273-840b-fd41ba22de0c_cf8ac8200249c83dbbcdf4d713e583fc; fstest=8",
    'cache-control': "no-cache"
    }


for j in w:
    k = j.strip().split('<')[0]
    urls.append(k)
print(len(urls))

class Profile:

    def __init__(self):
        self.name =

    def extract_name(soup):
        try:
            name = soup.find("div", {"class": "profile-title"}).find("a").text
        except:
            name = ""
        return name

    
    def extract_username(soup):
        try:
            name = soup.find('a',{'class':'profile-full-name'}).get('href')
            name = name.split('/')[-2]
        except:
            name = ""
        return name

    
    def extract_profile_pic(soup,image_url,uu_id):
        try:
            pic = soup.find('img',{'class':'profile-pic'}).get('src')
            if pic == '':
                pic = ""
            else:
                wget.download(pic, '{}profile.jpeg'.format(uu_id))
                transfer.upload_file('{}profile.jpeg'.format(uu_id), 'housemundynew', 'Images1/{}/{}profile.jpeg'.format(uu_id, uu_id))
                pic = '{}profile.jpeg'.format(uu_id)
                os.remove('{}profile.jpeg'.format(uu_id))
        except:
            pic = ''
        return pic

    
    def extract_description(soup):
        try:
            d = soup.find('div', {'class': 'profile-content-wide about-section'})
            e = d.getText()
            description = e.partition('Services Provided')[0].strip()
            description = description.replace("\n$('.profile-about').peekable();", '')
        except:
            description = ''
        return description.strip()

    
    def extract_services_provided(soup):
        d = soup.find('div', {'class': 'profile-content-wide about-section'})
        try:
            e = d.getText()
            service = e.partition('Services Provided')[2].partition('Areas Served')[0].strip()
            service = service.replace("\n$('.profile-about').peekable();", '')
        except:
            service = ''
        return service

    
    def extract_areas_serviced(soup):
        try:
            d = soup.find('div', {'class': 'profile-content-wide about-section'})
            e = d.getText()
            areas = e.partition('Services Provided')[2].partition('Areas Served')[2].partition('Certifications and Awards')[0].strip()
            areas = areas.replace("\n$('.profile-about').peekable();", '')
        except:
            areas = ''
        return areas

    
    def extract_social_details(soup):
        social = {}
        try:
            f = soup.find('a', {'class': 'sprite-profile-icons f'}).get('href')
            facebook = requests.get(f, headers=headers, proxies=proxies)
            facebook = facebook.url
        except:
            facebook = ''
        social['facebook'] = facebook
        try:
            t = soup.find('a', {'class': 'sprite-profile-icons t'}).get('href')
            twitter = requests.get(t, headers=headers, proxies=proxies)
            twitter = twitter.url
        except:
            twitter = ''
        social['twitter'] = twitter
        try:
            g = soup.find('a', {'class': 'sprite-profile-icons g'}).get('href')
            google = requests.get(g, headers=headers, proxies=proxies)
            google = google.url
        except:
            google = ''
        social['google'] = google
        try:
            l = soup.find('a', {'class': 'sprite-profile-icons l'}).get('href')
            linkedin = requests.get(l, headers=headers, proxies=proxies)
            linkedin = linkedin.url
        except:
            linkedin = ''
        social['linkedin'] = linkedin
        try:
            b = soup.find('a', {'class': 'sprite-profile-icons b'}).get('href')
            blog = requests.get(b, headers=headers, proxies=proxies)
            blog = blog.url
        except:
            blog = ''
        social['blog'] = blog
        return social

    
    def extract_profession(soup):
        try:
            pro = soup.find("div", {"class": "info-list-text"}).text.strip()
            pro = pro.replace("\n", "")
            pro = pro.replace("Professionals", "")
        except:
            pro = ""
        return pro

    
    def extract_contact_details(soup):
        contact_details = {}
        address = ""
        locality = ''
        postal_code = ""
        country = ""
        st = soup.find_all("span", {"itemprop": "streetAddress"})
        if st != []:
            for i in st:
                address = i.get_text()
        else:
            address = ""
        contact_details['address'] = address
        loc = soup.find_all("span", {"itemprop": "addressLocality"})
        try:
            for i in loc:
                locality = i.get_text()
        except:
            locality = ""
        contact_details['locality'] = locality
        pin = soup.find_all("span", {"itemprop": "postalCode"})
        if pin != []:
            for i in pin:
                postal_code = i.get_text()
        else:
            postal_code = ""
        contact_details['pincode'] = postal_code
        place = soup.find_all("span", {"itemprop": "addressCountry"})
        if place != []:
            for i in place:
                country = i.get_text()
        else:
            country = ""
        contact_details['country'] = country
        try:
            contact_number = soup.find("span", {"class": "pro-contact-text"}).text
        except:
            contact_number = ""
        contact_details['phone_number'] = contact_number
        try:
            website = soup.find("a", {"class": "proWebsiteLink"}).get("href")
        except:
            website = ""
        contact_details['website'] = website
        contact_details['email'] = ''
        return contact_details

    
    def extract_followers(soup):
        try:
            followers = soup.find("span", {"class": "follow-count"}).text
        except:
            followers = ""
        return followers

class Project:
    
    def extract_all_project_urls(soup):
        website_list = []
        website = soup.find_all("div", {"class": "sidebar-body"})
        for i in website:
            k = i.find_all("a")
            for j in k:
                l = j.get("href")
                if "user" not in l:
                    website_list.append(l)
        return website_list

    
    def isProject(soup):
        try:
            project = soup.find('div',{'class':'project-section'}).text
        except:
            project = ""
        return project

    
    def extract_project_url(soup):
        try:
            url = soup.find('div', {'class': 'project-section'}).find('a').get('href')
        except:
            url = ""
        return url

    
    def extract_project_year(soup):
        try:
            year = soup.find("div", {"class": "project-year"}).text.split(":")[1].strip()
            if year == "":
                year = ""
        except:
            year = ""
        return year

    
    def extract_project_cost(soup):
        try:
            cost = soup.find("div",{"class":"project-cost"}).text.split(":")[1].strip()
            if cost == "":
                cost = ""
        except:
            cost = ""
        return cost

    
    def extract_project_country(soup):
        try:
            country = soup.find("div",{"class":"project-country"}).text.split(":")[1].strip()
            if country == "":
                country = ""
        except:
            country = ""
        return country

    
    def extract_project_pincode(soup):
        try:
            country = soup.find("div",{"class":"project-zip"}).text.split(":")[1].strip()
            if country == "":
                country = ""
        except:
            country = ""
        return country

    
    def extract_project_title(soup):
        try:
            title = soup.find("h1", {"class": "header-1 top"}).text
        except:
            title = ""
        return title

    
    def extract_images(soup, uniq_id, proj_id):
        img = soup.find_all("div", {"class": "imageArea "})
        image_list = []
        for i in img:
            i = i.find('a').get('href')
            uu_id = uuid.uuid4().hex
            wget.download(i, '{}.jpeg'.format(uu_id))
            image_list.append('{}.jpeg'.format(uu_id))
            transfer.upload_file('{}.jpeg'.format(uu_id), 'housemundynew' , 'Images1/{}/{}/{}.jpeg'.format(uniq_id,proj_id,uu_id))
            os.remove('{}.jpeg'.format(uu_id))
        return image_list

    
    def getting_projects_list(list, mydir, uniq_id):
        projects = []
        for j, i in enumerate(list):
            proj_id = uuid.uuid4().hex
            proj = {}
            url_requests = requests.request('GET', i, headers=headers, proxies=proxies)
            soup = BeautifulSoup(url_requests.content, 'lxml')
            proj['id'] = proj_id
            proj['name'] = Project.extract_project_title(soup)
            proj['description'] = ''
            proj['year'] = Project.extract_project_year(soup)
            proj['cost'] = Project.extract_project_cost(soup)
            proj['country'] = Project.extract_project_country(soup)
            proj['images'] = Project.extract_images(soup, uniq_id, proj_id)
            projects.append(proj)
        return projects


for j,i in enumerate(urls[8052:], start=8052):
    if '/pro/' in i:
        print(i)
        u_id = ''
        u_id = uuid.uuid4().hex
        mydir = os.path.join('/Users/keshavreddy/PersonalProjects/Data/tmp/', u_id)
        os.mkdir(mydir)
        os.chdir(mydir)
        user = {}
        url_requests = requests.request('GET', i, headers=headers, proxies=proxies)
        soup = BeautifulSoup(url_requests.content, 'lxml')
        user['name'] = Profile.extract_name(soup)
        u_name = Profile.extract_username(soup)
        user['username'] = u_name
        user['id'] = str(u_id)
        user['profile_image'] = Profile.extract_profile_pic(soup,mydir,u_id)
        user['description'] = Profile.extract_description(soup)
        user['services_provided'] = Profile.extract_services_provided(soup)
        user['areas_serviced'] = Profile.extract_areas_serviced(soup)
        user['profession'] = Profile.extract_profession(soup)
        user['social_media_details'] = Profile.extract_social_details(soup)
        user['contact_details'] = Profile.extract_contact_details(soup)
        p_url = Project.extract_project_url(soup)
        if p_url is not '':
            url_requests = requests.request('GET', p_url, headers=headers, proxies=proxies)
            soup1 = BeautifulSoup(url_requests.content, 'lxml')
            url_list = Project.extract_all_project_urls(soup1)
            user['projects'] = Project.getting_projects_list(url_list, mydir, u_id)
        else:
            user['projects'] = ''
        print(j)
        f = open('/Users/keshavreddy/PersonalProjects/Data/json/' + str(u_id) + '.json', 'wt')
        f.write(json.dumps(user,ensure_ascii=False))
        f.close()
        transfer.upload_file('/Users/keshavreddy/PersonalProjects/Data/json/' + str(u_id) + '.json', 'housemundynew', 'Json_dump1/{}.json'.format(str(u_id)))
        os.remove('/Users/keshavreddy/PersonalProjects/Data/json/{}.json'.format(str(u_id)))





