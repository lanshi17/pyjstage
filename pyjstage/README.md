# pyjstage
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/matsurih/pyjstage/Python%20package)
![PyPI version](https://img.shields.io/pypi/v/pyjstage)

## Overview
[J-STAGE WebAPI](https://www.jstage.jst.go.jp/static/pages/OtherJstageServices/TAB2/-char/ja) Wrapper for Python3.
- J-STAGE is an electronic journal platform for science and technology information in Japan, developed and managed by the Japan Science and Technology Agency (JST). 

## Prerequisites
- Python >= 3.6

## Setup
```shell script
$ pip install pyjstage
```

## Usage
You can try this library like this:

```python
from pyjstage.pyjstage import Pyjstage


jstage = Pyjstage()

ret_search = jstage.search(issn='2186-6619', count=1)
ret_list = jstage.list(issn='2186-6619')

# ret_(search/list) is a (Search/List)Result Object.
```

If you need more information, see function-definitions in jstage/jstage.py (Sorry for no documentation... I'll write later.)

## License
- MIT License, see [LICENSE](https://github.com/matsurih/pyjstage/blob/master/LICENSE) file.
