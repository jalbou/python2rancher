from flask import Flask
import workloadfunc as workload
app = Flask(__name__)

@app.route("/")
def hello():
    workload.create('web',2)

if __name__ == '__main__':
    app.run(debug=True)