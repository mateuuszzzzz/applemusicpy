from abc import ABCMeta, abstractmethod
from calendar import c
import jwt
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

from applemusicpy.exceptions import AppleMusicAuthException

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
            self.server.get_count = self.server.get_count + 1
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.server.source.format(token=self.server.developer_token,
                                                        endpoint=self.server.endpoint).encode('UTF-8'))

    def do_POST(self):
        if self.path == '/token':
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.server.user_token = self.rfile.read(int(self.headers['Content-Length'])).decode()
            self.wfile.write(str({'details': 'success'}).encode('UTF-8'))

class AuthBase(metaclass = ABCMeta):
    """
    AuthBase is useful when one wants to implement custom Auth object
    All abstract methods are necessary because they're used by Client
    """
    @abstractmethod
    def generate_developer_token(self):
        pass

    @abstractmethod
    def generate_user_token(self):
        pass

    @abstractmethod
    def get_developer_token(self):
        pass

    @abstractmethod
    def get_user_token(self):
        pass

    @abstractmethod
    def is_token_expired(self):
        pass

class Auth(AuthBase):
    """
    Auth class provides methods that enables authentication
    """
    def __init__(self,
                secret_key=None,
                key_id=None,
                team_id=None,
                session_length=24,
                address = '127.0.0.1',
                port = 8000
                ):
        
        self.secret_key = secret_key
        self.key_id = key_id
        self.team_id = team_id
        self.session_length = session_length
        self.developer_token = None
        self.user_token = None
        self.exp = None
        self.address = address
        self.port = port

    def generate_developer_token(self):
        self.exp = datetime.now() + timedelta(hours=self.session_length)

        headers = {
            'alg': 'ES256',
            'kid': self.key_id
        }

        payload = {
            'iss': self.team_id,
            'iat': int(datetime.now().timestamp()),
            'exp': int(self.exp.timestamp())
        }

        self.developer_token = jwt.encode(payload, self.secret_key, algorithm='ES256', headers=headers)
        return self.developer_token

    def generate_user_token(self):
        if self.developer_token is None or self.is_token_expired():
            self.generate_developer_token()

        source = \
        """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset=utf-8>
            <link rel="shortcut icon" href="#" />
            <title>applemusicpy authorization</title>
        </head>
        <body>
            <p>Authorization</p>
            <button onclick="authorize()">Click to authorize</button>
            <script src="https://js-cdn.music.apple.com/musickit/v1/musickit.js"></script>
            <script> 

                function authorize() {{

                    devtoken = '{token}';
                    const music = MusicKit.configure({{
                        developerToken: devtoken,
                        app: {{
                            name: 'applemusicpy',
                            build: '1.0.0'
                        }}
                    }});

                    music.authorize().then(musicUserToken => {{
                        const response = fetch('{endpoint}',{{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'text/html'
                            }},
                            body: musicUserToken
                        }});
                    }});
                }}

            </script>
        </body>
        </html>
        """

        auth_url = 'http://' + self.address + ':' + str(self.port)
        server = self._start_http_server(RequestHandler, source, auth_url + '/token')

        try:
            webbrowser.open(auth_url, new=1)
            print(f"Opened {auth_url} in your browser")
        except webbrowser.Error:
            print(f"Paste following url in your browser: {auth_url}")

        server.handle_request()
        server.handle_request()

        if server.get_count == 2:
            server.handle_request() # Some browsers might load page twice

        if server.user_token:
            self.user_token = server.user_token
        else:
            raise AppleMusicAuthException("Cannot retrieve user token")

    def get_developer_token(self):
        return self.developer_token

    def get_user_token(self):
        return self.user_token

    def is_token_expired(self):
        if self.exp is None:
            return False
        return not datetime.now() <= self.exp

    def _start_http_server(self, handler, source, endpoint):
        server = HTTPServer((self.address, self.port), handler)

        server.allow_reuse_address = True

        server.developer_token = self.developer_token
        server.source = source
        server.endpoint = endpoint
        server.user_token = None
        server.get_count = 0

        return server
