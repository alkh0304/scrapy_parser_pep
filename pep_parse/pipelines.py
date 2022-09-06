import csv

from datetime import datetime as dt
from pathlib import Path
from scrapy.exceptions import DropItem

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = Path('results')
DT_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILE_NAME = 'status_summary_{}.csv'


class PepParsePipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / RESULTS_DIR
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
            self.results[item['status']] = self.results.get(
                item['status'], 0) + 1
            return item
        raise DropItem('Статус PEP не обнаружен.')

    def close_spider(self, spider):
        self.file.writerow(['Статус', 'Количество'])
        self.results['Total'] = sum(self.results.values())
        self.file.writerows(self.results.items())
