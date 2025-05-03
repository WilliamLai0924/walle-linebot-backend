import google.generativeai as genai
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

key = os.environ.get('gkey', None)
if key is None:
    key = config['gemini']['key']

genai.configure(api_key = key)

model = genai.GenerativeModel('gemini-2.0-flash')

def chat(prompt):
    return model.generate_content(prompt).text