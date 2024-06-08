# PyShortener Documentation

## Overview

`pyshortener` is a Python module for shortening and expanding URLs using the is.gd and v.gd services.

## Functions

### `shorten()`

Shortens a URL.

#### Parameters

- `long_url` (str): The URL to be shortened.
- `custom_short_url` (str, optional): The custom short URL to be used. Defaults to None.
- `service` (str, optional): Either 'is.gd' or 'v.gd'. Defaults to 'is.gd'.
- `server_timeout` (int, optional): Server timeout in seconds. Defaults to 30.
- `log_stats` (bool, optional): Log statistics. Defaults to False.

#### Returns

The shortened URL as a string.

### `expand()`

Expands a shortened URL.

#### Parameters

- `short_url` (str): The shortened URL to be expanded.
- `service` (str, optional): Either 'is.gd' or 'v.gd'. Defaults to 'is.gd'.
- `server_timeout` (int, optional): Server timeout in seconds. Defaults to 30.

#### Returns

The expanded URL as a string.

## Exceptions

- `LongUrlError`: Raised when there is a problem with the long URL provided.
- `ShortUrlError`: Raised when there was a problem with the short URL provided (for custom short URLs).
- `RateLimitError`: Raised when the rate limit is exceeded.
- `GenericError`: Raised when any other error (includes potential problems with the service such as a maintenance period) occurs.
