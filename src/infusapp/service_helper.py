import re
import random


### ID/NAME IN DATABASE?
def check_existence(entries, field_name, search_value):
    for entry in entries:
        if getattr(entry, field_name) == search_value:
            return True
    return False


### NAME VALID?
def val_name(search_value):
    return bool(re.search(r"^[a-zA-Z]{2,16} [a-zA-Z]{2,16}$", search_value.strip()))


### FIND ID/NAME WITH NAME/ID
def find_by_value(entries, field_name, search_value):
    for entry in entries:
        if getattr(entry, field_name) == search_value:
            return entry  # Patient Name and Patient ID
    return None

### GENERATE ID
def generate_id(entries, field_name, min_value, max_value):
    while True:
        new_id = str(random.randrange(min_value, max_value))
        if not check_existence(entries, field_name, new_id):
            return new_id
