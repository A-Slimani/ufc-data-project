from ufcstats.items import Fighter
from ufcstats.models import SherdogIds
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import scrapy
import string
import os


class FightersSpider(scrapy.Spider):
    name = "fighters_all"
    allowed_domains = ["www.ufcstats.com"]
    start_urls = [
        f"http://www.ufcstats.com/statistics/fighters?page=all&char={char}"
        for char in string.ascii_lowercase
    ]

    custom_settings = {
        "ITEM_PIPELINES": {"ufcstats.pipelines.fighter_pipeline": 300},
        "DUPEFILTER_CLASS": "scrapy.dupefilters.BaseDupeFilter",
    }


    def data_strip(self, data, type):
        if type == str:
            return (
                None
                if data.css("::text").get().replace("\n", "").strip() == "--"
                else type(data.css("::text").get().replace("\n", "").strip())
            )
        elif type == int:
            return (
                None
                if data.css("::text").get().replace("\n", "").strip() == "--"
                else int(
                    float(
                        data.css("::text")
                        .get()
                        .replace("\n", "")
                        .replace('"', "")
                        .strip()
                    )
                )
            )

    def parse(self, response):
        table = response.css("table.b-statistics__table")
        table_rows = table.css("tr.b-statistics__table-row")
        for row in table_rows:
            cells = row.css("td.b-statistics__table-col")
            if len(cells) == 11:
                fighter = Fighter()
                fighter["first_name"] = cells[0].css("a::text").get()
                fighter["last_name"] = cells[1].css("a::text").get()
                fighter["nickname"] = (
                    None
                    if cells[2].css("a::text").get() == ""
                    else cells[2].css("a::text").get()
                )
                fighter["height"] = self.data_strip(cells[3], str)
                fighter["weight"] = self.data_strip(cells[4], str)
                fighter["reach"] = self.data_strip(cells[5], int)
                fighter["stance"] = self.data_strip(cells[6], str)
                fighter["wins"] = int(
                    cells[7].css("::text").get().replace("\n", "").strip()
                )
                fighter["losses"] = int(
                    cells[8].css("::text").get().replace("\n", "").strip()
                )
                fighter["draws"] = int(
                    cells[9].css("::text").get().replace("\n", "").strip()
                )
                fighter["belt"] = (
                    False
                    if cells[10].css("::text").get().replace("\n", "").strip() == ""
                    else True
                )
                try:
                    uri = os.getenv("URI")
                    conn = psycopg2.connect(uri)
                    cursor = conn.cursor()
                    cursor.execute(
                        f"SELECT * FROM sherdog_ids WHERE name = '{fighter['first_name']} {fighter['last_name']}'"
                    )
                    matching_fighter = cursor.fetchone()
                    if matching_fighter is not None:
                        fighter["sherdog_id"] = matching_fighter[2]
                        yield response.follow(
                            f"https://www.sherdog.com/fighter/{matching_fighter[2]}",
                            callback=self.parse_sherdog,
                            meta={"fighter": fighter},
                            dont_filter=True,
                        )
                    else:
                        print("No matching fighter found")
                        yield fighter
                except Exception as e:
                    return {"Database Error: ", e}
                finally:
                    cursor.close()
                    conn.close()

    def parse_sherdog(self, response):
        fighter = response.meta["fighter"]
        fighter_data = response.css("div[class='fighter-data']")
        age_data = fighter_data.css("div[class='bio-holder'] td b::text").get()
        fighter["nationality"] = response.css(
            'strong[itemprop="nationality"]::text'
        ).get()
        fighter["locality"] = response.css('span[class="locality"]::text').get()
        try:
            fighter["age"] = int(age_data)
        except:
            fighter["age"] = None

        yield fighter
