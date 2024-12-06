from flask import Flask
import os
import logging

def config_log(app: Flask):
    log_path = os.path.join(app.root_path, "logs")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_handler:logging.FileHandler = logging.FileHandler(f"{log_path}/default.log")
    file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s: in %(module)s% : %(message)s")
        )
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
    return app