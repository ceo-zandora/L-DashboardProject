from agent import getData
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

def convert_data(raw_data):
    data = []
    for item in raw_data:
        key = item['d_key']
        if key != "NEWS":
            value = json.loads(item['d_value'])  # Convert string to JSON
            # Replace underscores with spaces in the keys of the value dictionary
            new_value = {k.replace('_', ' '): v for k, v in value.items()}
            data.append({key: new_value})
        else:
            news = str(item['d_value'])

    return data, news

@app.route('/')
def index():
    raw_data = getData()
    processed_data, news = convert_data(raw_data)
    return render_template('index.html', data=processed_data, news=news)

if __name__ == '__main__':
    app.run()