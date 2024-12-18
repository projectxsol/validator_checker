import requests
import subprocess
import logging
import schedule
import time
import signal
import sys
from sys import argv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Общий уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('validator_status.log'),  # Логирование в файл
        logging.StreamHandler()  # Логирование в консоль
    ]
)

def validator_status(base_url, relayer_key):
    """
    Проверяет статус валидатора.
    """
    endpoint = f"{base_url}/validator/status"
    params = {'relayer_key': relayer_key}

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        connected = response.json().get('connected', False)
        logging.info(f"Validator {relayer_key} status: {'connected' if connected else 'not connected'}")
        return connected
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking validator {relayer_key} status: {e}")
        return False

def restart_relayer():
    """
    Рестартует службу relayer через systemctl.
    """
    try:
        result = subprocess.run(['sudo', 'systemctl', 'restart', 'relayer'], check=True, text=True, capture_output=True)
        logging.info(f"Relayer service restarted successfully. Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to restart relayer: {e}. Output: {e.output}, Error: {e.stderr}")

def check_and_restart(base_url, relayer_key):
    """
    Проверяет статус валидатора и перезапускает relayer при необходимости.
    """
    is_connected = validator_status(base_url, relayer_key)
    if not is_connected:
        logging.warning(f"Validator {relayer_key} is not connected. Restarting relayer service...")
        restart_relayer()
    else:
        logging.info(f"Validator {relayer_key} is connected.")

def handle_exit(signum, frame):
    """
    Обрабатывает сигнал завершения программы.
    """
    logging.info("Shutting down validator check service.")
    sys.exit(0)

if __name__ == "__main__":
    # Обработка сигналов завершения
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # Проверка наличия аргумента
    if len(argv) < 2:
        logging.error("Relayer key is required as a command-line argument.")
        sys.exit("Error: Relayer key is required as a command-line argument.")

    base_url = "https://projectx.run"
    relayer_key = argv[1]  # Один ключ передаётся через параметры

    # Немедленная проверка при старте
    check_and_restart(base_url, relayer_key)

    # Планирование задачи каждые 10 минут
    schedule.every(10).minutes.do(check_and_restart, base_url=base_url, relayer_key=relayer_key)

    logging.info("Validator status check service started.")

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"An error occurred while running scheduled tasks: {e}")
