# Desplegar DeepSeek-V3 localmente en Docker con Flask

Este repositorio contiene los pasos necesarios para desplegar el modelo DeepSeek-V3 en un contenedor Docker utilizando Flask. El modelo se carga localmente desde archivos descargados previamente, lo que evita la necesidad de descargarlo desde Hugging Face cada vez que se ejecuta el contenedor.

---

## Requisitos previos

1. **Docker**: Asegúrate de tener Docker instalado en tu sistema. Puedes descargarlo desde [la página oficial de Docker](https://www.docker.com/products/docker-desktop).
2. **Archivos del modelo**: Descarga todos los archivos del modelo DeepSeek-V3 (incluyendo los pesos y la configuración) y colócalos en una carpeta local (por ejemplo, `modelo_local/`).

---

## Estructura del proyecto

El proyecto debe tener la siguiente estructura de archivos:

```
/proyecto
│
├── Dockerfile
├── requirements.txt
├── app.py
└── modelo_local/
    ├── config.json
    ├── pytorch_model.bin
    ├── model-00001-of-000163
    ├── model-00002-of-000163
    ├── ...
    └── special_tokens_map.json
```

---

## Pasos para desplegar el modelo

### 1. Crear el archivo `app.py`

Este archivo contiene el código de Flask para cargar el modelo y exponer un endpoint para generar texto.

```python
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__)

# Ruta local al modelo
MODEL_PATH = "/app/modelo_local"

# Cargar el tokenizador y el modelo
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

# Crear una pipeline para generación de texto
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')
    result = text_generator(text, max_length=50)  # Ajusta los parámetros según sea necesario
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### 2. Crear el archivo `requirements.txt`

Este archivo lista las dependencias de Python necesarias.

```
flask
torch
transformers
```

---

### 3. Crear el archivo `Dockerfile`

Este archivo define la imagen Docker que ejecutará la aplicación.

```Dockerfile
# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el modelo local
COPY modelo_local /app/modelo_local

# Copiar el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
```

---

### 4. Construir la imagen Docker

Ejecuta el siguiente comando en la terminal para construir la imagen Docker:

```bash
docker build -t deepseek-local .
```

---

### 5. Ejecutar el contenedor

Una vez construida la imagen, ejecuta el contenedor con el siguiente comando:

```bash
docker run -p 5000:5000 deepseek-local
```

Esto mapeará el puerto 5000 del contenedor al puerto 5000 de tu máquina local.

---

### 6. Probar la aplicación

Envía una solicitud POST a `http://localhost:5000/predict` con un cuerpo JSON que contenga el texto que deseas procesar. Por ejemplo:

```json
{
  "text": "Hola, ¿cómo estás?"
}
```

Deberías recibir una respuesta con el texto generado por el modelo.

---

## Opcional: Usar un volumen para el modelo

Si prefieres no copiar el modelo en la imagen Docker, puedes montar la carpeta del modelo como un volumen al ejecutar el contenedor:

```bash
docker run -p 5000:5000 -v /ruta/al/modelo_local:/app/modelo_local deepseek-local
```

Esto evitará que el modelo se incluya en la imagen Docker, lo que puede ser útil si el modelo es muy grande o si cambia con frecuencia.

---

## Consideraciones adicionales

- **Sin GPU**: El modelo se ejecutará en la CPU, lo que puede ser lento para modelos grandes. Considera reducir el tamaño del modelo o utilizar técnicas de optimización como la cuantización.
- **Tamaño del contenedor**: Si el modelo es muy grande, la imagen Docker resultante también será grande. Usar volúmenes puede ayudar a reducir el tamaño de la imagen.

---

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
