from scripts.department_scraper import scrape_department
from scripts.fragments.common_frags import get_html_soup, Config


def scrape_mns():
    soup = get_html_soup(Config.mns["mns_url"])
    # print(soup)
    mns_department_urls = extract_department_urls(soup, Config.mns["mns_department_ul_id"])

    print("\nUrls to Scrape:")
    sn = 0
    for url in mns_department_urls:
        sn += 1
        print(sn, ":", url)

    sn = 0
    for url in mns_department_urls:
        sn += 1
        print("\nScraping:", sn, url)
        scrape_department(url, Config.mns["base_url"])
        print("\nScraped:", sn, url)


def extract_department_urls(soup, mns_department_ul_id):
    try:
        mns_department_ul = soup.find(id=mns_department_ul_id)
        # print(mns_department_ul)
        mns_department_urls = list(map(lambda x: x['href'], mns_department_ul.find_all('a')))
    except Exception as e:
        print("ERROR: Unable to Scrape Department Urls.\nError Details:", e)
        raise RuntimeError
    return mns_department_urls
