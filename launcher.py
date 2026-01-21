import subprocess
import time
import sys
import os
import webbrowser
import threading

# Configuration
# Use explicit paths based on where launcher.py runs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BOT_DIR = os.path.join(BASE_DIR, "telegram-bot")

# Global processes list
processes = []

def log(service, message):
    print(f"[{service}] {message}")

def stream_output(process, prefix):
    """Lê a saída do processo e imprime com prefixo (opcional, mas complexo com cores)
    Aqui vamos deixar fluir direto para o stdout para não bloquear."""
    pass

def start_service(command_list, cwd, name):
    try:
        log("LAUNCHER", f"Iniciando {name}...")
        
        # Set environment variable to force unbuffered output
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        # We start the process and let it inherit stdout/stderr
        # This means all logs will mix in the main window
        process = subprocess.Popen(
            command_list,
            cwd=cwd,
            env=env,
            shell=False  # Better for control
            # stdout=None, stderr=None means inherit from parent
        )
        processes.append((name, process))
        return process
    except Exception as e:
        log("ERROR", f"Falha ao iniciar {name}: {e}")
        return None

def kill_all():
    print("\n" + "="*50)
    print("🛑 ENCERRANDO SISTEMA...")
    print("="*50)
    for name, p in processes:
        if p.poll() is None: # If still running
            log("LAUNCHER", f"Matando {name}...")
            p.terminate() # SIGTERM
            
            # Additional force kill for Windows if needed
            if sys.platform == 'win32':
                # Give it a second
                time.sleep(0.5)
                if p.poll() is None:
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    sys.exit(0)

def main():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"""
    ╔════════════════════════════════════════════════════╗
    ║           SISTEMA DE ORDENS DE SERVIÇO             ║
    ╠════════════════════════════════════════════════════╣
    ║  1. Backend API (Porta 8000)                       ║
    ║  2. Frontend Web (Porta 8080)                      ║
    ║  3. Bot Telegram                                   ║
    ╚════════════════════════════════════════════════════╝
    """)
    print(">> Pressione CTRL+C para parar tudo <<\n")

    python_exe = sys.executable

    # 1. Start Backend
    # python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    backend_cmd = [python_exe, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    start_service(backend_cmd, BACKEND_DIR, "BACKEND")
    
    time.sleep(2) # Give backend a head start

    # 2. Start Frontend
    # python -m http.server 8080
    frontend_cmd = [python_exe, "-m", "http.server", "8080"]
    start_service(frontend_cmd, FRONTEND_DIR, "FRONTEND")

    # 3. Start Bot
    # python bot.py
    bot_cmd = [python_exe, "bot.py"]
    start_service(bot_cmd, BOT_DIR, "BOT-TELEGRAM")

    print("\n✅ TUDO RODANDO! OS LOGS APARECERÃO ABAIXO:\n")
    print("-" * 60)

    # Open browser
    try:
        webbrowser.open("http://localhost:8080")
    except:
        pass

    try:
        while True:
            time.sleep(1)
            # Check for crashes
            for name, p in processes:
                code = p.poll()
                if code is not None:
                    print(f"\n❌ OPPS! {name} PAROU COM CÓDIGO {code}")
                    # If it's the backend, we probably should stop everything
                    if name == "BACKEND":
                        raise KeyboardInterrupt
                    
    except KeyboardInterrupt:
        kill_all()

if __name__ == "__main__":
    main()
