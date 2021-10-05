import os

import requests
from app.scraper.headers import Headers
from bs4 import BeautifulSoup as bs



class Spider:
    
    def __init__(self, seedlist):
        self.seedlist = self.generate_seedlist(seedlist)
        
        
    def generate_seedlist(self, seedlist):
        for seed in seedlist:
            seed["source_seed"] = f"https://www.allmusic.com/search/artists/{seed['Name'].replace(' ','%20').replace('/','%20')}"
        return seedlist

    def run(self):
        try: 
            os.mkdir(os.path.join(os.getcwd(), "downloaded_images"))
        except: pass
        
        for seed in self.seedlist:
            res = requests.get(seed['source_seed'], headers=Headers(os="mac", referer="https://google.com", headers=True).generate())
            soup = bs(res.text, "lxml")
            try:
                image_link = soup.find("ul", {'class': 'search-results'}).find('div', {'class': 'photo'}).find("img")['src']
                img_data = requests.get(image_link).content
                with open(os.path.join(os.getcwd(), "downloaded_images", f"{seed['ArtistId']}.jpg"), 'wb') as dest:
                    dest.write(img_data)
                seed['artist_image'] = image_link
            except:  pass
            soup.decompose()
        
        return self.seedlist