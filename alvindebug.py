import os

def setExctDirt(directory):
    dir_old = os.getcwd()
    try:
        os.chdir(directory)
        print("Debug path successfully changed to {}".format(directory))
    except Exception as e:
        print("Debug directory changing failed...")
        print(e)
    
    return