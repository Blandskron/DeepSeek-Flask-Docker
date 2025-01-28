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