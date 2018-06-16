class FileHelper:
    file = None
    
    def __init__(self, file_name):
        self.file = open(file_name, 'w')

    def write(self, data):
        self.file.write(data)

    def write_line(self, line):
        self.file.write(line + "\n")