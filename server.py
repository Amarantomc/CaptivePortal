"""
Módulo del servidor HTTP del portal cautivo.
Maneja las peticiones HTTP y el endpoint de login.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import logging
from threading import Thread


class CaptivePortalHandler(BaseHTTPRequestHandler):
    """Manejador de peticiones HTTP para el portal cautivo."""
    
    def log_message(self, format, *args):
        """Sobrescribe el método de logging por defecto."""
        logging.info(f"{self.address_string()} - {format % args}")
    
    def _set_headers(self, content_type='text/html', status_code=200):
        """
        Establece las cabeceras HTTP de la respuesta.
        
        Args:
            content_type: Tipo de contenido MIME
            status_code: Código de estado HTTP
        """
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
    
    def _get_client_ip(self):
        """
        Obtiene la dirección IP del cliente.
        
        Returns:
            Dirección IP del cliente
        """
        return self.client_address[0]
    
    def _get_login_page(self, message=""):
        """
        Genera la página HTML de login.
        
        Args:
            message: Mensaje a mostrar al usuario
            
        Returns:
            Código HTML de la página de login
        """
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Cautivo - Iniciar Sesión</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            max-width: 400px;
            width: 100%;
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }}
        .subtitle {{
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        label {{
            display: block;
            color: #555;
            margin-bottom: 5px;
            font-weight: 500;
        }}
        input[type="text"],
        input[type="password"] {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        input[type="text"]:focus,
        input[type="password"]:focus {{
            outline: none;
            border-color: #667eea;
        }}
        button {{
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        button:hover {{
            transform: translateY(-2px);
        }}
        button:active {{
            transform: translateY(0);
        }}
        .message {{
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            text-align: center;
        }}
        .error {{
            background: #fee;
            color: #c33;
            border: 1px solid #fcc;
        }}
        .success {{
            background: #efe;
            color: #3c3;
            border: 1px solid #cfc;
        }}
        .info {{
            background: #def;
            color: #36c;
            border: 1px solid #bcf;
            margin-top: 20px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Portal Cautivo</h1>
        <p class="subtitle">Inicia sesión para acceder a la red</p>
        
        {"<div class='message error'>" + message + "</div>" if message else ""}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Usuario</label>
                <input type="text" id="username" name="username" required autofocus>
            </div>
            
            <div class="form-group">
                <label for="password">Contraseña</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit">Iniciar Sesión</button>
        </form>
        
        <div class="info">
            <strong>Usuarios de prueba:</strong><br>
            admin / admin123<br>
            usuario1 / pass1234<br>
            usuario2 / pass5678
        </div>
    </div>
</body>
</html>
        """
        return html
    
    def _get_success_page(self, username):
        """
        Genera la página HTML de éxito tras el login.
        
        Args:
            username: Nombre del usuario autenticado
            
        Returns:
            Código HTML de la página de éxito
        """
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso Concedido</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }}
        .icon {{
            font-size: 80px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #11998e;
            margin-bottom: 10px;
        }}
        p {{
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }}
        .username {{
            color: #11998e;
            font-weight: bold;
        }}
        .info-box {{
            background: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            text-align: left;
        }}
        .info-box strong {{
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">✅</div>
        <h1>¡Acceso Concedido!</h1>
        <p>
            Bienvenido, <span class="username">{username}</span>.<br>
            Has iniciado sesión exitosamente en la red.
        </p>
        <p>
            Ahora puedes navegar libremente por Internet.<br>
            Tu sesión permanecerá activa durante 1 hora.
        </p>
        <div class="info-box">
            <strong>Información:</strong><br>
            • Tu IP ha sido autorizada para acceder a Internet<br>
            • La sesión expirará automáticamente por inactividad<br>
            • Puedes cerrar esta ventana
        </div>
    </div>
</body>
</html>
        """
        return html
    
    def do_GET(self):
        """Maneja las peticiones HTTP GET."""
        client_ip = self._get_client_ip()
        
        # Obtener referencias a los managers desde el servidor
        session_manager = self.server.session_manager
        
        # Verificar si ya está autenticado
        if session_manager.is_authenticated(client_ip):
            username = session_manager.get_username_by_ip(client_ip)
            self._set_headers()
            self.wfile.write(self._get_success_page(username).encode())
        else:
            # Mostrar página de login
            self._set_headers()
            self.wfile.write(self._get_login_page().encode())
    
    def do_POST(self):
        """Maneja las peticiones HTTP POST."""
        client_ip = self._get_client_ip()
        
        # Leer el contenido del POST
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        # Obtener credenciales
        username = params.get('username', [''])[0]
        password = params.get('password', [''])[0]
        
        # Obtener referencias a los managers desde el servidor
        user_manager = self.server.user_manager
        session_manager = self.server.session_manager
        firewall_manager = self.server.firewall_manager
        
        # Autenticar usuario
        if user_manager.authenticate(username, password):
            # Crear sesión
            session_manager.create_session(client_ip, username)
            
            # Permitir acceso en el firewall
            firewall_manager.allow_ip(client_ip)
            
            logging.info(f"Usuario '{username}' autenticado desde {client_ip}")
            
            # Mostrar página de éxito
            self._set_headers()
            self.wfile.write(self._get_success_page(username).encode())
        else:
            # Autenticación fallida
            logging.warning(f"Intento de login fallido desde {client_ip} con usuario '{username}'")
            
            self._set_headers()
            self.wfile.write(self._get_login_page("Usuario o contraseña incorrectos").encode())


class CaptivePortalServer:
    """Servidor HTTP del portal cautivo con soporte multihilo."""
    
    def __init__(self, host='0.0.0.0', port=80, user_manager=None, 
                 session_manager=None, firewall_manager=None):
        """
        Inicializa el servidor del portal cautivo.
        
        Args:
            host: Dirección en la que escuchar
            port: Puerto en el que escuchar
            user_manager: Instancia de UserManager
            session_manager: Instancia de SessionManager
            firewall_manager: Instancia de FirewallManager
        """
        self.host = host
        self.port = port
        self.user_manager = user_manager
        self.session_manager = session_manager
        self.firewall_manager = firewall_manager
        self.server = None
        self.server_thread = None
    
    def start(self):
        """Inicia el servidor HTTP."""
        self.server = HTTPServer((self.host, self.port), CaptivePortalHandler)
        
        # Adjuntar los managers al servidor para que el handler pueda acceder
        self.server.user_manager = self.user_manager
        self.server.session_manager = self.session_manager
        self.server.firewall_manager = self.firewall_manager
        
        # Ejecutar en un hilo separado
        self.server_thread = Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        
        logging.info(f"Servidor HTTP iniciado en {self.host}:{self.port}")
    
    def stop(self):
        """Detiene el servidor HTTP."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logging.info("Servidor HTTP detenido")

