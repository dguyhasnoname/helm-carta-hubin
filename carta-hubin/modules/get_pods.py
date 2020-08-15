from kubernetes import client, config
from kubernetes.client.rest import ApiException

try:
    config.load_kube_config()
except:
    config.load_incluster_config()

core = client.CoreV1Api()

class K8sPods:    
    def get_pods(ns):
        try:
            if ns == 'all':
                print ("\n[INFO] Fetching all namespace pods data...")         
                pods = core.list_pod_for_all_namespaces(timeout_seconds=10)
            else:
                print ("\n[INFO] Fetching {} namespace pods data...".format(ns))  
                namespace = ns
                pods = core.list_namespaced_pod(namespace, timeout_seconds=10)
            return pods
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)