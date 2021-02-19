import sys
from urllib.parse import urlparse

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor

sys.path.append("../..")
from {{cookiecutter.project_slug}}.items import QuoteItem  # noqa: E402


class Spider(scrapy.Spider):
    name = "spider"
    start_urls = ["http://quotes.toscrape.com/random"]
    allowed_domains = [urlparse(url).netloc for url in start_urls]
    referer = start_urls[0]

    custom_settings = {
        "ITEM_PIPELINES": {
            "{{cookiecutter.project_slug}}.pipelines.pipelines.DBPipeline": 300,
        },
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url,
                headers={"Referer": self.referer},
                callback=self.parse,
                {%- if cookiecutter.use_mitmweb == "y" %}
                meta = {
                    "proxy": "http://docker:docker@mitmweb:8080"
                },  # if tor_privoxy was choosen, upstrem is setted up to tor_proxy
                {%- elif cookiecutter.use_tor_privoxy == "y" %}
                meta = {"proxy": "http://tor-privoxy:8118"},#tor via privoxy
                {%- endif %}
            )

    def parse(self, response, **kwargs):
        self.logger.info(response.url)
        q = QuoteItem()
        q["author"] = response.css("small.author::text").get()
        q["content"] = response.css("span.text::text").get()
        yield q


if __name__ == "__main__":
    settings = get_project_settings()
    {%- if cookiecutter.async_reactor != "n" %}
    install_reactor(settings["TWISTED_REACTOR"])
    {%- endif %}
    process = CrawlerProcess()
    process.crawl(Spider)
    process.start()  # the script will block here until the crawling is finished
