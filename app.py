from flask import Flask, request
#from main import model

app = Flask(__name__)

@app.route('/')
def home():
    return "HELLO"

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        obj = request.json
        print(obj)
    else:
        return "REQUEST INVALID"


if __name__ == "__main__":
    app.run(debug=True)
