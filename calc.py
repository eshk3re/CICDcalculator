from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])

def calculate():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')
    operator = data.get('operator')

    if a is None or b is None or operator is None:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        a = int(a)
        b = int(b)
    except ValueError:
        return jsonify({'error': 'Invalid numbers'}), 400

    if operator == '+':
        result = a + b
    elif operator == '-':
        result = a - b
    elif operator == '*':
        result = a * b
    elif operator == '/':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a / b
    else:
        return jsonify({'error': 'Invalid operator'}), 400
    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
