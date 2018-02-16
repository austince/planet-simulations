from csv import DictWriter, DictReader
from abc import abstractmethod, ABCMeta


class Simulation(metaclass=ABCMeta):
    fieldnames = []

    def get_csv_reader(self, csvfile):
        return DictReader(csvfile, fieldnames=self.fieldnames)

    def get_csv_writer(self, csvfile):
        return DictWriter(csvfile, fieldnames=self.fieldnames)

    def prepare_file(self, outfile):
        with open(outfile, 'w') as csvfile:
            writer = self.get_csv_writer(csvfile)
            writer.writeheader()

    def get_key_index(self, key):
        return self.fieldnames.index(key)

    @abstractmethod
    def write_row(self, outfile):
        pass

    @abstractmethod
    def run(self, outfile):
        pass
