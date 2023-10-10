import tkinter as tk
import json
import random
from datetime import datetime
import os


class Test_to_you:
    def __init__(self, app):
        self.ventana = app
        self.interfaz_principal = tk.Frame(self.ventana)
        self.interfaz_elegir_preguntas = tk.Frame(self.ventana)
        self.interfaz_preguntas = tk.Frame (self.ventana) 
        self.interfaz_de_nota = tk.Frame(self.ventana)
        self.numero_entrada = tk.StringVar(self.ventana)
        self.numero_salida = tk.StringVar(self.ventana)

        self.nota = 0

        self.cargar_interfaz_principal()


    def cnd(self):
        self.interfaz_principal.pack_forget()
        self.ventana.title("CND")
        self.numero_preguntas_examen = 100
        self.fichero= "cnd.json"
        self.leer_fichero()
        self.elegir_nuemero_preguntas()

    def ceh(self):
        self.interfaz_principal.pack_forget()
        self.ventana.title("CEH")
        self.numero_preguntas_examen = 10
        self.fichero= "ceh.json"
        self.leer_fichero()
        self.elegir_nuemero_preguntas()


    def lpic1(self):
        self.interfaz_principal.pack_forget()
        self.ventana.title("LPIC1")
        self.numero_preguntas_examen = 60
        self.fichero= "lpic1-101.json"
        self.leer_fichero()
        self.elegir_nuemero_preguntas()

    def cargar_interfaz_principal(self):
        self.ventana.title("Test yourself")
        '''tk.Button(
            self.interfaz_principal,
            compound="top",
            width=12,
            height=7,
            text="CND",
            bg= "#2271b3",
            command=self.cnd
        ).pack(
            side="left",
            fill=tk.BOTH,
            expand=True
            )'''
        
        tk.Button(
            self.interfaz_principal,
            font=("Curier 14", 30),
            width=5,
            height=2,
            text="CEH",
            fg= "#a52019",
            command=self.ceh
        ).pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=60,
            pady=11
            )
        
        tk.Button(
            self.interfaz_principal,
            font=("Curier 14", 30),
            width=5,
            height=2,
            text="LPIC1",
            fg= "#fbd900",
            command=self.lpic1
        ).pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=11
            )
        tk.Label(
            self.interfaz_principal,
            text="by Lawko",
            font=('Times 14', 7),
            ).pack(
                side=tk.BOTTOM
            )
        
        self.interfaz_principal.pack()

    def leer_fichero(self):
        self.now = datetime.now()
        self.formatted = self.now.strftime("%d%m%Y-%H%M%S")
        with open(self.fichero, "r") as file:
            self.json_preguntas = json.load(file)
        with open(f"{self.json_preguntas['nombre']} {self.formatted}.txt", "a") as self.escritura:
            self.escritura.write(f"{self.json_preguntas['nombre']}\n")
        self.preguntas = self.json_preguntas['test']

    def elegir_nuemero_preguntas(self):        
        tk.Label(
            self.interfaz_elegir_preguntas,
            text=f'Hay un total de {len(self.preguntas)} preguntas, elige un rango de numeros o puedes elegir hacer el "Examen".\nDesde',
            font=('Times 14', 14),
            ).pack()
        
        tk.Entry(
            self.interfaz_elegir_preguntas,
            font=('Times 14', 12),
            width=10,
            textvariable= self.numero_entrada
            ).pack()       

        tk.Label(
            self.interfaz_elegir_preguntas,
            text="Hasta",
            font=('Times 14', 14),
            anchor=tk.W
            ).pack()
                
        tk.Entry(
            self.interfaz_elegir_preguntas,
            font=('Times 14', 12),
            width=10,
            textvariable= self.numero_salida
            ).pack()
        
        tk.Button(
            self.interfaz_elegir_preguntas,
            text="Aceptar",
            command=self.guardar_numero_preguntas,
            font=('Times 14', 12)
            ).pack()
        
        tk.Button(
            self.interfaz_elegir_preguntas,
            text="Examen de prueba",
            command=self.boton_test_prueba,
            font=('Times 14', 12)
            ).pack() 
        
        tk.Label(
            self.interfaz_elegir_preguntas,
            text="by Lawko",
            font=('Times 14', 7),
            ).pack(
                side=tk.RIGHT
            )
        
        self.interfaz_elegir_preguntas.pack()

    def guardar_numero_preguntas(self):
        self.variable = self.preguntas_corridas
        self.pregunta_actual = int(self.numero_entrada.get()) - 1
        self.pregunta_final = int(self.numero_salida.get())
        self.ventana.title(f"{self.json_preguntas['nombre']} del {self.numero_entrada.get()} al {self.numero_salida.get()}")
        self.interfaz_elegir_preguntas.pack_forget()
        
        self.interface_preguntas()
        self.preguntas_corridas()

    def boton_test_prueba(self):
        self.variable = self.test_pruebas
        self.pregunta_test = 0
        self.ventana.title(f"Examen de prueba - {self.json_preguntas['nombre']}")
        self.posiciones_aleatorias = [] # Lista para almacenar las posiciones aleatorias
        self.cantidad_posiciones = self.numero_preguntas_examen # Número de posiciones que deseas imprimir de forma aleatoria
        while len(self.posiciones_aleatorias) < self.cantidad_posiciones:
            posicion = random.randint(0, len(self.json_preguntas['test']) - 1)
            if posicion not in self.posiciones_aleatorias:
                self.posiciones_aleatorias.append(posicion)
        self.interfaz_elegir_preguntas.pack_forget()
        
        self.interface_preguntas()
        self.revelar_ocultar.destroy()
        self.test_pruebas()
    
    def preguntas_corridas(self):
        if self.pregunta_actual < self.pregunta_final:
            self.cargar_pregunta()
        else:
            os.startfile(f"{self.json_preguntas['nombre']} {self.formatted}.txt")
            self.ventana.destroy()
        
    def test_pruebas(self):
        if self.pregunta_test < self.cantidad_posiciones:
            self.pregunta_actual = self.posiciones_aleatorias[self.pregunta_test]
            self.cargar_pregunta()
        else:
            self.interfaz_nota()

    def interface_preguntas(self):        
        self.label_pregunta = tk.Label(
            self.interfaz_preguntas,
            text="",
            font=('Times 14', 14),
            justify='left'
            )
        self.label_pregunta.pack(anchor="w")
        
        self.revelar_ocultar = tk.Button(self.interfaz_preguntas,
                text="Revelar Respuesta",
                command=self.revelar_ocultar_respuesta,
                font=('Times 14', 12)
                )
        self.revelar_ocultar.pack()
        
        self.respuesta_visible = tk.BooleanVar(value=False)  # Variable de control para rastrear si la respuesta está visible 

        tk.Button(
            self.interfaz_preguntas,
            text="Siguiente",
            command=self.siguiente_pregunta,
            font=('Times 14', 12)
            ).pack(side='bottom', expand=True)
        
        self.interfaz_preguntas.pack()
        
    def cargar_pregunta(self):
        self.opciones_respuestas = []
        self.pregunta = self.preguntas[self.pregunta_actual]
        if self.variable == self.preguntas_corridas:
            self.label_pregunta.config(
                text=f"{self.pregunta['numero']}. {self.pregunta['enunciado']} \n",
                wraplength=self.interfaz_preguntas.winfo_screenwidth()*0.8
                )
        else:
            self.label_pregunta.config(
                text=f"{self.pregunta_test + 1}. {self.pregunta['enunciado']} \n",
                wraplength=self.interfaz_preguntas.winfo_screenwidth()*0.8
                )    
        
        if self.preguntas[self.pregunta_actual]["tipo"] == "test":            
            self.respuesta_correcta = self.pregunta["resp"]
            if len(self.respuesta_correcta) == 1:
                self.una_respuesta()
            elif len(self.respuesta_correcta) > 1:
                self.varias_respuestas()
        else:
            self.entrada_respuesta = tk.Entry(
                self.interfaz_preguntas,
                font=('Times 14', 12),
                width=50
               )
            self.entrada_respuesta.pack()

    


    def varias_respuestas(self):
        pregunta = self.preguntas[self.pregunta_actual]
        for letra, respuesta in pregunta["respuestas"].items():
            self.variable_checkbutton = tk.BooleanVar()
            opcion = tk.Checkbutton(
                self.interfaz_preguntas,
                text=f"{letra.upper()}. {respuesta}",
                variable=self.variable_checkbutton,
                font=('Times 14', 12)
                )
            opcion.pack(anchor="w") # "w" para alinear a la izquierda
            self.opciones_respuestas.append([opcion, letra, self.variable_checkbutton])


    def una_respuesta(self):
        pregunta = self.preguntas[self.pregunta_actual]
        self.variable_radiobutton = tk.StringVar()
        for letra, respuesta in pregunta["respuestas"].items():
            opcion = tk.Radiobutton(
                self.interfaz_preguntas,
                text=f"{letra.upper()}. {respuesta}",
                variable=self.variable_radiobutton,
                value=letra,
                font=('Times 14', 12)
                )
            opcion.pack(anchor="w") # "w" para alinear a la izquierda
            self.opciones_respuestas.append(opcion)
    
    def siguiente_pregunta(self):
        if self.preguntas[self.pregunta_actual]["tipo"] == "test":
            if len(self.respuesta_correcta) > 1:
                self.respuesta_usuario = [_ for opcion, _, variable in self.opciones_respuestas if variable.get()]
                self.respuestas_usuario = [letra for check_button, letra, variable in self.opciones_respuestas if variable.get()]
                self.respuestas_correctas = set(self.respuesta_correcta)
                self.respuestas_usuario = set(self.respuestas_usuario)
            
                self.corregir()
                # Eliminar los botones de radio anteriores
                for check_button, letra, variable in self.opciones_respuestas:
                    check_button.destroy()
                
            elif len(self.respuesta_correcta) == 1:
                self.respuesta_usuario = [self.variable_radiobutton.get()]
                self.corregir()
                # Eliminar los botones de radio anteriores
                for radio_button in self.opciones_respuestas:
                    radio_button.destroy()
            if self.variable == self.preguntas_corridas:
                self.pregunta_actual += 1
                self.variable()
            else:
                self.pregunta_test += 1
                self.variable()
        else:
            ##Para preguntas de rellenar
            self.respuesta_usuario = self.entrada_respuesta.get()
            self.respuesta_correcta = self.preguntas[self.pregunta_actual]["resp"][0]
            print(f"USUARIO: {self.entrada_respuesta.get()}, CORRECTA:{self.respuesta_correcta}")
    
            if self.respuesta_usuario.lower() == self.respuesta_correcta.lower():
                print(f"Pregunta {self.pregunta_actual}: Respuesta correcta")
            else:
                print(f"Pregunta {self.pregunta_actual + 1}: Respuesta incorrecta. \nLa respuesta correcta era {self.respuesta_correcta}")
                self.agregar_linea_a_archivo(f"Fallo en la pregunta {self.pregunta_actual + 1}\n")
   
            self.entrada_respuesta.delete(0, tk.END)
            self.entrada_respuesta.destroy()
            if self.variable == self.preguntas_corridas:
                self.pregunta_actual += 1
                self.variable()
            else:
                self.pregunta_test += 1
                self.variable()
    
    def corregir(self): 
        if self.respuesta_usuario == self.respuesta_correcta:
            print(f"Pregunta {self.pregunta_actual + 1}: Respuesta correcta\n")
            self.nota += 1
        else:
            print(f"Pregunta {self.pregunta_actual + 1}: Respuesta incorrecta. \nRespuesta(s) correcta(s): {', '.join(self.respuesta_correcta).upper()}\n")
            self.agregar_linea_a_archivo(f"Fallo en la pregunta {self.pregunta_actual + 1}\n")
        
    def interfaz_nota(self):
        self.interfaz_preguntas.pack_forget()
        if self.json_preguntas['nombre'] == "CND" or \
        self.json_preguntas['nombre'] == "CEH":
            if self.nota >= 70:
                estado = "PASSED"
            else:
                estado = "FAILED"
                
            print(estado)
        tk.Label(
                self.interfaz_de_nota,
                text=f"Score:{self.nota} | {estado}",
                font=('Times 14', 20),
                ).pack()
        
        tk.Button(
            self.interfaz_de_nota,
            text="CERRAR",
            command= lambda: self.ventana.destroy(),
            font=('Times 14', 12)
            ).pack(side='bottom', expand=True)
        
        self.interfaz_de_nota.pack(expand=60)

        os.startfile(f"{self.json_preguntas['nombre']} {self.formatted}.txt")
        #self.ventana.destroy()
                
    
    def agregar_linea_a_archivo(self, agregar_linea):
        # Método para agregar una línea al archivo de texto
        with open(f"{self.json_preguntas['nombre']} {self.formatted}.txt", "a") as self.escritura:
            self.escritura.write(agregar_linea)


    def revelar_ocultar_respuesta(self):
        if len(self.preguntas[self.pregunta_actual]["resp"]) == 1:
            respuesta_actual = self.preguntas[self.pregunta_actual]["resp"][0]
        if len(self.preguntas[self.pregunta_actual]["resp"]) > 1:
            respuesta_actual = ', '.join(self.respuesta_correcta)

        if not self.respuesta_visible.get():
            self.label_pregunta.config(text=self.label_pregunta.cget("text") + f"\nRespuesta: {respuesta_actual}")
            self.revelar_ocultar.config(text="Ocultar Respuesta")
        else:
            self.label_pregunta.config(text=self.label_pregunta.cget("text").replace(f"\nRespuesta: {respuesta_actual}", ""))
            self.revelar_ocultar.config(text="Revelar Respuesta")
        self.respuesta_visible.set(not self.respuesta_visible.get())

if __name__ == "__main__":
    root = tk.Tk()
    ventana = Test_to_you(root)
    root.mainloop()