from packaging import version
import os, time, json, csv
import pandas as pd
import xlsxwriter
from columnar import columnar

class Output:
    # calulcates time taken in script execution
    def time_taken(start_time):
        print("\nTotal time taken: " + \
        "{}s".format(round((time.time() - start_time), 2)))

    # remove unicode characters for reporting
    def remove_unicode(x):
        a = ['No' if v in [u'\u2717', None] else v for v in x]
        b = ['Yes' if v in [u'\u2714'] else v for v in a]
        return b         

    # define filename for csv_out and json_out functions
    def filename(directory, k8s_object, extension):
        filename =  directory + k8s_object + "_" + extension
        return filename

    def print_table(data):
        l1, l2 = len(data), len(data[0])
        pd.DataFrame(data, index=['']*l1, columns=['']*l2).T

    def csv_out(data, headers, k8s_object):
        directory = './reports/csv/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = Output.filename(directory, k8s_object, 'report.csv')
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(i for i in headers)
            for j in data:
                x = Output.remove_unicode(j)
                writer.writerow(x)

    # generating json data
    def json_out(data, headers, k8s_object):
        json_data = []
        headers = [x.lower() for x in headers]
        for item in data:
            temp_dic = {}
            # storing json data in dict for each list in data
            for i in range(len(headers)):
                for j in range(len(item)):
                    temp_dic.update({headers[i]:item[i]})

            # appending all json dicts to form a list
            json_data.append(temp_dic)
        directory = './reports/json/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        # writing out json data in file based on object type and config being checked
        filename = Output.filename(directory, k8s_object, 'report.json')
        f = open(filename, 'w')
        f.write(json.dumps(json_data))
        f.close()
        return json_data

    # prints table from lists of lists: data
    def print_table(data, headers, verbose):
        if verbose and len(data) != 0:
            table = columnar(data, headers, no_borders=True, row_sep='-')
            print (table)
        else:
            return        