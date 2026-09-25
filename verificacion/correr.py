import json, sys
from playwright.sync_api import sync_playwright
js = open(sys.argv[1]).read(); cfg = json.loads(sys.argv[2]); out = sys.argv[3]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:47900/"); pg.wait_for_timeout(1500)
    r = pg.evaluate(js, cfg)
    json.dump(r, open(out, "w"), ensure_ascii=False)
    print("errores de página:", errs[:3])
    b.close()
