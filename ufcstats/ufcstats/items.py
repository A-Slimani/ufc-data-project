# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UfcstatsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Fighter(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    age = scrapy.Field()
    nickname = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    reach = scrapy.Field()
    stance = scrapy.Field()
    wins = scrapy.Field()
    total_wins_by_ko_tko = scrapy.Field()
    total_wins_by_submission = scrapy.Field()
    total_wins_by_decision = scrapy.Field()
    losses = scrapy.Field()
    total_losses_by_ko_tko = scrapy.Field()
    total_losses_by_submission = scrapy.Field()
    total_losses_by_decision = scrapy.Field()
    draws = scrapy.Field()
    belt = scrapy.Field()
    sherdog_id = scrapy.Field()

class Event(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()

class Fight(scrapy.Item):
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
    fight_weight = scrapy.Field()
    method = scrapy.Field()
    sub_method = scrapy.Field()
    round = scrapy.Field()
    time = scrapy.Field()

class Sherdog_ID(scrapy.Item):
    name = scrapy.Field()
    sherdog_id = scrapy.Field()