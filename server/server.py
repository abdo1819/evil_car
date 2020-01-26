from flask import Flask,jsonify,request,render_template
import json
app = Flask(__name__)
violations_list= []
speedLimit = 0.1

@app.route('/speed',methods=["GET"])
def getSpeed():
    # return request.args.get('long')+" - "+request.args.get('lat')
    # TODO: do some server logic here
    long = float(request.args.get('long'))
    lat = float(request.args.get('lat'))
    return jsonify(speed = speedLimit,endingLong=long+1,endingLat=lat+1)

@app.route('/report',methods=["GET","POST"])
def report():
    if request.method=="POST":
        #TODO: do more than printing the data here
        violations_list.append(request.get_data(as_text=True))
        print(violations_list)
        print("really?!")
        return "thanks for using our service"
    else:
        return "use post to post your violation"


@app.route('/violations/json',methods=["GET"])
def get_violations_json():
    objects ={}
    for string in violations_list : 
        objects.update( json.loads(string))
    return jsonify(objects)

@app.route('/violations', methods=['GET'])
def get_violations():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)