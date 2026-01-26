from src.Core.LoginSystem.Auth.Authentication import *
from src.Core.Modules.User import *
from src.Core.DB.DataBaseConnection import *

ExpectedVerdict = []
OutputedVerdict = []

def cleanup_test_users():
    """Clean up test users from previous runs"""
    try:
        dummy = User("dummyuser@mail.com", "dummyuser", "1234567890", "dummy", "user", "9999999901")
        dummy.DeleteUser()
    except:
        pass
    try:
        register_test = User("RegisterTest@mail.com", "RegisterTest", "1234567890", "Register", "Test", "9999999902")
        register_test.DeleteUser()
    except:
        pass

def Test():
    # Cleanup any existing test data first
    cleanup_test_users()
    
    # Use unique contact numbers for test users
    DUMMY_USER = User("dummyuser@mail.com", "dummyuser", "1234567890", "dummy", "user", "9999999901")

    # TEST 1: Register DUMMY_USER first (should succeed)
    ExpectedVerdict.append(True)
    Verdict = Authentication.Register(DUMMY_USER.getEmail(), DUMMY_USER.getUserName(), DUMMY_USER.getPassword(), DUMMY_USER.getFirstName(), DUMMY_USER.getLastName(), DUMMY_USER.getContactNumber())    
    OutputedVerdict.append(Verdict)

    # TEST 2: Try to register same user again (should fail - user already exists)
    ExpectedVerdict.append(False)
    Verdict = Authentication.Register(DUMMY_USER.getEmail(), DUMMY_USER.getUserName(), DUMMY_USER.getPassword(), DUMMY_USER.getFirstName(), DUMMY_USER.getLastName(), DUMMY_USER.getContactNumber())    
    OutputedVerdict.append(Verdict)

    # TEST 3: Login with DUMMY_USER (should succeed now that user exists)
    ExpectedVerdict.append(True)
    Verdict = Authentication.Login(DUMMY_USER.getUserName(), "1234567890")    
    OutputedVerdict.append(Verdict)

    # TEST 4: Register a new user (should succeed)
    ExpectedVerdict.append(True)
    Verdict = Authentication.Register("RegisterTest@mail.com", "RegisterTest", "1234567890", "Register", "Test", "9999999902")    
    OutputedVerdict.append(Verdict)

    # Cleanup after tests
    cleanup_test_users()

Test()
for i in range(len(ExpectedVerdict)):
    if ExpectedVerdict[i] == OutputedVerdict[i]:
        print("Test " + str(i) + " Passed")
    else:
        print("Test " + str(i) + " Failed")
