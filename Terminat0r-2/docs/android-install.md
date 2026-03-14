# встановлення на android

## передумови

1. **Node.js** — має бути в PATH. перевір: `node -v`. якщо не знайдено: docs/setup-node.md
2. **Java 17+** та **Android SDK** — тільки для локальної збірки

## спосіб 1: EAS Build (рекомендовано)

не потребує Android SDK. збірка в хмарі Expo — найстабільніший варіант.

```powershell
cd app
npm install
npx eas login
npm run build:apk
```

після збірки отримаєш посилання на APK. завантаж на телефон і встанови.

---

## спосіб 2: локальна збірка (експериментально)

потребує: node, java 17+, android sdk.

**увага:** на Expo 51 локальна збірка може падати з помилками `SDK location not found`, `expo-module-gradle-plugin not found` та `release property`. це відома несумісність. якщо так — використовуй EAS Build (спосіб 1).

### налаштування Android SDK

1. встанови [Android Studio](https://developer.android.com/studio) або тільки [Command Line Tools](https://developer.android.com/studio#command-tools)
2. файл `app/android/local.properties` вже створено — відредагуй `sdk.dir`, якщо SDK в іншому місці:
   ```
   sdk.dir=C:\\Users\\Labradoro\\AppData\\Local\\Android\\Sdk
   ```
   на Windows подвійні зворотні слеші `\\` обовʼязкові.
3. або встанови змінну середовища `ANDROID_HOME` на шлях до SDK

**патч для Expo 51:** `release` property виправлено через patch-package (папка `app/patches/`). після `npm install` патч застосовується автоматично.

```powershell
cd app
npm install
.\build-android.ps1 -Local
```

apk буде в `app\terminat0r2.apk` при успішній збірці.

---

## встановлення apk на телефон

1. завантаж apk на телефон (usb, drive, посилання)
2. дозволь встановлення з невідомих джерел (налаштування → безпека)
3. відкрий apk → встановити

---

## expo go (без збірки)

для швидкого тесту без apk:

```powershell
cd app
npm install
npx expo start
```

відскануй qr код додатком expo go з google play.
