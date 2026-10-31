# Рендеры для сайта

Все изображения на сайте — рендеры three.js (макет условного объекта и устройства), вставлены в `index.html`
как `data:image/webp;base64`. Пересоздать после правок `render.html`:

```bash
cd tools/3d
npm init -y && npm i three@0.160.0 playwright
python3 -m http.server 8765 &            # three.js загружается как ES-модули, нужен локальный сервер
node render.js                           # пишет out/*.png и out/anchors.json (координаты подписей)
python3 prepare.py                       # обрезка и сжатие в web/*.webp, web/anchors.json
```

Затем заменить base64 нужных картинок в `index.html` (и проценты `--x/--y` у подписей `.pin` из `web/anchors.json`).
В Chromium без видеокарты нужен флаг `--use-angle=swiftshader` (уже в `render.js`).
