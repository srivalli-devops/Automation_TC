import subprocess,re
from time import sleep


def __getPrefixCommand():
    return "adb "
    
def executeCommandOnDevice(command):
    try:
        output = None
        commandToExecute = __getPrefixCommand()
        commandToExecute += command
        output = subprocess.check_output(commandToExecute, shell=True)
        if output is not None:
            outputStr = output.decode('utf-8')
            return outputStr
    except Exception as e:
        print("Error: {}".format(e.__str__()))
        return None
        
def getDeviceProperty(property,deviceId):
    '''
    It will give the property of the device
    :param property:
    :return:
    '''
    try:
        cmd = "-s {} shell getprop".format(deviceId)
        output = executeCommandOnDevice(cmd)
        if output is not None:
            lines = output.splitlines()
            for line in lines:
                if property in line:
                    (key,value) = line.split(':')
                    patternObj = re.search(r'\[(.*)\]',value)
                    if patternObj:
                        return patternObj.group(1)
        else:
            print("property is not found in getprop list")
            return None
    except Exception as e:
        print("Error:Unable to get the device property")
        print(e.__str__())

def getDeviceBrand(deviceId):
    '''
    It will return the brand of the device(Ex: Samsung,onePlus..etc)
    :return:
    '''
    brand = getDeviceProperty('ro.product.brand',deviceId)
    return brand

def getDeviceModel(deviceId):
    '''
    It will return the model of the device
    :return:
    '''
    model = getDeviceProperty('ro.product.model',deviceId)
    return  model
    
def getDeviceID():
    '''
    Get the connected device id to the host
    :return: device id
    '''
    deviceIds = []
    try:
        cmd = "devices"
        output = executeCommandOnDevice(cmd)
        if output is not None:
            for line in output.splitlines():
                reObj = re.search(r'(\w+).*device\b', line)
                if reObj:
                    deviceId = reObj.group(1).strip()
                    deviceIds.append(deviceId)
    except Exception as e:
        print("Error: unable to get the device id")
        print(e.__str__())
    return deviceIds

def rootAndRemount():
    '''
    Provide the root and remount permissions to the connected device
    :return: None
    '''
    root()
    sleep(2)
    remount()

def root():
    '''
    Provide the root permissions to connected device
    :return: None
    '''
    cmd = "root"
    executeCommandOnDevice(cmd)

def remount():
    '''
    Provide the remount permissions to connected device
    :return: None
    '''
    cmd = "remount"
    executeCommandOnDevice(cmd)
    
if __name__ == "__main__":
 deviceInfo = {}
 deviceIds = getDeviceID()
 if len(deviceIds) >= 1:     
    for deviceId in deviceIds:
        deviceInfo[deviceId] = []
        deviceBrand = getDeviceBrand(deviceId)
        deviceModel = getDeviceModel(deviceId)
        print("DeviceID:{}".format(deviceId))
        print("Device Brand:{}".format(deviceBrand))
        print("Device Model:{}".format(deviceModel))        
        deviceInfo[deviceId].append(deviceBrand)
        deviceInfo[deviceId].append(deviceModel)
        print(deviceInfo)
 else:
    print("unable to get the device id.Check the usb connection");        
 
