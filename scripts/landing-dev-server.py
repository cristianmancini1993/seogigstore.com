#!/usr/bin/env python3
"""Static server with JSON save API for landing editor."""

from __future__ import annotations

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get('LP_PORT', '8765'))


class LandingHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if not self.path.startswith('/api/save-json'):
            self.send_error(404)
            return

        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode('utf-8'))
            rel_path = payload['path']
            data = payload['data']
        except (json.JSONDecodeError, KeyError, TypeError):
            self.send_error(400, 'Invalid payload')
            return

        rel_path = unquote(rel_path).lstrip('/')
        if '..' in rel_path or not rel_path.startswith('content/') or not rel_path.endswith('.json'):
            self.send_error(403, 'Forbidden path')
            return

        target = ROOT / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        body = json.dumps({'ok': True, 'path': rel_path}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    os.chdir(ROOT)
    server = ThreadingHTTPServer(('127.0.0.1', PORT), LandingHandler)
    print(f'Landing dev server: http://127.0.0.1:{PORT}')
    print(f'Editor: http://127.0.0.1:{PORT}/it/fresh-air-pro/editor.html')
    server.serve_forever()
