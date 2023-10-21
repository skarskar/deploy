from flask import Flask, request, jsonify
import joblib
import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd

app = Flask(__name__)

# Load the model and scaler
model = load_model('content/model')
scaler = joblib.load('capstone_scaler.pkl')
encoder = joblib.load('capstone_encoder.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json['data']
        if(input_data['recoveries']>7.5):
            input_data['recoveries']=1
        if(input_data['collection_recovery_fee']>1.3):
            input_data['collection_recovery_fee']=1
        if(input_data['total_received_late_fee']>1.3):
            input_data['total_received_late_fee']=1
        print(input_data)
        df = pd.DataFrame.from_dict(pd.json_normalize(input_data), orient='columns')
        df.rename(columns={"delinquency_two_years": "delinquency_-_two_years", 
                    "inquires_six_months": "inquires_-_six_months", 
                    "revolving_balance": "log_revolving_balance", 
                    "total_current_balance": "log_total_current_balance", 
                    "total_revolving_credit_limit": "log_total_revolving_credit_limit",
                    "collection_recovery_fee": "collection_recovery_fee_ind",
                    "total_received_late_fee": "total_received_late_fee_ind",
                    "recoveries": "recoveries_ind"}, inplace=True)
        df.log_revolving_balance=np.log(1+df.log_revolving_balance)
        df.log_total_current_balance=np.log(1+df.log_total_current_balance)
        df.log_total_revolving_credit_limit=np.log(1+df.log_total_revolving_credit_limit)
        
        encoded = encoder.transform(df)
        scaled_data = scaler.transform(encoded)
        prediction = model.predict(scaled_data)
        return jsonify(prediction.tolist())
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
