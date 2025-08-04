# import logging
import scrapy
import time

import boto3
import os
from dotenv import load_dotenv
from scrapers.items import GreenhouseJobDepartmentsItem
from scrapers.utils import general as util
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from datetime import datetime

load_dotenv()
# logger = logging.getLogger("logger")


class GreenhouseJobDepartmentsSpider(scrapy.Spider):
    name = "greenhouse_job_departments"
    allowed_domains = ["boards.greenhouse.io", "job-boards.greenhouse.io"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spider_id = kwargs.pop("spider_id", 1)
        self.use_existing_html = kwargs.pop("use_existing_html", 0)
        self.careers_page_url = kwargs.pop("careers_page_url")
        self.run_hash = kwargs.pop("run_hash")
        self.url_id = kwargs.pop("url_id", 0)
        self.html_source = (
            self.careers_page_url[:-1]
            if self.careers_page_url[-1] == "/"
            else self.careers_page_url
        )
        self.settings = get_project_settings()
        self.current_time = time.time()
        self.page_number = 1  # default
        self.updated_at = int(self.current_time)
        self.created_at = int(self.current_time)
        self.current_date_utc = datetime.utcfromtimestamp(self.current_time).strftime(
            "%Y-%m-%d"
        )
        self.existing_html_used = False  # Initially set this to false, change later on in finalize_response if True
        self.logger.info(f"Initialized Spider, {self.html_source}")

    @property
    def s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION"),
        )

    @property
    def s3_html_path(self):
        return self.settings["S3_HTML_PATH"].format(**self._get_uri_params())

    @property
    def html_file(self):
        if self.use_existing_html == False:
            return ""
        try:
            return self.s3_client.get_object(
                Bucket=self.settings["S3_HTML_BUCKET"], Key=self.s3_html_path
            )
        except:
            return ""

    @property
    def url(self):
        if self.html_file == "":
            # Remove final "/" so company_name is correct
            return self.html_source
        else:
            return self.settings["DEFAULT_HTML"]

    @property
    def company_name(self):
        # Different format for embedded html
        if "for=" in self.html_source:
            return self.html_source.split("for=")[-1]
        # Traditional format
        return self.html_source.split("/")[-1].split("?")[0]

    @property
    def full_s3_html_path(self):
        if self.settings.get("S3_HTML_BUCKET"):
            return "s3://" + self.settings["S3_HTML_BUCKET"] + "/" + self.s3_html_path
        else:
            return "local://no-s3-configured"

    def determine_partitions(self):
        return f"date={self.current_date_utc}/company={self.company_name}"

    def _get_uri_params(self):
        params = {}
        params["source"] = self.allowed_domains[0].split(".")[1]
        params["bot_name"] = self.settings["BOT_NAME"]
        params["partitions"] = self.determine_partitions()
        params["file_name"] = (
            f"{self.company_name}-{self.allowed_domains[0].split('.')[1]}.html"
        )

        return params

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def export_html(self, response_html):
        # Only export to S3 if bucket is configured
        if self.settings.get("S3_HTML_BUCKET"):
            try:
                self.s3_client.put_object(
                    Bucket=self.settings["S3_HTML_BUCKET"],
                    Key=self.s3_html_path,
                    Body=response_html,
                    ContentType="text/html",
                )
                self.logger.info("Uploaded raw HTML to s3")
            except Exception as e:
                self.logger.warning(f"Failed to upload to S3: {e}")
        else:
            self.logger.info("S3 bucket not configured, skipping HTML upload")

    def determine_row_id(self, i):
        # Include company name in the ID generation to ensure global uniqueness
        # This prevents duplicate IDs across different companies
        company_hash = hash(self.company_name) % 10000  # Convert company name to a number
        return util.hash_ids.encode(
            self.spider_id, i, self.url_id, int(self.created_at), company_hash
        )

    def finalize_response(self, response):
        if self.html_file != "":
            self.created_at = int(self.html_file["LastModified"].timestamp())
            self.existing_html_used = True
            return self.html_file["Body"].read()
        else:
            self.export_html(response.text)
            return response.text

    # Greenhouse has exposed a new URL with different features for scraping for some companies
    def parse_job_boards_prefix(self, i, department):
        il = ItemLoader(
            item=GreenhouseJobDepartmentsItem(),
            selector=Selector(text=department.get(), type="html"),
        )
        self.logger.info(f"Parsing row {i+1}, {self.company_name}, {self.name}")

        il.add_value("department_id", self.company_name + "_" + department.get())
        il.add_value("department_name", department.get())
        il.add_value("department_category", "level-0")

        il.add_value("id", self.determine_row_id(i))
        il.add_value("created_at", self.created_at)
        il.add_value("updated_at", self.updated_at)

        il.add_value("source", self.html_source)
        il.add_value("company_name", self.company_name)
        il.add_value("run_hash", self.run_hash)
        il.add_value("raw_html_file_location", self.full_s3_html_path)
        il.add_value("existing_html_used", self.existing_html_used)

        return il

    def parse(self, response):
        response_html = self.finalize_response(response)
        selector = Selector(text=response_html, type="html")
        if self.careers_page_url.split(".")[0].split("/")[-1] == "job-boards":
            all_departments = selector.xpath(
                "//div[(@class='job-posts')]/*[starts-with(name(), 'h')]/text()"
            )
            for i, department in enumerate(all_departments):
                il = self.parse_job_boards_prefix(i, department)
                yield il.load_item()
            if len(all_departments) != 0:
                self.page_number += 1
                yield response.follow(
                    self.careers_page_url + f"?page={self.page_number}", self.parse
                )

            # for i, department in enumerate(all_departments):
            #     il = ItemLoader(
            #         item=GreenhouseJobDepartmentsItem(),
            #         selector=Selector(text=department.get(), type="html"),
            #     )
            #     self.logger.info(f"Parsing row {i+1}, {self.company_name}, {self.name}")

            #     department_id = self.company_name + "_" + department.get()
            #     il.add_value("department_id", department_id)
            #     il.add_value("department_name", department.get())
            #     il.add_value("department_category", "level-0")

            #     il.add_value("id", self.determine_row_id(i))
            #     il.add_value("created_at", self.created_at)
            #     il.add_value("updated_at", self.updated_at)

            #     il.add_value("source", self.html_source)
            #     il.add_value("company_name", self.company_name)
            #     il.add_value("run_hash", self.run_hash)
            #     il.add_value("raw_html_file_location", self.full_s3_html_path)
            #     il.add_value("existing_html_used", self.existing_html_used)

            #     # print(il.load_item())

            #     yield il.load_item()

        else:
            all_departments = selector.xpath('//section[contains(@class, "level")]')

            for i, department in enumerate(all_departments):
                il = ItemLoader(
                    item=GreenhouseJobDepartmentsItem(),
                    selector=Selector(text=department.get(), type="html"),
                )
                dept_loader = il.nested_xpath(
                    f"//section[contains(@class, 'level')]/*[starts-with(name(), 'h')]"
                )
                self.logger.info(f"Parsing row {i+1}, {self.company_name}, {self.name}")

                dept_loader.add_xpath("department_id", "@id")
                dept_loader.add_xpath("department_name", "text()")
                il.add_xpath(
                    "department_category", "//section[contains(@class, 'level')]/@class"
                )

                il.add_value("id", self.determine_row_id(i))
                il.add_value("created_at", self.created_at)
                il.add_value("updated_at", self.updated_at)

                il.add_value("source", self.html_source)
                il.add_value("company_name", self.company_name)
                il.add_value("run_hash", self.run_hash)
                il.add_value("raw_html_file_location", self.full_s3_html_path)
                il.add_value("existing_html_used", self.existing_html_used)

                yield il.load_item()

            # self.logger.info(f"{dep_xpath} Department here")
