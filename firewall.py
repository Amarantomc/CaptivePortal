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
    
    def _run_command(self, command):
        """
        Ejecuta un comando del sistema.
        
        Args:
            command: Lista con el comando y sus argumentos
            
        Returns:
            True si el comando se ejecutó exitosamente, False en caso contrario
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                self.logger.error(f"Error ejecutando comando: {' '.join(command)}")
                self.logger.error(f"Error: {result.stderr}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Excepción al ejecutar comando: {e}")
            return False
    
    def setup_initial_rules(self):
        """
        Configura las reglas iniciales del firewall.
        Bloquea todo el tráfico de forwarding por defecto.
        """
        with self.lock:
            # Permitir tráfico local
            self._run_command(["iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"])
            
            # Permitir conexiones establecidas y relacionadas
            self._run_command([
                "iptables", "-A", "FORWARD", "-m", "state",
                "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"
            ])
            
            # Bloquear todo el forwarding por defecto (política DROP)
            self._run_command(["iptables", "-P", "FORWARD", "DROP"])
            
            # Habilitar NAT para las conexiones autorizadas
            self._run_command([
                "iptables", "-t", "nat", "-A", "POSTROUTING",
                "-o", self.interface, "-j", "MASQUERADE"
            ])
            
            self.logger.info("Reglas iniciales de firewall configuradas")
    
    def allow_ip(self, ip_address):
        """
        Permite el tráfico para una dirección IP específica.
        
        Args:
            ip_address: Dirección IP a permitir
            
        Returns:
            True si se añadió la regla exitosamente
        """
        with self.lock:
            # Permitir forwarding desde esta IP
            success = self._run_command([
                "iptables", "-I", "FORWARD", "1",
                "-s", ip_address, "-j", "ACCEPT"
            ])
            
            if success:
                self.logger.info(f"IP permitida: {ip_address}")
            
            return success