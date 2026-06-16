# 🎬 CineHub

Навчальний проєкт **Модуля 3 (Django)** курсу Python Fullstack у JavaRush.

Це **наскрізний проєкт**: протягом 25 лекцій ми крок за кроком будуємо один цілісний застосунок —
каталог фільмів із рецензіями, оцінками та списком «до перегляду». На кожній парі перша половина —
теорія з презентації, друга — застосування теми на CineHub.

У підсумку модуля проєкт матиме **три інтерфейси поверх однієї бази**:
веб-сайт (Django-шаблони) · REST API (DRF) · GraphQL.

---

## Що вміє застосунок (фінальна ціль)

- Каталог фільмів: жанри, режисери/актори, постери, рік, опис.
- Рецензії та оцінки (1–10) від користувачів; середній рейтинг фільму.
- Особистий список «до перегляду» (watchlist).
- Реєстрація / вхід, профіль користувача.
- Адмін-зона для контент-менеджерів.
- REST API з JWT, пагінацією, фільтрами, документацією (Swagger).
- GraphQL-ендпойнт для гнучких вкладених запитів.

> Повний план занять — у [`docs/ROADMAP.md`](docs/ROADMAP.md).
> Архітектура й моделі — у [`docs/PROJECT.md`](docs/PROJECT.md).
> Покрокові конспекти пар — у [`docs/lessons/`](docs/lessons/).

---

## Стек

| Шар | Технологія |
|-----|------------|
| Мова | Python 3.12+ |
| Фреймворк | Django 6.0 |
| База даних | PostgreSQL 17 (через Docker) |
| API | Django REST Framework + SimpleJWT |
| GraphQL | graphene-django |
| Тести | pytest-django |

---

## Швидкий старт (для студента)

```bash
# 1. Клонувати репозиторій і зайти в папку
git clone <url> module3_project
cd module3_project

# 2. Створити та активувати віртуальне оточення
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell: .venv\Scripts\Activate.ps1)
# source .venv/bin/activate     # macOS / Linux

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Підняти базу даних (потрібен Docker)
copy .env.example .env          # і за потреби відредагувати
docker compose up -d

# 5. Застосувати міграції та запустити сервер
python manage.py migrate
python manage.py runserver
```

Відкрити: http://127.0.0.1:8000/

> ⚠️ Кроки 4–5 зʼявляться, коли ми створимо Django-проєкт на Рівні 1–2.
> На старті репозиторій містить лише документацію та конфіги.

---

## Структура репозиторію (цільова)

```
module3_project/
├── cinehub/            # конфіг Django-проєкту (settings, urls, wsgi)
├── apps/               # наші застосунки
│   ├── catalog/        #   фільми, жанри, персони
│   ├── accounts/       #   профілі, реєстрація, вхід
│   ├── reviews/        #   рецензії, оцінки, watchlist
│   └── api/            #   DRF + GraphQL поверх моделей
├── templates/          # HTML-шаблони
├── static/             # CSS / JS / зображення
├── docs/               # документація курсу (план, конспекти)
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── .env.example
```
