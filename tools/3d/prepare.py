"""Обрезка, уменьшение и сжатие рендеров в WebP + координаты подписей на макете.
Запуск из tools/3d после `node render.js`: python3 prepare.py"""
from PIL import Image
import json, os
os.makedirs('web', exist_ok=True)
spec = {'hero': 1600, 'fire': 1100, 'video': 1100, 'access': 1100, 'detector': 760, 'camera': 760, 'reader': 760, 'panel': 760}
for n, w in spec.items():
    im = Image.open('out/%s.png' % n).convert('RGBA')
    bb = None
    if n in ('hero', 'detector', 'camera', 'reader', 'panel'):
        bb = im.getchannel('A').point(lambda a: 255 if a > 6 else 0).getbbox(); pad = int(max(im.size) * .03)
        bb = (max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.size[0], bb[2] + pad), min(im.size[1], bb[3] + pad)); im = im.crop(bb)
        if n == 'hero':
            a = json.load(open('out/anchors.json')); W, H = bb[2] - bb[0], bb[3] - bb[1]
            json.dump({k: [round((x - bb[0]) / W * 100, 1), round((y - bb[1]) / H * 100, 1)] for k, (x, y) in a.items()}, open('web/anchors.json', 'w'))
    if n in ('detector', 'camera', 'reader', 'panel'):
        s = max(im.size); c = Image.new('RGBA', (s, s), (0, 0, 0, 0)); c.paste(im, ((s - im.size[0]) // 2, (s - im.size[1]) // 2)); im = c
    im = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS); im.save('web/%s.webp' % n, 'WEBP', quality=80, method=6)
