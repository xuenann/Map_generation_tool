# AGENTS.md - Development Guide for Map Generation Tool

## Project Overview
- **Type**: Django 5.2 Web Application
- **Purpose**: Convert CSV geographic data into interactive visualization maps (Gaode/Baidu)
- **Python**: 3.8+ | **Database**: SQLite (db.sqlite3)

---

## Build / Run Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server (http://127.0.0.1:8000/)
python manage.py runserver

# Django management
python manage.py migrate          # Apply database migrations
python manage.py makemigrations    # Create migrations
python manage.py createsuperuser  # Create admin user
python manage.py check            # Validate project configuration
```

---

## Testing Commands

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test fileapp

# Run single test class
python manage.py test fileapp.tests.CoordinateTransformTest

# Run single test method (full path required)
python manage.py test fileapp.tests.CoordinateTransformTest.test_wgs84_to_gcj02
```

---

## Code Style Guidelines

### General Rules
- Follow PEP 8 Python style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 120 characters
- Add docstrings to all public functions

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Functions/Variables | snake_case | `generate_map`, `file_path` |
| Classes | PascalCase | `MapConfig`, `FileHandler` |
| Constants | UPPER_SNAKE_CASE | `MAX_ZOOM_LEVEL` |
| Django Views | snake_case | `upload_file`, `generate_map` |

### Import Order (PEP 8)
1. Standard library (`os`, `json`, `math`)
2. Third-party (`django`, `pyproj`)
3. Local application (`.`, `fileapp`)

```python
import os
import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse

from . import tomap
from .map_function import gaode_marker
```

### Type Hints
- Recommended for new functions
- Use built-in types: `str`, `int`, `float`, `bool`, `list`, `dict`
- Use `typing.Optional`, `List`, `Dict`, `Tuple`

```python
def process_file(file_path: str, user_ip: str) -> tuple[bool, str]:
    """Process uploaded file and return success status and message."""
    pass
```

### Error Handling
- Use try/except for file I/O and parsing
- Return tuple `(bool, str)` for operations
- Log errors with `print()` or logging module

```python
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    return True, data
except FileNotFoundError:
    return False, "File not found"
except Exception as e:
    print(e)
    return False, str(e)
```

---

## Django-Specific Patterns

### Views
- Use `@csrf_exempt` for AJAX POST APIs
- Return `JsonResponse` for JSON APIs
- Use `request.META.get('REMOTE_ADDR')` for user IP

```python
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        user_ip = request.META.get('REMOTE_ADDR', 'unknown_ip')
    return JsonResponse({'error': 'Only POST allowed'})
```

### URL Routing
- App URLs: `fileapp/urls.py`
- Main URLs: `myproject/urls.py`

### Dictionary Keys
Prefer snake_case for new keys:
```python
coordinate_func_dict = {
    'wgs84_gaode': coordinate_transform.wgs84_to_gcj02,
}
map_type = data.get('map_type', 'gaode_marker')
```

---

## File Handling
- Use `encoding='utf-8'` for all text files
- Use `os.path.join()` for path construction
- Handle both Windows and Unix path separators

### Templates & Configuration
- HTML templates: `fileapp/templates/`
- Static config files (start.txt, mid.txt, end.txt) in `fileapp/templates/<map_type>/`
- API keys in `myproject/settings.py` (use `settings.GAODE_API_KEY`, `settings.BAIDU_API_KEY`)
- **Never commit actual API keys to version control**

---

## Project Structure

```
Map_generation_tool/
├── fileapp/
│   ├── map_function/          # Map generation modules
│   │   ├── baidu_marker.py
│   │   ├── gaode_marker.py
│   │   ├── gaode_hotmap.py
│   │   └── ...
│   ├── migrations/
│   ├── templates/             # HTML templates and config files
│   ├── coordinate_transform.py
│   ├── tomap.py              # Core map generation logic
│   ├── views.py              # Django views
│   └── models.py
├── myproject/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

---

## Adding New Map Types

1. Create module in `fileapp/map_function/`
2. Implement `read_<map>_config(data)` and `to_<map>(map_config, map_data, new_file_path)`
3. Register in `tomap.py`: `config_func_dict` and `map_func_dict`
4. Add template files in `fileapp/templates/<map_type>/`

---

## Testing Guidelines
- Tests in `fileapp/tests.py`
- Use Django's `TestCase` class

```python
from django.test import TestCase
from fileapp.coordinate_transform import wgs84_to_gcj02

class CoordinateTransformTest(TestCase):
    def test_wgs84_to_gcj02(self):
        lng, lat = wgs84_to_gcj02(116.397428, 39.90923)
        self.assertIsNotNone(lng)
        self.assertIsNotNone(lat)
```
