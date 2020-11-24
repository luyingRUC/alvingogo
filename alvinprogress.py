import time

def reportProgress(taskDescription, n_total, n_current, n_step = 1):
    if(n_current % n_step == 0):
        print("   Current Task: %s, Current Progress: %i/%i, %f percentage "%(taskDescription, n_current, n_total, 100 * (n_current/n_total)))
    return 

def alvinSleep(sleep_length):
    print("\t sleeping for {0} seconds... wait... ".format(sleep_length))
    time.sleep(sleep_length)
    return