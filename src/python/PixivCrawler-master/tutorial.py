import datetime
import os

from pixiv_utils.pixiv_crawler import (
    BookmarkCrawler,
    KeywordCrawler,
    RankingCrawler,
    UserCrawler,
    checkDir,
    displayAllConfig,
    download_config,
    network_config,
    ranking_config,
    user_config,
)


def downloadRanking():
    """
    Download artworks from rankings

    NOTE: Require cookie for R18 images!

    Args:
        capacity (int): flow capacity, default is 1024MB
    """
    user_config.user_id = "93874938"
    user_config.cookie = "first_visit_datetime_pc=2024-06-16%2022%3A10%3A39; p_ab_id=2; p_ab_id_2=6; p_ab_d_id=1051492474; yuid_b=NgVCQw; privacy_policy_notification=0; a_type=0; b_type=1; _ga_MZ1NL4PHH0=GS1.1.1718543449.1.0.1718543452.0.0.0; privacy_policy_agreement=7; login_ever=yes; _gcl_au=1.1.1923493114.1718543972; cc1=2024-07-25%2021%3A09%3A47; cf_clearance=nL7lDEwnNdUe1fr2upoSc.pVhS3rCj3_iv0Ab.egXHI-1721909393-1.0.1.1-7mDvSWrpWAuFZs8Ys4qDwEwWb1ocwIMEzb5gWBO6epLwGPMN1CZ90gR22788YECj2hTzeeasCpyJeISUJhcaew; _gid=GA1.2.796555619.1721909391; PHPSESSID=93874938_cTi3zSHEHCfKTGkR9x5pTi1hXtHznR9o; device_token=d67374ad8993ab82c3f738168586f7d8; c_type=20; _im_vid=01J3MWRQTQKYY08HXBG0E4JYQJ; __cf_bm=VPnqP3LkPzx92r_5K7GExIjLzzzvTs_dQdsxWnxTX6w-1721911229-1.0.1.1-xQkr8Y7512S7HCjmiLmo444aHtTzE3_LXbRXytyjFmHICi760QUEYu0WTJLN_VGpyqF.7L8T2YdEKIh1KGxdTgd4t1QoZRjeRiXV.Ht2Ew8; _ga_75BBYNYN9J=GS1.1.1721909389.2.1.1721911391.0.0.0; _ga=GA1.1.1806556431.1718543440"
    download_config.with_tag = False
    ranking_config.start_date = datetime.date(2024, 5, 1)
    ranking_config.range = 2
    ranking_config.mode = "daily"
    ranking_config.content_mode = "illust"
    ranking_config.num_artwork = 50

    displayAllConfig()
    checkDir(download_config.store_path)

    app = RankingCrawler(capacity=200)
    app.run()


def downloadBookmark():
    """
    Download artworks from bookmark

    NOTE: Require cookie!

    Args:
        n_images (int): max download number, default is 200
        capacity (int): flow capacity, default is 1024MB
    """
    download_config.with_tag = False
    user_config.user_id = "[TODO]: Your user_id here"
    user_config.cookie = "[TODO]: Your cookie here"

    displayAllConfig()
    checkDir(download_config.store_path)

    app = BookmarkCrawler(n_images=20, capacity=200)
    app.run()


def downloadUser():
    """
    Download artworks from a single artist

    NOTE: Require cookie for R18 images!

    Args:
        artist_id (str): artist id
        capacity (int): flow capacity, default is 1024MB
    """
    user_config.user_id = ""
    user_config.cookie = ""
    download_config.with_tag = False

    displayAllConfig()
    checkDir(download_config.store_path)

    app = UserCrawler(artist_id="32548944", capacity=200)
    app.run()


def downloadKeyword():
    """
    Download search results of a keyword (sorted by popularity if order=True)
    Support advanced search, e.g. "(Lucy OR 边缘行者) AND (5000users OR 10000users)", refer to https://www.pixiv.help/hc/en-us/articles/235646387-I-would-like-to-know-how-to-search-for-content-on-pixiv

    NOTE: Require cookie for R18 images!
    NOTE: Require premium account for popularity sorting!

    Args:
        keyword (str): search keyword
        order (bool): order by popularity or not, default is False
        mode (str): content mode, default is "safe", support ["safe", "r18", "all"]
        n_images (int): max download number, default is 200
        capacity (int): flow capacity, default is 1024MB
    """
    user_config.user_id = ""
    user_config.cookie = ""
    download_config.with_tag = False

    displayAllConfig()
    checkDir(download_config.store_path)

    app = KeywordCrawler(
        keyword="(Lucy OR 边缘行者) AND (5000users OR 10000users)",
        order=False,
        mode=["safe", "r18", "all"][-1],
        n_images=20,
        capacity=200,
    )
    app.run()


def loadEnv():
    """
    Load environment variables for proxy, cookie, and user_id
    """
    # Use system proxy settings
    proxy = os.getenv("https_proxy") or os.getenv("HTTPS_PROXY")
    if proxy is not None:
        network_config.proxy["https"] = proxy

    # Use system user_id and cookie
    cookie = os.getenv("PIXIV_COOKIE")
    uid = os.getenv("PIXIV_UID")
    if cookie is not None:
        user_config.cookie = cookie
    if uid is not None:
        user_config.user_id = uid


if __name__ == "__main__":
    # loadEnv()

    downloadRanking()
    downloadBookmark()
    downloadUser()
    downloadKeyword()
