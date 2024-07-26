import re
import requests
import xml.etree.ElementTree as et


def fetch_xml(channel_id: str) -> et.Element:
    """
    Returns YouTubes feed XML element
    :param channel_id: channel id
    :return: XML Element
    """

    channel_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'

    # get request
    r = requests.get(channel_url)

    # generate XML tree
    return et.fromstring(r.content)


def fetch_videos(channel_id: str, num: int) -> list[str]:
    """
    Returns a list of N last videos posted on the channel
    :param channel_id: channel id
    :param num: number of videos to fetch (max 20)
    :return: list of video's id's
    """

    # fetch XML tree
    tree = fetch_xml(channel_id)

    # xml namespace (I guess?)
    namespace = re.findall(r"\{(.*?)\}", tree.tag)[0]

    # get all entries
    entries = tree.findall("entry", {"": namespace})

    # fetch all videoId's (also lets hope YouTube won't swap something)
    videos = [e[0][1].text for e in zip(entries, range(num))]

    # return videos
    return videos


def fetch_channel_name(channel_id: str) -> str:
    """
    Returns channel name string.
    :param channel_id: channel id
    :return: channel name
    """

    # fetch XML tree
    tree = fetch_xml(channel_id)

    # xml namespace (I guess?)
    namespace = re.findall(r"\{(.*?)\}", tree.tag)[0]

    # find author tag
    author = tree.find("author", {"": namespace})

    # return channel name
    # zeroth element should be a name, if it's not, oh well
    return author[0].text
