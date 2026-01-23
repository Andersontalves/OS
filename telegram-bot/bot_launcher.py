"""
Launcher do Bot Telegram com Interface Gráfica
- Mostra logs em tempo real
- Botão para iniciar/parar/reiniciar
- Fácil de usar
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

class BotLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Telegram - Sistema O.S")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configurar ícone se existir
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Variáveis
        self.process = None
        self.running = False
        self.log_queue = queue.Queue()
        
        # Criar interface
        self.create_widgets()
        
        # Iniciar thread de atualização de logs
        self.update_logs()
        
        # Fechar processo quando fechar janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Auto-iniciar bot
        self.root.after(1000, self.start_bot)
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            title_frame, 
            text="Bot Telegram - Sistema O.S",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Status
        self.status_var = tk.StringVar(value="Parado")
        self.status_label = ttk.Label(
            title_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 12)
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Frame de botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botão Iniciar
        self.start_btn = ttk.Button(
            button_frame,
            text="Iniciar",
            command=self.start_bot,
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão Parar
        self.stop_btn = ttk.Button(
            button_frame,
            text="Parar",
            command=self.stop_bot,
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão Reiniciar
        self.restart_btn = ttk.Button(
            button_frame,
            text="Reiniciar",
            command=self.restart_bot,
            width=15
        )
        self.restart_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão Limpar Logs
        self.clear_btn = ttk.Button(
            button_frame,
            text="Limpar Logs",
            command=self.clear_logs,
            width=15
        )
        self.clear_btn.pack(side=tk.RIGHT)
        
        # Área de Logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags de cores
        self.log_text.tag_configure("info", foreground="#4fc3f7")
        self.log_text.tag_configure("success", foreground="#81c784")
        self.log_text.tag_configure("warning", foreground="#ffb74d")
        self.log_text.tag_configure("error", foreground="#e57373")
        self.log_text.tag_configure("timestamp", foreground="#9e9e9e")
        
        # Info no rodapé
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        info_label = ttk.Label(
            info_frame,
            text="O bot conecta na API do Render. Os dados sao salvos no Supabase.",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        info_label.pack(side=tk.LEFT)
    
    def log(self, message, level="info"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put((timestamp, message, level))
    
    def update_logs(self):
        """Atualiza a área de logs com mensagens da fila"""
        try:
            while True:
                timestamp, message, level = self.log_queue.get_nowait()
                
                self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
                self.log_text.insert(tk.END, f"{message}\n", level)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Agendar próxima atualização
        self.root.after(100, self.update_logs)
    
    def read_output(self, pipe, is_error=False):
        """Lê saída do processo em thread separada"""
        try:
            for line in iter(pipe.readline, ''):
                if line:
                    line = line.strip()
                    # Determinar nível baseado no conteúdo
                    if "erro" in line.lower() or "error" in line.lower():
                        level = "error"
                    elif "aviso" in line.lower() or "warning" in line.lower():
                        level = "warning"
                    elif "sucesso" in line.lower() or "success" in line.lower():
                        level = "success"
                    else:
                        level = "error" if is_error else "info"
                    
                    self.log(line, level)
        except:
            pass
    
    def start_bot(self):
        """Inicia o bot"""
        if self.running:
            self.log("Bot ja esta rodando!", "warning")
            return
        
        self.log("Iniciando bot...", "info")
        
        try:
            # Verificar se .env existe
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            if not os.path.exists(env_path):
                self.log("ERRO: Arquivo .env nao encontrado!", "error")
                self.log("Crie o arquivo .env com as configuracoes necessarias.", "error")
                messagebox.showerror(
                    "Erro", 
                    "Arquivo .env nao encontrado!\n\n"
                    "Crie o arquivo telegram-bot/.env com:\n"
                    "TELEGRAM_BOT_TOKEN=seu_token\n"
                    "API_BASE_URL=https://os-sistema-api.onrender.com\n"
                    "CLOUDINARY_URL=sua_url"
                )
                return
            
            # Caminho do bot.py
            bot_path = os.path.join(os.path.dirname(__file__), "bot.py")
            
            # Iniciar processo
            self.process = subprocess.Popen(
                [sys.executable, bot_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=os.path.dirname(__file__),
                env={**os.environ, "PYTHONUNBUFFERED": "1"}
            )
            
            self.running = True
            self.status_var.set("[ONLINE] Rodando")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.log("Bot iniciado com sucesso!", "success")
            
            # Threads para ler stdout e stderr
            threading.Thread(
                target=self.read_output, 
                args=(self.process.stdout, False),
                daemon=True
            ).start()
            
            threading.Thread(
                target=self.read_output, 
                args=(self.process.stderr, True),
                daemon=True
            ).start()
            
            # Thread para monitorar processo
            threading.Thread(
                target=self.monitor_process,
                daemon=True
            ).start()
            
        except Exception as e:
            self.log(f"Erro ao iniciar bot: {e}", "error")
            self.running = False
    
    def monitor_process(self):
        """Monitora se o processo ainda está rodando"""
        if self.process:
            self.process.wait()
            
            if self.running:  # Se não foi parado manualmente
                self.running = False
                self.log("Bot parou inesperadamente!", "error")
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_ui_stopped)
    
    def update_ui_stopped(self):
        """Atualiza UI quando bot para"""
        self.status_var.set("[OFFLINE] Parado")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def stop_bot(self):
        """Para o bot"""
        if not self.running:
            self.log("Bot nao esta rodando.", "warning")
            return
        
        self.log("Parando bot...", "info")
        
        try:
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
        except Exception as e:
            self.log(f"Erro ao parar: {e}", "error")
        
        self.running = False
        self.process = None
        self.status_var.set("[OFFLINE] Parado")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.log("Bot parado.", "info")
    
    def restart_bot(self):
        """Reinicia o bot"""
        self.log("Reiniciando bot...", "info")
        self.stop_bot()
        time.sleep(1)
        self.start_bot()
    
    def clear_logs(self):
        """Limpa a área de logs"""
        self.log_text.delete(1.0, tk.END)
    
    def on_closing(self):
        """Chamado quando fecha a janela"""
        if self.running:
            if messagebox.askokcancel("Fechar", "O bot esta rodando. Deseja parar e fechar?"):
                self.stop_bot()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    # Configurar encoding para Windows
    if sys.platform == 'win32':
        import ctypes
        try:
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        except:
            pass
    
    root = tk.Tk()
    
    # Estilo
    style = ttk.Style()
    style.theme_use('clam')
    
    app = BotLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
