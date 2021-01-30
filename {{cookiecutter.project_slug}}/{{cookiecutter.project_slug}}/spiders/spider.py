import sys
from urllib.parse import urlparse

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

sys.path.append("../..")
from {{cookiecutter.project_slug}}.items import QuoteItem  # noqa: E402


class Spider(scrapy.Spider):
    name = "spider"
    start_urls = ["http://quotes.toscrape.com/random"]
    allowed_domains = [urlparse(url).netloc for url in start_urls]
    referer = start_urls[0]

    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "pipelines.celery.CeleryPipeline": 100,
    #     },
    # }
    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url,
                headers={"Referer": self.referer},
                callback=self.parse,
                {%- if cookiecutter.use_mitmweb == "y" %}
                meta={"proxy": "http://docker:docker@mitmweb:8080"},
                {%- endif %}
            )

    def parse(self, response, **kwargs):
        self.logger.info(response.url)
        q = QuoteItem()
        q["author"] = response.css("small.author::text").get()
        q["content"] = response.css("span.text::text").get()
        yield q


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(Spider)
    process.start()  # the script will block here until the crawling is finished
