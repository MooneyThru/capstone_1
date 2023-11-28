from flask import Flask, request, jsonify
import webbrowser
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html', encoding='utf-8').read()

@app.route('/add_animal', methods=['POST'])
def add_animal():
    data = request.json
    animal = data.get('animal')
    with open('cart_items.txt', 'a') as file:
        file.write(animal + '\n')
    return '', 204

@app.route('/get_animals', methods=['GET'])
def get_animals():
    with open('animals.txt', 'r') as file:
        animals = file.readlines()
    animals = [animal.strip() for animal in animals]
    return jsonify(animals=animals)

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # 웹 브라우저를 별도의 스레드에서 열기
    threading.Timer(1.25, open_browser).start()
    app.run(host='0.0.0.0', port=5000)
