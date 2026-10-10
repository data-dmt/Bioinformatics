"""Servidor HTTP local de la interfaz web."""

import argparse
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from json import JSONDecodeError
from pathlib import Path
from urllib.parse import urlsplit

from simulator import simulate as run_simulation, validate_dna

WEB_DIR = Path(__file__).resolve().parent / "web"
MAX_BASES = 600
MAX_REQUEST_BYTES = 10_000

STATIC_ROUTES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/diagrams.js": ("diagrams.js", "application/javascript; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
}


def simulate(sequence: str, fragment_size: int = 5) -> dict:
    sequence = validate_dna(sequence)
    if len(sequence) > MAX_BASES:
        raise ValueError(f"Utiliza como máximo {MAX_BASES} bases.")
    return run_simulation(sequence, fragment_size)


class Handler(BaseHTTPRequestHandler):
    server_version = "DogmaCentralCourseSimulator/1.0"

    def respond(self, status: int, data, content_type="application/json; charset=utf-8"):
        if isinstance(data, (dict, list)):
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        elif isinstance(data, str):
            body = data.encode("utf-8")
        else:
            body = data

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "connect-src 'self'; img-src 'self' data:; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'",
        )
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, status: int, message: str):
        self.respond(status, {"error": message})

    def do_GET(self):
        route = STATIC_ROUTES.get(urlsplit(self.path).path)
        if route is None:
            self.send_error_json(404, "Recurso no encontrado.")
            return

        filename, content_type = route
        try:
            content = (WEB_DIR / filename).read_bytes()
        except OSError:
            self.send_error_json(500, "No se ha podido cargar la interfaz.")
            return

        self.respond(200, content, content_type)

    def do_POST(self):
        if urlsplit(self.path).path != "/api/simulate":
            self.send_error_json(404, "Ruta no encontrada.")
            return

        length_header = self.headers.get("Content-Length")
        if length_header is None:
            self.send_error_json(411, "Falta Content-Length.")
            return

        try:
            content_length = int(length_header)
        except ValueError:
            self.send_error_json(400, "Content-Length no válido.")
            return

        if content_length <= 0:
            self.send_error_json(400, "La petición está vacía.")
            return
        if content_length > MAX_REQUEST_BYTES:
            self.send_error_json(413, "La petición es demasiado grande.")
            return
        if self.headers.get_content_type() != "application/json":
            self.send_error_json(415, "La petición debe ser application/json.")
            return

        origin = self.headers.get("Origin")
        port = self.server.server_address[1]
        allowed_origins = {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}
        if origin is not None and origin not in allowed_origins:
            self.send_error_json(403, "Origen no permitido.")
            return

        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, JSONDecodeError):
            self.send_error_json(400, "JSON no válido.")
            return

        if not isinstance(payload, dict) or "sequence" not in payload:
            self.send_error_json(400, "Falta la secuencia de ADN.")
            return

        try:
            result = simulate(payload["sequence"], payload.get("fragment_size", 5))
        except (ValueError, TypeError) as error:
            self.send_error_json(400, str(error))
            return

        self.respond(200, result)

    def log_message(self, format, *args):
        print(f"[WEB] {self.address_string()} - {format % args}")


def valid_port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("El puerto debe ser entero.") from error
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("El puerto debe estar entre 0 y 65535.")
    return port


def main():
    parser = argparse.ArgumentParser(description="Simulador web del dogma central.")
    parser.add_argument("--port", type=valid_port, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError as error:
        parser.exit(1, f"No se puede abrir el puerto {args.port}: {error}\n")

    port = server.server_address[1]
    url = f"http://127.0.0.1:{port}"
    print(f"\nSimulador iniciado en {url}\nPulsa Ctrl+C para detenerlo.\n", flush=True)

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
