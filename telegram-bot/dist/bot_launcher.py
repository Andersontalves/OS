"""
Launcher do Bot Telegram com Interface Grafica
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import sys
import os
import queue
import time
from datetime import datetime

# ============================================
# DETECTAR PASTA DO EXECUTAVEL
# ============================================
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    EXE_NAME = os.path.basename(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_NAME = "python.exe"

# ============================================
# VERIFICACAO DE INSTANCIA UNICA
# ============================================
def count_running_instances():
    """Conta instancias do executavel rodando"""
    try:
        result = subprocess.run(
            ['tasklist', '/FI', f'IMAGENAME eq {EXE_NAME}', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            creationflags=0x08000000  # CREATE_NO_WINDOW
        )
        lines = [l for l in result.stdout.strip().split('\n') if EXE_NAME.lower() in l.lower()]
        return len(lines)
    except:
        return 1

def check_already_running():
    """Retorna True se ja existe outra instancia"""
    count = count_running_instances()
    return count > 1


class BotLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Telegram - Sistema O.S")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Variaveis
        self.process = None
        self.running = False
        self.log_queue = queue.Queue()
        self.error_count = 0
        self.last_error_time = None
        
        # Criar interface
        self.create_widgets()
        
        # Iniciar atualizacao de logs
        self.update_logs()
        
        # Fechar processo quando fechar janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # FORCAR JANELA VISIVEL
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(500, lambda: self.root.attributes('-topmost', False))
        self.root.focus_force()
        
        # Auto-iniciar bot
        self.root.after(1000, self.start_bot)
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titulo e Status
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="Bot Telegram - Sistema O.S", 
                  font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="Parado")
        ttk.Label(title_frame, textvariable=self.status_var,
                  font=("Segoe UI", 12)).pack(side=tk.RIGHT)
        
        # Botoes
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_btn = ttk.Button(btn_frame, text="Iniciar", command=self.start_bot, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_btn = ttk.Button(btn_frame, text="Parar", command=self.stop_bot, width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.restart_btn = ttk.Button(btn_frame, text="Reiniciar", command=self.restart_bot, width=15)
        self.restart_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(btn_frame, text="Limpar Logs", command=self.clear_logs, width=15).pack(side=tk.RIGHT)
        
        # Logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 10),
                                                   bg="#1e1e1e", fg="#ffffff")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_text.tag_configure("info", foreground="#4fc3f7")
        self.log_text.tag_configure("success", foreground="#81c784")
        self.log_text.tag_configure("warning", foreground="#ffb74d")
        self.log_text.tag_configure("error", foreground="#e57373")
        self.log_text.tag_configure("timestamp", foreground="#9e9e9e")
        
        # Rodape
        ttk.Label(main_frame, text="Bot conecta na API do Render. Dados salvos no Supabase.",
                  font=("Segoe UI", 9), foreground="gray").pack(fill=tk.X, pady=(10, 0))
    
    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put((timestamp, message, level))
    
    def update_logs(self):
        try:
            while True:
                timestamp, message, level = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
                self.log_text.insert(tk.END, f"{message}\n", level)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.update_logs)
    
    def read_output(self, pipe, is_error=False):
        try:
            for line in iter(pipe.readline, ''):
                if line:
                    line = line.strip()
                    if "erro" in line.lower() or "error" in line.lower() or "falha" in line.lower():
                        level = "error"
                        # Incrementar contador de erros
                        if hasattr(self, 'error_count'):
                            self.error_count += 1
                            self.last_error_time = time.time()
                    elif "warning" in line.lower():
                        level = "warning"
                    elif "sucesso" in line.lower() or "success" in line.lower():
                        level = "success"
                    else:
                        level = "error" if is_error else "info"
                    self.log(line, level)
        except:
            pass
    
    def start_bot(self):
        if self.running:
            self.log("Bot ja esta rodando!", "warning")
            return
        
        self.log("Iniciando bot...", "info")
        
        try:
            env_path = os.path.join(APP_DIR, ".env")
            bot_path = os.path.join(APP_DIR, "bot.py")
            
            if not os.path.exists(env_path):
                self.log("ERRO: .env nao encontrado!", "error")
                messagebox.showerror("Erro", f"Arquivo .env nao encontrado em:\n{APP_DIR}")
                return
            
            if not os.path.exists(bot_path):
                self.log("ERRO: bot.py nao encontrado!", "error")
                return
            
            self.log("Arquivos encontrados!", "success")
            
            self.process = subprocess.Popen(
                [sys.executable, bot_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=APP_DIR,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
                creationflags=0x08000000  # CREATE_NO_WINDOW
            )
            
            self.running = True
            self.status_var.set("[ONLINE] Rodando")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.log("Bot iniciado!", "success")
            
            threading.Thread(target=self.read_output, args=(self.process.stdout, False), daemon=True).start()
            threading.Thread(target=self.read_output, args=(self.process.stderr, True), daemon=True).start()
            threading.Thread(target=self.monitor_process, daemon=True).start()
            
            # Monitorar se está em loop de erro (detectar múltiplos erros em pouco tempo)
            self.error_count = 0
            self.last_error_time = None
            threading.Thread(target=self.detect_error_loop, daemon=True).start()
            
        except Exception as e:
            self.log(f"Erro: {e}", "error")
            self.running = False
    
    def monitor_process(self):
        """Monitora o processo e detecta loops"""
        if self.process:
            self.process.wait()
            if self.running:
                self.running = False
                self.log("Bot parou inesperadamente!", "error")
                self.log("Se continuar dando erro, verifique o token do Telegram.", "warning")
                self.root.after(0, self.update_ui_stopped)
    
    def update_ui_stopped(self):
        self.status_var.set("[OFFLINE] Parado")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def stop_bot(self):
        if not self.running:
            return
        self.log("Parando bot...", "info")
        try:
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=5)
        except:
            if self.process:
                self.process.kill()
        self.running = False
        self.process = None
        self.status_var.set("[OFFLINE] Parado")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("Bot parado.", "info")
    
    def restart_bot(self):
        self.log("Reiniciando...", "info")
        self.stop_bot()
        time.sleep(1)
        self.start_bot()
    
    def detect_error_loop(self):
        """Detecta se o bot está em loop de erros"""
        while self.running:
            time.sleep(5)
            # Se tiver mais de 3 erros em 30 segundos, parar
            if self.error_count >= 3:
                self.log("ERRO: Bot em loop de erros! Parando automaticamente.", "error")
                self.root.after(0, self.stop_bot)
                break
            # Reset contador a cada 30 segundos
            if self.last_error_time and (time.time() - self.last_error_time) > 30:
                self.error_count = 0
    
    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)
    
    def on_closing(self):
        if self.running:
            if messagebox.askokcancel("Fechar", "Parar bot e fechar?"):
                self.stop_bot()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    # Verificar instancia unica
    if check_already_running():
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Aviso", "Bot ja esta aberto!\n\nProcure na barra de tarefas ou\nfinalize no Gerenciador de Tarefas.")
        root.destroy()
        return
    
    # Criar janela principal
    root = tk.Tk()
    root.withdraw()  # Esconde temporariamente
    
    style = ttk.Style()
    style.theme_use('clam')
    
    app = BotLauncher(root)
    
    # Mostra a janela
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    main()
