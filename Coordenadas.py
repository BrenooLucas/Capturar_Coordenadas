import tkinter as tk
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key


class CoordinateCaptor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧭 Capturador de Coordenadas")
        self.root.geometry("460x500")
        self.root.configure(bg="#1e1e1e")
        self.root.iconbitmap("pc.ico")
        self.root.resizable(False, False)

        self.coordenadas = []
        self.capturando = False
        self.finalizar = False
        self.ignore_areas = []

        self.create_widgets()

        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)

        self.keyboard_listener.start()
        self.mouse_listener.start()

        self.root.after(100, self.check_finalizar)
        self.root.mainloop()

    def create_widgets(self):
        # Título
        tk.Label(
            self.root,
            text="📍 Capturador de Coordenadas",
            font=("Segoe UI", 16, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        ).pack(pady=(20, 10))

        # Botões
        btn_font = ("Segoe UI", 11, "bold")

        self.start_button = tk.Button(
            self.root,
            text="▶ Iniciar Captura",
            font=btn_font,
            command=self.start_capturing,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            relief="flat",
            width=20,
            height=2,
            cursor="hand2"
        )
        self.start_button.pack(pady=(5, 10))

        self.stop_button = tk.Button(
            self.root,
            text="⛔ Encerrar Captura",
            font=btn_font,
            command=self.stop_capturing,
            bg="#f44336",
            fg="white",
            activebackground="#da190b",
            relief="flat",
            width=20,
            height=2,
            cursor="hand2",
            state="disabled"
        )
        self.stop_button.pack(pady=(0, 15))

        # Lista de coordenadas
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(padx=20, fill="both", expand=True)

        self.listbox = tk.Listbox(
            frame,
            bg="#2e2e2e",
            fg="#ffffff",
            font=("Consolas", 10),
            selectbackground="#555",
            activestyle="none",
            bd=0,
            highlightthickness=0
        )
        self.listbox.pack(side="left", fill="both", expand=True, pady=10)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)

        # Rodapé
        tk.Label(
            self.root,
            text="Pressione ESC para encerrar captura via teclado.",
            font=("Segoe UI", 9,"bold"),
            bg="#1e1e1e",
            fg="#aaaaaa"
        ).pack(pady=(5, 10))

    def start_capturing(self):
        self.capturando = True
        self.coordenadas.clear()
        self.listbox.insert("end", "🟢 Captura iniciada. Clique onde desejar.")
        self.listbox.see("end")

        self.ignore_areas = [
            self.get_widget_bbox(self.start_button),
            self.get_widget_bbox(self.stop_button),
        ]

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_capturing(self):
        self.capturando = False
        self.listbox.insert("end", "🔴 Captura encerrada.")
        self.listbox.see("end")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def on_mouse_click(self, x, y, button, pressed):
        if pressed and self.capturando:
            if self.is_ignored_area(x, y):
                return
            coord = (x, y)
            self.coordenadas.append(coord)
            self.listbox.insert("end", f"🖱️ Coordenada: {coord}")
            self.listbox.see("end")

    def on_key_press(self, key):
        if key == Key.esc:
            self.finalizar = True
            return False

    def check_finalizar(self):
        if self.finalizar:
            self.mouse_listener.stop()
            self.listbox.insert("end", "\n✅ Captura finalizada via ESC.")
            self.listbox.insert("end", f"\n📌 Total: {len(self.coordenadas)} coordenadas.")
            for coord in self.coordenadas:
                self.listbox.insert("end", str(coord))
            self.listbox.see("end")
            self.stop_button.config(state="disabled")
            self.start_button.config(state="normal")
        else:
            self.root.after(100, self.check_finalizar)

    def get_widget_bbox(self, widget):
        widget.update()
        x1 = widget.winfo_rootx()
        y1 = widget.winfo_rooty()
        x2 = x1 + widget.winfo_width()
        y2 = y1 + widget.winfo_height()
        return (x1, y1, x2, y2)

    def is_ignored_area(self, x, y):
        for area in self.ignore_areas:
            x1, y1, x2, y2 = area
            if x1 <= x <= x2 and y1 <= y <= y2:
                return True
        return False


if __name__ == "__main__":
    CoordinateCaptor()