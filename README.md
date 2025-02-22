# Validator Checker Service

Python-скрипт для мониторинга подключения релеера к `blockEngine`. Если релеер оказывается отключённым, скрипт автоматически перезагружает службу релеера для восстановления подключения. Все события, включая статус проверки и перезагрузки, логируются для дальнейшего анализа.

---

## Установка

### Шаг 1. Клонирование репозитория

Склонируйте репозиторий на локальную машину:

```bash
git clone <URL репозитория>
cd <имя директории>
```

### Шаг 2. Установка зависимостей

Убедитесь, что у вас установлен Python 3. Установите необходимые зависимости командой:

```bash
pip install -r requirements.txt
```

---

## Использование

Для запуска скрипта вручную используйте следующую команду:

```bash
python validator_checker.py <ключ релеера>
```

---

## Описание работы

Скрипт выполняет опрос подключения к `blockEngine` каждые 10 минут. Если релеер оказывается отключённым, происходит автоматическая перезагрузка службы релеера для восстановления подключения. 

---

## Запуск как системный сервис

### Шаг 1. Создание файла службы

Создайте файл `/etc/systemd/system/validator_checker.service`:

```bash
sudo nano /etc/systemd/system/validator_checker.service
```

Добавьте следующее содержимое:

```ini
[Unit]
Description=Validator Checker Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/validator_checker/validator_checker.py <YOUR_RELAYER_KEY> # незабываем проверить путь у вас они могут быть другими
Restart=always
WorkingDirectory=/opt/validator_checker # незабываем проверить путь у вас они могут быть другими
User=your_username  # Укажите имя пользователя, под которым будет запускаться сервис
Group=your_username  # Укажите группу
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### Шаг 2. Настройка прав

Убедитесь, что скрипт доступен для чтения и выполнения:

```bash
sudo chmod +x /opt/validator_checker/validator_checker.py # незабываем проверить путь у вас они могут быть другими
sudo chown your_username:your_username /opt/validator_checker/validator_checker.py # незабываем проверить путь у вас они могут быть другими
```

### Шаг 3. Перезагрузка и запуск сервиса

1. Перезагрузите `systemd`, чтобы зарегистрировать новый сервис:

   ```bash
   sudo systemctl daemon-reload
   ```

2. Включите сервис для автоматического запуска:

   ```bash
   sudo systemctl enable validator_checker.service
   ```

3. Запустите сервис:

   ```bash
   sudo systemctl start validator_checker.service
   ```

4. Проверьте статус сервиса:

   ```bash
   sudo systemctl status validator_checker.service
   ```

---

## Логирование

Для просмотра логов сервиса используйте команду:

```bash
journalctl -u validator_checker.service -f
```

---

## Примечания

- Убедитесь, что вы указали правильный путь к скрипту и файлам в конфигурации сервиса.
- Если требуется изменение ключа релеера, отредактируйте файл службы и перезапустите сервис.

---

## Лицензия

Этот проект распространяется под лицензией MIT.
