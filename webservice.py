from flask import Flask , render_template
import workloadfunc as workload
app = Flask(__name__)

@app.route("/create")
def hello():
    workload.create('minecraft',1)
    workload.create('web',1)

if __name__ == '__main__':
    app.run(debug=True)