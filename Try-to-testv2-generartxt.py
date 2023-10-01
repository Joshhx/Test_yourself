import tkinter as tk
import json
import random
from datetime import datetime
import os

class VentanaPrincipal(tk.Frame):
    def __init__(self, master,):
        super().__init__(master)
        self.master.title("Try to test")
        self.pack()

        self.aciertos = 0
        self.fallos = 0

        # Creamos los botones
        self.boton_1 = tk.Button(self, text="CND", compound="top", width=12, height=7, command=self.abrir_cnd, font=('Times 14', 12, 'bold'))
        self.boton_2 = tk.Button(self, text="CEH", compound="top", width=12, height=7, command=self.abrir_ceh, font=('Times 14', 12, 'bold'))
        self.boton_3 = tk.Button(self, text="LPIC1",compound="top", width=12, height=7, command=self.abrir_lpic1, font=('Times 14', 12,'bold'))

        # Colocamos los botones en la ventana
        self.boton_1.pack(side="left", padx=1)
        self.boton_2.pack(side="left", padx=20)
        self.boton_3.pack(side="left")

    def abrir_cnd(self):
        # Creamos una instancia de la clase 1
        self.destruir_botones_main()
        clase_1 = Cnd(self.master)
        clase_1.mainloop()

    def abrir_ceh(self):
        # Creamos una instancia de la clase 2
        self.destruir_botones_main()
        clase_2 = Ceh(self.master)
        clase_2.mainloop()

    def abrir_lpic1(self):
        # Creamos una instancia de la clase LPIC
        self.destruir_botones_main()
        lpic1 = Lpic1(self.master)
        lpic1.mainloop()

    def destruir_botones_main(self):
        self.boton_1.destroy()
        self.boton_2.destroy()
        self.boton_3.destroy()
    
    def leer_fichero(self,archivo, numero_preguntas_examen):
        self.now = datetime.now()
        self.formatted = self.now.strftime("%d%m%Y-%H%M%S")
        with open(archivo, "r") as file:
            self.json_preguntas = json.load(file)
        with open(f"{self.json_preguntas['nombre']} {self.formatted}.txt", "a") as self.escritura:
            self.escritura.write(f"{self.json_preguntas['nombre']}\n")
        self.preguntas = self.json_preguntas['test']
        self.numero_preguntas_examen = numero_preguntas_examen

    def elegir_nuemero_preguntas(self):        
        self.label_pregunta_numero = tk.Label(self, text="", font=('Times 14', 14))
        self.label_pregunta_numero.pack()
        self.label_pregunta_numero.config(text=f'Hay un total de {len(self.preguntas)} preguntas o puedes elegir hacer el "Examen"\nDesde')
        self.entrada_numero = tk.Entry(self, font=('Times 14', 12), width=10)
        self.entrada_numero.pack()       
        self.label_pregunta_numero1 = tk.Label(self, text="", font=('Times 14', 14))
        self.label_pregunta_numero1.pack()
        self.label_pregunta_numero1.config(text='Hasta')
        self.salida_numero = tk.Entry(self, font=('Times 14', 12), width=10)
        self.salida_numero.pack()
        self.boton_siguiente_numero = tk.Button(self, text="Aceptar", command=self.guardar_numero_preguntas, font=('Times 14', 12))
        self.boton_siguiente_numero.pack()
        self.boton_test_prueba_numero = tk.Button(self, text="Examen de prueba", command=self.boton_test_prueba, font=('Times 14', 12))
        self.boton_test_prueba_numero.pack() 
        
    def boton_test_prueba(self):
        self.variable = self.test_pruebas
        self.pregunta_test = 0
        self.master.title(f"Examen de prueba - {self.json_preguntas['nombre']}")
        self.posiciones_aleatorias = [] # Lista para almacenar las posiciones aleatorias
        print(len(self.preguntas))
        self.cantidad_posiciones = self.numero_preguntas_examen # Número de posiciones que deseas imprimir de forma aleatoria
        # Generar 60 posiciones aleatorias únicas
        while len(self.posiciones_aleatorias) < self.cantidad_posiciones:
            posicion = random.randint(0, len(self.json_preguntas['test']) - 1)
            if posicion not in self.posiciones_aleatorias:
                self.posiciones_aleatorias.append(posicion)

        self.label_pregunta_numero.destroy()
        self.boton_siguiente_numero.destroy()
        self.label_pregunta_numero1.destroy()
        self.entrada_numero.destroy()
        self.salida_numero.destroy()
        self.boton_test_prueba_numero.destroy()
        
        self.interface_preguntas()
        self.boton_revelar_ocultar.destroy()
        self.test_pruebas()

    def guardar_numero_preguntas(self):
        self.variable = self.preguntas_corridas
        self.pregunta_actual = int(self.entrada_numero.get()) - 1
        self.pregunta_final = int(self.salida_numero.get())
        self.master.title(f"{self.json_preguntas['nombre']} del {self.entrada_numero.get()} al {self.salida_numero.get()}")
        self.label_pregunta_numero.destroy()
        self.boton_siguiente_numero.destroy()
        self.label_pregunta_numero1.destroy()
        self.entrada_numero.destroy()
        self.salida_numero.destroy()
        self.boton_test_prueba_numero.destroy()

        self.interface_preguntas()
        self.preguntas_corridas()

    def preguntas_corridas(self):
        if self.pregunta_actual < self.pregunta_final:
            self.cargar_pregunta()
        else:
            #PONER LA NOTA
            os.startfile(f"{self.json_preguntas['nombre']} {self.formatted}.txt")
            self.master.destroy()
        
    def test_pruebas(self):
        # Imprimir las posiciones seleccionadas
        #for posicion in self.posiciones_aleatorias:
        print(self.posiciones_aleatorias)
        if self.pregunta_test < self.cantidad_posiciones:
            self.pregunta_actual = self.posiciones_aleatorias[self.pregunta_test]
            self.cargar_pregunta()
        else:
            os.startfile(f"{self.json_preguntas['nombre']} {self.formatted}.txt")
            self.master.destroy()
       
    def interface_preguntas(self):
        
        self.label_pregunta = tk.Label(self, text="", font=('Times 14', 14))
        self.label_pregunta.pack()
        
        self.boton_revelar_ocultar = tk.Button(self, text="Revelar Respuesta", command=self.revelar_ocultar_respuesta, font=('Times 14', 12))
        self.boton_revelar_ocultar.pack()
        self.respuesta_visible = tk.BooleanVar(value=False)  # Variable de control para rastrear si la respuesta está visible 

        self.boton_siguiente = tk.Button(self, text="Siguiente", command=self.siguiente_pregunta, font=('Times 14', 12))
        self.boton_siguiente.pack(side='bottom', expand=True)

    def cargar_pregunta(self):
        self.opciones_respuestas = []
        self.pregunta = self.preguntas[self.pregunta_actual]
        if self.variable == self.preguntas_corridas:
            self.label_pregunta.config(text=f"{self.pregunta['numero']}. {self.pregunta['enunciado']} \n")
        else:
            self.label_pregunta.config(text=f"{self.pregunta_test + 1}. {self.pregunta['enunciado']} \n")    
        if self.preguntas[self.pregunta_actual]["tipo"] == "test":            
            self.respuesta_correcta = self.pregunta["resp"]
            if len(self.respuesta_correcta) == 1:
                self.una_respuesta()
            elif len(self.respuesta_correcta) > 1:
                self.varias_respuestas()
        else:
            self.entrada_respuesta = tk.Entry(self, font=('Times 14', 12), width=50)
            self.entrada_respuesta.pack()

    def varias_respuestas(self):
        pregunta = self.preguntas[self.pregunta_actual]
        for letra, respuesta in pregunta["respuestas"].items():
            self.variable_checkbutton = tk.BooleanVar()
            opcion = tk.Checkbutton(self, text=f"{letra.upper()}. {respuesta}", variable=self.variable_checkbutton, font=('Times 14', 12))
            self.opciones_respuestas.append([opcion, letra, self.variable_checkbutton])
            opcion.pack(anchor="w")  # "w" para alinear a la izquierda

    def una_respuesta(self):
        pregunta = self.preguntas[self.pregunta_actual]
        self.variable_radiobutton = tk.StringVar()
        for letra, respuesta in pregunta["respuestas"].items():
            opcion = tk.Radiobutton(self, text=f"{letra.upper()}. {respuesta}", variable=self.variable_radiobutton, value=letra, font=('Times 14', 12))
            self.opciones_respuestas.append(opcion)
            opcion.pack(anchor="w")  # "w" para alinear a la izquierda
    
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
            print(f"Pregunta {self.pregunta_actual}: Respuesta correcta")
        else:
            print(f"Pregunta {self.pregunta_actual + 1}: Respuesta incorrecta. \nRespuesta(s) correcta(s): {', '.join(self.respuesta_correcta)}")
            self.agregar_linea_a_archivo(f"Fallo en la pregunta {self.pregunta_actual + 1}\n")
    
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
            self.boton_revelar_ocultar.config(text="Ocultar Respuesta")
        else:
            self.label_pregunta.config(text=self.label_pregunta.cget("text").replace(f"\nRespuesta: {respuesta_actual}", ""))
            self.boton_revelar_ocultar.config(text="Revelar Respuesta")
        self.respuesta_visible.set(not self.respuesta_visible.get())

