import os, time

class Output:
    # calulcates time taken in script execution
    def time_taken(start_time):
        print("\nTotal time taken: " + \
        "{}s".format(round((time.time() - start_time), 2)))
