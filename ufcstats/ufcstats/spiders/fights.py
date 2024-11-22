from ufcstats.items import FightItem
import scrapy


class FightsSpider(scrapy.Spider):
    name = "fights"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/events/completed?page=all"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'ufcstats.pipelines.fight_pipeline': 500 
        }
    }

    def parse(self, response):
        fights = response.css("a.b-link.b-link_style_black::attr(href)").getall()
        for fight in fights:
            yield response.follow(url=fight, callback=self.parse_fights)

    def parse_fights(self, response):
        rows = response.css("tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click")
        event_name = response.css("span.b-content__title-highlight::text").get().strip().replace('\n', '') 
        for row in rows:
            fight = FightItem()
            fight['event_name'] = event_name
            names = [name.strip().replace('\n', '') for name in row.css("a.b-link.b-link_style_black::text").getall()]
            fight['r_fighter']= names[0]
            fight['l_fighter']= names[1]

            data = [d.strip().replace('\n', '') for d in row.css("p.b-fight-details__table-text::text").getall()]
            data = [d for d in data if d != '']
            flag = row.css("i.b-flag__text::text").getall()
            if len(flag) == 2:
                # to tackle the case where the fight is a draw or a No contest there is an extra element
                if flag[0] == 'nc':
                    fight['r_status'] = 'NC'
                    fight['l_status'] = 'NC'
                else:
                    fight['r_status'] = 'DRAW'
                    fight['l_status'] = 'DRAW'
            else:
                fight['r_status'] = 'WIN'
                fight['l_status'] = 'LOSS'

            fight['r_knockdowns'] = data[0] if data[0].isdigit() else None
            fight['l_knockdowns'] = data[1] if data[1].isdigit() else None
            fight['r_significant_strikes'] = data[2] if data[2].isdigit() else None
            fight['l_significant_strikes'] = data[3] if data[3].isdigit() else None
            fight['r_takedowns'] = data[4] if data[4].isdigit() else None
            fight['l_takedowns'] = data[5] if data[5].isdigit() else None 
            fight['r_submission_attempts'] = data[6] if data[6].isdigit()  else None
            fight['l_submission_attempts'] = data[7] if data[7].isdigit()  else None 
            fight['weight_class'] = data[8]
            fight['method'] = data[9]
            # this to skip the extra element of Perf. of the night 
            if len(data) == 13:
                fight['sub_method'] = data[10]
                fight['round'] = data[11]
                fight['time'] = data[12]
            else:
                fight['sub_method'] = None
                fight['round'] = data[10]
                fight['time'] = data[11]

            yield fight