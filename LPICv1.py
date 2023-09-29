import tkinter as tk
import json

class Cuestionario:
    def __init__(self, ventana, preguntas):
        self.ventana = ventana
        self.ventana.title("LPIC")
        
        self.preguntas = preguntas["tests"]
        self.respuestas_usuario = []  # Lista para almacenar las respuestas del usuario
        self.pregunta_actual = 18

        self.frame_pregunta = tk.Frame(ventana)
        self.frame_pregunta.pack()
        
        self.label_pregunta = tk.Label(self.frame_pregunta, text="", font=('Times 14', 14))
        self.label_pregunta.pack()
        
        self.frame_botones = tk.Frame(ventana)
        self.frame_botones.pack()
        
        self.opciones_respuestas = []
        self.respuesta_correcta = []
        
        self.boton_siguiente = tk.Button(self.frame_botones, text="Siguiente", command=self.mostrar_siguiente_pregunta, font=('Times 14', 12))
        self.boton_siguiente.pack()
        
        self.boton_revelar_ocultar = tk.Button(self.frame_botones, text="Revelar Respuesta", command=self.revelar_ocultar_respuesta, font=('Times 14', 12))
        self.boton_revelar_ocultar.pack()
        self.respuesta_visible = tk.BooleanVar(value=False)  # Variable de control para rastrear si la respuesta está visible o no
        
        self.cargar_pregunta()
    
    def cargar_pregunta(self):
        self.opciones_respuestas = []
        pregunta = self.preguntas[self.pregunta_actual]
        self.label_pregunta.config(text=f"{pregunta['numero']}. {pregunta['enunciado']} \n")
        
        if self.preguntas[self.pregunta_actual]["tipo"] == "test":
            if self.pregunta_actual < len(self.preguntas):
                self.respuesta_correcta = pregunta["resp"]
                if len(self.respuesta_correcta) == 1:
                    self.una_respuesta()
                elif len(self.respuesta_correcta) > 1:
                    self.varias_respuestas()
            else:
                self.ventana.destroy()
                print("Cuestionario completado")
        else:
            self.entrada_respuesta = tk.Entry(self.frame_pregunta, font=('Times 14', 12), width=50)
            self.entrada_respuesta.pack()
    
    def varias_respuestas(self):
        pregunta = self.preguntas[self.pregunta_actual]
        for letra, respuesta in pregunta["respuestas"].items():
            self.variable_checkbutton = tk.BooleanVar()
            opcion = tk.Checkbutton(self.frame_pregunta, text=f"{letra.upper()}. {respuesta}", variable=self.variable_checkbutton, font=('Times 14', 12))
            self.opciones_respuestas.append([opcion, letra, self.variable_checkbutton])
            opcion.pack(anchor="w")  # "w" para alinear a la izquierda

    def una_respuesta(self):
        pregunta = self.preguntas[self.pregunta_actual]
        self.variable_radiobutton = tk.StringVar()
        for letra, respuesta in pregunta["respuestas"].items():
            opcion = tk.Radiobutton(self.frame_pregunta, text=f"{letra.upper()}. {respuesta}", variable=self.variable_radiobutton, value=letra, font=('Times 14', 12))
            self.opciones_respuestas.append(opcion)
            opcion.pack(anchor="w")  # "w" para alinear a la izquierda
    
    def mostrar_siguiente_pregunta(self):

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
                self.cargar_pregunta()
                
            elif len(self.respuesta_correcta) == 1:
                self.respuesta_usuario = [self.variable_radiobutton.get()]
                self.corregir()
                # Eliminar los botones de radio anteriores
                for radio_button in self.opciones_respuestas:
                    radio_button.destroy()
                self.cargar_pregunta()
        else:
            self.respuesta_usuario = self.entrada_respuesta.get()
            self.respuesta_correcta = self.preguntas[self.pregunta_actual]["resp"][0]
    
            if self.respuesta_usuario.lower() == self.respuesta_correcta.lower():
                print("Respuesta correcta")
            else:
                print("Respuesta incorrecta")
            print(f"entre por aqui! y {self.entrada_respuesta.get()}, ANd {self.respuesta_correcta}")    

            self.entrada_respuesta.delete(0, tk.END)
            self.entrada_respuesta.destroy()
            self.pregunta_actual += 1
            self.cargar_pregunta()
    
    def corregir(self):   
        if self.respuesta_usuario == self.respuesta_correcta:
            print(f"Pregunta {self.pregunta_actual + 1}: Respuesta correcta")
        else:
            print(f"Pregunta {self.pregunta_actual + 1}: Respuesta incorrecta. Respuesta(s) correcta(s): {', '.join(self.respuesta_correcta)}")
        self.pregunta_actual += 1
    
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

def cargar_preguntas_desde_json(archivo):
    with open(archivo, "r") as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    preguntas = cargar_preguntas_desde_json("json_cnd.json")
    
    ventana_principal = tk.Tk()
    app = Cuestionario(ventana_principal, preguntas)
    ventana_principal.mainloop()
