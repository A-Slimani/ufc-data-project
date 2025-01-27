from ufcstats.items import Fighter, Sherdog_ID
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
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

    custom_settings = {"ITEM_PIPELINES": {"ufcstats.pipelines.fighter_pipeline": 300}}

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
                # In order to follow I need to get the link to the fighters page on sherdog
                # 2 paths
                # 1. Have a table that has all the sherdog links
                # 2. If not run the sherdog.xml scraper to update and get the new name
                # Make a SQL request to get the fighter name based of the table
                try:
                    uri = os.getenv("URI")
                    if uri is None:
                        raise ValueError(
                            "Database URI is not set in environment variables"
                        )
                    engine = create_engine(uri)
                    session = sessionmaker(bind=engine)
                    with session() as s:
                        def get_matching_fighter():
                            matching_fighter = (
                                s.query(Sherdog_ID)
                                .filter_by(
                                    name=" ".join(
                                        [fighter["first_name"], fighter["last_name"]]
                                    )
                                )
                                .first()
                            )
                            if matching_fighter is not None:
                                fighter["sherdog_id"] = matching_fighter.sherdog_id
                            else:
                                # Run the sherdog xml scraper again
                                # Potential infinite loop???
                                get_matching_fighter()
                                pass

                except Exception as e:
                    return {"Database Error: ", e}

                # yield response.follow(url=)
                # if True:
                #     url = 'https://www.sherdog.com/sitemap-fighters.xml'
                # else:
                #     yield fighter

    def parse_sherdog(self, response):
        pass
