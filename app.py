from flask import Flask, render_template, request

import pickle

# from sklearn.preprocessing import StandardScaler
from datetime import date
app = Flask(__name__)
model = pickle.load(open('decision_tree_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


# standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        current_date=date.today()
        age=current_date.year-Year
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven=Kms_Driven/1000
        Owner_fresh=1
        Own=request.form['Owner']
        if(Own=="Second Hand"):
            Owner_fresh=0

        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0
        Fuel=request.form['Fuel']
        if(Fuel=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif Fuel=='Diesel':
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Seller_Type=request.form['Seller_Type_Individual']
        Seller_Type_Individual=0
        if(Seller_Type=='Individual'):
            Seller_Type_Individual=1
        Transmission=request.form['Transmission_Mannual']
        Transmission_Mannual=0
        if(Transmission=='Mannual'):
            Transmission_Mannual=1
        prediction=model.predict([[Present_Price,Kms_Driven,age,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual,Owner_fresh]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)