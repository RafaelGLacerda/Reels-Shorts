import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import yt_dlp
import shutil  # usado para detectar se o ffmpeg existe


class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Downloader de Vídeos")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # 🎨 Estilo dark mode
        self.bg_color = "#1e1e2f"
        self.fg_color = "#ffffff"
        self.accent_color = "#4CAF50"
        self.entry_bg = "#2b2b3d"
        self.root.configure(bg=self.bg_color)

        # Detecta se ffmpeg está instalado
        self.ffmpeg_instalado = shutil.which("ffmpeg") is not None

        # Variável de pasta de download
        self.download_path = tk.StringVar()
        self.download_path.set(os.getcwd())

        # Título
        tk.Label(root, text="📥 Downloader de Vídeos",
                 font=("Arial", 16, "bold"),
                 fg=self.accent_color, bg=self.bg_color).pack(pady=15)

        tk.Label(root, text="YouTube · TikTok · Instagram · Facebook",
                 font=("Arial", 10),
                 fg="#cccccc", bg=self.bg_color).pack(pady=2)

        # Campo de links
        tk.Label(root, text="Cole os links (um por linha):",
                 fg=self.fg_color, bg=self.bg_color,
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=5)

        self.text_links = tk.Text(root, height=7, width=80, wrap="word",
                                  bg=self.entry_bg, fg=self.fg_color, insertbackground="white",
                                  relief="flat", font=("Consolas", 10))
        self.text_links.pack(padx=15, pady=5)

        # Botão de escolher pasta
        tk.Button(root, text="📂 Escolher pasta de destino",
                  command=self.choose_folder,
                  bg="#3a3a52", fg="white", relief="flat",
                  activebackground=self.accent_color, activeforeground="white",
                  font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=5)

        self.label_path = tk.Label(root, text=f"Pasta atual: {self.download_path.get()}",
                                   fg="#87CEFA", bg=self.bg_color,
                                   wraplength=650, justify="left")
        self.label_path.pack(pady=3)

        # Botão de iniciar download
        tk.Button(root, text="⬇️ Baixar Vídeos", command=self.start_download,
                  bg=self.accent_color, fg="white", relief="flat",
                  activebackground="#45a049", activeforeground="white",
                  font=("Arial", 11, "bold"), padx=15, pady=8).pack(pady=10)

        # Caixa de status
        tk.Label(root, text="Status:",
                 fg=self.fg_color, bg=self.bg_color,
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=15)

        self.text_status = tk.Text(root, height=15, width=80, state="disabled", wrap="word",
                                   bg=self.entry_bg, fg=self.fg_color,
                                   insertbackground="white", relief="flat",
                                   font=("Consolas", 9))
        self.text_status.pack(padx=15, pady=5)

        # Aviso sobre FFmpeg
        if not self.ffmpeg_instalado:
            self.log_status("⚠️ FFmpeg não encontrado. Baixando vídeos no melhor formato único disponível.\n")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path.set(folder)
            self.label_path.config(text=f"Pasta atual: {folder}")

    def log_status(self, message):
        self.text_status.config(state="normal")
        self.text_status.insert(tk.END, message + "\n")
        self.text_status.see(tk.END)
        self.text_status.config(state="disabled")

    def start_download(self):
        links = self.text_links.get("1.0", tk.END).strip().split("\n")
        links = [l.strip() for l in links if l.strip()]
        if not links:
            messagebox.showwarning("Aviso", "Insira pelo menos um link!")
            return
        threading.Thread(target=self.download_videos, args=(links,), daemon=True).start()

    def download_videos(self, links):
        self.log_status("🚀 Iniciando downloads...\n")
        for link in links:
            self.log_status(f"Baixando: {link}")
            try:
                if self.ffmpeg_instalado:
                    ydl_opts = {
                        'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
                        'format': 'bestvideo+bestaudio/best',
                        'merge_output_format': 'mp4',
                        'quiet': True,
                        'noprogress': True,
                    }
                else:
                    ydl_opts = {
                        'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
                        'format': 'best',
                        'quiet': True,
                        'noprogress': True,
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                self.log_status(f"✅ Concluído: {link}\n")
            except Exception as e:
                self.log_status(f"❌ Erro ao baixar {link}: {str(e)}\n")

        self.log_status("🎉 Todos os downloads foram finalizados!")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
