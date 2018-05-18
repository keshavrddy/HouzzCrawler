import requests
from config import ConfigSectionMap
from bs4 import BeautifulSoup
import boto3
from boto3.s3.transfer import S3Transfer
import wget
import os
import json
import uuid

cfg_setup = ConfigSectionMap('setup')

class Profile:

    def __init__(self, soup):
        self.soup = soup
        self.name = self.extract_name(self.soup)
        self.user_name = self.extract_username(self.soup)
        self.profile_pic = self.extract_profile_pic(self.soup)
        self.description = self.extract_description(self.soup)
        self.services_provided = self.extract_services_provided(self.soup)
        self.areas_serviced = self.extract_areas_serviced(self.soup)
        self.social_details = self.extract_social_details(self.soup)
        self.profession  = self.extract_profession(self.soup)
        self.contact_details = self.extract_contact_details(self.soup)
        self.followers = self.extract_followers(self.soup)

    def __repr__(self):
        return repr(json.dumps({
            "name": self.name,
            "user_name" : self.user_name,
            "profile_image" : self.profile_pic,
            "description" : self.description,
            "services_provided" : self.services_provided,
            "areas_serviced" : self.areas_serviced,
            "social_details" : self.social_details,
            "profession" : self.profession,
            "contact_details" : self.contact_details,
            "followers" : self.followers
        }))

    def extract_name(self,soup):
        try:
            name = soup.find("div", {"class": "profile-title"}).find("a").text
        except:
            name = ""
        return name

    def extract_username(self,soup):
        try:
            name = soup.find('a', {'class': 'profile-full-name'}).get('href')
            name = name.split('/')[-2]
        except:
            name = ""
        return name

    def extract_profile_pic(self,soup, uu_id):
        try:
            pic = soup.find('img', {'class': 'profile-pic'}).get('src')
            if pic == '':
                pic = ""
            else:
                wget.download(pic, '{}profile.jpeg'.format(uu_id))
                transfer.upload_file('{}profile.jpeg'.format(uu_id), 'housemundynew',
                                     'Images1/{}/{}profile.jpeg'.format(uu_id, uu_id))
                pic = '{}profile.jpeg'.format(uu_id)
                os.remove('{}profile.jpeg'.format(uu_id))
        except:
            pic = ''
        return pic

    def extract_description(self,soup):
        try:
            d = soup.find('div', {'class': 'profile-content-wide about-section'})
            e = d.getText()
            description = e.partition('Services Provided')[0].strip()
            description = description.replace("\n$('.profile-about').peekable();", '')
        except:
            description = ''
        return description.strip()

    def extract_services_provided(self,soup):
        d = soup.find('div', {'class': 'profile-content-wide about-section'})
        try:
            e = d.getText()
            service = e.partition('Services Provided')[2].partition('Areas Served')[0].strip()
            service = service.replace("\n$('.profile-about').peekable();", '')
        except:
            service = ''
        return service

    def extract_areas_serviced(self,soup):
        try:
            d = soup.find('div', {'class': 'profile-content-wide about-section'})
            e = d.getText()
            areas = \
            e.partition('Services Provided')[2].partition('Areas Served')[2].partition('Certifications and Awards')[
                0].strip()
            areas = areas.replace("\n$('.profile-about').peekable();", '')
        except:
            areas = ''
        return areas

    def extract_social_details(self,soup):
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

    def extract_profession(self,soup):
        try:
            pro = soup.find("div", {"class": "info-list-text"}).text.strip()
            pro = pro.replace("\n", "")
            pro = pro.replace("Professionals", "")
        except:
            pro = ""
        return pro

    def extract_contact_details(self,soup):
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

    def extract_followers(self,soup):
        try:
            followers = soup.find("span", {"class": "follow-count"}).text
        except:
            followers = ""
        return followers


class Project:

    def __init__(self, soup):
        self.soup = soup
        self.unique_id = uuid.uuid4().hex
        self.project_urls = self.extract_all_project_urls(self.soup)
        self.project_list = self.getting_projects_list(self.project_urls, self.unique_id)


    def __repr__(self):
        return self.project_list

    def extract_all_project_urls(self,soup):
        website_list = []
        website = soup.find_all("div", {"class": "sidebar-body"})
        for i in website:
            k = i.find_all("a")
            for j in k:
                l = j.get("href")
                if "user" not in l:
                    website_list.append(l)
        return website_list

    def extract_project_url(self,soup):
        try:
            url = soup.find('div', {'class': 'project-section'}).find('a').get('href')
        except:
            url = ""
        return url

    def extract_project_year(self,soup):
        try:
            year = soup.find("div", {"class": "project-year"}).text.split(":")[1].strip()
            if year == "":
                year = ""
        except:
            year = ""
        return year

    def extract_project_cost(self,soup):
        try:
            cost = soup.find("div", {"class": "project-cost"}).text.split(":")[1].strip()
            if cost == "":
                cost = ""
        except:
            cost = ""
        return cost

    def extract_project_country(self,soup):
        try:
            country = soup.find("div", {"class": "project-country"}).text.split(":")[1].strip()
            if country == "":
                country = ""
        except:
            country = ""
        return country

    def extract_project_pincode(self,soup):
        try:
            country = soup.find("div", {"class": "project-zip"}).text.split(":")[1].strip()
            if country == "":
                country = ""
        except:
            country = ""
        return country

    def extract_project_title(self,soup):
        try:
            title = soup.find("h1", {"class": "header-1 top"}).text
        except:
            title = ""
        return title

    def extract_images(self,soup, uniq_id, proj_id):
        img = soup.find_all("div", {"class": "imageArea "})
        image_list = []
        for i in img:
            i = i.find('a').get('href')
            uu_id = uuid.uuid4().hex
            wget.download(i, '{}.jpeg'.format(uu_id))
            image_list.append('{}.jpeg'.format(uu_id))
            transfer.upload_file('{}.jpeg'.format(uu_id), 'housemundynew',
                                 'Images1/{}/{}/{}.jpeg'.format(uniq_id, proj_id, uu_id))
            os.remove('{}.jpeg'.format(uu_id))
        return image_list

    def getting_projects_list(self,list, uniq_id):
        projects = []
        for j, i in enumerate(list):
            proj_id = uuid.uuid4().hex
            proj = {}
            url_requests = requests.request('GET', i, headers=cfg_setup['headers'], proxies=cfg_setup['proxies'])
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


class Data:

    def __init__(self, url):
        self.request_profile = requests.request('GET', url=url, headers=cfg_setup['headers'],
                                                proxies=cfg_setup['proxies'])
        self.soup = BeautifulSoup(self.request_profile.content, 'lxml')
        self.project_url = Project.extract_project_url(self.soup)
        self.profile_data = Profile(self.soup)
        if self.project_url is not '':
            self.request_project = requests.request('GET', url=self.project_url, headers=cfg_setup['headers'],
                                                    proxies=cfg_setup['proxies'])
            self.project_soup = BeautifulSoup(self.request_project.content, 'lxml')
            self.project_data = Project(self.project_soup)
        else:
            self.project_data = ''

    def __repr__(self):
        return repr(json.dumps(
            {
                "Profile" : self.profile_data,
                "Project" : self.project_data
            }
        ))
