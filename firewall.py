import subprocess
import logging
from threading import Lock

class FirewallManager:
    """Gestiona las reglas de iptables para el portal cautivo."""
    
    def __init__(self, interface="eth0"):
        """
        Inicializa el gestor de firewall.
        
        Args:
            interface: Interfaz de red a controlar (ej: eth0, wlan0)
        """
        self.interface = interface
        self.lock = Lock()
        self.logger = logging.getLogger(__name__)