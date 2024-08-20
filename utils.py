def extract_coordinates_from_url(url: str) -> tuple[float, float]:
    """
    Extracts latitude and longitude coordinates from a Google Maps URL.

    Args:
        url (str): A Google Maps URL containing coordinates.

    Returns:
        tuple[float, float]: A tuple containing latitude and longitude as floats.
    """
    coordinates = url.split('/@')[-1].split('/')[0]
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

def extract_business_name(name_with_extra: str) -> str:
    """
    Extracts the business name from a string that may contain additional information.

    Args:
        name_with_extra (str): A string containing the business name along with extra data (e.g., 'Business Name · Category').

    Returns:
        str: The clean business name without any extra information.
    """
    if '·' in name_with_extra:
        return name_with_extra.split('·')[0].strip()
    return name_with_extra.strip()


data_locators = {
    'name_attribute': 'aria-label',
    'address_xpath': '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]',
    'website_xpath': '//a[@data-item-id="authority"]',
    'phone_number_xpath': '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]',
    'review_count_xpath': '//button[@jsaction="pane.reviewChart.moreReviews"]//span',
    'reviews_average_xpath': '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]'
}

business_locators = {
    'searchbox': '//input[@id="searchboxinput"]',
    'business_listing': '//a[contains(@href, "https://www.google.com/maps/place")]'
}
