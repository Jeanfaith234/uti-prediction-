import numpy as np
import pandas as pd
import pickle
from flask_mongoengine import MongoEngine
from flask import Flask, request, render_template, jsonify
import json
import sys

app = Flask(__name__,template_folder="templates")
app.config['MONGODB_SETTINGS'] = {
    'db': 'MDRTB',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    age = db.StringField()
    sex = db.StringField()
    marital_status = db.StringField()
    poverty_level = db.StringField()
    prison_history = db.StringField()
    completed_secondary = db.StringField()
    tobacco_use= db.StringField()
    alcohol_use = db.StringField()
    drug_use = db.StringField()
    rehab = db.StringField()
    body_mass_index = db.StringField()
    chronic_disease = db.StringField()
    hiv_status = db.StringField()
    diabetes =db.StringField()
    treatment = db.StringField()
    label =db.StringField()
    def to_json(self):
        return {'Age':self.age,
        'Sex':self.sex,
        'Marital Status':self.marital_status,
        'Poverty Level':self.poverty_level,
        'Prison History':self.prison_history,
        'Completed Secondary Education':self.completed_secondary,
        'History of Tobacco Use':self.tobacco_use,
        'Alcohol Use at Least Once Per Week':self.alcohol_use,
        'History of Drug Use':self.drug_use,
        'History of Rehab':self.rehab,
        'Body Mass Index':self.body_mass_index,
        'History of Chronic Disease':self.chronic_disease
        ,'HIV Status':self.hiv_status,
        'History Diabetes Melitus':self.diabetes,
        'Treatment Outcome':self.treatment,
            "label": self.label}

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')   
@app.route('/getdata')
def getdata():
    return render_template('fetch.html')      

# Route 'classify' accepts GET request
@app.route('/classify',methods=['POST'])
def classify_type():
    try:
        age = request.form.get('age') # Get parameters for sepal length
        sex = request.form.get('sex')
        marital_status = request.form.get('marital_status')
        poverty_level = request.form.get('poverty_level')
        prison_history = request.form.get('prison_history')
        completed_secondary = request.form.get('completed_secondary')
        tobacco_use= request.form.get('tobacco_use')
        alcohol_use = request.form.get('alcohol_use')
        drug_use = request.form.get('drug_use')
        rehab = request.form.get('rehab')
        body_mass_index = request.form.get('body_mass_index')
        chronic_disease = request.form.get('chronic_disease')
        hiv_status = request.form.get('hiv_status')
        diabetes = request.form.get('diabetes')
        treatment = request.form.get('treatment')

        int_features = [x for x in request.form.values()]
        #print(int_features)
        final = np.array(int_features)
        data_unseen = pd.DataFrame([final], columns = [ 'Age','Sex','Marital Status','Poverty Level','Prison History','Completed Secondary Education','History of Tobacco Use','Alcohol Use at Least Once Per Week','History of Drug Use','History of Rehab','Body Mass Index','History of Chronic Disease','HIV Status','History Diabetes Melitus','Treatment Outcome'])                         
        
        prediction = model.predict(data_unseen)

        output = prediction
        
        if output == 1:
            label = 'Yes'
        else:
            label = 'No'



        user = User(age=age,
                sex=sex,
                marital_status=marital_status,
                poverty_level =poverty_level,
                prison_history =prison_history,
                completed_secondary=completed_secondary,
                tobacco_use=tobacco_use,
                alcohol_use=alcohol_use,
                drug_use =drug_use,
                rehab= rehab,
                body_mass_index=body_mass_index,
                chronic_disease=chronic_disease,
                hiv_status=hiv_status,
                diabetes=diabetes,
                treatment =treatment,
                label =label
)
        user.save()
        #print((user.to_json()))

        # Render the output in new HTML page
        return render_template('output.html', variety='MDR-TB Classification Status is {}'.format(label))
    except:
        return 'Error'    



## database functions 
@app.route('/fetchall', methods=['GET'])
def query_records():
    #age = str(request.args.get('age'))
    #print(age)
    #user = User.objects(age=age)
    user = User.objects()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        labels = json.loads(user.to_json())
        return render_template('dbvalues.html', labels=labels)
           

@app.route('/delete', methods=['DELETE',"POST","GET"])
def delete_record():
    user = User.objects()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
        return jsonify({'error': 'data not found'})

if __name__ =="__main__":
    app.run(debug = True)