from google import genai
import json
import os
from dotenv import load_dotenv

# Secure tareeke se API key load karna
load_dotenv()

def extract_invoice_details(image):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"error": "API Key is missing! Please check your .env file."}
            
        client = genai.Client(api_key=api_key)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # 🚨 THE UPDATED GOD-MODE PROMPT (WITH TAX INCLUDED) 🚨
        prompt = """
        You are a highly advanced OCR and Data Parsing AI. Read EVERY SINGLE DETAIL from this bill.
        Return ONLY a valid JSON object. Do not include markdown blocks like ```json.
        Structure it exactly like this, capturing all available text:
        {
            "Shop Details": {
                "Vendor Name": "",
                "Address": "",
                "Phone Numbers": "",
                "GSTIN": ""
            },
            "Customer Details": {
                "Name": "",
                "Address": ""
            },
            "Bill Info": {
                "Invoice Number": "",
                "Date": "YYYY-MM-DD"
            },
            "Items List": [
                {"Item Name": "Name of product", "Qty": "Quantity", "Rate": "Price", "Amount": "Total"}
            ],
            "Financials": {
                "Tax Amount": "Total tax (like GST, CGST, SGST) if present, else 0",
                "Total Amount": "Final total amount in numbers only"
            }
        }
        If any specific piece of info is missing, leave it empty "".
        """
        
        print("🤖 Secure connection established. Scanning models...")
        
        available_models = [m.name for m in client.models.list()]
        chosen_model = 'gemini-1.5-flash' 
        
        for m in available_models:
            name = m.replace('models/', '') 
            if 'gemini' in name and 'embed' not in name and 'vision' not in name:
                chosen_model = name
                if 'flash' in name: 
                    break
        
        response = client.models.generate_content(
            model=chosen_model,
            contents=[prompt, image]
        )
        
        print("✅ Success! Bill read securely.")

        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:-3]
        elif text_response.startswith("```"):
            text_response = text_response[3:-3]
            
        data = json.loads(text_response)
        return data
        
    except Exception as e:
        return {"error": f"Google Server Error: {str(e)}"}