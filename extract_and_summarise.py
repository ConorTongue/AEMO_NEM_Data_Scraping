import requests
import pandas as pd
import scrapers
import logging
from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile as zipfile
from bs4 import BeautifulSoup
import os


def extract(tables, output_dir):
    # this functions uses the tables defined in main.py, as well as user-defined inputs, to extract relevant data from the downloaded files
    output_dir = "output"
    duid = input("Enter the DUID to extract data for:").strip()
    state = input("Enter the state to extract data for (NSW1, QLD1, SA1, TAS1, VIC1):").strip().upper()
    if state not in ['NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1']:
        print("Invalid state entered. Please enter a valid state code.")
        return  
    print(f"Extracting data for DUID: {duid} and State: {state}")

    for table in tables:
        table_dir = os.path.join(output_dir, table)
        if not os.path.exists(table_dir):
            print(f"No data found for table {table}. Skipping extraction.")
            logging.warning(f"No data found for table {table}. Skipping extraction.")   
            continue
    # Create a directory for filtered results
        filtered_dir = os.path.join(table_dir, 'filtered')
        os.makedirs(filtered_dir, exist_ok=True)
        
        for filename in os.listdir(table_dir):
            if filename.endswith('.zip'):
                file_path = os.path.join(table_dir, filename)
                try:
                    # Extract the zip file
                    with zipfile(file_path) as zf:
                        zf.extractall(table_dir)
                        print(f"Extracted {filename} to {table_dir}")
                        logging.info(f"Extracted {filename} to {table_dir}")
                        
                    # Process each CSV in the extracted files
                    for csv_file in os.listdir(table_dir):
                        if csv_file.endswith('.CSV'):
                            # check if file has already been processed
                            csv_path = os.path.join(table_dir, csv_file)
                            date_str = os.path.splitext(csv_file)[0].split('_')[-1]  # Extract date from filename
                            asset_output_filename = f"{duid}_{table}_{date_str}.csv"
                            asset_output_path = os.path.join(filtered_dir, asset_output_filename)
                            state_output_filename = f"{state}_{table}_{date_str}.csv"
                            state_output_path = os.path.join(filtered_dir, state_output_filename)
                            if (os.path.exists(asset_output_path) or os.path.exists(state_output_path)):
                                print(f"File {csv_file} already processed. Skipping.")
                                logging.info(f"File {csv_file} already processed. Skipping.")
                                continue
                            try:
                                df = pd.read_csv(csv_path, low_memory=False, header=1)
                                # Filter data based on DUID or REGION
                                if 'DUID' in df.columns:
                                    filtered_df = df[df['DUID'] == duid]
                                    if not filtered_df.empty:
                                        # Create sensible output filename
                                        # Save filtered data
                                        filtered_df.to_csv(asset_output_path, index=False)
                                        print(f"Saved filtered data to {asset_output_path}")
                                        logging.info(f"Saved filtered data to {asset_output_path}")

                                elif 'REGIONID' in df.columns:
                                    filtered_df = df[df['REGIONID'] == state]
                                    if not filtered_df.empty:
                                        # Create sensible output filename
                                        # Save filtered data
                                        filtered_df.to_csv(state_output_path, index=False)
                                        print(f"Saved filtered data to {state_output_path}")
                                        logging.info(f"Saved filtered data to {state_output_path}")

                                # Clean up the extracted CSV
                                os.remove(csv_path)
                                
                            except Exception as e:
                                print(f"Failed to process CSV {csv_file}: {e}")
                                logging.error(f"Failed to process CSV {csv_file}: {e}")
                                
                except Exception as e:
                    print(f"Failed to extract {file_path}: {e}")
                    logging.error(f"Failed to extract {file_path}: {e}")
