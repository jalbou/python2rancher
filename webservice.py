from flask import Flask , render_template
import workloadfunc as workload
app = Flask(__name__)

@app.route("/create/<service>")
def create(service):
    return workload.create(service)
@app.route("/remove/<name>")
def remove(name):
    return str(workload.remove(name))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)