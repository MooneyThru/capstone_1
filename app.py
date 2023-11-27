from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html', encoding='utf-8').read()

@app.route('/add_animal', methods=['POST'])
def add_animal():
    data = request.json
    animal = data.get('animal')
    with open('animals.txt', 'a') as file:
        file.write(animal + '\n')
    return '', 204

@app.route('/get_animals', methods=['GET'])
def get_animals():
    with open('animals.txt', 'r') as file:
        animals = file.readlines()
    animals = [animal.strip() for animal in animals]
    return jsonify(animals=animals)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
