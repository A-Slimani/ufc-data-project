from ufcstats.items import EventItem
import datetime
import scrapy


class EventsSpider(scrapy.Spider):
    name = "events"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/events/completed"] # change to all once pipeline is working

    custom_settings = {
        'ITEM_PIPELINES': {
            'ufcstats.pipelines.event_pipeline': 400
        }
    }

    def parse(self, response):
        table_rows = response.css("tr.b-statistics__table-row")
        for row in table_rows:

            event = EventItem()
            name = row.css('a.b-link.b-link_style_black::text').get()
            date = row.css('span.b-statistics__date::text').get()
            location = row.css('td.b-statistics__table-col.b-statistics__table-col_style_big-top-padding::text').get()

            if name is not None:
                event['name'] = name.strip()
            else:
                continue

            if date is not None:
                event['date'] = datetime.datetime.strptime(date.strip(), '%B %d, %Y').strftime('%Y-%m-%d')
            else:
                continue

            if location is not None:
                event['location'] = location.strip()
            else:
                continue

            yield event
