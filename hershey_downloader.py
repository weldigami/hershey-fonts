import os
import requests
from bs4 import BeautifulSoup

def fetch_jhf_files(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    jhf_links = [link['href'] for link in links if link['href'].endswith('.jhf')]
    return jhf_links

def download_file(url, folder):
    local_filename = url.split('/')[-1]
    local_path = os.path.join(folder, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f'Downloaded {local_filename}')
    return local_path

def download_all_jhf_files(main_url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    jhf_links = fetch_jhf_files(main_url)
    for link in jhf_links:
        download_file(link, folder)

if __name__ == '__main__':
    main_url = 'https://emergent.unpythonic.net/software/hershey'
    download_folder = 'fonts/'
    download_all_jhf_files(main_url, download_folder)
    os.remove('fonts/japanese.jhf')
