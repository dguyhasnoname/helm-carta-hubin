from kubernetes import client, config
from kubernetes.client.rest import ApiException
from . import logging as logger

try:
    config.load_kube_config()
except:
    config.load_incluster_config()

core = client.CoreV1Api()

class K8sSecrets:
    global _logger
    _logger = logger.get_logger('K8sSecrets')
    def get_secrets(ns):
        try:
            if ns != 'all':
                _logger.info("\"Fetching {} namespace configMaps data\"".format(ns))
                namespace = ns
                secrets = core.list_namespaced_config_map(namespace, timeout_seconds=10)
            else:
                _logger.info("\"Fetching all namespace secrets data\"")
                secrets = core.list_secret_for_all_namespaces(label_selector='owner=helm', timeout_seconds=10)
            return secrets
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_secret_for_all_namespaces: %s\n" % e)