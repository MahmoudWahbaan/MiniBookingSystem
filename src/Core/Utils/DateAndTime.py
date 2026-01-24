from datetime import datetime
FORMAT = '%Y:%m:%d:%H:%M'

def validateDate(date):
    try:
        datetime.strptime(date, FORMAT)
        return True
    except ValueError:
        return False

def PrepareDate(date):
    return datetime.strptime(date, FORMAT)

'''
TESTS
'''
def Test():
    Test_1 = "2022:13:12:23:00" # Expected False
    Test_2 = "-1:01:01:00:00" # Expected False
    Test_3 = "2022:01:01:00:00" # Expected True
    Test_4 = "2022:01:100:00:00" # Expected False
    Tests = [Test_1, Test_2, Test_3, Test_4]
    Expected  = [False, False, True, False]
    for i in range(len(Tests)):
        print(f"Test {i+1}: {Tests[i]} - Expected: {Expected[i]} - Result: {validateDate(Tests[i])}")
