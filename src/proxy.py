"""
AI-DRIVEN WEB APPLICATION FIREWALL (WAF)
========================================

A smart proxy that inspects incoming HTTP requests, uses the autonomous
learning system to analyze potential threats, and blocks malicious traffic.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from urllib.parse import urlparse, parse_qs

from src.core.models import EvolvableSeed, DefenseType

class WAFProxy(BaseHTTPRequestHandler):
    """
    The core WAF proxy handler. It intercepts requests, analyzes them with the
    defense system, and either blocks them or forwards them to the target app.
    """

    # Class-level properties to be set by the main orchestrator
    target_host: str = "localhost"
    target_port: int = 5000
    defense_seed: EvolvableSeed = None

    def do_POST(self):
        """Handle POST requests, which are the primary vector for our login form."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Analyze the payload with our AI
        is_malicious, reason = self._analyze_payload(post_data)

        if is_malicious:
            self._block_request(reason)
        else:
            self._forward_request(post_data)

    def _analyze_payload(self, payload: str) -> tuple[bool, str]:
        """
        Uses the EvolvableSeed to analyze the payload against all active defenses.
        """
        if self.defense_seed is None:
            return False, "No defense seed configured"

        # Analyze the payload against every type of defense
        for defense_type in DefenseType:
            blocked, reason = self.defense_seed.test_defense(defense_type, payload)
            if blocked:
                return True, f"Blocked by {defense_type.name}: {reason}"

        return False, "Passed all defenses"

    def _block_request(self, reason: str):
        """Sends a 403 Forbidden response."""
        self.send_response(403)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = f'{{"status": "Request blocked by AI Firewall", "reason": "{reason}"}}'
        self.wfile.write(response.encode('utf-8'))

    def _forward_request(self, post_data: str):
        """Forwards the request to the target application."""
        try:
            target_url = f"http://{self.target_host}:{self.target_port}{self.path}"
            headers = {key: val for key, val in self.headers.items()}

            resp = requests.post(target_url, headers=headers, data=post_data, timeout=5)

            self.send_response(resp.status_code)
            for key, val in resp.headers.items():
                self.send_header(key, val)
            self.end_headers()
            self.wfile.write(resp.content)

        except requests.exceptions.RequestException as e:
            self.send_error(502, f"Proxy error: {e}")

    def log_message(self, format, *args):
        """Suppress default logging to keep the console clean."""
        return

def run_proxy(seed: EvolvableSeed, target_host: str, target_port: int, proxy_port: int):
    """
    Configures and runs the WAF proxy server.
    """
    WAFProxy.defense_seed = seed
    WAFProxy.target_host = target_host
    WAFProxy.target_port = target_port

    server_address = ('', proxy_port)
    httpd = HTTPServer(server_address, WAFProxy)

    print(f"🛡️  AI Firewall (WAF Proxy) started on port {proxy_port}")
    print(f"   -> Forwarding traffic to http://{target_host}:{target_port}")

    # We will run this in a separate thread in the main orchestrator
    return httpd
