import logging
import signal
import sys
import time
from threading import Thread

from users import UserManager
from sessions import SessionManager
from firewall import FirewallManager
from server import CaptivePortalServer

class CaptivePortal:
    """Clase principal que coordina todos los componentes del portal cautivo."""
    
    def __init__(self, interface="eth0", port=80, session_timeout=3600):
        """
        Inicializa el portal cautivo.
        
        Args:
            interface: Interfaz de red a controlar (ej: eth0, wlan0)
            port: Puerto HTTP para el servidor web
            session_timeout: Tiempo de expiración de sesiones en segundos
        """
        self.interface = interface
        self.port = port
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Inicializar componentes
        self.logger.info("Inicializando componentes del portal cautivo...")
        
        self.user_manager = UserManager()
        self.session_manager = SessionManager(session_timeout=session_timeout)
        self.firewall_manager = FirewallManager(interface=interface)
        
        self.server = CaptivePortalServer(
            host='0.0.0.0',
            port=port,
            user_manager=self.user_manager,
            session_manager=self.session_manager,
            firewall_manager=self.firewall_manager
        )
        
        # Hilo para limpieza de sesiones
        self.cleanup_thread = None
        self.running = False