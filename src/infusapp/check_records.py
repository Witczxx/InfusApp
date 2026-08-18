from tabulate import tabulate 

class CheckRecords:
    def __init__(self, records):
        self.records = records

    def show_records(self):
        print(self.records)
        return self.records


def main():
    records = get_records()
    all_keys = list(records[0].keys())
    print("Choose Values to display")
    for x, key in enumerate(all_keys, start=1):
        print(f"{x}: {key}")
    print("Enter all numbers of keys you want ")
    choices = input("Input: ")
    chosen_keys = []
    for number in choices.replace(",", " ").split():
        idx = int(number) - 1
        chosen_keys.append(all_keys[idx])
    rows = [{k: r[k] for k in chosen_keys} for r in records]
    print(tabulate(rows, headers="keys", tablefmt="grid", maxcolwidths=15))




def get_records():
    records = [{
        'nurse_id': '1000000',
        'nurse_name': 'Max Mustermann',
        'patient_id': '1000000000',
        'patient_name': 'Anna Schmidt',
        'medication': 'FUROSEMIDE',
        'strength': '10MG/ML',
        'dose_format': 'INJECTABLE | SOLUTION',
        'unit': '5 Units',
        'carrier_fluid': 'NaCl 0.9%',
        'fluid_volume': '500',
        'drops_per_min': 87.00539442643309,
        'ml_per_hour': 261.0161832792993,
        }]
    return records



if __name__ == "__main__":
    main()
