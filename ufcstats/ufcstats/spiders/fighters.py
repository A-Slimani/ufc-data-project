from ufcstats.items import FighterItem
import scrapy
import string


class FightersSpider(scrapy.Spider):
    name = "fighters"
    allowed_domains = ["www.ufcstats.com"]
    start_urls = [f"http://www.ufcstats.com/statistics/fighters?page=all&char={char}" for char in string.ascii_lowercase]

    custom_settings = {
        'ITEM_PIPELINES': {
            'ufcstats.pipelines.fighter_pipeline': 300
        }
    }

    def parse(self, response):
        table = response.css("table.b-statistics__table")
        # headers = [header.replace('\n', '').strip() for header in table.css("th::text").getall()]    
        table_rows = table.css("tr.b-statistics__table-row")
        for row in table_rows:
            cells = row.css("td.b-statistics__table-col")
            if len(cells) == 11:
                fighter = FighterItem()
                fighter['first_name'] = cells[0].css("a::text").get()
                fighter['last_name'] = cells[1].css("a::text").get()
                fighter['nickname'] = None if cells[2].css("a::text").get() == ''  else cells[2].css("a::text").get()
                fighter['height'] = None if cells[3].css("::text").get().replace('\n', '').strip() == '--' else cells[3].css("::text").get().replace('\n', '').strip()
                fighter['weight'] = None if cells[4].css("::text").get().replace('\n', '').strip() == '--' else cells[4].css("::text").get().replace('\n', '').strip()
                fighter['reach'] = None if cells[5].css("::text").get().replace('\n', '').strip() == '--' else int(float(cells[5].css("::text").get().replace('\n', '').replace('"', '').strip()))
                fighter['stance'] = None if cells[6].css("::text").get().replace('\n', '').strip() == '--' else cells[6].css("::text").get().replace('\n', '').strip()
                fighter['wins'] = int(cells[7].css("::text").get().replace('\n', '').strip())
                fighter['losses'] = int(cells[8].css("::text").get().replace('\n', '').strip())
                fighter['draws'] = int(cells[9].css("::text").get().replace('\n', '').strip())
                fighter['belt'] = False if cells[10].css("::text").get().replace('\n', '').strip() == '' else True
                yield fighter 

