# ⚡ ПОТУЖНО Shop — Комерційна E-Commerce Платформа

> Сучасна, високопродуктивна платформа електронної комерції, побудована за стандартами чистої архітектури та Enterprise-розробки.

---

## 🛠 Технологічний стек
* **Core:** Python 3.11+, Django 6.0, Django REST Framework (DRF)
* **Database:** PostgreSQL, SQLite (для тестового середовища)
* **Concurrency & Safety:** Транзакції (`@transaction.atomic`), блокування рядків (`select_for_update`), точні фінансові розрахунки через `Decimal`
* **API Documentation:** `drf-spectacular` (OpenAPI 3, Swagger UI, ReDoc)
* **Testing:** Pytest, pytest-django (повне покриття модульних та API тестів)
* **CI/CD:** GitHub Actions (автоматизований пайплайн міграцій та тестів)

---

## 📂 Архітектура проєкту
Проєкт реалізовано за принципом **Single Responsibility** з чітко розбитою модульною структурою:
* 🛍 **`apps/shop/`** — каталог товарів, категорії, бренди, розміри, розширені фільтри та API ViewSets.
* 🛒 **`apps/cart/`** — ізольований сервісний шар (`CartService`), розмежування бази даних для авторизованих користувачів та сесій для гостів, а також автоматичне злиття кошика при вході в систему.
* 📦 **`apps/orders/`** — транзакційне оформлення замовлень, динамічна валідація актуальних цін з бази даних, атомарне списання залишків через `F()`-вирази та збереження історії (`SET_NULL` разом із захисними знімками даних).
* 👤 **`apps/accounts/`** — управління профілями користувачів, кастомні форми та розширена аутентифікація.
* ⭐ **`apps/reviews/`** — система відгуків, рейтинги та інтерактивний список бажаного (Wishlist).

---

## 🚀 Швидкий старт та розгортання

1. **Клонуйте репозиторій:**
   ```bash
   git clone [https://github.com/pixsus228/my_potuzhno_shop.git](https://github.com/pixsus228/my_potuzhno_shop.git)
   cd my_potuzhno_shop
Створіть та активуйте віртуальне середовище:

Bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\Activate.ps1
Встановіть залежності:

Bash
pip install --upgrade pip
pip install -r requirements.txt
Застосуйте міграції та заповніть базу початковими даними:

Bash
python manage.py migrate
python manage.py seed_products
Запустіть локальний сервер:

Bash
python manage.py runserver
🧪 Тестування
Для запуску повного пакету автоматичних тестів використайте:

Bash
python -m pytest
📄 Документація API
Інтерактивна документація для тестування ендпоінтів доступна за посиланнями:

📘 Swagger UI: http://127.0.0.1:8000/api/docs/

📑 ReDoc: http://127.0.0.1:8000/api/redoc/

🔌 OpenAPI Schema: http://127.0.0.1:8000/api/schema/