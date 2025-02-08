from flask import Flask, request, jsonify
from PIL import Image
import io
import google.generativeai as genai

api_key = "AIzaSyCIeHx-ufHGYjt17e53LkT-jGJDukXLF9I"
genai.configure(api_key=api_key)

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Retrieve the image file from the request
        image_file = request.files['image']
        prompt = request.form['prompt']

        # Read the image file using PIL
        image = Image.open(io.BytesIO(image_file.read()))

        # Function to generate response from Gemini AI
        def get_gemini_response(input_prompt, image):
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([input_prompt, image])
            return response.text

        # Get response text from Gemini AI
        response_text = get_gemini_response(prompt, image)

        # Prepare response JSON
        response = {
            "response": response_text
        }

        return jsonify(response), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
