from manager import Manager

if __name__ == '__main__':
    filename = "selects.sql"
    #filename = "sample_database.sql"
    file = open(filename, "r")
    text = file.read()

    m = Manager("test")
    m.execute(text)


