# PyShortener Documentation

## Overview

`pyshortener` is a Python module for shortening and expanding URLs using the is.gd and v.gd services.

## Install

You can install `pyshortener` using pip:

```bash
pip install pyshortener
```

## Functions

### `shorten()`

Shortens a URL.

```python
import pyshortener

long_url = "https://www.example.com"

short_url = pyshortener.shorten(long_url, custom_short_url="myshorturl", log_stats=True, service="v.gd", server_timeout=10)
print(short_url)
```

#### Parameters

- `long_url` (str): The URL to be shortened.
- `custom_short_url` (str, optional): The custom short URL to be used. Defaults to None.
- `log_stats` (bool, optional): Log statistics. Defaults to False.
- `service` (str, optional): Either 'is.gd' or 'v.gd'. Defaults to 'is.gd'.
- `server_timeout` (int, optional): Server timeout in seconds. Defaults to 30.

#### Returns

The shortened URL as a string.

### `expand()`

Expands a shortened URL.

```python
import pyshortener

shorturl = "https://is.gd/example"

expanded_url = pyshortener.expand(short_url, service="v.gd", server_timeout=10)
print(expanded)
```

#### Parameters

- `short_url` (str): The shortened URL to be expanded (not including 'is.gd' or 'v.gd')
- `service` (str, optional): Either 'is.gd' or 'v.gd'. Defaults to 'is.gd'.
- `server_timeout` (int, optional): Server timeout in seconds. Defaults to 30.

#### Returns

The expanded URL as a string.

### `get_stats()`

Retrieves statistics for a shortened URL.

```python
import pyshortener

short_url = "example"

stats = pyshortener.get_stats(short_url, stats_type='hitsweek', service="v.gd", server_timeout=10)
print(stats)
```

#### Parameters

- `short_url` (str): The shortened URL to get statistics for.
- `stats_type` (str): The type of statistics to retrieve.
    - 'hitsweek': Number of hits in the past week.
    - 'hitsmonth': Number of hits in the past month.
    - 'hitsyear': Number of hits in the past year.
    - 'dayofweek': Number of hits by day of the week.
    - 'hourofday': Number of hits by hour of the day.
    - 'country': Number of hits by country.
    - 'browser': Number of hits by browser.
    - 'platform': Number of hits by platform.
- `service` (str, optional): Either 'is.gd' or 'v.gd'. Defaults to 'is.gd'.
- `server_timeout` (int, optional): Server timeout in seconds. Defaults to 30.

#### Returns

A dictionary containing the requested statistics.

## Exceptions

- `LongUrlError`: Raised when there is a problem with the long URL provided.
- `ShortUrlError`: Raised when there was a problem with the short URL provided (for custom short URLs).
- `RateLimitError`: Raised when the rate limit is exceeded.
- `GenericError`: Raised when any other error (includes potential problems with the service such as a maintenance period) occurs.
