from flask import Flask
from task import TaskManager
from logging_config import setup_logging
import config

app = Flask(__name__)
setup_logging()

task_manager = TaskManager()

@app.route('/')
def index():
    return "欢迎福报系统！"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.PORT)
