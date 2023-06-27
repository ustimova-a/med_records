import os
import yaml
# from starlette.config import Config
# config = Config('config.yaml')


with open("src/config.yaml", "r") as file_object:
    config = yaml.load(file_object, Loader=yaml.SafeLoader)


# Конфигурация для подключения к базе данных
DATABASE_HOST = config['Database'].get('host', 'localhost')
DATABASE_PORT = config['Database'].get('port', '5432')
DATABASE_NAME = config['Database'].get('db_name')
DATABASE_LOGIN = config['Database'].get('login')
DATABASE_PASSWORD = config['Database'].get('password')

# Название подключения, который будет показываться в списке
# сессий в базе данных. Необходим для администратирования базы
DATABASE_APPLICATION_NAME = config['Application'].get('app_name', 'med_records')

DATABASE_POOL_SIZE = config['Database'].get('pool_size', 4)  # Размер пула сессий с базой данных
DATABASE_POOL_MAX = config['Database'].get('pool_max', 10)  # Максимальный размер пула сессий


# Дебаг состояние приложения. Включается некоторые функции.
APP_DEBUG = config['Application'].get('debug', False)


# Static files
DEFAULT_STATIC_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "../../../dist"
))
STATIC_DIR = config['Application'].get('app_name', DEFAULT_STATIC_DIR)

LOG_DIR = config['Application'].get('log_dir', './')
STORAGE_DIR = config['Application'].get('storage_dir', './')
