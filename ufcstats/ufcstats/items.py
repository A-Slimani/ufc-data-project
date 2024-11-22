# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UfcstatsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FighterItem(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    nickname = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    reach = scrapy.Field()
    stance = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    draws = scrapy.Field()
    belt = scrapy.Field()

class EventItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()

class FightItem(scrapy.Item):
    event_name = scrapy.Field()
    r_fighter = scrapy.Field()
    l_fighter = scrapy.Field()
    r_status = scrapy.Field()
    l_status = scrapy.Field()
    r_knockdowns = scrapy.Field()
    l_knockdowns = scrapy.Field()
    r_significant_strikes = scrapy.Field()
    l_significant_strikes = scrapy.Field()
    r_takedowns = scrapy.Field()
    l_takedowns = scrapy.Field()
    r_submission_attempts = scrapy.Field()
    l_submission_attempts = scrapy.Field()
    weight_class = scrapy.Field()
    method = scrapy.Field()
    sub_method = scrapy.Field()
    round = scrapy.Field()
    time = scrapy.Field()