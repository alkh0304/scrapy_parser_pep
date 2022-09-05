import csv

from datetime import datetime as dt
from pathlib import Path
from scrapy.exceptions import DropItem

BASE_DIR = Path(__file__).parent.parent
DT_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILE_NAME = 'status_summary_{}.csv'


class PepParsePipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        file_name = self.results_dir / FILE_NAME.format(
            dt.now().strftime(DT_FORMAT)
        )
        self.file = csv.writer(
            open(file_name, mode='w', encoding='utf-8')
        )
        self.results = {}

    def process_item(self, item, spider):
        if 'status' in item:
            if item['status'] in self.results:
                self.results[item['status']] += 1
                return item
            else:
                self.results[item['status']] = 1
                return item
        else:
            raise DropItem('Статус PEP не обнаружен.')

    def close_spider(self, spider):
        self.file.writerow(['Статус', 'Количество'])
        self.results['Total'] = sum(self.results.values())
        self.file.writerows(self.results.items())
