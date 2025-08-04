# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
from threading import Lock

class JsonExportPipeline:
    """Pipeline to export items to JSON file with proper handling of concurrent writes"""
    
    def __init__(self):
        self.file_path = 'scraped_data.json'
        self.lock = Lock()
        self.items = []
        
    def open_spider(self, spider):
        """Called when spider opens"""
        # Don't clear the file - we want to append data from multiple spiders
        pass
    
    def process_item(self, item, spider):
        """Process each item and add to the list"""
        with self.lock:
            self.items.append(dict(item))
        return item
    
    def close_spider(self, spider):
        """Called when spider closes - append items to JSON file"""
        with self.lock:
            if self.items:
                # Read existing data if file exists
                existing_data = []
                if os.path.exists(self.file_path):
                    try:
                        with open(self.file_path, 'r', encoding='utf-8') as f:
                            existing_data = json.load(f)
                    except (json.JSONDecodeError, FileNotFoundError):
                        existing_data = []
                
                # Append new items
                all_data = existing_data + self.items
                
                # Write all data back to file
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(all_data, f, indent=2, ensure_ascii=False)
                
                spider.logger.info(f"Added {len(self.items)} items to {self.file_path} (total: {len(all_data)})")

class JobScraperPipelinePostgres:
    def __init__(self):
        ## Connection Details
        self.hostname = os.environ.get("PG_HOST")
        self.username = os.environ.get("PG_USER")
        self.password = os.environ.get("PG_PASSWORD")
        self.database = os.environ.get("PG_DATABASE")

        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=self.hostname,
            user=self.username,
            password=self.password,
            dbname=self.database,
        )

        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

    def open_spider(self, spider):
        self.table_name = spider.name
        initial_table_schema = pipline_util.set_initial_table_schema(self.table_name)
        create_table_statement = pipline_util.create_table_schema(
            self.table_name, initial_table_schema
        )
        self.cur.execute(create_table_statement)

    def process_item(self, item, spider):
        ## Execute insert of data into database
        insert_item_statement, table_values_list = pipline_util.create_insert_item(
            self.table_name, item
        )
        # logger.info(f"INSERT STMT {insert_item_statement} ____ {table_values_list}")
        self.cur.execute(insert_item_statement, tuple(table_values_list))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
