from ufcstats.items import Event
import datetime
import scrapy


class EventsSpider(scrapy.Spider):
    name = "events"
    allowed_domains = ["www.sherdog.com"]
    start_urls = [
        "https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2"
    ]

    custom_settings = {"ITEM_PIPELINES": {"ufcstats.pipelines.event_pipeline": 400}}

    def parse(self, response):
        event_table = response.css('table[class="new_table event"] tr[onclick]')
        for event in event_table:
            title = event.css('span[itemprop="name"]::text').get()
            if "Road to UFC" in title:  # dont want no Road to UFC events
                continue
            location = event.css('td[itemprop="location"]::text').get()
            date_str = event.css(
                'meta[itemprop="startDate"]::attr(content)'
            ).get()[:10]
            date: datetime.date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            url: str = event.css("a::attr(href)").get()
            event_item = Event(title=title, date=date, location=location, url=url)
            yield event_item
        # hacky way to get all pages
        for page_no in range(1, 10):
            yield response.follow(
                f"https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{page_no}",
                callback=self.parse,
            )
