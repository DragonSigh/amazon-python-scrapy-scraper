import json
import scrapy
from urllib.parse import urljoin
import re


class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"

    custom_settings = {
        "FEEDS": {
            "data/%(name)s_%(time)s.xlsx": {
                "format": "xlsx",
            }
        }
    }

    def start_requests(self):
        keyword_list = [
            "Bird Cage Accessories",
            "Bird Cage Bird Baths",
            "Bird Cage Food & Water Dishes",
        ]
        for keyword in keyword_list:
            keyword = keyword.replace("&", "%26").replace(" ", "+")
            amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page=1"
            yield scrapy.Request(
                url=amazon_search_url,
                callback=self.discover_product_urls,
                meta={"keyword": keyword, "page": 1},
            )

    def discover_product_urls(self, response):
        page = response.meta["page"]
        keyword = response.meta["keyword"]

        ## Discover Product URLs
        search_products = response.css(
            "div.s-result-item[data-component-type=s-search-result]"
        )
        if len(search_products) >= 10:
            search_products = search_products[:10]
        for product in search_products:
            relative_url = product.css("h2>a::attr(href)").get()
            # If the link contains '/ref'
            if "/ref" in relative_url:
                # Extract the base URL
                product_url = urljoin(
                    "https://www.amazon.com/", relative_url.split("/ref")[0]
                )
            # If the link contains '/sspa/click?ie'
            elif "/sspa/click?ie" in relative_url:
                # Extract the product ID and clean the URL
                product_id = relative_url.split("%2Fref%")[0]
                clean_url = product_id.replace("%2Fdp%2F", "/dp/")
                urls = clean_url.split("url=%2F")[1]
                product_url = urljoin("https://www.amazon.com/", urls)
            # If the link doesn't contain either '/sspa/click?ie' or '/ref'
            else:
                product_url = urljoin("https://www.amazon.com/", relative_url).split(
                    "?"
                )[0]
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product_data,
                meta={"keyword": keyword, "page": page},
            )

        ## Get All Pages
        # if page == 1:
        #    available_pages = response.xpath(
        #        '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
        #    ).getall()
        #
        #    last_page = available_pages[-1]
        #    for page_num in range(2, int(last_page)):
        #        amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
        #        yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})

    def parse_product_data(self, response):
        # image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
        # variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
        feature_bullets = [
            bullet.strip()
            for bullet in response.css("#feature-bullets li ::text").getall()
        ]
        price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        descriptions = response.xpath(
            "//*[@id='productDescription']/p/span//text()"
        ).getall()
        product_description = " ".join(_ for _ in descriptions)
        if not price:
            price = response.css(".a-price .a-offscreen ::text").get("")
        yield {
            "name": response.css("#productTitle::text").get("").strip(),
            "price": price,
            "stars": response.css("i[data-hook=average-star-rating] ::text")
            .get("")
            .strip(),
            "rating_count": response.css("div[data-hook=total-review-count] ::text")
            .get("")
            .strip(),
            "description": product_description,
            # "description": response.css("#productDescription > p > span ::text").get().strip(),
            "feature_bullets": feature_bullets,
            "url": response.request.url,
            # "images": image_data,
            # "variant_data": variant_data,
        }
