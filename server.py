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