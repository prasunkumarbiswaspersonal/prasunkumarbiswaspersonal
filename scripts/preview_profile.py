#!/usr/bin/env python3
"""Local preview of this README's HTML and metrics table; no pip dependencies."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import webbrowser

REPO = Path(__file__).resolve().parents[1]
STYLE = """
:root{color-scheme:dark;--bg:#0d1117;--screen:#151b23;--fg:#e6edf3;--line:#30363d;--link:#58a6ff}
@media(prefers-color-scheme:light){:root{color-scheme:light;--bg:#fff;--screen:#f6f8fa;--fg:#1f2328;--line:#d0d7de;--link:#0969da}}
*{box-sizing:border-box}body{margin:0;padding:24px 12px;background:var(--bg);color:var(--fg);font:16px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}
article{max-width:900px;margin:auto;padding:24px;border:1px solid var(--line);border-radius:6px}p{margin:0 0 16px}img{max-width:100%;height:auto;vertical-align:middle}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}hr{border:0;border-top:1px solid var(--line);margin:24px 0}
pre{padding:16px;overflow:auto;font:85%/1.45 ui-monospace,SFMono-Regular,Consolas,monospace;background:var(--screen);border-radius:6px;margin:0 0 16px;white-space:pre}
table{width:100%;border-collapse:collapse;margin-bottom:16px}th,td{padding:10px;border:1px solid var(--line);text-align:left;vertical-align:top}
summary{cursor:pointer;margin-bottom:16px}@media(max-width:600px){article{padding:14px}th,td{padding:6px}}
"""


def render_readme():
    content = (REPO / "README.md").read_text(encoding="utf-8")
    table = re.search(r"(?m)^\| Metrics[^\n]*\n\|[^\n]*\n\|[^\n]*", content)
    if not table:
        raise ValueError("Expected Metrics/Stats table not found")
    rows = table.group().splitlines()
    headers, cells = (rows[n].strip("|").split("|") for n in (0, 2))
    result = "<table><thead><tr>" + "".join(f"<th>{x.strip()}</th>" for x in headers)
    result += "</tr></thead><tbody><tr>" + "".join(f"<td>{x.strip()}</td>" for x in cells)
    result += "</tr></tbody></table>"
    content = content[:table.start()] + result + content[table.end():]
    content = re.sub(r"(?m)^---[ \t]*$", "<hr>", content)
    return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prasun Kumar Biswas — local preview</title><style>' + STYLE + "</style></head><body><article>" + content + "</article></body></html>"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] in ("/", "/index.html"):
            content = render_readme().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            super().do_GET()


def main():
    port = 8765
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"\nPreview: {url}\nRefresh after edits. Ctrl+C stops the preview.\n", flush=True)
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
