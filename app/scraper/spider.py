import os
import time
import requests
from app.scraper.headers import Headers
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import shutil


def get_request(url):
    """
    Function to handle recursively calling requests while changing proxies
    """
    try:
        res = requests.get(url, headers=Headers(os="mac", referer="https://google.com", headers=True).generate())
    except Exception as e:
        print(e)
        return get_request(url)
    return res


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

        with tqdm(total=len(self.seedlist)) as pbar:
            no_image = requests.get('https://st4.depositphotos.com/14953852/22772/v/600/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg').content
            for seed in self.seedlist:
                res = get_request(seed['source_seed'])
                soup = bs(res.text, "lxml")
                time.sleep(1)

                with open(os.path.join(os.getcwd(), "downloaded_images", f"{seed['ArtistId']}.jpg"), 'wb') as dest:
                    try:
                        image_link = soup.find("ul", {'class': 'search-results'}).find('div', {'class': 'photo'}).find("img")['src']
                        seed['artist_image'] = image_link

                    except: seed['artist_image'] = "No Image found"
                    try:
                        if seed['artist_image'] !=  "No Image found":
                            img_data = requests.get(seed['artist_image'], stream = True, headers=Headers(os="mac", referer="https://google.com", headers=True).generate())

                            if img_data.status_code == 200:
                                img_data.raw.decode_content = True
                                shutil.copyfileobj(img_data.raw, dest)
                        else:
                            dest.write(no_image)
                    except Exception as e:
                        print(e)
                        dest.write(no_image)
                pbar.update(1)

        return self.seedlist