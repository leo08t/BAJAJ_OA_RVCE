import json
import pandas as pd
from datetime import datetime
from collections import Counter
from scipy.stats import pearsonr

# Load the JSON file
with open('C:/Users/soura/Downloads/DataEngineeringQ2.json') as f:
    data = json.load(f)


# Extract patientDetails and medicines from consultationData
records = []
for record in data:
    patient_details = record['patientDetails']
    consultation_data = record['consultationData']
    medicines = consultation_data['medicines']
    for medicine in medicines:
        patient_info = {
            'patient_id': patient_details.get('_id', ''),
            'first_name': patient_details.get('firstName', ''),
            'last_name': patient_details.get('lastName', ''),
            'email_id': patient_details.get('emailId', ''),
            'gender': patient_details.get('gender', ''),
            'birth_date': patient_details.get('birthDate', ''),
            'phone_number': record.get('phoneNumber', '')
        }
        medicine_info = {
            'medicine_id': medicine.get('medicineId', ''),
            'medicine_name': medicine.get('medicineName', ''),
            'frequency': medicine.get('frequency', ''),
            'duration': medicine.get('duration', ''),
            'duration_in': medicine.get('durationIn', ''),
            'instruction': medicine.get('instruction', ''),
            'is_active': medicine.get('isActive', '')
        }
        combined_record = {**patient_info, **medicine_info}
        records.append(combined_record)

# Create a DataFrame
df = pd.DataFrame(records)

# Convert birth_date to datetime
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')

# Summarize medications by patient
medication_summary = df.groupby(['patient_id', 'first_name', 'last_name']).agg({
    'medicine_name': lambda x: ', '.join(x),
    'duration': 'sum'
}).reset_index()

# Validation
missing_values = df.isnull().sum()
unique_patient_ids = df['patient_id'].nunique() == len(df['patient_id'])

# Insights
common_meds = df['medicine_name'].value_counts().head(10)
most_meds = df.groupby('patient_id').size().sort_values(ascending=False).head(10)

# Output results
print("Missing Values:\n", missing_values)
print("\nUnique Patient IDs:", unique_patient_ids)
print("\nMost Common Medications:\n", common_meds)
print("\nPatients with Most Medications:\n", most_meds)
print("\nMedication Summary:\n", medication_summary.head())


# QUESTION NUMBER 4

patient_details = [record['patientDetails'] for record in data]

# Create a DataFrame
df = pd.DataFrame(patient_details)

# Define a function to calculate the percentage of missing values
def calculate_missing_percentage(column):
    total = len(column)
    missing = column.apply(lambda x: x == '' or pd.isna(x)).sum()
    percentage = (missing / total) * 100
    return round(percentage, 2)

# Calculate missing percentages for the specified columns
first_name_missing_percentage = calculate_missing_percentage(df['firstName'])
last_name_missing_percentage = calculate_missing_percentage(df['lastName'])
birth_date_missing_percentage = calculate_missing_percentage(df['birthDate'])

# Print the results in the required format
print(f"{first_name_missing_percentage}, {last_name_missing_percentage}, {birth_date_missing_percentage}")

# QUESTION NUMBER 5 

# Extract patientDetails
patient_details = [record['patientDetails'] for record in data]

# Create a DataFrame
df = pd.DataFrame(patient_details)

# Impute missing values in the gender column with the mode
mode_gender = df['gender'].mode()[0]
df['gender'].fillna(mode_gender, inplace=True)
df['gender'].replace('', mode_gender, inplace=True)

# Calculate the percentage of females
total_count = len(df)
female_count = (df['gender'] == 'F').sum()
female_percentage = (female_count / total_count) * 100
female_percentage_rounded = round(female_percentage, 2)

# Print the result
print(female_percentage_rounded)

# QUESTION NUMBER 6

# Extract patientDetails
patient_details = [record['patientDetails'] for record in data]

# Create a DataFrame
df = pd.DataFrame(patient_details)

# Convert birth_date to datetime
df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')

# Calculate age
current_year = datetime.now().year
df['age'] = current_year - df['birthDate'].dt.year