class Cnd(VentanaPrincipal):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Clase 1")
        super().__init__(master)
        super().destruir_botones_main()
        self.master.title("CND")
        self.fichero= "cnd.json"
        super().leer_fichero(self.fichero)
        super().elegir_nuemero_preguntas()
        self.pack()
        self.pack()
        # Mostramos un mensaje en la ventana
        tk.Label(self, text="Esta es la clase 1").pack()

class Ceh(VentanaPrincipal):
    def __init__(self, master):
        super().__init__(master)
        super().destruir_botones_main()
        self.master.title("CEH")
        self.numero_preguntas_examen = 100
        self.fichero= "ceh.json"
        super().leer_fichero(self.fichero,self.numero_preguntas_examen)
        super().elegir_nuemero_preguntas()
        self.pack()
        # Mostramos un mensaje en la ventana
        tk.Label(self, text="Esta es la clase 2").pack()

class Lpic1(VentanaPrincipal):
    def __init__(self, master):
        super().__init__(master)
        super().destruir_botones_main()
        self.master.title("LPIC1")
        self.numero_preguntas_examen = 60
        self.fichero= "json_cnd.json"
        super().leer_fichero(self.fichero, self.numero_preguntas_examen)
        super().elegir_nuemero_preguntas()
        #self.pack()

if __name__ == "__main__":
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    ventana_principal.mainloop()
