import re
from urllib.parse import urljoin


def extract_page_rank(p_page_rank_class, tile):
    try:
        page_rank = int(tile.find(class_=p_page_rank_class).get_text().replace('#', ''))
    except Exception as e:
        page_rank = None
        print("Error While Extracting Product Page Rank. Error Details:", e)
    return page_rank


def extract_title(p_title_class, tile):
    try:
        title = ' '.join(tile.find(class_=p_title_class).get_text().split())
    except Exception as e:
        title = None
        print("Error While Extracting Title. Error Details:", e)
    return title


def extract_image(tile):
    try:
        image = tile.find('img')['src']
    except Exception as e:
        image = None
        print("Error While Extracting Product Image. Error Details:", e)
    return image


def extract_link(base_url, p_link_class, tile):
    try:
        link = urljoin(base_url, tile.find(class_=p_link_class)["href"])
    except Exception as e:
        link = None
        print("Error While Extracting Product Link. Error Details:", e)
    return link


def extract_ranks(p_rank_class, tile):
    try:
        rank_details = tile.find(class_=p_rank_class).get_text()
        # #new_rank
        try:
            new_rank = int(re.findall(r'\d+', rank_details)[0])
        except Exception as e:
            new_rank = None
            print("Error While Extracting New Rank. Error Details:", e)

        # #old_rank
        try:
            old_rank = int(re.findall(r'\d+', rank_details)[1])
        except IndexError:
            old_rank = None
        except Exception as e:
            old_rank = None
            print("Error While Extracting Old Rank. Error Details:", e)

    except Exception as e:
        new_rank, old_rank = None, None
        print("Error While Extracting Rank Details. Error Details:", e)
    return new_rank, old_rank


def extract_rank_percent(p_rank_percent_class, tile):
    try:
        rank_percent = percent_to_int(tile.find(class_=p_rank_percent_class).get_text())
    except Exception as e:
        rank_percent = None
        print("Error While Extracting Rank Change. Error Details:", e)
    return rank_percent


def extract_rating(p_rating_class, tile):
    try:
        rating = float(re.findall(r'\d*\.\d+|\d+', tile.find(class_=p_rating_class).get_text())[0])
    except Exception as e:
        rating = None
        print("Error While Extracting Rating. Error Details:", e)
    return rating


def extract_total_ratings(p_total_ratings_css_selector, tile):
    try:
        total_ratings = int(tile.select(p_total_ratings_css_selector)[0].get_text().replace(',', ''))
    except Exception as e:
        total_ratings = None
        print("Error While Extracting Total Ratings. Error Details:", e)
    return total_ratings


def extract_price(p_price_class, tile):
    try:
        price = list(map(float, re.findall(r'\d*\.\d+|\d+',
                                           tile.find(class_=p_price_class).get_text().replace(',', ''))))
    except Exception as e:
        price = None
        print("Error While Extracting Product Price. Error Details:", e)
    return price


def percent_to_int(num_str: str) -> int:
    num = num_str.replace('%', '').replace(',', '')
    try:
        num = int(num)
    except ValueError:
        num = 0
    return num
