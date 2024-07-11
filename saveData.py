import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from the provided JSON file
credentials = service_account.Credentials.from_service_account_file(
    '/Users/lakshminarayanakakumanu/Documents/proven-dialect-412819-d4dd91d4e9c7.json', 
    scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Initialize the Sheets API client
service = build('sheets', 'v4', credentials=credentials)

# Define the Google Sheet ID
SHEET_ID = '1QLCXgobe44TusO1UlCr8Y6iDQKBY8R9EFPGRBv4WFNM'

# Function to get data from a specific sheet
def get_sheet_data(sheet_name):
    result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f'{sheet_name}!A1:Z').execute()
    values = result.get('values', [])
    return pd.DataFrame(values[1:], columns=values[0])

# Function to get formulas from a specific sheet
def get_sheet_formulas(sheet_name):
    result = service.spreadsheets().get(spreadsheetId=SHEET_ID, ranges=[f'{sheet_name}!A1:Z'], includeGridData=True).execute()
    sheet = result['sheets'][0]
    formulas = []
    for row in sheet['data'][0]['rowData']:
        row_formulas = []
        for cell in row.get('values', []):
            if 'userEnteredValue' in cell and 'formulaValue' in cell['userEnteredValue']:
                row_formulas.append(cell['userEnteredValue']['formulaValue'])
            else:
                row_formulas.append('')
        formulas.append(row_formulas)
    return pd.DataFrame(formulas[1:], columns=formulas[0])

# Get data and formulas from the specified sheets
stock_data = get_sheet_data('Stock')
sale_data = get_sheet_data('sale')
pur_data = get_sheet_data('Pur')
calculations_data = get_sheet_data('calculations')

stock_formulas = get_sheet_formulas('Stock')
sale_formulas = get_sheet_formulas('sale')
pur_formulas = get_sheet_formulas('Pur')
calculations_formulas = get_sheet_formulas('calculations')

# Save the data and formulas to CSV for review
stock_data.to_csv('stock_data.csv', index=False)
sale_data.to_csv('sale_data.csv', index=False)
pur_data.to_csv('pur_data.csv', index=False)
calculations_data.to_csv('calculations_data.csv', index=False)

stock_formulas.to_csv('stock_formulas.csv', index=False)
sale_formulas.to_csv('sale_formulas.csv', index=False)
pur_formulas.to_csv('pur_formulas.csv', index=False)
calculations_formulas.to_csv('calculations_formulas.csv', index=False)

# Display the data and formulas
print("Stock Data:")
print(stock_data.head())
print("Stock Formulas:")
print(stock_formulas.head())

print("Sale Data:")
print(sale_data.head())
print("Sale Formulas:")
print(sale_formulas.head())

print("Pur Data:")
print(pur_data.head())
print("Pur Formulas:")
print(pur_formulas.head())

print("Calculations Data:")
print(calculations_data.head())
print("Calculations Formulas:")
print(calculations_formulas.head())
