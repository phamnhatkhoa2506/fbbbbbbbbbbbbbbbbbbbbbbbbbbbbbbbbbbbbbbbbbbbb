import json
import os 
import pytz
import time
from dotenv import load_dotenv
from typing import Any, List
from datetime import datetime

from apify_client import ApifyClient
from google.cloud import storage


# Constants
INPUT_FILEPATH = 'urls.txt'
SOURCE_FILEPATH = 'scraped_data.json'
BUCKET_NAME = "influencer-profile"
MAX_ITEMS = 10

def get_key() -> str:
    '''
        Get key for everyday

        Return:
            The Apify key for that day
    '''

    # Load biến môi trường từ file .env
    load_dotenv()

    # Lấy API key từ biến môi trường
    api_token = os.getenv("APIFY_TOKEN_1")

    return api_token


def load_urls(filepath: str) -> List[str]:
    '''
        Load the urls file and read the urls

        Return:
            The list of urls
    '''

    with open(filepath, 'r') as f:
        urls = f.readlines()

    url_dicts = [
        {
            "url": url
        }
        for url in urls
    ]

    return url_dicts


def save_result(filepath: str, data: List) -> None:
    '''
        Save result to json file
    '''

    # Save to a file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Scraped data saved to {filepath}")


def run_actor(api_token: str, url_dict_list: List) -> List:
    '''
        Run the actor to scrape the facebook pages
    '''

    # Initialize the ApifyClient with your API token
    client = ApifyClient(api_token)

    # Prepare the Actor input
    run_input = {
        "startUrls": url_dict_list,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("4Hv5RhChiaDk6iwad").call(run_input=run_input, max_items=MAX_ITEMS)

    # Fetch results and save to JSON file
    results = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    return results


def upload_to_gcs(bucket_name, source_file_path) -> str:
    '''
        Upload the result to google cloud service
    '''

    client = storage.Client()  # Tạo client
    bucket = client.bucket(bucket_name)  # Lấy bucket

    now = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    year = now.year
    month = now.strftime("%m")
    day = now.strftime("%d")
    time_ = round(time.time())

    destination_blob_path = f'facebook/year={year}/month={month}/day={day}/facebook_page_info_{time_}.json'

    blob = bucket.blob(destination_blob_path)  # Định nghĩa file đích

    blob.upload_from_filename(source_file_path)  # Upload file

    print(f"File {source_file_path} đã được tải lên {bucket_name}/{destination_blob_path}")

    return f'gs://{bucket_name}/{destination_blob_path}'


def crawl_facebook_pages(request: Any) -> None:
    '''
        Crawl facebook pages
    '''

    api_token = get_key()
    url_dicts = load_urls(INPUT_FILEPATH)
    data = run_actor(api_token, url_dicts)
    save_result(SOURCE_FILEPATH, data)
    upload_to_gcs(BUCKET_NAME, SOURCE_FILEPATH)


if __name__ == '__main__':

    api_token = get_key()
    url_dicts = load_urls(INPUT_FILEPATH)
    data = run_actor(api_token, url_dicts)
    save_result(SOURCE_FILEPATH, data)
    upload_to_gcs(BUCKET_NAME, SOURCE_FILEPATH)