# Define age groups
def categorize_age(age):
    if pd.isna(age):
        return 'Unknown'
    elif age <= 12:
        return 'Child'
    elif 13 <= age <= 19:
        return 'Teen'
    elif 20 <= age <= 59:
        return 'Adult'
    elif age >= 60:
        return 'Senior'
    else:
        return 'Unknown'

# Create ageGroup column
df['ageGroup'] = df['age'].apply(categorize_age)

# Count the number of adults
adult_count = df[df['ageGroup'] == 'Adult'].shape[0]

# Print the result
print(adult_count)

# QUESTION NUMBER 7

medicine_counts = []
for record in data:
    consultation_data = record['consultationData']
    medicines = consultation_data['medicines']
    medicine_counts.append(len(medicines))

# Calculate the average number of medicines prescribed
average_medicines = sum(medicine_counts) / len(medicine_counts)
average_medicines_rounded = round(average_medicines, 2)

# Print the result
print(average_medicines_rounded)

# QUESTION NUMBER 8 

medicine_names = []
for record in data:
    consultation_data = record['consultationData']
    medicines = consultation_data['medicines']
    for medicine in medicines:
        medicine_names.append(medicine['medicineName'])

# Count the frequency of each medicine name
medicine_counts = Counter(medicine_names)

# Determine the 3rd most frequently prescribed medicine name
most_common_medicines = medicine_counts.most_common()
third_most_frequent_medicine = most_common_medicines[2][0]

# Print the result
print(third_most_frequent_medicine)

# QUESTION NUMBER 9 

active_count = 0
inactive_count = 0

for record in data:
    consultation_data = record['consultationData']
    medicines = consultation_data['medicines']
    for medicine in medicines:
        if medicine['isActive']:
            active_count += 1
        else:
            inactive_count += 1

# Calculate total number of medicines
total_medicines = active_count + inactive_count

# Calculate the percentage distribution
active_percentage = (active_count / total_medicines) * 100
inactive_percentage = (inactive_count / total_medicines) * 100

# Round the percentages to 2 decimal places
active_percentage = round(active_percentage, 2)
inactive_percentage = round(inactive_percentage, 2)

# Print the result in the required format
print(f"{active_percentage}, {inactive_percentage}")

# QUESTION NUMBER 10

patient_details = [record['patientDetails'] for record in data]
phone_numbers = [record.get('phoneNumber', '') for record in data]

# Create a DataFrame
df = pd.DataFrame(patient_details)
df['phoneNumber'] = phone_numbers

# Define the function to check if a phone number is valid
def is_valid_mobile(phone_number):
    # Remove any spaces or special characters
    phone_number = phone_number.replace(' ', '').replace('-', '')

    # Check for prefix '+91' or '91'
    if phone_number.startswith('+91'):
        phone_number = phone_number[3:]
    elif phone_number.startswith('91'):
        phone_number = phone_number[2:]

    # Check if the remaining number is within the valid range
    if phone_number.isdigit() and len(phone_number) == 10:
        phone_number_int = int(phone_number)
        if 6000000000 <= phone_number_int <= 9999999999:
            return True
    return False

# Add the isValidMobile column to the DataFrame
df['isValidMobile'] = df['phoneNumber'].apply(is_valid_mobile)

# Count the number of valid phone numbers
valid_phone_count = df['isValidMobile'].sum()

# Print the result
print(valid_phone_count)

# QUESTION NUMBER 11

records = []
for record in data:
    patient_details = record['patientDetails']
    consultation_data = record['consultationData']
    medicines = consultation_data['medicines']
    num_medicines = len(medicines)
    
    birth_date = patient_details.get('birthDate', None)
    if birth_date:
        birth_date = pd.to_datetime(birth_date, errors='coerce')
        age = datetime.now().year - birth_date.year
    else:
        age = None
    
    records.append({
        'patient_id': patient_details.get('_id', ''),
        'age': age,
        'num_medicines': num_medicines
    })

# Create a DataFrame
df = pd.DataFrame(records)

# Drop rows where age is NaN
df = df.dropna(subset=['age'])

# Calculate Pearson correlation
correlation, _ = pearsonr(df['age'], df['num_medicines'])

# Round the Pearson correlation to two decimal places
correlation_rounded = round(correlation, 2)

# Print the result
print(correlation_rounded)
