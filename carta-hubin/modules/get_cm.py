from kubernetes import client, config
from kubernetes.client.rest import ApiException
from . import logging as logger

try:
    config.load_kube_config()
except:
    config.load_incluster_config()

core = client.CoreV1Api()

class K8sConfigMap:
    global _logger
    _logger = logger.get_logger('K8sSecrets')
    def get_cm(ns):
        try:
            if ns != 'all':
                _logger.info("Fetching {} namespace configMaps data...".format(ns))
                namespace = ns
                configmaps = core.list_namespaced_config_map(namespace, timeout_seconds=10)
            else:
                _logger.info("Fetching all namespace configMaps data...")
                configmaps = core.list_config_map_for_all_namespaces(timeout_seconds=10)
            return configmaps
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_config_map: %s\n" % e)