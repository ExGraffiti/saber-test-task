# Build System Microservice

Микросервис для управления задачами и билдами в игровой разработке. Позволяет получать список задач для указанного билда с учётом их зависимостей.

## 📦 Установка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/ExGraffiti/saber-task.git
cd <repository_dir>
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

🚀 Запуск
Запустите сервис:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Сервис будет доступен по адресу:
http://127.0.0.1:8000

Для тестирования используйте:

```bash
pytest
```

📌 Использование
Эндпоинт:
POST /get_tasks
Принимает JSON с именем билда и возвращает отсортированный список задач.

Пример запроса:

```json
{
  "build": "forward_interest"
}
```
Пример ответа:

```json
{
  "tasks": ["task_1", "task_2", ...]
}
```

Ошибки:
404 Not Found — билд не найден.

400 Bad Request — циклические зависимости.

500 Internal Server Error — проблемы с конфигурацией.


### Описание ключевых компонентов

- **`builds/`**:  
  Содержит YAML-файлы с описанием билдов (`builds.yaml`) и задач (`tasks.yaml`).

- **`src/config/`**:  
  - `loader.py` — загружает и кэширует конфигурацию.  
  - `validator.py` — проверяет корректность конфигурации.

- **`src/services/`**:  
  - `dependency.py` — находит все зависимости для задач.  
  - `sorter.py` — реализует топологическую сортировку (алгоритм Кана).

- **`src/api/`**:  
  `endpoints.py` — эндпоинт `/get_tasks` для обработки запросов.

- **`tests/`**:  
  - `test_unit.py` — тесты бизнес-логики.  
  - `test_api.py` — тесты API (через TestClient).  
  - `conftest.py` — моки и фикстуры.


🛠 Технологии
Python 3.9+

FastAPI

Pydantic

PyYAML

pytest (для тестирования)
