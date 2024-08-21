# Google maps business data scraper

The project aim to scrape the business data from the google maps using playwright.



 


## Business data attributes:

 - name (str): The name of the business.
 - address (str): The street address of the business.
 - city (str): The city where the business is located.
 - area (str): The larger area or region where the business operates.
 - website (str): The website URL of the business.
 - phone_number (str): The contact phone number of the business.
 - reviews_count (str): The total number of reviews for the business.
 - reviews_average (str): The average rating of the business based on reviews.
 - latitude (float): The latitude of the business location.
 - longitude (float): The longitude of the business location.
 - google_maps_url (str): The Google Maps URL for the business location.


## Installation


```bash
    pip install -r requirements.txt
    playwright install
```

## Running the project

To run the scraper

```bash
  python main.py
```
with optional arguments:
 - -s="City Area Type" (Optional) 
 - -t=int (Optional) 
 - -hb=bool (Optional)

Or specify "City Area Type" in the input.txt file