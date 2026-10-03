from tabulate import tabulate

class RecordUi:

    def __init__(self, record_rep):
        self.record_rep = record_rep

    def run(self, nurse):
        records = self.record_rep.get_records(nurse=nurse)
        print(tabulate(records, headers=records[0].keys(), tablefmt="grid", maxcolwidths=15))
        input("\n---Press any key to return to the Home Screen---")
