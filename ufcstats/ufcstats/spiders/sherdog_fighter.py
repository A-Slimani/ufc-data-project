from scrapy.spiders.feed import XMLFeedSpider
from scrapy.selector.unified import Selector
from scrapy.exceptions import CloseSpider
from ufcstats.items import Sherdog_ID
from scrapy import Spider


class TestSpider(Spider):
    name = "sherdog_fighter"
    allowed_domains = ["www.sherdog.com"]
    page_number = 1 
    start_urls = [f"https://www.sherdog.com/sitemap-fighters{page_number}.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {"ufcstats.pipelines.sherdog_id_pipeline": 600}
    }

    def parse(self, response):
        selector = Selector(text=response.text)

        urls = selector.xpath("//url/loc/text()").extract()
        if urls == []: 
            raise CloseSpider('No more products to scrape')

        for url in urls:
            item = Sherdog_ID()
            name = url.split("/")[-1].split("-")[:-1]
            name = " ".join(name)
            item["name"] = name
            item["sherdog_id"] = url
            yield item
        
        self.page_number += 1
        next_page = f"https://www.sherdog.com/sitemap-fighters{self.page_number}.xml"
        yield response.follow(next_page, self.parse)
