from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    url = 'https://www.youtube.com/watch?v=KQ-u4RcFLBY'
    query = urlparse(url)
        ParseResult(scheme='https', netloc='www.youtube.com', path='/watch', params='', query='v=KQ-u4RcFLBY', fragment='')
    """
    query = urlparse(url)
    print(query)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]

    return None
