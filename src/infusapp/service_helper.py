import re


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
