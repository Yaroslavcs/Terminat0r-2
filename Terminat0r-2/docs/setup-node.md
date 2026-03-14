# встановлення Node.js (для npm)

## варіант 1: офіційний інсталятор

1. Відкрий https://nodejs.org
2. Завантаж **LTS** версію
3. Запусти інсталятор
4. Постав галочку **"Add to PATH"**
5. Перезапусти PowerShell після встановлення

## варіант 2: winget (Windows)

```powershell
winget install OpenJS.NodeJS.LTS
```

потім перезапусти термінал

## перевірка

```powershell
node -v
npm -v
```

якщо показує версії — можна робити `npm install`
