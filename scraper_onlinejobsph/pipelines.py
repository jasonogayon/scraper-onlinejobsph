from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem



class ScraperOnlinejobsphPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        id = 'role'

        # Drop duplicate records
        adapter = ItemAdapter(item)
        if adapter[id] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter[id])
            return item