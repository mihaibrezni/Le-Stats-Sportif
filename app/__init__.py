import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import logging
from logging.handlers import RotatingFileHandler

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

# webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1
webserver.logger = logging.getLogger('webserver.log')
webserver.logger.setLevel(logging.INFO)

webserver.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Crearea și configurarea handler-ului RotatingFileHandler
log_file = 'webserver.log'
max_file_size_bytes = 1024 * 1024  # 1 MB
max_files_count = 5
webserver.file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size_bytes, backupCount=max_files_count)
webserver.file_handler.setFormatter(webserver.formatter)
webserver.logger.addHandler(webserver.file_handler)

# create result files
if not os.path.exists('results'):
    os.mkdir('./results')

from app import routes
