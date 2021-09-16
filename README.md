# Python URL Parser
![PyPI - Format](https://img.shields.io/pypi/format/hi-urlparser)
![PyPI - Status](https://img.shields.io/pypi/status/hi-urlparser)
![Downloads](https://pepy.tech/badge/hi-urlparser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hi-urlparser)

A nice package to help you parse all types of URL's in vanilla python and return the parsed URL in groups.

Version 2.1 also included `get_base_url` a small yet neat function to get a the main url back from a string

### Installation
```
pip install hi-urlparser
```

### Usage

```python
from hiurlparser import parse_url, get_base_url


url = parse_url('https://open.prospecta.app/my_user_login?user=hi-urlparser&password=H3ll0') # returns url sections as a dict  
url_object = get_url('https://open.prospecta.app/my_user_login?user=hi-urlparser&password=H3ll0') # Does the same, bur returns a object  
basic_url = get_base_url('https://open.prospecta.app/my_user_login?user=hi-urlparser&password=H3ll0') # Returns just the main url  

print(url['domain']) # Outputs -> prospecta  
print(url_object.domain) # Outputs -> prospecta  
print(basic_url) # Outputs -> https://open.prospecta.app  
```

### Keywords `parse_url`

When using the `parse_url` function, you get a dict back with different parts of the URL.

The different parts can be accessed by keywords:

For `parse_url` use: `result['top_domain]`


Here is a list of all the available keywords:

| Keyword | Desription | Value when not present in URL
| ------ | ------ | ------ |
| protocol | The protocol, e.g. **https** or **ftp** | None
| www | Returns **www** if www is used in the URL | None
| sub_domain | The sub domain, e.g. **my.subdomain** in **my.subdomain.example.com**. Note that the sub domain also includes www. | None
| domain | The domain, e.g. **example** in **example.com** | Is always present
| top_domain | The domain, e.g. **com** in **example.com** | Is always present
| dir | The directory, e.g. **/my/directory/** in **example.com/my/directory/** | None
| file | The file, e.g. **my_file.js** in **example.com/home/my_file.js** | None
| path | The full path, e.g. **/home/my_file.js** in **example.com/home/my_file.js** | None
| fragment | The URL fragment, e.g. **my_link** in **example.com#my_link** | None
| query | The URL query, e.g. **my_parameter=1&foo=bar** in **example.com?my_parameter=1&foo=bar** | None

### Testing

Use the following command to run tests.

```bash
python -m unittest hiurlparser.tests.test_url_parser
```

### Changelog:

See CHANGELOG.md
