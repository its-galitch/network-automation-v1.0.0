import csv
import os

def load_inventory_from_csv(file_path):
    """טעינת מכשירים מקובץ CSV והפיכתם לרשימת מילונים"""
    device_list = []
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        return []
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        # DictReader משתמש בשורה הראשונה ככותרות למפתחות במילון
        reader = csv.DictReader(f)
        for row in reader:
            device_list.append(row)
    return device_list