import pyautogui
import pytesseract
import time
import re
import requests
import json
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
import threading

# Configuración
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajustar según instalación
intervalo_captura = 5  # segundos entre capturas
DEEPSEEK_API_KEY = "sk-b0b4237dd6b04467a9196a275e57158c"  # Reemplazar con tu API key real
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Verificar URL actual de la API

class QuestionDetectorApp:
    def __init__(self, root):
        self.root = root
        root.title("Detector de Preguntas con DeepSeek")
        
        # Configuración de la interfaz
        self.setup_ui()
        
        # Variables de control
        self.running = False
        self.last_question = ""
        
    def setup_ui(self):
        # Área de texto para mostrar preguntas detectadas
        self.question_label = tk.Label(self.root, text="Pregunta detectada:")
        self.question_label.pack(pady=5)
        
        self.question_text = scrolledtext.ScrolledText(self.root, height=5, width=60)
        self.question_text.pack(pady=5)
        
        # Área de texto para mostrar respuestas de DeepSeek
        self.answer_label = tk.Label(self.root, text="Respuesta de DeepSeek:")
        self.answer_label.pack(pady=5)
        
        self.answer_text = scrolledtext.ScrolledText(self.root, height=15, width=60)
        self.answer_text.pack(pady=5)
        
        # Botones de control
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Iniciar", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(self.button_frame, text="Detener", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.exit_button = tk.Button(self.button_frame, text="Salir", command=self.root.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
    def start_detection(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Iniciar el hilo de detección
        self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
        self.detection_thread.start()
        
    def stop_detection(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
    def detection_loop(self):
        while self.running:
            try:
                # 1. Capturar pantalla
                screenshot = pyautogui.screenshot()
                
                # 2. Procesar imagen con OCR
                texto = pytesseract.image_to_string(screenshot)
                
                # 3. Buscar signos de interrogación
                if re.search(r'\?', texto):
                    self.last_question = texto
                    self.root.after(0, self.update_question_display, texto)
                    
                    # 4. Obtener respuesta de DeepSeek
                    respuesta = self.get_deepseek_response(texto)
                    self.root.after(0, self.update_answer_display, respuesta)
                    
                time.sleep(intervalo_captura)
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(intervalo_captura)
                
    def update_question_display(self, question):
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(tk.END, question)
        
    def update_answer_display(self, answer):
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, answer)
        
    def get_deepseek_response(self, question):
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",  # Verificar modelo actual
            "messages": [
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "No se pudo obtener respuesta")
            
        except requests.exceptions.RequestException as e:
            return f"Error al conectar con DeepSeek: {str(e)}"
            
    def on_closing(self):
        self.running = False
        self.root.destroy()

# Función principal
def main():
    root = tk.Tk()
    app = QuestionDetectorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    print("Iniciando sistema de detección de preguntas con DeepSeek...")
    main()