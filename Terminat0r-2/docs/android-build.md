# збірка для android

## expo go (швидкий тест)

```bash
cd app
npm install
npx expo start
```

відскануй qr код додатком Expo Go на android

## apk (standalone)

1. встанови eas cli: `npm i -g eas-cli`
2. увійди: `eas login`
3. збірка: `cd app && eas build --platform android --profile preview`

результат — apk для встановлення на пристрій

## налаштування

- app.json: package `com.terminat0r2.app`
- permissions: camera, internet
- android 5+ (api 21+)
