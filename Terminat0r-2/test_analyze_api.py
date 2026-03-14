#!/usr/bin/env python3
"""Тест API аналізу сцени: згенероване фото брудного столу -> перевірка відповіді ШІ."""
import base64
import json
import sys
import time
from pathlib import Path

import requests

API_BASE = "http://localhost:8000"


def create_test_image():
    """Завантажує тестове зображення брудного столу з Unsplash (без PIL)."""
    url = "https://images.unsplash.com/photo-1593062096033-9a26b09da705?w=640"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print(f"   Не вдалося завантажити зображення: {e}")
    return None


def main():
    IMG_PATH = Path(__file__).resolve().parent / "assets" / "dirty-desk-test.jpg"
    if IMG_PATH.exists():
        img_data = IMG_PATH.read_bytes()
        print(f"Використовується зображення: {IMG_PATH}")
    else:
        print("Згенероване зображення не знайдено. Створюю тестове зображення брудного столу...")
        img_data = create_test_image()
        if not img_data:
            print("Помилка: не вдалося отримати тестове зображення. Покладіть dirty-desk-test.jpg в assets/")
            sys.exit(1)
    img_b64 = base64.b64encode(img_data).decode("utf-8")

    print("1. Відправка запиту POST /api/analyze...")
    try:
        r = requests.post(
            f"{API_BASE}/api/analyze",
            json={"image_b64": img_b64},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Помилка: не вдалося підключитися до backend. Запустіть: uvicorn backend.main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка запиту: {e}")
        sys.exit(1)

    data = r.json()
    job_id = data.get("job_id")
    if not job_id:
        print("Помилка: API не повернув job_id")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        sys.exit(1)

    print(f"   job_id: {job_id}")

    print("2. Очікування результату (polling /api/job/{id})...")
    for i in range(25):
        time.sleep(1.5)
        try:
            r2 = requests.get(f"{API_BASE}/api/job/{job_id}", timeout=5)
            r2.raise_for_status()
        except Exception as e:
            print(f"   Помилка poll: {e}")
            continue

        job = r2.json()
        status = job.get("status")

        if status == "completed":
            result = job.get("result", {})
            print("\n3. Результат аналізу ШІ:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            fact = result.get("fact")
            help_task = result.get("help")
            display_type = result.get("display_type")
            category = result.get("category")
            keywords = result.get("keywords", [])
            event_type = result.get("event_type")

            print("\n4. Перевірка шаблону поради:")
            if display_type == "help" and help_task:
                print("   [OK] display_type = 'help' - показується допомога з routine-events")
                print(f"   [OK] Текст поради: {fact}")
                print(f"   [OK] Категорія: {category}")
                print(f"   [OK] Keywords від ШІ: {keywords}")
            elif fact:
                print("   [i] display_type = 'fact' - показується факт (допомоги для категорії немає)")
                print(f"   Текст: {fact}")
                print(f"   Категорія: {category}")
            else:
                print("   [!] Немає fact/help у відповіді")

            if category == "room_workspace":
                print("\n   [OK] Для брудного столу очікується категорія room_workspace")
            print("\n   ШІ має генерувати пораду на основі шаблонів (не копіювати дослівно)")
            return

        if status == "failed":
            print(f"\nПомилка аналізу: {job.get('error', 'unknown')}")
            sys.exit(1)

    print("\nТаймаут: аналіз не завершився за 25 спроб")
    sys.exit(1)


if __name__ == "__main__":
    main()
