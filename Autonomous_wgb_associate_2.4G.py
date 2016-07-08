
########################################################################################################################
## Script Header
# Script Name :
#     Autonomous_basic_scenario
# Description :
#    This script verify Autonomous AP basic scenario
#    1)wireless client associate, get IP, traffic okay
#    2)WGB associate, get IP (BVI) traffic okay
#    3)wired client behind WGB get IP, traffic okay
# Author :
#     jiawqu
# Mandatory Arguments :
#     --testbed                  Default Argument for Testbed
#     --log_level                Default Argument for Script Log Level at Runtime
#     --virtual                  Virtual run(without actual devices)
#     --AP_1_1_1                 Device Handle
#     --WGB_1
#
# Optional Arguments :
#     --radio                    802.11a/802.11b
# Sample Usage :
#     python Autonomous_wgb_associate.py  --testbed "<yaml_file>" --log_level 1 --virtual no  --AP_1_1_1 AP_1_1_1 --WGB_1 WGB_1
#     easypy Autonomous_wgb_scenario.py  --testbed "<yaml_file>" --log_level 1 --virtual no  --AP_1_1_1 AP_1_1_1 --WGB_1 WGB_1
#     (Note : easypy will upload logs to TRADe)
## End Header
########################################################################################################################
## Get packages required for the script
from pyNG.lib.core.wireless import *
import time
########################################################################################################################
## Validate script arguments and initialize
parser = argparse.ArgumentParser(description = "standalone parser")


# Mandatory Arguments
mandatory_args = parser.add_argument_group('mandatory arguments')
mandatory_args.add_argument('--testbed', dest = 'testbed', required = True, type = str)
mandatory_args.add_argument('--log_level', dest = 'log_level', required = True, type = str)
parser.add_argument('--virtual', dest = 'virtual', type = str, choices = ['yes','no'], default = 'no')
mandatory_args.add_argument('--AP_1_1_1', dest = 'AP_1_1_1', required = True, type = str)
mandatory_args.add_argument('--WGB_1', dest = 'WGB_1', required = True, type = str)


# parse args
args, unknown = parser.parse_known_args()

# post-parsing processing
testbed = testbed_loader(args.testbed)
print(testbed.data[args.AP_1_1_1])
log_level = args.log_level
virtual = args.virtual
AP_1_1_1 = device_loader(testbed.data[args.AP_1_1_1], virtual)
WGB_1 = device_loader(testbed.data[args.WGB_1], virtual)
ssid1='test_jiawen'
########################################################################################################################

class ScriptCommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_devices (self):
        logger.info("Connecting Devices")
        AP_1_1_1.connect()
        WGB_1.connect()
    @aetest.subsection
    def configure_base_state (self):
        logger.info("Configuring Base State for Script")

class testcase_Basic_scenario(aetest.Testcase):
    @aetest.setup
    def setup (self):
        logger.info("Testcase Setup")
    
    @aetest.test
    def testcase_autonomous_basic_scenario (self):
        logger.info("Testcase Section")
        # test 2.4G 
        call('create_ap_personnel_ssid', AP=AP_1_1_1, pers_ssid=ssid1,radio=0, mode='config')
        call('config_wgb_open_association', WGB=WGB_1, ssid=ssid1, radio=0, mode='config', parent="", is_v_int=True)
        call('ap_check_wgb_association', AP=AP_1_1_1, client_mac_address=WGB_1.data['mac_addr'])
        ipaddr=call('get_ap_ip', WGB=WGB_1, ap_mac_address=AP_1_1_1.data['radio-b']['mac_addr'])
        WGB_1.exec_cli("clear bridge")
        call('wgb_ping', WGB=WGB_1, ip_address=ipaddr, count=10, iterations=1, option='ipv4')
        call('wgb_check_traceback', WGB=WGB_1)
        call('ap_check_traceback', AP=AP_1_1_1)
        ipaddr1=call('get_wgb_ip', AP=AP_1_1_1, client_mac_address=WGB_1.data['mac_addr'])
        AP_1_1_1.exec_cli("clear bridge")
        call('ap_ping_test', AP=AP_1_1_1, ip_address=ipaddr1, count=10, iterations=1, option='ipv4')
        
    @aetest.cleanup
    def cleanup (self):
        logger.info("Testcase Cleanup")
        call('create_ap_personnel_ssid', AP=AP_1_1_1, pers_ssid=ssid1,radio=0, mode='unconfig')
        call('config_wgb_open_association', WGB=WGB_1, ssid=ssid1, radio=0,mode='unconfig', parent="", is_v_int=True)

class ScriptCommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def remove_testbed_configurations (self):
        logger.info("Removing configurations")
    @aetest.subsection
    def disconnect_devices (self):
        logger.info("Disconnecting Devices")
        WGB_1.disconnect()
########################################################################################################################
## main()
def main():
    run(testscript='Autonomous_wgb_scenario.py')

if __name__ == '__main__':
    # set default logger level
    logger.setLevel(logging.INFO)
    # and pass all arguments to aetest.main() as kwargs
    aetest.main(testbed = testbed, log_level = log_level, virtual = virtual, AP_1_1_1 = AP_1_1_1, WGB_1=WGB_1)
########################################################################################################################
## Commit History
# 2015-11-21 19:16:31 - sapardes - Script Created for LogicalId : config_ap_global_power
########################################################################################################################
