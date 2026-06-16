# pyjstage2

![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![PyPI version](https://img.shields.io/pypi/v/pyjstage2)

## Overview

[J-STAGE WebAPI](https://www.jstage.jst.go.jp/static/pages/OtherJstageServices/TAB2/-char/ja) Wrapper for Python 3.

- J-STAGE is an electronic journal platform for science and technology information in Japan, developed and managed by the Japan Science and Technology Agency (JST).
- This package is a **Python 3.12 compatible fork** of [pyjstage](https://pypi.org/project/pyjstage/).

## Acknowledgments

This project is modified based on [matsurih/pyjstage](https://github.com/matsurih/pyjstage) (v0.0.2).

Special thanks to the original author [@matsurih](https://github.com/matsurih) for creating this useful J-STAGE API wrapper.

## What's Changed

| Package | Original | Forked |
|---------|----------|--------|
| lxml | 4.4.2 | >=5.0.0 |
| requests | 2.22.0 | >=2.31.0 |
| urllib3 | 1.25.7 | >=2.0.0 |
| certifi | 2019.11.28 | >=2023.0.0 |

- Fixed absolute imports to relative imports
- Fixed private method name mangling (`__finish_setup` → `_finish_setup`)
- Added `__init__.py` export for cleaner imports

## Prerequisites

- Python >= 3.12

## Installation

```shell
$ pip install pyjstage2
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

### v0.1.2 (2026-06-16)

- **Fix**: Null-safe XML parsing in `SearchResult` and `ListResult` — handles missing/empty XML elements without raising `AttributeError`
- **Fix**: `WARN_002` (too many results) is now treated as a warning instead of raising an error, since the API still returns valid data

### v0.1.1 (2026-05-18)

- First PyPI release as `pyjstage2`
- Python 3.12 compatibility
- Updated dependencies (lxml >=5.0, requests >=2.31, urllib3 >=2.0)

## Source Code

https://github.com/lanshi17/pyjstage

## License

MIT License - see [LICENSE](https://github.com/lanshi17/pyjstage/blob/master/LICENSE) file.
