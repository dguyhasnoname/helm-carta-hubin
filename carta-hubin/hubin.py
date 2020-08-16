import sys, time, os, getopt, re
import simplejson as json
import base64, zlib
from subprocess import check_output
from distutils.version import StrictVersion
start_time = time.time()
from modules import helpers as k8s
from modules.get_secrets import K8sSecrets
from modules import logging as logger

class Charts:
    global _logger, installed_charts
    _logger = logger.get_logger('Charts')
    
    def get_installed_charts(namespace):
        data, temp_item = [], ''
        _logger.info("checking helm charts")
        ns = 'all'
        secrets = K8sSecrets.get_secrets(ns)
        for item in secrets.items:
            # decoding base64 twice
            item_zip = base64.b64decode(base64.b64decode(item.data['release']))

            # decompressing output of base64. shell equivalent command: 
            # kubectl get secrets -n kube-system -l owner=helm -o json \
            # | jq .data.release | tr -d '"' | base64 --decode | base64 --decode | gzip -d 
            item_decompressed = zlib.decompress(item_zip, 16+zlib.MAX_WBITS)
            item_json =  (json.dumps(item_decompressed))
            item_chart_metadata = item_json.replace('\\', '')

            # re to find chart metadata as var item_chart_metadata is not json
            # item_chart_metadata = re.findall(r'chart":(.+?),"lock', item_chart_metadata)

            item_chart_name = re.findall(r'metadata":{"name":"(.+?)"', \
                              item_chart_metadata)


            if not item_chart_name[0][0] == temp_item:
                item_chart_version = re.findall(r'version":"(.+?)"', \
                                    item_chart_metadata)
                item_chart_app_version = re.findall(r'appVersion":"(.+?)"', \
                                        item_chart_metadata)                
                # print (''.join(map(str, item_chart_name)), \
                # ''.join(map(str, item_chart_version)), \
                # ''.join(map(str, item_chart_app_version)))
                data.append([item_chart_name, item_chart_version, item_chart_app_version])

            temp_item = item_chart_name[0][0]
        data.sort()
        return data

    def get_charts_list(namespace):
        temp_item = ''
        installed_charts = Charts.get_installed_charts(namespace)
        _logger.info("adding all helm repos")
        
        for item in installed_charts:
            item_chart_name = item[0][0]
            item_chart_version_installed = item[1][0]
            os.system("./helm-repo.sh  >/dev/null 2>&1")

            if not item[0][0] == temp_item:
                item_chart_latest_version, chart_type = '', ''
                _logger.info("checking {} helm chart for latest version"\
                .format(item_chart_name))
                latest_version_json = check_output("helm search repo {} \
                -o json".format(item_chart_name), shell=True).decode('ascii')    
                latest_version = re.findall(r'version":"(.+?)","app_version', \
                latest_version_json)
                if latest_version:
                    item_chart_latest_version = latest_version[0]
                    chart_type = 'external'

                    if StrictVersion(item_chart_version_installed) >= StrictVersion(item_chart_latest_version):
                        chart_version_status = 'latest'
                    else:
                        chart_version_status = 'outdated'
                else:
                    item_chart_latest_version = item_chart_version_installed
                    chart_type = 'internal'
                    chart_version_status = 'latest'

                _logger.info(json.dumps({
                    "chart": item_chart_name,
                    "chart_type": chart_type,
                    "chart_installed_version": item_chart_version_installed,
                    "chart_latest_version": item_chart_latest_version,
                    "chart_version_status": chart_version_status
                    }))

            temp_item = item[0][0]

def call_all(namespace):  
    Charts.get_charts_list(namespace)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:", ["help", "namespace"])
        if not opts:        
            call_all("")
            k8s.Output.time_taken(start_time)
            sys.exit()
            
    except getopt.GetoptError as err:
        print(err)
        return
    verbose, ns = '', ''
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-n", "--namespace"):
            namespace = a          
        else:
            assert False, "unhandled option"
    call_all(namespace)
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