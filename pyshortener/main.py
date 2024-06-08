"""
pyshortener
"""

import json

import requests

def shorten(long_url: str,
            custom_short_url: str = None,
            service: str = "is.gd",
            server_timeout: int = 30,
            log_stats: bool = False):

    """Shortens a URL using the is.gd API.
    
    Parameters:
    
        long_url: The URL to be shortened.

        custom_short_url: The custom short URL to be used. (Optional, defaults to None)

        service: Either 'is.gd' or 'v.gd'. (Optional, defaults to 'is.gd')

        server_timeout: Server timeout in seconds. (Optional, defaults to 30)

        log_stats: Log statistics. (Optional, defaults to False)
    """

    if service not in ["is.gd", "v.gd"]:
        raise ValueError("Invalid service. Choose either 'is.gd' or 'v.gd'.")

    parameters = {
        "url": long_url,
        "shorturl": custom_short_url,
        "logstats": int(log_stats),
        "format": "json"
    }

    shortened_url = requests.get(f"https://{service}/create.php",
                                 params=parameters,
                                 timeout=server_timeout)

    shortened_url = json.loads(shortened_url)

    if "errorcode" in shortened_url:

        if shortened_url["errorcode"] == 1:
            raise LongUrlError(shortened_url["errormessage"])

        elif shortened_url["errorcode"] == 2:
            raise ShortUrlError(shortened_url["errormessage"])

        elif shortened_url["errorcode"] == 3:
            raise RateLimitError(shortened_url["errormessage"])

        elif shortened_url["errorcode"] == 4:
            raise GenericError(shortened_url["errormessage"])

        else:
            raise GenericError(shortened_url["errormessage"])

    else:
        return shortened_url


def expand(short_url: str, service: str = "is.gd", server_timeout: int = 30):
    """Expands a shortened URL using the is.gd API.
    
    Parameters:

        short_url: The shortened URL to be expanded.

        service: Either 'is.gd' or 'v.gd'. (Optional, defaults to 'is.gd')

        server_timeout: Server timeout in seconds. (Optional, defaults to 30)
    """

    parameters = {
        "shorturl": short_url,
        "format": "json"
    }

    expanded_url = requests.get(f"https://{service}/forward.php",
                                params=parameters,
                                timeout=server_timeout)

    expanded_url = json.loads(expanded_url)

    if "errorcode" in expanded_url:

        if expanded_url["errorcode"] == 1:
            raise LongUrlError(expanded_url["errormessage"])

        elif expanded_url["errorcode"] == 2:
            raise ShortUrlError(expanded_url["errormessage"])

        elif expanded_url["errorcode"] == 3:
            raise RateLimitError(expanded_url["errormessage"])

        else:
            raise GenericError(expanded_url["errormessage"])

    else:
        return expanded_url

class LongUrlError(Exception):
    """
    Raised when the long URL is invalid.
    """


class ShortUrlError(Exception):
    """
    Raised when the short URL is invalid.
    """


class RateLimitError(Exception):
    """
    Raised when the rate limit is exceeded.
    """

class GenericError(Exception):
    """
    Raised when an unknown error occurs.
    """
