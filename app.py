import pickle
from flask import Flask, render_template, request, redirect
import requests
import numpy as np
import sklearn


app = Flask(__name__)

# Loading model
model = pickle.load(open("Linear_regressor.pkl", "rb"))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')
# This function is executed when the form is posted
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        # Accessing content of form using there name attribute
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Age = int(request.form['Age'])
        Fuel_Type = request.form['Fuel_Type']
        if(Fuel_Type == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        Seller_Type = request.form['Seller_Type']
        if(Seller_Type == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission = request.form['Transmission']
        if(Transmission == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0

        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Age, Fuel_Type_Diesel,
                                     Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])

        output = round(prediction[0], 2)

        if output < 0:
            return render_template('result.html', prediction_text="<h2>Sorry you cannot sell this car</h2>")
        else:
            return render_template('result.html', prediction_text="You can sell the car at {} Lacs".format(output))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)