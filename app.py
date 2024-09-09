from flask import Flask,render_template,request
import pandas as pd 
import tensorflow as tf 
import numpy as np
import pickle
 
app = Flask(__name__)

#load the model
with open('prediction.pkl', 'rb') as file:
    model = pickle.load(file) 

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict',methods=['get','post'])

def predict():
    if request.method=='POST':
        # Date_of_Journey
        date_dep = request.form["dep_Time"]
        Flight_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Flight_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hr = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
    

        # Arrival
        date_arr = request.form["arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)

        # Duration
        Duration_hours = (Arrival_hour - Dep_hr)
        Duration_mins = (Arrival_min - Dep_min)
 

        # Total Stops
        Stop = int(request.form["stop"])
        

        # Airline
        airline=request.form['airline']
        if(airline=='Air_India'):
           Airline_Air_India=1
           Airline_Vistara=0
           Airline_SpiceJet=0
           Airline_AirAsia=0
           Airline_GO_FIRST=0
           Airline_Indigo=0
           Airline_Trujet=0
           Airline_StarAir=0 

        elif (airline=='Vistara'):
           Airline_Air_India=0
           Airline_Vistara=1
           Airline_SpiceJet=0
           Airline_AirAsia=0
           Airline_GO_FIRST=0
           Airline_Indigo=0
           Airline_Trujet=0
           Airline_StarAir=0 

        elif (airline=='SpiceJet'):
           Airline_Air_India=0
           Airline_Vistara=0
           Airline_SpiceJet=1
           Airline_AirAsia=0
           Airline_GO_FIRST=0
           Airline_Indigo=0
           Airline_Trujet=0
           Airline_StarAir=0 
            
        elif (airline=='AirAsia'):
           Airline_Air_India=0
           Airline_Vistara=0
           Airline_SpiceJet=0
           Airline_AirAsia=1
           Airline_GO_FIRST=0
           Airline_Indigo=0
           Airline_Trujet=0
           Airline_StarAir=0 
            
        elif (airline=='GO_FIRST'):
           Airline_Air_India=0
           Airline_Vistara=0
           Airline_SpiceJet=0
           Airline_AirAsia=0
           Airline_GO_FIRST=1
           Airline_Indigo=0
           Airline_Trujet=0
           Airline_StarAir=0 
            
        elif (airline=='Indigo'):
           Airline_Air_India=0
           Airline_Vistara=0
           Airline_SpiceJet=0
           Airline_AirAsia=0
           Airline_GO_FIRST=0
           Airline_Indigo=1
           Airline_Trujet=0
           Airline_StarAir=0 

        elif (airline=='Trujet'):
           Airline_Air_India=0
           Airline_Vistara=0
           Airline_SpiceJet=0
           Airline_AirAsia=0
           Airline_GO_FIRST=0
           Airline_Indigo=0
           Airline_Trujet=1
           Airline_StarAir=0 

        else:
           Airline_Air_India=0
           Airline_Vistara=0
           Airline_SpiceJet=0
           Airline_AirAsia=0
           Airline_GO_FIRST=0
           Airline_Indigo=0
           Airline_Trujet=0
           Airline_StarAir=1

         
        Source = request.form["source"]
        if (Source == 'Delhi'):
            Source_Delhi = 1
            Source_Mumbai = 0
            Source_Bangalore = 0
            Source_Kolkata=0
            Source_Hyderabad=0
            Source_Chennai=0

        elif (Source == 'Mumbai'):
            Source_Delhi = 0
            Source_Mumbai = 1
            Source_Bangalore = 0
            Source_Kolkata=0
            Source_Hyderabad=0
            Source_Chennai=0

        elif (Source == 'Bangalore'):
            Source_Delhi = 0
            Source_Mumbai = 0
            Source_Bangalore = 1
            Source_Kolkata=0
            Source_Hyderabad=0
            Source_Chennai=0

        elif (Source == 'Kolkata'):
            Source_Delhi = 0
            Source_Mumbai = 0
            Source_Bangalore = 0
            Source_Kolkata=1
            Source_Hyderabad=0
            Source_Chennai=0

        elif (Source == 'Hyderabad'):
            Source_Delhi = 0
            Source_Mumbai = 0
            Source_Bangalore = 0
            Source_Kolkata=0
            Source_Hyderabad=1
            Source_Chennai=0

        else:
            Source_Delhi = 0
            Source_Mumbai = 0
            Source_Bangalore = 0
            Source_Kolkata=0
            Source_Hyderabad=0
            Source_Chennai=1

    
        Destination = request.form["destination"]
        if (Destination == 'Delhi'):
            Destination_Delhi = 1
            Destination_Mumbai = 0
            Destination_Bangalore = 0
            Destination_Kolkata=0
            Destination_Hyderabad=0
            Destination_Chennai=0

        elif (Destination == 'Mumbai'):
            Destination_Delhi = 0
            Destination_Mumbai = 1
            Destination_Bangalore = 0
            Destination_Kolkata=0
            Destination_Hyderabad=0
            Destination_Chennai=0

        elif (Destination == 'Bangalore'):
            Destination_Delhi = 0
            Destination_Mumbai = 0
            Destination_Bangalore = 1
            Destination_Kolkata=0
            Destination_Hyderabad=0
            Destination_Chennai=0

        elif (Destination == 'Kolkata'):
            Destination_Delhi = 0
            Destination_Mumbai = 0
            Destination_Bangalore = 0
            Destination_Kolkata=1
            Destination_Hyderabad=0
            Destination_Chennai=0

        elif (Destination == 'Hyderabad'):
            Destination_Delhi = 0
            Destination_Mumbai = 0
            Destination_Bangalore = 0
            Destination_Kolkata=0
            Destination_Hyderabad=1
            Destination_Chennai=0

        else:
            Destination_Delhi = 0
            Destination_Mumbai = 0
            Destination_Bangalore = 0
            Destination_Kolkata=0
            Destination_Hyderabad=0
            Destination_Chennai=1
        
        Class=int(request.form['class'])
        input_data=pd.DataFrame({
            'Stop':[Stop],
            'Class':[Class],
            'Dep_hr':[Dep_hr],
            'Dep_min':[Dep_min],
            'Flight_day':[Flight_day],
            'Flight_month':[Flight_month],
            'Duration_hours':[Duration_hours],
            'Duration_mins':[Duration_mins],
            'Airline_Air India':[Airline_Air_India],
            'Airline_AirAsia':[Airline_AirAsia],
            'Airline_GO FIRST':[Airline_GO_FIRST],
            'Airline_Indigo':[Airline_Indigo],
            'Airline_SpiceJet':[Airline_SpiceJet],
            'Airline_StarAir':[Airline_StarAir],
            'Airline_Trujet':[Airline_Trujet],
            'Airline_Vistara':[Airline_Vistara],
            'Source_Bangalore':[Source_Bangalore],
            'Source_Chennai':[Source_Chennai],
            'Source_Delhi':[Source_Delhi],
            'Source_Hyderabad':[Source_Hyderabad],
            'Source_Kolkata':[Source_Kolkata],
            'Source_Mumbai':[Source_Mumbai],
            'Destination_Bangalore':[Destination_Bangalore],
            'Destination_Chennai':[Destination_Chennai],
            'Destination_Delhi':[Destination_Delhi],
            'Destination_Hyderabad':[Destination_Hyderabad],
            'Destination_Kolkata':[Destination_Kolkata],
            'Destination_Mumbai':[Destination_Mumbai]
        })
        print(input_data)
        prediction=model.predict(input_data)
        output=round(prediction[0],2)
     
        return render_template('index.html',prediction_text="Your Flight price is Re.{}".format(output))
    
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


