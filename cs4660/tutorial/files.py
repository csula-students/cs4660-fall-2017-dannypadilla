"""Files tests simple file read related operations"""

class SimpleFile(object):
    """SimpleFile tests using file read api to do some simple math"""
    def __init__(self, file_path):
        self.numbers = [] # used lineSplit instead
        """
        TODO: reads the file by path and parse content into two
        dimension array (numbers)
        """
        self.openFile = open(file_path)
        self.readFile = self.openFile.read()
        self.splitReadFile = self.readFile.split("\n")
        self.lineSplit = [line.split(" ") for line in self.splitReadFile] # list comprehension X)
        self.openFile.close()

    def get_mean(self, line_number):
        """
        get_mean retrieves the mean value of the list by line_number (starts
        with zero)
        """
        return self.get_sum(line_number) * 1.0 / len(self.lineSplit[line_number]) # for python2 compatibility (float)

    def get_max(self, line_number):
        """
        get_max retrieves the maximum value of the list by line_number (starts
        with zero)
        """
        numMax = self.lineSplit[line_number]
        numMax.sort()
        return int(numMax[-1])

    def get_min(self, line_number):
        """
        get_min retrieves the minimum value of the list by line_number (starts
        with zero)
        """
        numMin = self.lineSplit[line_number]
        numMin.sort()
        return int(numMin[0])

    def get_sum(self, line_number):
        """
        get_sum retrieves the sumation of the list by line_number (starts with
        zero)
        """
        sum = 0
        for number in self.lineSplit[line_number]:
            sum += int(number)
        return sum
