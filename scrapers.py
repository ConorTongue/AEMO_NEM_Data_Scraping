import requests
import pandas
import logging
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
from zipfile import ZipFile
from io import BytesIO


# This script is used to scrape data from the NEM Web site.
# It constructs a URL based on the specified year and month, retrieves the page,
# and prints the status code of the request.

def scrape_nem_data(table, output_dir):
    print(f"Scraping data for table: {table}")

    # Define the years and months to scrape data for

    years = ['2024']
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    #months = ['01']

    # Loop through each year and month to construct the URL and retrieve data

    for year in years:
        for month in months:
            print("Year: {}, Month: {}".format(year, month))
            base = 'https://www.nemweb.com.au'
            data_archive = '/Data_Archive/Wholesale_Electricity/MMSDM/{}/MMSDM_{}_{}/MMSDM_Historical_Data_SQLLoader/data/'.format(year, year, month)
            url = base + data_archive
            page = requests.get(url)
            if page.status_code == 200:
                print("Successfully connected to AEMO databse for {}/{}".format(year, month))
            else:
                # If the request fails, log the error and skip to the next month
                print("Failed to connect to AEMO databse for {}/{}: Status code {}. Skipping this month.".format(year, month, page.status_code))
                logging.warning(f"Failed to connect to AEMO database for {year}/{month}: Status code {page.status_code}. Skipping this month.")
                continue
            
            # now we begin to scrape the data in earnest
            soup = BeautifulSoup(page.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                filename = os.path.basename(href)
                # Only look for files that match the pattern (filename only)
                if filename.startswith(f'PUBLIC_DVD_{table}') and filename.endswith('.zip'):
                    file_url = base + href  # url already ends with /
                    file_path = os.path.join(output_dir + '/' + f'{table}' + '/' + filename)
                    try:
                        if not os.path.exists(output_dir + '/' + f'{table}'):
                            os.makedirs(output_dir + '/' + f'{table}')
                        urlretrieve(file_url, file_path)
                        logging.info(f"Downloaded {href} to {file_path}")
                    except Exception as e:
                        print(f"Failed to download {file_url}: {e}")
                        logging.warning(f"Failed to download {file_url}: {e}")




