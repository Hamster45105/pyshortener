"""
pyshortener
"""
import csv
import io
import requests

def validate_service(service: str):
    """
    Validates the service parameter
    """
    if service not in ["is.gd", "v.gd"]:
        raise ValueError("Invalid service. Choose either 'is.gd' or 'v.gd'.")

def handle_errors(response_json):
    """
    Handles errors returned by the API
    """
    if "errorcode" in response_json:
        error_message = response_json.get("errormessage", "An error occurred.")
        if response_json["errorcode"] == 1:
            raise LongUrlError(error_message)
        elif response_json["errorcode"] == 2:
            raise ShortUrlError(error_message)
        elif response_json["errorcode"] == 3:
            raise RateLimitError(error_message)
        elif response_json["errorcode"] == 4:
            raise GenericError(error_message)

def shorten(long_url: str,
            custom_short_url: str = None,
            log_stats: bool = False,
            service: str = "is.gd",
            server_timeout: int = 30):
    """
    Shortens a URL using the is.gd/v.gd API.
    
    Parameters:
    
        long_url: The URL to be shortened.

        custom_short_url: The custom short URL to be used. (Optional, defaults to None)

        log_stats: Log statistics. (Optional, defaults to False)

        service: Either 'is.gd' or 'v.gd'. (Optional, defaults to 'is.gd')

        server_timeout: Server timeout in seconds. (Optional, defaults to 30)
    """

    validate_service(service)

    parameters = {
        "url": long_url,
        "shorturl": custom_short_url,
        "logstats": int(log_stats),
        "format": "json"
    }

    try:
        response = requests.get(f"https://{service}/create.php",
                                params=parameters,
                                timeout=server_timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GenericError("An error occurred while making the request.") from exc

    response_json = response.json()
    handle_errors(response_json)

    return response_json["shorturl"]

def expand(short_url: str,
           service: str = "is.gd",
           server_timeout: int = 30):
    """
    Expands a shortened URL using the is.gd/v.gd API.
    
    Parameters:

        short_url: The shortened URL to be expanded.

        service: Either 'is.gd' or 'v.gd'. (Optional, defaults to 'is.gd')

        server_timeout: Server timeout in seconds. (Optional, defaults to 30)
    """

    validate_service(service)

    parameters = {
        "shorturl": short_url,
        "format": "json"
    }

    try:
        response = requests.get(f"https://{service}/forward.php",
                                params=parameters,
                                timeout=server_timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GenericError("An error occurred while making the request.") from exc

    response_json = response.json()
    handle_errors(response_json)

    return response_json["url"]

def get_stats(short_url: str,
              stats_type: str,
              include_title: bool = False,
              format_response: bool = False,
              service: str = "is.gd",
              server_timeout: int = 30):
    """
    Gets statistics for a shortened URL using the is.gd/v.gd API.
    
    Parameters:

        short_url: The shortened URL to get statistics for

        stats_type (str): The type of statistics to retrieve. This can be one of the following:
            - 'hitsweek': Number of hits in the past week.
            - 'hitsmonth': Number of hits in the past month.
            - 'hitsyear': Number of hits in the past year.
            - 'dayofweek': Number of hits by day of the week.
            - 'hourofday': Number of hits by hour of the day.
            - 'country': Number of hits by country.
            - 'browser': Number of hits by browser.
            - 'platform': Number of hits by platform.
        
        format_response: Whether to format the response as a CSV. (Optional, defaults to False)
            
        include_title: Whether to include the title in the CSV output. (Optional, defaults to False)

        service: Either 'is.gd' or 'v.gd'. (Optional, defaults to 'is.gd')

        server_timeout: Server timeout in seconds. (Optional, defaults to 30)
    """

    valid_stats_types = ["hitsweek",
                         "hitsmonth", 
                         "hitsyear", 
                         "dayofweek", 
                         "hourofday", 
                         "country", 
                         "browser", 
                         "platform"]

    if stats_type not in valid_stats_types:
        raise ValueError(f"Invalid stats type. Choose one of the following: {', '.join(valid_stats_types)}.")

    validate_service(service)

    if short_url.startswith(("https://is.gd", "http://is.gd", "https://v.gd", "http://v.gd")):
        short_url = short_url.split("/")[-1]

    parameters = {
        "shorturl": short_url,
        "url": short_url,
        "type": stats_type,
        "format": "json"
    }

    # Check if short URL is valid
    try:
        expand(short_url, service=service)
    except LongUrlError as exc:
        raise GenericError("The short URL provided is invalid.") from exc

    # Make Request
    try:
        response = requests.get(f"https://{service}/graphdata.php",
                                params=parameters,
                                timeout=server_timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GenericError("An error occurred while making the request.") from exc

    # Decode reponse
    try:
        stats = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise StatsDecodeError("An error occurred while decoding the JSON response.") from exc

    if format_response is not True:
        return stats

    # Convert JSON response to CSV format
    output = io.StringIO()
    writer = csv.writer(output)

    # Write title if include_title is True
    if include_title and 'title' in stats.get('p', {}):
        writer.writerow([stats['p']['title']])

    # Write CSV header
    header = [col['label'] for col in stats['cols']]
    writer.writerow(header)

    # Write CSV data
    for row in stats['rows']:
        writer.writerow([cell['v'] for cell in row['c']])

    return output.getvalue()

class LongUrlError(Exception):
    """Raised when there is a problem with the long URL provided"""

class ShortUrlError(Exception):
    """Raised when there was a problem with the short URL provided (for custom short URLs)"""

class RateLimitError(Exception):
    """Raised when the rate limit is exceeded"""

class GenericError(Exception):
    """Raised for generic errors"""

class StatsDecodeError(Exception):
    """Raised when there is an error decoding the stats response"""
