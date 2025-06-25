# PREZ — PDF Presentation Generator API

**PREZ** — это простой API-сервис для генерации PDF-презентаций из текстовых данных.

---

## Возможности

- Принимает структурированные данные (заголовки, тексты слайдов) через POST-запрос
- Генерирует и возвращает PDF-презентацию
- Можно использовать локально или в Docker

---

## Требования

- Python 3.10+
- pip
- (опционально) Docker

---

## Установка

**Локально:**
```bash
git clone https://github.com/Nikolai/PREZ.git
cd PREZ
python3 -m pip install -r requirements.txt
