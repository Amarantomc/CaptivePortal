import time
from threading import Lock
from datetime import datetime, timedelta

class SessionManager:
    """Gestiona las sesiones de usuarios autenticados."""
    
    def __init__(self, session_timeout=3600):
        """
        Inicializa el gestor de sesiones.
        
        Args:
            session_timeout: Tiempo de expiración de sesión en segundos (default: 1 hora)
        """
        self.sessions = {}  # {ip_address: {'username': str, 'login_time': float, 'last_activity': float}}
        self.lock = Lock()
        self.session_timeout = session_timeout
    
    def create_session(self, ip_address, username):
        """
        Crea una nueva sesión para un usuario autenticado.
        
        Args:
            ip_address: Dirección IP del usuario
            username: Nombre de usuario autenticado
            
        Returns:
            True si se creó la sesión exitosamente
        """
        with self.lock:
            current_time = time.time()
            self.sessions[ip_address] = {
                'username': username,
                'login_time': current_time,
                'last_activity': current_time
            }
            return True
    
    def is_authenticated(self, ip_address):
        """
        Verifica si una IP tiene una sesión activa válida.
        
        Args:
            ip_address: Dirección IP a verificar
            
        Returns:
            True si la sesión existe y es válida, False en caso contrario
        """
        with self.lock:
            if ip_address not in self.sessions:
                return False
            
            session = self.sessions[ip_address]
            current_time = time.time()
            
            # Verificar si la sesión ha expirado
            if current_time - session['last_activity'] > self.session_timeout:
                del self.sessions[ip_address]
                return False
            
            # Actualizar última actividad
            session['last_activity'] = current_time
            return True
    
    def get_session_info(self, ip_address):
        """
        Obtiene información de la sesión de una IP.
        
        Args:
            ip_address: Dirección IP
            
        Returns:
            Diccionario con información de la sesión o None si no existe
        """
        with self.lock:
            if ip_address not in self.sessions:
                return None
            
            session = self.sessions[ip_address]
            return {
                'username': session['username'],
                'login_time': datetime.fromtimestamp(session['login_time']).strftime('%Y-%m-%d %H:%M:%S'),
                'last_activity': datetime.fromtimestamp(session['last_activity']).strftime('%Y-%m-%d %H:%M:%S'),
                'active': time.time() - session['last_activity'] <= self.session_timeout
            }
    
    def end_session(self, ip_address):
        """
        Termina la sesión de una IP.
        
        Args:
            ip_address: Dirección IP
            
        Returns:
            True si se terminó la sesión, False si no existía
        """
        with self.lock:
            if ip_address in self.sessions:
                del self.sessions[ip_address]
                return True
            return False
    
    def get_all_sessions(self):
        """
        Obtiene todas las sesiones activas.
        
        Returns:
            Diccionario con todas las sesiones {ip: info}
        """
        with self.lock:
            result = {}
            current_time = time.time()
            
            # Crear copia de las sesiones para no mantener el lock demasiado tiempo
            for ip, session in list(self.sessions.items()):
                if current_time - session['last_activity'] <= self.session_timeout:
                    result[ip] = {
                        'username': session['username'],
                        'login_time': datetime.fromtimestamp(session['login_time']).strftime('%Y-%m-%d %H:%M:%S'),
                        'last_activity': datetime.fromtimestamp(session['last_activity']).strftime('%Y-%m-%d %H:%M:%S')
                    }
            
            return result
    
    def cleanup_expired_sessions(self):
        """
        Limpia las sesiones expiradas.
        
        Returns:
            Lista de IPs cuyas sesiones fueron eliminadas
        """
        with self.lock:
            current_time = time.time()
            expired_ips = []
            
            for ip, session in list(self.sessions.items()):
                if current_time - session['last_activity'] > self.session_timeout:
                    expired_ips.append(ip)
                    del self.sessions[ip]
            
            return expired_ips
    
    def get_session_count(self):
        """
        Obtiene el número de sesiones activas.
        
        Returns:
            Número de sesiones activas
        """
        with self.lock:
            return len(self.sessions)
    
    def get_username_by_ip(self, ip_address):
        """
        Obtiene el nombre de usuario asociado a una IP.
        
        Args:
            ip_address: Dirección IP
            
        Returns:
            Nombre de usuario o None si no existe sesión
        """
        with self.lock:
            if ip_address in self.sessions:
                return self.sessions[ip_address]['username']
            return None