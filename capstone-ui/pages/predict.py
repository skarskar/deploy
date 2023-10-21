import streamlit as st
import requests

st.set_option('deprecation.showPyplotGlobalUse', False)
#st.set_option('showWarningOnDirectExecution ', False)

st.title('Input data to Predict using the Model')
loan_amount = st.number_input('Loan Amount',help='Loan Amount applied',format='%i', value='min',min_value=1000)
funded_amount = st.number_input('Funded Amount',help='The total amount committed to that loan at that point in time.',format='%i', value='min',min_value=0)
funded_amount_investor = st.number_input('Funded Amount by Investors',help='The total amount committed by investors for that loan at that point in time.',format='%i', value='min',min_value=0)
term = st.selectbox(
    'Term: ',
    (36, 58, 59), index=0)
# batch_enrolled = st.selectbox(
#     'Batch Enrolled: ',
#     ('BAT1104812', 'BAT1135695', 'BAT1184694', 'BAT1467036',
#        'BAT1586599', 'BAT1761981', 'BAT1766061', 'BAT1780517',
#        'BAT1930365', 'BAT2003848', 'BAT2078974', 'BAT2136391',
#        'BAT224923', 'BAT2252229', 'BAT2333412', 'BAT2428731',
#        'BAT2522922', 'BAT2558388', 'BAT2575549', 'BAT2803411',
#        'BAT2833642', 'BAT3193689', 'BAT3461431', 'BAT3726927',
#        'BAT3865626', 'BAT3873588', 'BAT4136152', 'BAT4271519',
#        'BAT4351734', 'BAT4694572', 'BAT4722912', 'BAT4808022',
#        'BAT5341619', 'BAT5489674', 'BAT5525466', 'BAT5547201',
#        'BAT5629144', 'BAT5714674', 'BAT5811547', 'BAT5849876',
#        'BAT5924421'), help='batch numbers to representatives')
interest_rate = st.number_input('Interest Rate',help='Interest Rate (%) on loan',value='min',min_value=0.00)
grade = st.selectbox(
    'Grade: ',
    ('A', 'B', 'C', 'D', 'E', 'F', 'G'), help='grade by the bank', index=0)
sub_grade = st.selectbox(
    'Sub Grade: ',
    ('A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1',
       'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2',
       'E3', 'E4', 'E5', 'F1', 'F2', 'F3', 'F4', 'F5', 'G1', 'G2', 'G3',
       'G4', 'G5'), help='sub-grade by the bank', index=0)
home_ownership = st.selectbox(
    'Home Ownership: ',
    ('MORTGAGE', 'OWN', 'RENT'), index=0)
annual_income = st.number_input('Annual Income', value='min',min_value=0.00)
loan_title = st.selectbox(
    'Loan Title: ',
    ('BATHROOM', 'BILLS', 'BILL_CONSOLIDATION', 'BILL_PAYOFF',
       'BUSINESS', 'CARDS', 'CARD_CONSOLIDATION', 'CAR_FINANCING',
       'CAR_LOAN', 'CC', 'CC-REFINANCE', 'CC_CONSOLIDATION', 'CC_LOAN',
       'CC_REFI', 'CC_REFINANCE', 'CONSO', 'CONSOLIDATE', 'CONSOLIDATED',
       'CONSOLIDATION', 'CONSOLIDATION_LOAN', 'CREDIT', 'CREDIT_CARD',
       'CREDIT_CARDS', 'CREDIT_CARD_CONSOLIDATION', 'CREDIT_CARD_DEBT',
       'CREDIT_CARD_LOAN', 'CREDIT_CARD_PAYDOWN', 'CREDIT_CARD_PAYOFF',
       'CREDIT_CARD_PAY_OFF', 'CREDIT_CARD_REFI', 'CREDIT_CARD_REFINANCE',
       'CREDIT_CARD_REFINANCE_LOAN', 'CREDIT_CARD_REFINANCING',
       'CREDIT_CONSOLIDATION', 'CREDIT_LOAN', 'CREDIT_PAYOFF',
       'CREDIT_PAY_OFF', 'DEBT', 'DEBT_CONSOLIDATION',
       'DEBT_CONSOLIDATION_2013', 'DEBT_CONSOLIDATION_LOAN', 'DEBT_FREE',
       'DEBT_LOAN', 'DEBT_PAYOFF', 'DEBT_REDUCTION', 'DEPT_CONSOLIDATION',
       'FREEDOM', 'GETTING_AHEAD', 'GET_DEBT_FREE', 'GET_OUT_OF_DEBT',
       'GREEN_LOAN', 'HOME', 'HOME_BUYING', 'HOME_IMPROVEMENT',
       'HOME_IMPROVEMENT_LOAN', 'HOME_LOAN', 'HOUSE', 'LENDING_CLUB',
       'LENDING_LOAN', 'LOAN', 'LOAN1', 'LOAN_1', 'LOAN_CONSOLIDATION',
       'MAJOR_PURCHASE', 'MEDICAL', 'MEDICAL_EXPENSES', 'MEDICAL_LOAN',
       'MOVING_AND_RELOCATION', 'MYLOAN', 'MY_LOAN', 'OTHER', 'PAYOFF',
       'PAY_OFF', 'PAY_OFF_BILLS', 'PERSONAL', 'PERSONAL_LOAN', 'POOL',
       'REFI', 'REFINANCE', 'REFINANCE_LOAN', 'RELIEF', 'VACATION',
       'WEDDING_LOAN'), index=31)
