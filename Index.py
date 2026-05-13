import tkinter as tk
from tkinter import ttk, messagebox
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        self.expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.setup_styles()
        
        self.create_widgets()
        
        self.setup_keyboard_shortcuts()
    
    def setup_styles(self):
        """Configurar estilos de los botones"""
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12, 'bold'))
        
        self.colors = {
            'bg': '#2c3e50',
            'display_bg': '#34495e',
            'display_fg': '#ecf0f1',
            'button_bg': '#3498db',
            'button_fg': 'white',
            'operator_bg': '#e67e22',
            'operator_fg': 'white',
            'clear_bg': '#e74c3c',
            'clear_fg': 'white',
            'equal_bg': '#27ae60',
            'equal_fg': 'white',
            'special_bg': '#95a5a6',
            'special_fg': 'white'
        }
    
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        display_frame = tk.Frame(main_frame, bg=self.colors['display_bg'], height=120)
        display_frame.pack(fill='x', pady=(0, 20))
        display_frame.pack_propagate(False)
        
        self.display_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 28, 'bold'),
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            anchor='e',
            padx=15,
            pady=20
        )
        self.display_label.pack(fill='both', expand=True)
        
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        buttons_frame.pack(expand=True, fill='both')
        
        buttons_config = [
            ('C', 0, 0, 'clear', 1), ('⌫', 0, 1, 'clear', 1), ('%', 0, 2, 'special', 1), ('/', 0, 3, 'operator', 1),
            ('7', 1, 0, 'number', 1), ('8', 1, 1, 'number', 1), ('9', 1, 2, 'number', 1), ('*', 1, 3, 'operator', 1),
            ('4', 2, 0, 'number', 1), ('5', 2, 1, 'number', 1), ('6', 2, 2, 'number', 1), ('-', 2, 3, 'operator', 1),
            ('1', 3, 0, 'number', 1), ('2', 3, 1, 'number', 1), ('3', 3, 2, 'number', 1), ('+', 3, 3, 'operator', 1),
            ('0', 4, 0, 'number', 2), ('.', 4, 2, 'special', 1), ('=', 4, 3, 'equal', 1)
        ]
        
        for config in buttons_config:
            text = config[0]
            row = config[1]
            col = config[2]
            btn_type = config[3]
            colspan = config[4] if len(config) > 4 else 1
            
            btn = self.create_button(buttons_frame, text, btn_type, colspan)
            btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky='nsew')
        
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def create_button(self, parent, text, btn_type, colspan=1):
        """Crear un botón con estilo específico"""
        if btn_type == 'clear':
            bg_color = self.colors['clear_bg']
            fg_color = self.colors['clear_fg']
        elif btn_type == 'operator':
            bg_color = self.colors['operator_bg']
            fg_color = self.colors['operator_fg']
        elif btn_type == 'equal':
            bg_color = self.colors['equal_bg']
            fg_color = self.colors['equal_fg']
        elif btn_type == 'special':
            bg_color = self.colors['special_bg']
            fg_color = self.colors['special_fg']
        else: 
            bg_color = self.colors['button_bg']
            fg_color = self.colors['button_fg']
        
        btn = tk.Button(
            parent,
            text=text,
            font=('Arial', 14, 'bold'),
            bg=bg_color,
            fg=fg_color,
            activebackground=self.darken_color(bg_color),
            activeforeground=fg_color,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        
        if btn_type == 'number':
            btn.config(command=lambda t=text: self.add_to_expression(t))
        elif btn_type == 'operator':
            btn.config(command=lambda t=text: self.add_operator(t))
        elif text == 'C':
            btn.config(command=self.clear)
        elif text == '⌫':
            btn.config(command=self.backspace)
        elif text == '=':
            btn.config(command=self.calculate)
        elif text == '%':
            btn.config(command=self.percentage)
        
        return btn
    
    def darken_color(self, color):
        """Oscurecer un color para efecto hover"""
        colors_map = {
            '#3498db': '#2980b9',
            '#e67e22': '#d35400',
            '#e74c3c': '#c0392b',
            '#27ae60': '#229954',
            '#95a5a6': '#7f8c8d'
        }
        return colors_map.get(color, '#2c3e50')
    
    def add_to_expression(self, value):
        """Agregar número al display"""
        current = self.result_var.get()
        if current == "0" or current == "Error":
            self.result_var.set(value)
        else:
            self.result_var.set(current + value)
    
    def add_operator(self, operator):
        """Agregar operador matemático"""
        current = self.result_var.get()
        if current and current != "Error":
            last_char = current[-1] if current else ""
            if last_char in ['+', '-', '*', '/', '%']:
                self.result_var.set(current[:-1] + operator)
            else:
                self.result_var.set(current + operator)
    
    def calculate(self):
        """Calcular la expresión matemática"""
        try:
            expression = self.result_var.get()
            if expression and expression != "Error":
                expression = expression.replace('×', '*').replace('÷', '/')
                
                result = eval(expression)
                
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 10)
                
                self.result_var.set(str(result))
        except Exception:
            self.result_var.set("Error")
            messagebox.showerror("Error", "Expresión inválida")
    
    def clear(self):
        """Limpiar el display"""
        self.result_var.set("0")
    
    def backspace(self):
        """Borrar último carácter"""
        current = self.result_var.get()
        if current and current != "Error" and current != "0":
            if len(current) == 1:
                self.result_var.set("0")
            else:
                self.result_var.set(current[:-1])
    
    def percentage(self):
        """Calcular porcentaje"""
        try:
            current = self.result_var.get()
            if current and current != "Error":
                value = float(eval(current))
                result = value / 100
                self.result_var.set(str(result))
        except:
            self.result_var.set("Error")
    
    def setup_keyboard_shortcuts(self):
        """Configurar atajos de teclado"""
        self.root.bind('<Key>', self.key_press)
        
        for key in '0123456789':
            self.root.bind(str(key), lambda e, k=key: self.add_to_expression(k))
        
        for op in ['+', '-', '*', '/']:
            self.root.bind(op, lambda e, o=op: self.add_operator(o))
        
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Escape>', lambda e: self.clear())
        self.root.bind('<Delete>', lambda e: self.clear())
        self.root.bind('.', lambda e: self.add_to_expression('.'))
        self.root.bind('%', lambda e: self.percentage())
    
    def key_press(self, event):
        """Manejar eventos de teclado"""
        key = event.char
        if key == '=' or key == '\r':
            self.calculate()
        elif key == 'c' or key == 'C':
            self.clear()
        elif key == '\b':
            self.backspace()

def main():
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()

if __name__ == "__main__":
    main()