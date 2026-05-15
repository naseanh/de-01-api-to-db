"""
Simple HTTP metrics server for Prometheus-style metrics exposure.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

from src.metrics_exporter import generate_prometheus_metrics


HOST = "0.0.0.0"
PORT = 8000


class MetricsHandler(BaseHTTPRequestHandler):
    """
    HTTP handler for metrics endpoint.
    """

    def do_GET(self):  # pylint: disable=invalid-name
        """
        Handle HTTP GET requests.
        """

        if self.path == "/metrics":
            metrics_output = generate_prometheus_metrics()

            self.send_response(200)
            self.send_header(
                "Content-type",
                "text/plain; version=0.0.4",
            )
            self.end_headers()

            self.wfile.write(metrics_output.encode())

        else:
            self.send_response(404)
            self.end_headers()


def start_metrics_server():
    """
    Start HTTP metrics server.
    """

    server = HTTPServer((HOST, PORT), MetricsHandler)

    print(f"Metrics server running at http://{HOST}:{PORT}/metrics")

    server.serve_forever()


if __name__ == "__main__":
    start_metrics_server()
