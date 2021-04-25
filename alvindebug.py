import os

def setDebugDirt(directory):
    dir_old = os.getcwd()
    try:
        os.chdir(directory)
        print("Debug path successfully changed from {} to {}".format(dir_old, directory))
    except Exception as e:
        print("Debug directory changing failed...")
        print(e)
    
    return