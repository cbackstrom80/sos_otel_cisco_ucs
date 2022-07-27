import yaml
import json
import logging
import sys
import signalfx
class UCSTOSPLUNKO11Y:
    with open("ucs_api_config.yaml", 'r') as stream:
        try:
            config=yaml.safe_load(stream)
            #print(config['storeinfo'])
        except yaml.YAMLError as exc:
            print(exc)

    #DEFINE VARS
    REALM = config['CISCO-UCS_METRICS']['app']['options']['realm']
    METRICBASENAME = config['CISCO-UCS_METRICS']['app']['options']['metric-base-name']
    TOKEN = config['CISCO-UCS_METRICS']['app']['options']['token']
    OTELCOLLECTORINGEST = config['CISCO-UCS_METRICS']['app']['options']['otelcollectoringest']
    UCS_CLUSTER_ADDRESS = config['CISCO-UCS_METRICS']['ucs']['cluster_address']
    UCS_CLUSTER_USERNAME = config['CISCO-UCS_METRICS']['ucs']['username']
    UCS_CLUSTER_PASSWORD = config['CISCO-UCS_METRICS']['ucs']['password']




    from ucsmsdk.ucshandle import UcsHandle

    # Create a connection handle
    handle = UcsHandle(UCS_CLUSTER_ADDRESS, UCS_CLUSTER_USERNAME, UCS_CLUSTER_PASSWORD)




    def get_attrib_from_yaml(object, string):
        return getattr(object,string)


    def post_results_to_collector(metricdict,dimdict):
        client = signalfx.SignalFx(ingest_endpoint=UCSTOSPLUNKO11Y.OTELCOLLECTORINGEST)
        ingest = client.ingest(UCSTOSPLUNKO11Y.TOKEN)
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        for metricname, metricvalue in metricdict.items():
            if metricvalue == 'unassociated' or 'off':
                metricvalue = 0
            if metricvalue == 'license-ok':
                metricvalue = 1





            payload = ingest.send(gauges=[{
                                'metric': UCSTOSPLUNKO11Y.METRICBASENAME + '.' + "{}".format(metricname),
                                'value': metricvalue,
                                'dimensions': dimdict
                                }])


        return (True)






    def get_blade_metrics():




        # Login to the server
        UCSTOSPLUNKO11Y.handle.login()
        blades = UCSTOSPLUNKO11Y.handle.query_classid("computeBlade")
        # Parse Blade section of config Yaml
        blade_metrics_to_collect = UCSTOSPLUNKO11Y.config['CISCO-UCS_METRICS']['app']['options']['blade_metrics_to_collect']
        blade_dims_to_collect = UCSTOSPLUNKO11Y.config['CISCO-UCS_METRICS']['app']['options']['blade_dims_to_collect']
        for blade in blades:
            # Build SIGNALFX JSON Object
            sfx_blade_json_metrics = {}
            sfx_blade_json_dimensions = {}
            #print(sfx_blade_json_metrics)
            for key, value in blade_metrics_to_collect.items():
                #print('{} = {}'.format(key, value))
                if value == True:

                    #print(get_attrib_from_yaml(blade, key))
                    sfx_blade_json_metrics[key] = UCSTOSPLUNKO11Y.get_attrib_from_yaml(blade, key)
                    #print(sfx_blade_json_metrics)
                else:
                    print('This is False')
                for key, value in blade_dims_to_collect.items():
                    if value == True:
                        #print(key)
                        sfx_blade_json_dimensions[key] = UCSTOSPLUNKO11Y.get_attrib_from_yaml(blade, key)
                print(sfx_blade_json_metrics)



            UCSTOSPLUNKO11Y.post_results_to_collector(sfx_blade_json_metrics,sfx_blade_json_dimensions)


        #return post_results_to_collector(sfx_blade_json_metrics,sfx_blade_json_dimensions)




    # Logout from the server
    handle.logout()




    def get_fex_metrics():





        # Login to the server
        UCSTOSPLUNKO11Y.handle.login()
        fexs = UCSTOSPLUNKO11Y.handle.query_classid("equipmentFex")
        fex_metrics_to_collect = UCSTOSPLUNKO11Y.config['CISCO-UCS_METRICS']['app']['options']['fex_metrics_to_collect']
        fex_dims_to_collect = UCSTOSPLUNKO11Y.config['CISCO-UCS_METRICS']['app']['options']['fex_dims_to_collect']
        for fex in fexs:
            # Build SIGNALFX JSON Object
            sfx_fex_json_metrics = {}
            sfx_fex_json_dimensions = {}
            for key, value in fex_metrics_to_collect.items():
                #print('{} = {}'.format(key, value))
                if value == True:

                    #print(get_attrib_from_yaml(blade, key))
                    sfx_fex_json_metrics[key] = UCSTOSPLUNKO11Y.get_attrib_from_yaml(fex, key)
                    #print(sfx_blade_json_metrics)
                else:
                    print('This is False')
                for key, value in fex_dims_to_collect.items():
                    if value == True:
                        #print(key)
                        sfx_fex_json_dimensions[key] = UCSTOSPLUNKO11Y.get_attrib_from_yaml(fex, key)
                print(sfx_fex_json_metrics)
            UCSTOSPLUNKO11Y.post_results_to_collector(sfx_fex_json_metrics, sfx_fex_json_dimensions)


UCSTOSPLUNKO11Y.get_fex_metrics()








