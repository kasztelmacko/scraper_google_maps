from dataclasses import dataclass, field, asdict
import pandas as pd
import os

@dataclass
class Business:
    """
    Represents a business entity with its essential details.

    Attributes:
        name (str): The name of the business.
        address (str): The street address of the business.
        city (str): The city where the business is located.
        area (str): The larger area or region where the business operates.
        website (str): The website URL of the business.
        phone_number (str): The contact phone number of the business.
        reviews_count (str): The total number of reviews for the business.
        reviews_average (str): The average rating of the business based on reviews.
        latitude (float): The latitude of the business location.
        longitude (float): The longitude of the business location.
        google_maps_url (str): The Google Maps URL for the business location.
    """
    name: str = None
    address: str = None
    city: str = None
    area: str = None
    website: str = None
    phone_number: str = None
    reviews_count: str = None
    reviews_average: str = None
    latitude: float = None
    longitude: float = None
    google_maps_url: str = None



@dataclass
class BusinessList:
    """
    Manages a collection of Business objects and provides functionality to save them as a CSV file.

    Attributes:
        business_list (list[Business]): A list of Business objects.
        save_at (str): Directory where the CSV files will be saved. Defaults to 'output'.

    Methods:
        dataframe() -> pd.DataFrame:
            Converts the list of Business objects into a pandas DataFrame.

        save_to_csv(filename: str):
            Saves the DataFrame to a CSV file in the specified directory.
    """
    
    business_list: list[Business] = field(default_factory=list)
    save_at: str = 'output'

    def dataframe(self) -> pd.DataFrame:
        """
        Converts the business_list to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the business data. 
            The keys in the Business dataclass are flattened and separated by underscores in the DataFrame columns.
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_csv(self, filename: str):
        """
        Saves the DataFrame created from the business_list to a CSV file.

        Args:
            filename (str): The name of the CSV file (without the extension).

        Raises:
            OSError: If the directory specified in save_at cannot be created.    
        """
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)
