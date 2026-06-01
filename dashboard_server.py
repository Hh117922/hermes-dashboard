#!/usr/bin/env python3
"""
Hermes 本地看板 — 后端服务器
零依赖（仅用 Python 标准库），读取 agent.log 提供 JSON API
"""
import http.server
import json
import os
import re
import time
from collections import deque

LOG_PATH = os.path.expanduser("~/.hermes/logs/agent.log")
MAX_EVENTS = 100
events = deque(maxlen=MAX_EVENTS)
stats = {"model": "—", "provider": "—", "total_calls": 0, "total_in": 0, "total_out": 0, "total_tokens": 0,
         "last_latency": 0, "last_cache": 0, "tools": [], "session": "—"}

def parse_log():
    """增量解析日志文件"""
    try:
        with open(LOG_PATH) as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                process_line(line.strip())
    except FileNotFoundError:
        pass

def process_line(line):
    m = re.search(r'\[([^\]]+)\].*API call #(\d+): model=(\S+) provider=(\S+) in=(\d+) out=(\d+) total=(\d+) latency=([\d.]+)s cache=(\d+)/(\d+)', line)
    if m:
        sid, num, model, prov, inp, out, total, lat, cache_hit, cache_total = m.groups()
        stats["model"] = model
        stats["provider"] = prov
        stats["total_calls"] = int(num)
        stats["total_in"] += int(inp)
        stats["total_out"] += int(out)
        stats["total_tokens"] += int(total)
        stats["last_latency"] = float(lat)
        stats["last_cache"] = round(int(cache_hit) / int(cache_total) * 100, 1) if int(cache_total) > 0 else 0
        stats["session"] = sid
        ev = {"type": "api", "time": time.strftime("%H:%M:%S"), "model": model, "in": int(inp), "out": int(out),
              "total": int(total), "latency": float(lat), "cache": stats["last_cache"], "call": int(num)}
        events.append(ev)
        return

    m = re.search(r'\[([^\]]+)\].*tool (\S+) completed \(([\d.]+)s, (\d+) chars\)', line)
    if m:
        sid, tool, dur, chars = m.groups()
        ev = {"type": "tool", "time": time.strftime("%H:%M:%S"), "tool": tool, "duration": float(dur), "chars": int(chars)}
        stats["tools"].insert(0, ev)
        stats["tools"] = stats["tools"][:20]
        events.append(ev)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/stats":
            self._json(stats)
        elif self.path == "/api/events":
            self._json(list(events))
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.expanduser("~/hermes-dashboard.html"), encoding="utf-8") as f:
                self.wfile.write(f.read().encode())
        else:
            self.send_response(404)
            self.end_headers()

    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        pass  # 静默

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=parse_log, daemon=True)
    t.start()
    print("Dashboard server: http://localhost:8090")
    http.server.HTTPServer(("127.0.0.1", 8090), Handler).serve_forever()
