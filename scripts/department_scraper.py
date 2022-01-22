"""
This Script Scrapes Products from "a" Amazon.in's Movers and Shakers Department
"""
import json

import requests
from bs4 import BeautifulSoup
from retrying import retry

from datatypes.department import Department
from datatypes.product import Product
from scripts.fragments.common_frags import Config, get_html_soup
from scripts.fragments.department_frags import *

# TODO: Make base_url dynamic by extracting directly from requests

def scrape_department(url: str, base_url: str):
    soup = get_html_soup(url)
    product_col = soup.find(id=Config.department["p_col_id"])
    product_tiles = product_col.findAll(class_=Config.department["p_tiles_class"])

    # department
    department = soup.find(class_=Config.department["current_department_class"]).get_text()
    print("\nDepartment:", department)

    # Products
    products = list()

    for tile in product_tiles:
        print()
        # page_rank
        page_rank = extract_page_rank(Config.department["p_page_rank_class"], tile)
        print("Page Rank:", page_rank)

        # title
        title = extract_title(Config.department["p_title_class"], tile)
        print("Title:", title)

        # image
        image = extract_image(tile)
        print("Product Image:", image)

        # link
        link = extract_link(base_url, Config.department["p_link_class"], tile)
        print("Product Link:", link)

        # Rank
        new_rank, old_rank = extract_ranks(Config.department["p_rank_class"], tile)
        print("New Rank:", new_rank)
        print("old Rank:", old_rank)

        # rank_percent
        rank_percent = extract_rank_percent(Config.department["p_rank_percent_class"], tile)
        print("Rank Change:", rank_percent, "%")

        # rating
        rating = extract_rating(Config.department["p_rating_class"], tile)
        print("Rating:", rating)

        # total_ratings
        total_ratings = extract_total_ratings(Config.department["p_total_ratings_css_selector"], tile)
        print("Total Ratings:", total_ratings)

        # price
        price = extract_price(Config.department["p_price_class"], tile)
        print("Price:", price)

        products.append(
            Product(
                page_rank=page_rank,
                title=title,
                image=image,
                new_rank=new_rank,
                old_rank=old_rank,
                rank_percent=rank_percent,
                rating=rating,
                total_ratings=total_ratings,
                link=link,
                price=price
            )
        )

    # Todo: Add Department to some DataBase
    print(Department(department, products))
    try:
        next_page = soup.find(class_=Config.department["next_page_link_class"]).find('a')['href']
        scrape_department(next_page, base_url)
    except Exception as e:
        next_page = None
        print("\nWARNING: Next Page Not Found.\nWarning Details:", e)
