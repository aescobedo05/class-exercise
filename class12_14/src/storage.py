import logging

logger = logging.getLogger(__name__)

class DataStorage:
    def __init__(self):
        self.datasets = {}
        self.counter = 0

    def save_data(self, df, filename):
        self.counter += 1
        dataset_id = self.counter

        self.datasets[dataset_id] = {"filename": filename, "data": df.copy()}

        logger.debug("Stored dataset: id=%s, rows=%s", dataset_id, len(df))
        return dataset_id

    def get_data(self, dataset_id):
        item = self.datasets.get(dataset_id)
        if item is None:
            logger.debug("Dataset not found: id=%s", dataset_id)
            return None
        logger.debug("Retrieved dataset: id=%s", dataset_id)

        return item['data'].copy()