debit_to_income = st.number_input('Debt to Income', value='min',min_value=0.00, help='ratio of representative''s total monthly debt repayment divided by self reported monthly income excluding mortgage')
delinquency_two_years = st.slider('Delinquency - two years: ', min_value=0, max_value=8, value=0, format='%i',step=1, help='The number of 30+ days past-due incidences of delinquency in the borrower''s credit file for the past 2 years')
inquires_six_months = st.slider('Inquires - six months: ', min_value=0, max_value=5, value=0, format='%i',step=1, help='total number of inquiries in last 6 months')
open_account = st.slider('Open Account: ', min_value=1, max_value=50, value=1, format='%i',step=1, help='number of open credit line in representative''s - credit line')

public_record = st.slider('Public Record: ', min_value=0, max_value=3, value=0, format='%i',step=1 )
revolving_balance = st.number_input('Revolving Balance', value='min',min_value=0, format='%i', help='total credit revolving balance')
revolving_utilities = st.number_input('Revolving Utilities', value='min',min_value=0.00, format='%f', help='amount of credit a representative is using - relative to revolving_balance')
total_accounts = st.slider('Total Accounts: ', min_value=1, max_value=100, value=1, format='%i',step=1, help='total number of credit lines available in - representatives credit line')

total_received_interest = st.number_input('Total Received Interest', value='min',min_value=0.00, format='%f', help='total interest received till date')
total_received_late_fee = st.number_input('Total Received Late Fee', value='min',min_value=0.00, format='%f', help='total late fee received till date')
recoveries = st.number_input('Recoveries', value='min',min_value=0.00, format='%f', help='post charge off gross recovery')
collection_recovery_fee = st.number_input('Collection Recovery Fee', value='min',min_value=0.00, format='%f', help='post charge off collection fee')

collection_12_months_medical = st.number_input('Collection 12 months Medical', value='min',min_value=0, format='%i', help='total collections in last 12 months - excluding medical collections')
last_week_pay = st.slider('Last week Pay (in weeks)', min_value=1, max_value=200, value=1,step=1, format='%i', help='indicates how long (in weeks) a representative has paid EMI after batch enrolled')
total_collection_amount = st.number_input('Total Collection Amount', value='min',min_value=0, format='%i', help='total collection amount ever owed')
total_current_balance = st.number_input('Total Current Balance', value='min',min_value=0, format='%i', help='total current balance from all accounts')
total_revolving_credit_limit = st.number_input('Total Revolving Credit Limit', value='min',min_value=0, format='%i', help='total revolving credit limit')


if st.button("Predict Loan Default", type="primary"):
    try:
        payload = {
            'loan_amount':0,
            'funded_amount':0,
            'funded_amount_investor':0,
            'term':0,
            'interest_rate':0.00,
            'grade':'A'.lower(),
            'sub_grade':'A1'.lower(),
            'home_ownership':'mortgage'.lower(),
            'annual_income':0.00,
            'loan_title': 'CREDIT_CARD_REFINANCE_LOAN'.lower(),
            'debit_to_income':0.00,
            'delinquency_two_years':0,
            'inquires_six_months':0,
            'open_account':1,
            'public_record':0,
            'revolving_utilities':0.00,
            'total_accounts':1,
            'total_received_interest':0.00,
            'collection_12_months_medical':0,
            'last_week_pay':1,
            'total_collection_amount':0,
            'total_current_balance':0,
            'total_revolving_credit_limit':0,
            'revolving_balance':0,
            'collection_recovery_fee':0.00,
            'total_received_late_fee':0.00,
            'recoveries':0.00,
        }
        payload['loan_amount']=loan_amount
        payload['funded_amount']=funded_amount
        payload['funded_amount_investor']=funded_amount_investor
        payload['term']=term
        payload['interest_rate']=interest_rate
        payload['grade']=grade.lower()
        payload['sub_grade']=sub_grade.lower()
        payload['home_ownership']=home_ownership.lower()
        payload['annual_income']=annual_income
        payload['loan_title']=loan_title.lower()
        payload['debit_to_income']=debit_to_income
        payload['delinquency_two_years']=delinquency_two_years
        payload['inquires_six_months']=inquires_six_months
        payload['open_account']=open_account
        payload['public_record']=public_record
        payload['revolving_utilities']=revolving_utilities
        payload['total_accounts']=total_accounts
        payload['total_received_interest']=total_received_interest
        payload['collection_12_months_medical']=collection_12_months_medical
        payload['last_week_pay']=last_week_pay
        payload['total_collection_amount']=total_collection_amount
        payload['total_current_balance']=total_current_balance
        payload['total_revolving_credit_limit']=total_revolving_credit_limit
        payload['revolving_balance']=revolving_balance
        payload['collection_recovery_fee']=collection_recovery_fee
        payload['total_received_late_fee']=total_received_late_fee
        payload['recoveries']=recoveries
        st.text('payload')
        st.code(payload)

        url = "https://5000-skarskar-deploy-llwiy9ll881.ws-us105.gitpod.io/predict"
        response = requests.post(url, json={'data': payload})
        response.raise_for_status()
        # Print the response from the microservice
        st.text("Status Code: {code}".format(code = response.status_code))
        st.text("Response JSON: {json}".format(json = response.json()))
    except requests.exceptions.HTTPError as errh:
        st.subheader('Error')
        st.text(errh.args)
