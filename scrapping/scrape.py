import os
import requests
from bs4 import BeautifulSoup
from scanned import is_scanned
from pdf2txt import extractt_Spdf, extractt_Npdf

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_utils import get_database

def scrape_and_store():
    db = get_database()
    collection = db['legal_pdfs']

    url = 'https://manshurat.org/'
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to access the website")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    links = []
    dropdown = soup.find('li', class_='dropdown')
    if dropdown:
        submenu = dropdown.find('ul', class_='dropdown-menu multi-level')
        if submenu:
            for item in submenu.find_all('li', class_='dropdown-submenu'):
                titles.append(item.a.text.strip())      # Get the main title
                links.append(item.a['href'])            # Get the main link

    # Directory to save PDFs
    scraped_pdfs_dir = os.path.join(r'snd_project\chatbot\scrapping', 'scraped_pdfs')
    os.makedirs(scraped_pdfs_dir, exist_ok=True)

    # Iterate over titles and links to scrape and store data
    for title, link in zip(titles, links):
        sub_folder = os.path.join(scraped_pdfs_dir, title)
        os.makedirs(sub_folder, exist_ok=True)

        sub_url = f'{url}{link[1:]}'
        sub_titles = []
        sub_links = []
        submenu_response = requests.get(sub_url)
        if submenu_response.status_code == 200:
            submenu_soup = BeautifulSoup(submenu_response.content, 'html.parser')

            for sub in submenu_soup.find_all('h2'):
                sub_title = sub.a.text.strip()
                sub_link = sub.a['href']
                sub_titles.append(sub_title)
                sub_links.append(sub_link)

        # Process and store the first 15 PDFs
        for i, (sub_title, sub_link) in enumerate(zip(sub_titles, sub_links[:15])):
            pdf_page_link = f'{url}{sub_link[1:]}'
            response = requests.get(pdf_page_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            pdf_link_tag = soup.find('a', href=True, text='Download')

            if pdf_link_tag and 'href' in pdf_link_tag.attrs:
                pdf_download_link = pdf_link_tag['href']

                if pdf_download_link.startswith('/'):
                    pdf_download_link = f'{url}{pdf_download_link[1:]}'  

                pdf_response = requests.get(pdf_download_link, stream=True)

                # Check if the content is a PDF
                if 'application/pdf' in pdf_response.headers.get('Content-Type', ''):
                    pdf_filename = f'pdf{i}.pdf'
                    pdf_filepath = os.path.join(sub_folder, pdf_filename)

                    # Save the PDF
                    with open(pdf_filepath, 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)

                    # Check if the PDF is scanned or native
                    if is_scanned(pdf_filepath):
                        print(f"Scanned PDF detected: {sub_title}. Skipping storage.")
                    else:
                        pdf_text = extractt_Npdf(pdf_filepath)

                        collection.insert_one({
                            'title': title,
                            'sub_title': sub_title,
                            'sub_link': pdf_page_link,  
                            'pdf_link': pdf_download_link,
                            'pdf_text': pdf_text  
                        })

                else:
                    print(f"No valid PDF found for {sub_title}")
            else:
                print(f"No PDF link found for {sub_title}")

if __name__ == "__main__":
    scrape_and_store()
