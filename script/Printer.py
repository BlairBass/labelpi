import cups

class Printer:
    def __init__(self, configuration):
        self.configuration = configuration
        self.conn = cups.Connection()


    def print_file(self, filename, callback=None, qty=1):
        self.conn.printFile("DYMO_LabelWriter_450_Turbo_ND", filename, title='test', options={"copies": str(qty)})
        if callback is not None:
            callback(filename)
