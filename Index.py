import tkinter as tk
from tkinter import ttk, messagebox
import re

class Calculadora:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Mi Calculadora")
        self.ventana.geometry("400x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg='#2c3e50')
        
        self.texto_pantalla = tk.StringVar()
        self.texto_pantalla.set("0")
        
        self.definir_colores()
        self.crear_interfaz()
        self.configurar_teclado()
    
    def definir_colores(self):
        """Aqui guardo los colores que voy a usar"""
        self.mis_colores = {
            'fondo': '#2c3e50',
            'pantalla_fondo': '#34495e',
            'pantalla_texto': '#ecf0f1',
            'boton_normal': '#3498db',
            'boton_normal_texto': 'white',
            'boton_operador': '#e67e22',
            'boton_operador_texto': 'white',
            'boton_borrar': '#e74c3c',
            'boton_borrar_texto': 'white',
            'boton_igual': '#27ae60',
            'boton_igual_texto': 'white',
            'boton_especial': '#95a5a6',
            'boton_especial_texto': 'white'
        }
    
    def crear_interfaz(self):
        """Creo todos los botones y la pantalla"""
        
        marco_principal = tk.Frame(self.ventana, bg=self.mis_colores['fondo'])
        marco_principal.pack(expand=True, fill='both', padx=10, pady=10)
        
        marco_pantalla = tk.Frame(marco_principal, bg=self.mis_colores['pantalla_fondo'], height=120)
        marco_pantalla.pack(fill='x', pady=(0, 20))
        marco_pantalla.pack_propagate(False)
        
        self.etiqueta_pantalla = tk.Label(
            marco_pantalla,
            textvariable=self.texto_pantalla,
            font=('Arial', 28, 'bold'),
            bg=self.mis_colores['pantalla_fondo'],
            fg=self.mis_colores['pantalla_texto'],
            anchor='e',
            padx=15,
            pady=20
        )
        self.etiqueta_pantalla.pack(fill='both', expand=True)
        
        marco_botones = tk.Frame(marco_principal, bg=self.mis_colores['fondo'])
        marco_botones.pack(expand=True, fill='both')
        
        mis_botones = [
            ('C', 0, 0, 'borrar'), ('⌫', 0, 1, 'borrar'), ('%', 0, 2, 'especial'), ('/', 0, 3, 'operador'),
            ('7', 1, 0, 'numero'), ('8', 1, 1, 'numero'), ('9', 1, 2, 'numero'), ('*', 1, 3, 'operador'),
            ('4', 2, 0, 'numero'), ('5', 2, 1, 'numero'), ('6', 2, 2, 'numero'), ('-', 2, 3, 'operador'),
            ('1', 3, 0, 'numero'), ('2', 3, 1, 'numero'), ('3', 3, 2, 'numero'), ('+', 3, 3, 'operador'),
            ('0', 4, 0, 'numero', 2), ('.', 4, 2, 'decimal'), ('=', 4, 3, 'igual')
        ]
        
        for boton_info in mis_botones:
            texto = boton_info[0]
            fila = boton_info[1]
            columna = boton_info[2]
            tipo = boton_info[3]
            ancho = boton_info[4] if len(boton_info) > 4 else 1
            
            mi_boton = self.hacer_boton(marco_botones, texto, tipo, ancho)
            mi_boton.grid(row=fila, column=columna, columnspan=ancho, padx=2, pady=2, sticky='nsew')
        
        for i in range(5):
            marco_botones.grid_rowconfigure(i, weight=1)
        for i in range(4):
            marco_botones.grid_columnconfigure(i, weight=1)
    
    def hacer_boton(self, padre, texto, tipo, ancho=1):
        """Funcion para crear un boton con su color y funcion"""
        
        if tipo == 'borrar':
            color_fondo = self.mis_colores['boton_borrar']
            color_texto = self.mis_colores['boton_borrar_texto']
        elif tipo == 'operador':
            color_fondo = self.mis_colores['boton_operador']
            color_texto = self.mis_colores['boton_operador_texto']
        elif tipo == 'igual':
            color_fondo = self.mis_colores['boton_igual']
            color_texto = self.mis_colores['boton_igual_texto']
        elif tipo == 'especial':
            color_fondo = self.mis_colores['boton_especial']
            color_texto = self.mis_colores['boton_especial_texto']
        else:
            color_fondo = self.mis_colores['boton_normal']
            color_texto = self.mis_colores['boton_normal_texto']
        
        boton = tk.Button(
            padre,
            text=texto,
            font=('Arial', 14, 'bold'),
            bg=color_fondo,
            fg=color_texto,
            activebackground=self.oscurecer_color(color_fondo),
            activeforeground=color_texto,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        
        if tipo == 'numero':
            boton.config(command=lambda t=texto: self.agregar_numero(t))
        elif tipo == 'operador':
            boton.config(command=lambda t=texto: self.agregar_operador(t))
        elif tipo == 'decimal':
            boton.config(command=self.agregar_punto)
        elif texto == 'C':
            boton.config(command=self.limpiar_todo)
        elif texto == '⌫':
            boton.config(command=self.borrar_ultimo)
        elif texto == '=':
            boton.config(command=self.calcular_resultado)
        elif texto == '%':
            boton.config(command=self.porcentaje)
        
        return boton
    
    def oscurecer_color(self, color):
        """Para cuando pasas el mouse por encima del boton"""
        colores_oscuros = {
            '#3498db': '#2980b9',
            '#e67e22': '#d35400',
            '#e74c3c': '#c0392b',
            '#27ae60': '#229954',
            '#95a5a6': '#7f8c8d'
        }
        return colores_oscuros.get(color, '#2c3e50')
    
    def agregar_numero(self, numero):
        """Agrega un numero a la pantalla"""
        valor_actual = self.texto_pantalla.get()
        if valor_actual == "0" or valor_actual == "Error":
            self.texto_pantalla.set(numero)
        else:
            self.texto_pantalla.set(valor_actual + numero)
    
    def agregar_punto(self):
        """Agrega un punto decimal si se puede"""
        valor_actual = self.texto_pantalla.get()
        
        if valor_actual == "Error":
            self.texto_pantalla.set("0.")
            return
        
        if valor_actual == "0":
            self.texto_pantalla.set("0.")
            return
        
        partes = re.split(r'[+\-*/%]', valor_actual)
        ultimo_numero = partes[-1] if partes else ""
        
        if '.' in ultimo_numero:
            return
        
        self.texto_pantalla.set(valor_actual + ".")
    
    def agregar_operador(self, operador):
        """Agrega un operador matematico (+, -, *, /)"""
        valor_actual = self.texto_pantalla.get()
        if valor_actual and valor_actual != "Error":
            ultimo_caracter = valor_actual[-1] if valor_actual else ""
            if ultimo_caracter in ['+', '-', '*', '/', '%']:
                self.texto_pantalla.set(valor_actual[:-1] + operador)
            else:
                self.texto_pantalla.set(valor_actual + operador)
    
    def calcular_resultado(self):
        """Hace la operacion matematica"""
        try:
            cuenta = self.texto_pantalla.get()
            if cuenta and cuenta != "Error":
                resultado = eval(cuenta)
                
                if isinstance(resultado, float):
                    if resultado.is_integer():
                        resultado = int(resultado)
                    else:
                        resultado = round(resultado, 10)
                
                self.texto_pantalla.set(str(resultado))
        except Exception as error:
            self.texto_pantalla.set("Error")
            messagebox.showerror("Error", "No se puede hacer esa operacion")
    
    def limpiar_todo(self):
        """Borra todo lo que hay en pantalla"""
        self.texto_pantalla.set("0")
    
    def borrar_ultimo(self):
        """Borra el ultimo numero o caracter"""
        valor_actual = self.texto_pantalla.get()
        if valor_actual and valor_actual != "Error" and valor_actual != "0":
            if len(valor_actual) == 1:
                self.texto_pantalla.set("0")
            else:
                self.texto_pantalla.set(valor_actual[:-1])
    
    def porcentaje(self):
        """Calcula el porcentaje"""
        try:
            valor_actual = self.texto_pantalla.get()
            if valor_actual and valor_actual != "Error":
                numero = eval(valor_actual)
                resultado = numero / 100
                if isinstance(resultado, float) and resultado.is_integer():
                    resultado = int(resultado)
                self.texto_pantalla.set(str(resultado))
        except:
            self.texto_pantalla.set("Error")
    
    def configurar_teclado(self):
        """Para que funcionen las teclas del teclado"""
        for tecla in '0123456789':
            self.ventana.bind(tecla, lambda e, num=tecla: self.agregar_numero(num))
        
        for operador in ['+', '-', '*', '/']:
            self.ventana.bind(operador, lambda e, op=operador: self.agregar_operador(op))
        
        self.ventana.bind('.', lambda e: self.agregar_punto())
        
        self.ventana.bind('<Return>', lambda e: self.calcular_resultado())
        self.ventana.bind('<BackSpace>', lambda e: self.borrar_ultimo())
        self.ventana.bind('<Escape>', lambda e: self.limpiar_todo())
        self.ventana.bind('<Delete>', lambda e: self.limpiar_todo())
        self.ventana.bind('%', lambda e: self.porcentaje())

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    mi_calculadora = Calculadora(ventana_principal)
    ventana_principal.mainloop()