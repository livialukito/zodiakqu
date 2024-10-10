from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI  # Updated import
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("Missing OpenAI API Key. Please ensure it is in the .env file.")

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI LLM via LangChain's updated OpenAI class
llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

# Function to determine zodiac sign
def get_zodiac_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    # Continue adding other zodiac signs...

# Function to call the OpenAI GPT model using LangChain's invoke method
def get_horoscope(zodiac_sign):
    # Create a prompt using PromptTemplate
    prompt_template = """
    You are a professional fortune teller. Give a detailed horoscope for the zodiac sign {zodiac_sign}. 
    The horoscope should include predictions for career, love, and health.
    """
    prompt = PromptTemplate(input_variables=["zodiac_sign"], template=prompt_template)
    
    # Call the OpenAI model using the LangChain invoke method
    result = llm.invoke(prompt.format(zodiac_sign=zodiac_sign))
    
    return result

# API endpoint to accept birthdate input and return zodiac horoscope
@app.route('/api/zodiac-horoscope', methods=['POST'])
def zodiac_horoscope():
    try:
        # Get data from request
        data = request.get_json()
        day = int(data['day'])
        month = int(data['month'])
        year = int(data['year'])

        # Get zodiac sign based on birthdate
        zodiac_sign = get_zodiac_sign(day, month)
        
        if zodiac_sign:
            # Get horoscope prediction
            horoscope = get_horoscope(zodiac_sign)
            response = {
                'zodiac_sign': zodiac_sign,
                'horoscope': horoscope
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid date of birth."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
