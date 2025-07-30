import requests
import pandas
import scrapers
import logging
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile as zipfile
from bs4 import BeautifulSoup
import os




def main():
    output_dir = "output"
    log_filename = f"nem_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        filename=f"output/{log_filename}",  # Save logs to output folder
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    print("Starting NEM data scraping...")
    # Define the tables to scrape data for
    tables = ['DISPATCHLOAD','DISPATCHPRICE']
    scrapers.scrape_nem_data(tables, output_dir)

if __name__ == "__main__":
    main()