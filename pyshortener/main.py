"""
pyshortener
"""

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
        if response_json["errorcode"] == 1:
            raise LongUrlError(response_json["errormessage"])
        elif response_json["errorcode"] == 2:
            raise ShortUrlError(response_json["errormessage"])
        elif response_json["errorcode"] == 3:
            raise RateLimitError(response_json["errormessage"])
        elif response_json["errorcode"] == 4:
            raise GenericError(response_json["errormessage"])

def shorten(long_url: str,
            custom_short_url: str = None,
            log_stats: bool = False,
            service: str = "is.gd",
            server_timeout: int = 30):

    """
    Shortens a URL using the is.gd API.
    
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

    shortened_url = requests.get(f"https://{service}/create.php",
                                 params=parameters,
                                 timeout=server_timeout)

    shortened_url = shortened_url.json()

    handle_errors(shortened_url)

    return shortened_url["shorturl"]

def expand(short_url: str, service: str = "is.gd", server_timeout: int = 30):
    """
    Expands a shortened URL using the is.gd API.
    
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

    expanded_url = requests.get(f"https://{service}/forward.php",
                                params=parameters,
                                timeout=server_timeout)

    expanded_url = expanded_url.json()

    handle_errors(expanded_url)

    return expanded_url["url"]

class LongUrlError(Exception):
    """
    Raised when there is a problem with the long URL provided
    """

class ShortUrlError(Exception):
    """
    Raised when there was a problem with the short URL provided (for custom short URLs)
    """

class RateLimitError(Exception):
    """
    Raised when the rate limit is exceeded
    """

class GenericError(Exception):
    """
    Raised when any other error occurs
    """
