from playwright.sync_api import sync_playwright
import pandas as pd
from dataclasses import dataclass, asdict, field

import argparse
import os
import sys

from business_schema import (Business, 
                      BusinessList)

from utils import (extract_business_name, 
    extract_coordinates_from_url, 
    business_locators, 
    data_locators)


def scraper():    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)      # "City Area Type" eg. "Warsaw Ochota Restaurant" (str)
    parser.add_argument("-t", "--total", type=int)       # number of places to scrape (int)
    parser.add_argument("-hb", "--headless", type=bool)   # headless browser (bool)
    args = parser.parse_args()
    
    if args.search:
        search_list = [args.search]
    
    if args.total:
        total = args.total
    else:
        total = 1_000_000
    
    if args.headless:
        headless = args.headless
    else:
        headless = False

    if not args.search:
        search_list = []
        input_file_name = 'input.txt'
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                search_list = file.readlines()
                
        if len(search_list) == 0:
            print('Error occured: You must either pass the -s search argument, or add searches to input.txt')
            sys.exit()
        

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(5000)
        
        for search_for_index, search_for in enumerate(search_list):
            search_for = search_for.strip()
            print(f"-----\n{search_for_index} - {search_for}")

            page.locator(business_locators["searchbox"]).fill(search_for)
            page.wait_for_timeout(3000)

            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            page.hover(business_locators["business_listing"])

            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(3000)

                if page.locator(business_locators["business_listing"]).count() >= total:
                    listings = page.locator(business_locators["business_listing"]).all()[:total]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
                    break
                else:
                    if page.locator(business_locators["business_listing"]).count() == previously_counted:
                        listings = page.locator(business_locators["business_listing"]).all()
                        print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                        break
                    else:
                        previously_counted = page.locator(business_locators["business_listing"]).count()
                        print(f"Currently Scraped: {previously_counted}")

            business_list = BusinessList()

            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(5000)

                    name_attribute = data_locators["name_attribute"]
                    address_xpath = data_locators["address_xpath"]
                    website_xpath = data_locators["website_xpath"]
                    phone_number_xpath = data_locators["phone_number_xpath"]
                    review_count_xpath = data_locators["review_count_xpath"]
                    reviews_average_xpath = data_locators["reviews_average_xpath"]

                    
                    business = Business()
                   
                    if len(listing.get_attribute(name_attribute)) >= 1:
                        business.name = extract_business_name(listing.get_attribute(name_attribute))
                    else:
                        business.name = ""
                    if page.locator(address_xpath).count() > 0:
                        business.address = page.locator(address_xpath).all()[0].inner_text()
                    else:
                        business.address = ""
                    if page.locator(website_xpath).count() > 0:
                        business.website = page.locator(website_xpath).get_attribute('href')
                    else:
                        business.website = ""
                    if page.locator(phone_number_xpath).count() > 0:
                        business.phone_number = page.locator(phone_number_xpath).all()[0].inner_text()
                    else:
                        business.phone_number = ""
                    if page.locator(review_count_xpath).count() > 0:
                        business.reviews_count = str(
                            page.locator(review_count_xpath).inner_text()
                            .split()[0]
                            .replace(',','')
                            .strip()
                        )
                    else:
                        business.reviews_count = ""
                        
                    if page.locator(reviews_average_xpath).count() > 0:
                        business.reviews_average = str(
                            page.locator(reviews_average_xpath).get_attribute(name_attribute)
                            .split()[0]
                            .replace(',','.')
                            .strip())
                    else:
                        business.reviews_average = ""

                    business.google_maps_url = page.url
                    business.city = search_for.split(" ")[0]
                    business.area = search_for.split(" ")[1]
                    
                    business.latitude, business.longitude = extract_coordinates_from_url(page.url)

                    business_list.business_list.append(business)
                    print("finished scraping:", business.name)

                except Exception as e:
                    print(f'Error occured: {e}')
            
            business_list.save_to_csv(f"google_maps_data_{search_for}".replace(' ', '_'))

        browser.close()


if __name__ == "__main__":
    scraper()
