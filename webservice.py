from flask import Flask , render_template, Response
import workloadfunc as workload
import json
app = Flask(__name__)

@app.route("/create/<service>")
def create(service):
    return workload.create(service)
@app.route("/remove/<name>")
def remove(name):
    return str(workload.remove(name))

@app.route("/get/<name>")
def get(name):
    return workload.get(name)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)