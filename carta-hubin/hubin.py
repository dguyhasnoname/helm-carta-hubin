import sys, time, os, getopt, json, re
from subprocess import check_output
start_time = time.time()
from modules import helpers as k8s
from modules import logging as logger

class Charts:
    global _logger, installed_charts_json
    _logger = logger.get_logger('Charts')
    
    def get_installed_charts_json():
        _logger.info("checking helm charts")
        # installed_charts_json = os.popen("helm list -A -o json").read()
        command = "helm list -A -o json"
        output = check_output(["helm", "list", "-A" , "-o", "json"]).decode("utf-8")
        # converting return object to json object
        installed_charts_json = json.loads(re.sub('(?<=[^,:{}])(\\\")(?=[^,:{}])','\\"',output))
        print (installed_charts_json)
        return installed_charts_json
    
    installed_charts_json = get_installed_charts_json()

    def get_charts_list():
        _logger.info("adding helm repos")
        os.system("./helm-repo.sh  >/dev/null 2>&1")
        
        for chart in installed_charts_json:
            chart_name = chart['name']
            latest_chart = check_output("helm", "search" "repo", chart_name , "-o", "json")
            print (chart['name'], latest_chart)

def call_all(v,namespace):
    Charts.get_charts_list()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvn:", ["help", "verbose", "namespace"])
        if not opts:        
            call_all("","")
            k8s.Output.time_taken(start_time)
            sys.exit()
            
    except getopt.GetoptError as err:
        print(err)
        return
    verbose, ns = '', ''
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-n", "--namespace"):
            if not verbose: verbose = False
            namespace = a          
        else:
            assert False, "unhandled option"
    call_all(verbose,namespace)
    k8s.Output.time_taken(start_time)     

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[ERROR] " \
        'Interrupted from keyboard!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)