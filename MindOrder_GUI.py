import customtkinter as ctk
import os
import shutil
from datetime import datetime
import webbrowser
import ctypes
from tkinter import filedialog, messagebox

# ==========================================
# CONFIGURACIÓN ESTÉTICA GLOBAL
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
COLOR_NEON = "#00adb5"

# Diccionario de idiomas y textos estáticos
TEXTOS = {
    "Español": {
        "titulo": "MindOrder v1.1.0 - Professional Edition",
        "limpieza": "🧹 LIMPIEZA",
        "sistema": "🛠️ SISTEMA",
        "ajustes": "⚙️ AJUSTES",
        "creador": "👤 CREADOR",
        "m_estandar": "MODO ESTÁNDAR (AUTO)",
        "m_quirurgico": "MODO QUIRÚRGICO (MANUAL)",
        "btn_pro": "ACTUALIZAR A PRO",
        "modo_claro": "Modo Claro",
        "idioma": "Idioma:",
        "log_inicio": ">>> SYSTEM ONLINE. El tablero está en tus manos.",
        "footer": "© 2026 Poposky Gomez | MindOrder Professional Edition. Todos los derechos reservados.",
        "creador_info": "DESARROLLADO POR POPOSKY GOMEZ\nVersión: 1.1.0\nStatus: Estable\n© 2026 Todos los derechos reservados."
    },
    "English": {
        "titulo": "MindOrder v1.1.0 - Professional Edition",
        "limpieza": "🧹 CLEANUP",
        "sistema": "🛠️ SYSTEM",
        "ajustes": "⚙️ SETTINGS",
        "creador": "👤 CREATOR",
        "m_estandar": "STANDARD MODE (AUTO)",
        "m_quirurgico": "SURGICAL MODE (MANUAL)",
        "btn_pro": "UPGRADE TO PRO",
        "modo_claro": "Light Mode",
        "idioma": "Language:",
        "log_inicio": ">>> SYSTEM ONLINE. The board is in your hands.",
        "footer": "© 2026 Poposky Gomez | MindOrder Professional Edition. All rights reserved.",
        "creador_info": "DEVELOPED BY POPOSKY GOMEZ\nVersion: 1.1.0\nStatus: Stable\n© 2026 All rights reserved."
    },
    "Русский": {
        "titulo": "MindOrder v1.1.0 - Professional Edition",
        "limpieza": "🧹 ОЧИСТКА",
        "sistema": "🛠️ СИСТЕМА",
        "ajustes": "⚙️ НАСТРОЙКИ",
        "creador": "👤 СОЗДАТЕЛЬ",
        "m_estandar": "СТАНДАРТ (АВТО)",
        "m_quirurgico": "ХИРУРГИЧЕСКИЙ (РУЧНОЙ)",
        "btn_pro": "ОБНОВИТЬ ДО PRO",
        "modo_claro": "Светлая тема",
        "idioma": "Язык:",
        "log_inicio": ">>> СИСТЕМА ОНЛАЙН. Все в твоих руках.",
        "footer": "© 2026 Poposky Gomez | MindOrder Professional Edition. Все права защищены.",
        "creador_info": "РАЗРАБОТЧИК: POPOSKY GOMEZ\nВерсия: 1.1.0\nСтатус: Стабильно\n© 2026 Все права защищены."
    },
    "Português": {
        "titulo": "MindOrder v1.1.0 - Professional Edition",
        "limpieza": "🧹 LIMPEZA",
        "sistema": "🛠️ SISTEMA",
        "ajustes": "⚙️ AJUSTES",
        "creador": "👤 CRIADOR",
        "m_estandar": "MODO PADRÃO (AUTO)",
        "m_quirurgico": "MODO CIRÚRGICO (MANUAL)",
        "btn_pro": "ATUALIZAR PARA PRO",
        "modo_claro": "Modo Claro",
        "idioma": "Idioma:",
        "log_inicio": ">>> SYSTEM ONLINE. O tabuleiro está em suas mãos.",
        "footer": "© 2026 Poposky Gomez | MindOrder Professional Edition. Todos os direitos reservados.",
        "creador_info": "DESENVOLVIDO POR POPOSKY GOMEZ\nVersão: 1.1.0\nStatus: Estável\n© 2026 Todos os direitos reservados."
    }
}

class MindOrderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "Español"

        # Constantes lógicas de directorios y extensiones
        self.HOME = os.path.expanduser("~")
        self.RUTA_MENTE_LIMPIA = os.path.join(self.HOME, "Documents", "MENTE LIMPIA")

        self.CARPETAS_ESTANDAR = [
            os.path.join(self.HOME, "Desktop"),
            os.path.join(self.HOME, "Downloads"),
            os.path.join(self.HOME, "Pictures"),
            os.path.join(self.HOME, "Music"),
            os.path.join(self.HOME, "Videos"),
            os.path.join(self.HOME, "3D Objects")
        ]

        self.CONFIG_CARPETAS = {
            '.pdf': '01_Documentos', '.docx': '01_Documentos', '.txt': '01_Documentos', '.pptx': '01_Documentos',
            '.jpg': '02_Imagenes', '.jpeg': '02_Imagenes', '.png': '02_Imagenes', '.gif': '02_Imagenes', '.svg': '02_Imagenes',
            '.mp4': '03_Videos', '.mov': '03_Videos', '.mkv': '03_Videos',
            '.mp3': '04_Audio', '.wav': '04_Audio',
            '.xlsx': '05_Datos_Excel', '.csv': '05_Datos_Excel',
            '.zip': '06_Comprimidos', '.rar': '06_Comprimidos',
            '.psd': '07_Disenos_Photoshop'
        }

        self.MESES_ESPANOL = {
            1: "01_Enero", 2: "02_Febrero", 3: "03_Marzo", 4: "04_Abril",
            5: "05_Mayo", 6: "06_Junio", 7: "07_Julio", 8: "08_Agosto",
            9: "09_Septiembre", 10: "10_Octubre", 11: "11_Noviembre", 12: "12_Diciembre"
        }

        # Configuración Ventana y asignación del icono del sistema (barra superior de Windows)
        self.title(TEXTOS[self.current_lang]["titulo"])
        self.geometry("650x780")
        self.resizable(False, False)
        
        # Integración del icono gráfico en la ventana
        self.icono_path = "log.ico"
        if os.path.exists(self.icono_path):
            self.iconbitmap(self.icono_path)
            # Carga de la imagen para usarla en el encabezado
            self.img_logo = ctk.CTkImage(light_image=ctk.Image.open(self.icono_path) if hasattr(ctk, 'Image') else None,
                                       dark_image=ctk.CTkImage(light_image=None, dark_image=None).cget("dark_image"), # Fallback seguro
                                       size=(36, 36))
        else:
            self.img_logo = None

        # --- UI Layout ---
        # Contenedor del encabezado con icono integrado al diseño
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(25, 10))
        
        if os.path.exists(self.icono_path) and hasattr(ctk, 'CTkImage'):
            try:
                from PIL import Image, ImageTk
                logo_image = Image.open(self.icono_path)
                logo_ctk = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(40, 40))
                self.lbl_icono_visual = ctk.CTkLabel(self.header_frame, text="", image=logo_ctk)
                self.lbl_icono_visual.pack(side="left", padx=(0, 15))
            except Exception:
                pass

        self.header_label = ctk.CTkLabel(self.header_frame, text="M I N D O R D E R",
                                         font=("Segoe UI", 32, "bold"),
                                         text_color=COLOR_NEON)
        self.header_label.pack(side="left")

        self.tabview = ctk.CTkTabview(self, width=600, height=350,
                                      corner_radius=15, border_width=1,
                                      border_color="#1e1e1e")
        self.tabview.pack(padx=25, pady=10)

        self.construir_tabs()

        # --- Consola ---
        self.log_box = ctk.CTkTextbox(self, height=150, fg_color="#070707",
                                     border_color="#1e1e1e", border_width=1, font=("Consolas", 11))
        self.log_box.pack(fill="x", padx=25, pady=(10, 5))
        self.log_box.insert("0.0", TEXTOS[self.current_lang]["log_inicio"])
        self.log_box.configure(state="disabled")

        self.footer = ctk.CTkLabel(self, text=TEXTOS[self.current_lang]["footer"],
                                   font=("Segoe UI", 10), text_color="#444444")
        self.footer.pack(side="bottom", pady=5)

    def construir_tabs(self):
        """Crea las pestañas de control."""
        t = TEXTOS[self.current_lang]

        # Limpieza
        self.tab_limpieza = self.tabview.add(t["limpieza"])
        self.btn_estandar = ctk.CTkButton(self.tab_limpieza, text=t["m_estandar"],
                                          command=self.ejecutar_modo_estandar,
                                          height=45, fg_color="#1e1e1e",
                                          border_width=1, border_color=COLOR_NEON, font=("Segoe UI", 12, "bold"))
        self.btn_estandar.pack(pady=20, padx=20, fill="x")

        self.btn_quirurgico = ctk.CTkButton(self.tab_limpieza, text=t["m_quirurgico"],
                                            command=self.ejecutar_quirurgico,
                                            height=45, fg_color="#1e1e1e",
                                            border_width=1, border_color="#ffffff", font=("Segoe UI", 12, "bold"))
        self.btn_quirurgico.pack(pady=10, padx=20, fill="x")

        # Sistema
        self.tab_sistema = self.tabview.add(t["sistema"])
        self.btn_pro = ctk.CTkButton(self.tab_sistema, text=t["btn_pro"],
                                     command=self.mostrar_pro,
                                     fg_color="#d6b400", text_color="black",
                                     font=("Segoe UI", 12, "bold"))
        self.btn_pro.pack(pady=20)
        self.btn_sfc = ctk.CTkButton(self.tab_sistema, text="SFC /SCANNOW",
                                     command=self.ejecutar_sfc, fg_color="#1e1e1e", font=("Segoe UI", 12, "bold"))
        self.btn_sfc.pack(pady=10)

        # Ajustes
        self.tab_ajustes = self.tabview.add(t["ajustes"])
        self.switch_theme = ctk.CTkSwitch(self.tab_ajustes, text=t["modo_claro"],
                                          command=self.cambiar_tema)
        self.switch_theme.pack(pady=20)
        self.label_lang = ctk.CTkLabel(self.tab_ajustes, text=t["idioma"])
        self.label_lang.pack()
        self.option_lang = ctk.CTkOptionMenu(self.tab_ajustes,
                                             values=["Español", "English", "Русский", "Português"],
                                             command=self.actualizar_idiomas)
        self.option_lang.pack(pady=10)
        self.option_lang.set(self.current_lang)

        # Creador
        self.tab_creador = self.tabview.add(t["creador"])
        self.lbl_creador = ctk.CTkLabel(self.tab_creador, text=t["creador_info"],
                                        font=("Consolas", 14), text_color=COLOR_NEON)
        self.lbl_creador.pack(pady=30)

    # --- Lógica de Idiomas y Tema ---
    def actualizar_idiomas(self, lang):
        self.current_lang = lang
        t = TEXTOS[self.current_lang]

        # Destruir pestañas de memoria limpiamente
        for tab_name in list(self.tabview._tab_dict.keys()):
            self.tabview.delete(tab_name)
        
        self.construir_tabs()

        # Actualizar textos fijos fuera de pestañas
        self.title(t["titulo"])
        self.footer.configure(text=t["footer"])
        self.log(t["log_inicio"])

    def cambiar_tema(self):
        if self.switch_theme.get() == 1:
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    # --- Motor de Lógica Operativa ---
    def log(self, mensaje):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", "\n" + mensaje)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def resolver_duplicado(self, ruta_destino_final):
        base, extension = os.path.splitext(ruta_destino_final)
        contador = 1
        while os.path.exists(ruta_destino_final):
            ruta_destino_final = f"{base}_{contador}{extension}"
            contador += 1
        return ruta_destino_final

    def obtener_ruta_cronologica(self, subcarpeta_base, ruta_archivo_origen):
        timestamp = os.path.getmtime(ruta_archivo_origen)
        fecha = datetime.fromtimestamp(timestamp)
        anio = str(fecha.year)
        mes_nombre = self.MESES_ESPANOL.get(fecha.month, f"{fecha.month:02d}_Mes")
        return os.path.join(self.RUTA_MENTE_LIMPIA, subcarpeta_base, anio, mes_nombre)

    def limpiar_resto_escritorio(self):
        ruta_escritorio = os.path.join(self.HOME, "Desktop")
        self.log(">>> [BARRIDO] Procesando escritorio general...")
        
        if not os.path.exists(ruta_escritorio):
            return

        for nombre_archivo in os.listdir(ruta_escritorio):
            ruta_completa = os.path.join(ruta_escritorio, nombre_archivo)
            if os.path.isdir(ruta_completa) or nombre_archivo.lower().endswith(('.lnk', '.url')):
                continue

            ruta_carpeta_destino = self.obtener_ruta_cronologica("08_Otros_Escritorio", ruta_completa)
            if not os.path.exists(ruta_carpeta_destino):
                os.makedirs(ruta_carpeta_destino)

            ruta_final = os.path.join(ruta_carpeta_destino, nombre_archivo)
            ruta_final = self.resolver_duplicado(ruta_final)
            
            try:
                shutil.move(ruta_completa, ruta_final)
                self.log(f" -> [Escritorio] Movido: {nombre_archivo}")
            except Exception as e:
                self.log(f" -> [Error Escritorio] {nombre_archivo}: {e}")

    def procesar_carpeta(self, carpeta_origen):
        if not os.path.exists(carpeta_origen):
            return 0

        self.log(f">>> [ESCANEO] Analizando: {os.path.basename(carpeta_origen)}")
        contador = 0

        for nombre_archivo in os.listdir(carpeta_origen):
            ruta_archivo_completa = os.path.join(carpeta_origen, nombre_archivo)
            if os.path.isdir(ruta_archivo_completa):
                continue

            _, extension = os.path.splitext(nombre_archivo)
            extension = extension.lower()

            if extension in self.CONFIG_CARPETAS:
                subcarpeta_identificador = self.CONFIG_CARPETAS[extension]
                ruta_carpeta_destino = self.obtener_ruta_cronologica(subcarpeta_identificador, ruta_archivo_completa)

                if not os.path.exists(ruta_carpeta_destino):
                    os.makedirs(ruta_carpeta_destino)

                ruta_final_archivo = os.path.join(ruta_carpeta_destino, nombre_archivo)
                ruta_final_archivo = self.resolver_duplicado(ruta_final_archivo)

                try:
                    shutil.move(ruta_archivo_completa, ruta_final_archivo)
                    self.log(f" -> Organizado: {nombre_archivo}")
                    contador += 1
                except Exception as e:
                    self.log(f" -> [Error archivo] {nombre_archivo}: {e}")
        return contador

    def ejecutar_modo_estandar(self):
        if not os.path.exists(self.RUTA_MENTE_LIMPIA):
            os.makedirs(self.RUTA_MENTE_LIMPIA)
            
        self.log(">>> INICIANDO BARRIDO ESTÁNDAR AUTOMÁTICO...")
        contador_total = 0
        for carpeta in self.CARPETAS_ESTANDAR:
            contador_total += self.procesar_carpeta(carpeta)
        
        self.limpiar_resto_escritorio()
        self.log(f">>> [OK] Barrido estándar finalizado. Total reubicados: {contador_total}")
        messagebox.showinfo("MindOrder", f"¡Limpieza estándar completada!\nTotal de elementos organizados: {contador_total}")

    def ejecutar_quirurgico(self):
        if not os.path.exists(self.RUTA_MENTE_LIMPIA):
            os.makedirs(self.RUTA_MENTE_LIMPIA)
            
        carpeta = filedialog.askdirectory(title="MindOrder - Carpeta objetivo manual")
        if carpeta:
            self.log(f">>> INICIANDO MODO QUIRÚRGICO MANUAL...")
            archivos_movidos = self.procesar_carpeta(carpeta)
            self.log(f">>> [OK] Modo quirúrgico terminado. Total: {archivos_movidos}")
            messagebox.showinfo("MindOrder", f"Modo Quirúrgico finalizado.\nArchivos procesados: {archivos_movidos}")
        else:
            self.log(">>> Operación manual cancelada por el usuario.")

    def ejecutar_sfc(self):
        self.log(">>> Lanzando escaneo de salud del sistema SFC (Requiere permisos de Administrador)...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe",
                                                "/k sfc /scannow", None, 1)
        except Exception as e:
            self.log(f">>> Error al invocar privilegios de consola: {e}")

    def mostrar_pro(self):
        messagebox.showinfo("MindOrder Professional",
                            "La versión PRO estará disponible muy pronto. ¡Sigue adelante!")

if __name__ == "__main__":
    app = MindOrderApp()
    app.mainloop()