from flask import Flask , render_template
import workloadfunc as workload
app = Flask(__name__)

@app.route("/create")
def create():
    return workload.create('web')
@app.route("/remove")
def remove():
    workload.remove('minecraft1')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)