#!/usr/bin/env python3
import csv
import json
import sys

def convert_demographics_csv_to_json():
    """Convert KFF demographics CSV to MongoDB JSON format"""
    demographics_data = []
    
    with open('data/KFF_Population_by_Race_Ethnicity.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip empty rows and metadata rows
            if not row['Location'] or row['Location'].startswith('Notes') or row['Location'].startswith('Sources'):
                continue
            
            # Skip United States total and Puerto Rico
            if row['Location'] in ['United States', 'Puerto Rico']:
                continue
                
            # Clean and convert data
            demographics_record = {
                "Location": row['Location'],
                "White": clean_percentage(row['White']),
                "Black": clean_percentage(row['Black']),
                "Hispanic": clean_percentage(row['Hispanic']),
                "American_Indian_Alaska_Native": clean_percentage(row['American Indian/Alaska Native']),
                "Asian": clean_percentage(row['Asian']),
                "Native_Hawaiian_Pacific_Islander": clean_percentage(row['Native Hawaiian/Other Pacific Islander']),
                "Two_Or_More_Races": clean_percentage(row['Two Or More Races']),
                "Total": clean_percentage(row['Total'])
            }
            demographics_data.append(demographics_record)
    
    # Write to JSON file
    with open('US_State_Demographics_By_Race.json', 'w') as f:
        json.dump(demographics_data, f, indent=2)
    
    print(f"Created US_State_Demographics_By_Race.json with {len(demographics_data)} records")

def clean_percentage(value):
    """Clean percentage values, handle special cases"""
    if not value or value == 'N/A':
        return "0"
    if value.startswith('<'):
        return "0.005"  # For values like "<.01"
    return value

def convert_police_killings_csv_to_json():
    """Convert Fatal Encounters CSV to MongoDB JSON format"""
    killings_data = []
    
    print("Converting police killings CSV... this may take a moment due to file size")
    
    with open('data/Fatal_Encounters_Police_Killings_2000_2020.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            count += 1
            if count % 5000 == 0:
                print(f"Processed {count} records...")
            
            # Skip empty rows
            if not row.get('Name') and not row.get('State'):
                continue
            
            # Create MongoDB document
            killing_record = {
                "Unique_ID": row.get('Unique ID', ''),
                "Name": row.get('Name', ''),
                "Age": clean_number(row.get('Age', '')),
                "Gender": row.get('Gender', ''),
                "Race": row.get('Race', ''),
                "Race with imputations": row.get('Race with imputations', ''),
                "Date": row.get('Date of injury resulting in death (month/day/year)', ''),
                "Location": row.get('Location of injury (address)', ''),
                "City": row.get('Location of death (city)', ''),
                "State": row.get('State', ''),
                "ZIP": row.get('Location of death (zip code)', ''),
                "County": row.get('Location of death (county)', ''),
                "Agency": row.get('Agency or agencies involved', ''),
                "Cause_of_death": row.get('Cause of death', ''),
                "Description": row.get('Brief description', ''),
                "Latitude": clean_number(row.get('Latitude', '')),
                "Longitude": clean_number(row.get('Longitude', ''))
            }
            killings_data.append(killing_record)
    
    # Write to JSON file
    with open('US_Police_Killings.json', 'w') as f:
        json.dump(killings_data, f, indent=2)
    
    print(f"Created US_Police_Killings.json with {len(killings_data)} records")

def clean_number(value):
    """Clean numeric values"""
    if not value or value == 'N/A':
        return None
    try:
        return float(value)
    except:
        return None

if __name__ == "__main__":
    print("Converting CSV files to MongoDB JSON format...")
    convert_demographics_csv_to_json()
    convert_police_killings_csv_to_json()
    print("Conversion complete!")