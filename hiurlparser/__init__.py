import re
import warnings

from hiurlparser.public_suffix_list import PublicSuffixList

public_suffix = PublicSuffixList.get_list()
public_suffix.sort()

DICT_NONE = {
    'protocol': None,
    'sub_domain': None,
    'domain': None,
    'top_domain': None,
    'host': None,
    'port': None,
    'path': None,
    'dir': None,
    'file': None,
    'fragment': None,
    'query': None
}

def _split_query_group(query_groups: list) -> dict:
    result = dict()

    for query_group in query_groups:
        query = query_group.split('=')

        if len(query) == 1:
            result[query[0]] = None
            continue

        result[query[0]] = query[1]

    return result

def _parse_url_with_top_domain(url, top_domain):

    regex = r"^(?:(?P<protocol>[\w\d]+)(?:\:\/\/))?" \
            r"(?P<sub_domain>" \
            r"(?:(?:[\w\d-]+|\.)*?)?" \
            r")(?:\.?)" \
            r"(?P<domain>[^./]+(?=\.))\." \
            r"(?P<top_domain>" + re.escape(top_domain) + r"(?![^/|:?#]))\:?" \
                                                            r"(?P<port>\d+)?" \
                                                            r"(?P<path>" \
                                                            r"(?P<dir>\/(?:[^/\r\n]+(?:/))+)?" \
                                                            r"(?:\/?)(?P<file>[^?#\r\n]+)?)?" \
                                                            r"(?:\#(?P<fragment>[^#?\r\n]*))?" \
                                                            r"(?:\?(?P<query>.*(?=$)))*$"

    dict_data = DICT_NONE.copy()
    match = re.search(regex, url)

    dict_data['protocol'] = match.group('protocol') if match.group('protocol') else None
    dict_data['sub_domain'] = match.group('sub_domain') if match.group('sub_domain') else None
    dict_data['domain'] = match.group('domain')
    dict_data['top_domain'] = top_domain
    dict_data['port'] = match.group('port') if match.group('port') else None
    dict_data['path'] = match.group('path') if match.group('path') else None
    dict_data['dir'] = match.group('dir') if match.group('dir') else None
    dict_data['file'] = match.group('file') if match.group('file') else None
    dict_data['fragment'] = match.group('fragment') if match.group('fragment') else None
    query = match.group('query') if match.group('query') else None

    if query is not None:
        query_groups = query.split('&')
        query = _split_query_group(query_groups)
        dict_data['query'] = query

    return dict_data

def _parse_url_without_top_domain(url):

    regex = r"^(?:(?P<protocol>[\w\d]+)(?:\:\/\/))?" \
            r"(?P<host>\[[:a-fA-F0-9]+\]|(?:\d{1,3}\.){3}\d{1,3}|[-a-zA-Z0-9.]+)" \
            r"\:?(?P<port>\d+)?" \
            r"(?P<path>" \
            r"(?P<dir>\/(?:[^/\r\n]+(?:/))+)?" \
            r"(?:\/?)(?P<file>[^?#\r\n]+)?)?" \
            r"(?:\#(?P<fragment>[^#?\r\n]*))?" \
            r"(?:\?(?P<query>.*(?=$)))*$"

    dict_data = DICT_NONE.copy()
    match = re.search(regex, url)

    if not match:
        return dict_data

    dict_data['protocol'] = match.group('protocol') if match.group('protocol') else None
    dict_data['host'] = match.group('host') if match.group('host') else None
    dict_data['port'] = match.group('port') if match.group('port') else None
    dict_data['path'] = match.group('path') if match.group('path') else None
    dict_data['dir'] = match.group('dir') if match.group('dir') else None
    dict_data['file'] = match.group('file') if match.group('file') else None
    dict_data['fragment'] = match.group('fragment') if match.group('fragment') else None
    query = match.group('query') if match.group('query') else None

    if query is not None:
        query_groups = query.split('&')
        query = _split_query_group(query_groups)
        dict_data['query'] = query

    return dict_data

def _parse_url_with_public_suffix(url):

    domain_regex = re.compile(r"^(.+://)?(?:[^@/\n]+@)?(?P<domain>[^:/#?\n]+)", re.IGNORECASE)
    match = re.search(domain_regex, url)

    if not match:
        return DICT_NONE

    domain = match.group('domain')
    domain_parts = domain.split('.')

    top_domain = None

    for i in range(len(domain_parts)):
        tail_gram = domain_parts[i:len(domain_parts)]
        tail_gram = '.'.join(tail_gram)

        if tail_gram in public_suffix:
            top_domain = tail_gram
            break

    if top_domain:
        data = _parse_url_with_top_domain(url, top_domain)
        host = (data["sub_domain"] + ".") if data["sub_domain"] else ""
        host += data["domain"] + "." + top_domain
        data["host"] = host
        return data
    else:
        return _parse_url_without_top_domain(url)

def get_base_url(url: str) -> str:
    url = parse_url(url)
    protocol = str(url["protocol"]) + '://' if url["protocol"] is not None else 'http://'
    sub_domain = str(url["sub_domain"]) + '.' if url["sub_domain"] is not None else ''
    return protocol + sub_domain + url["domain"] + '.' + url["top_domain"]

def parse_url(url: str) -> dict:
    return _parse_url_with_public_suffix(url)
    

