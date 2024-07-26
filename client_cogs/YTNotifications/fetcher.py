import re
import requests
import xml.etree.ElementTree as et


def fetch_videos(channel_id: str, num: int):
    channel_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'

    # get request
    r = requests.get(channel_url)

    # generate XML tree
    tree: et.Element = et.fromstring(r.content)

    # xml namespace (I guess?)
    namespace = re.findall(r"\{(.*?)\}", tree.tag)[0]

    # get all entries
    entries = tree.findall("entry", {"": namespace})

    # fetch all videoId's (also lets hope YouTube won't swap something)
    videos = [e[0][1].text for e in zip(entries, range(num))]

    # return videos
    return videos
