# pyjstage - Python 3.12 Compatible

![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## Overview

[J-STAGE WebAPI](https://www.jstage.jst.go.jp/static/pages/OtherJstageServices/TAB2/-char/ja) Wrapper for Python 3.

- J-STAGE is an electronic journal platform for science and technology information in Japan, developed and managed by the Japan Science and Technology Agency (JST).
- This fork adds **Python 3.12 support** and updates dependencies to modern versions.

## Acknowledgments

This project is modified based on [matsurih/pyjstage](https://github.com/matsurih/pyjstage) (v0.0.2).

Original PyPI package: [pyjstage 0.0.2](https://pypi.org/project/pyjstage/)

Special thanks to the original author [@matsurih](https://github.com/matsurih) for creating this useful J-STAGE API wrapper.

## What's New in This Fork

### Python 3.12 Compatibility

The original `pyjstage` (v0.0.2) was built for Python 3.6+ and cannot run on Python 3.12 due to:
1. Old `lxml==4.4.2` that fails to compile (removed `longintrepr.h` in Python 3.12)
2. Old `urllib3==1.25.7` incompatible with Python 3.12
3. Absolute imports that break in Python 3.12

This fork fixes all these issues:

| Package | Original | Forked |
|---------|----------|--------|
| lxml | 4.4.2 | >=5.0.0 |
| requests | 2.22.0 | >=2.31.0 |
| urllib3 | 1.25.7 | >=2.0.0 |
| certifi | 2019.11.28 | >=2023.0.0 |

### Code Changes

- **Relative imports**: Changed all absolute imports to relative imports (e.g., `from result import Result` → `from .result import Result`)
- **Private method name mangling**: Fixed `__finish_setup()` → `_finish_setup()` in `Result` class to work with Python 3.12's stricter name mangling
- **Added `__init__.py` export**: Added `from .pyjstage import Pyjstage` for cleaner imports

## Prerequisites

- Python >= 3.12

## Setup

### Using uv (Recommended)

```shell
$ uv sync
```

### Using pip

```shell
$ pip install -e ./pyjstage
```

## Usage

### Basic Usage

```python
from pyjstage.pyjstage import Pyjstage

jstage = Pyjstage()

# Search by ISSN
ret_search = jstage.search(issn='2186-6619', count=3)

# List articles in a journal
ret_list = jstage.list(issn='2186-6619')

# ret_(search/list) is a (Search/List)Result Object.
```

### Accessing Results

```python
for entry in ret_search.entries:
    print(f"Title: {entry.title}")
    print(f"Author: {entry.author.get('ja', '')}")
    print(f"Journal: {entry.material_title.get('ja', '')}")
    print(f"Year: {entry.pubyear}")
    print(f"DOI: {entry.doi}")
    print(f"Link: {entry.link}")
```

### Using Proxy (for restricted networks)

If you're behind a firewall or need a proxy:

```python
from pyjstage.pyjstage import Pyjstage
import requests

# Set proxy
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# Monkey-patch requests to use proxy
original_get = requests.get
def proxied_get(*args, **kwargs):
    kwargs['proxies'] = proxies
    kwargs['timeout'] = 15
    return original_get(*args, **kwargs)

requests.get = proxied_get

jstage = Pyjstage()
result = jstage.search(keyword='人工知能', count=5)
```

### Search Parameters

```python
jstage.search(
    pubyearfrom=2020,      # Search from year
    pubyearto=2024,        # Search to year
    material='journal',    # Journal name contains
    article='title',       # Article title contains
    author='name',         # Author name contains
    keyword='AI',          # Keyword contains
    issn='2186-6619',      # ISSN
    count=10               # Number of results (max 1000)
)
```

## Testing

### Local Data Test (No Network Required)

```shell
$ uv run python test_jstage.py
```

Tests XML parsing with local test data.

### API Test (With Proxy)

```shell
$ uv run python test_api_with_proxy.py
```

Tests real API requests through proxy (default: port 7890).

## Important Notes

### What J-STAGE API Provides

- ✅ **Literature search** - Search by ISSN, keyword, author, year, etc.
- ✅ **Metadata** - Title, author, journal, year, DOI, page numbers
- ✅ **Article links** - Links to J-STAGE article pages

### What J-STAGE API Does NOT Provide

- ❌ **Full-text PDF download** - The API does not provide direct PDF downloads
- ❌ **Full-text content** - The API returns metadata, not full article text

To access full-text content, use the `link` or `doi` fields to visit the publisher's website.

## Changelog

### v0.1.2 (2025-06-16)

- **Fix**: Null-safe XML parsing in `SearchResult` and `ListResult` — handles missing/empty XML elements without raising `AttributeError`
- **Fix**: `WARN_002` (too many results) is now treated as a warning instead of raising an error, since the API still returns valid data

### v0.1.1 (2025-05-18)

- First PyPI release as `pyjstage2`
- Python 3.12 compatibility
- Updated dependencies (lxml >=5.0, requests >=2.31, urllib3 >=2.0)

## License

- MIT License, see [LICENSE](pyjstage/LICENSE) file.
