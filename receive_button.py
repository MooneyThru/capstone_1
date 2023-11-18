from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    fruits = ['바나나', '사과', '키위']
    return render_template('index.html', fruits=fruits)

@app.route('/submit', methods=['POST'])
def submit():
    selected_fruit = request.form.get('fruit')
    return f'당신이 선택한 과일은: {selected_fruit}'

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
