import requests
import time
import yaml
import json
import csv
import pandas as pd
import numpy as np
csvFile=pd.read_csv("AllCompute.csv")
#s1=csvFile.max(axis=0)
l=[]
with open('pricing.yml') as file:
    try:
        databaseConfig = yaml.safe_load(file)   
        #print((databaseConfig))
    except yaml.YAMLError as exc:
        print(type(exc))

for index, row in csvFile[0:].iterrows():
    try:
        if(row['STATUS']=="RUNNING"):
            machine_type=row['MACHINE_TYPE']
            running_hours=(row['Running_hours'])
            disk=(row['DISK'])
    # print(machine_type,running_hours,disk)
            disk=int(''.join(filter(str.isdigit,disk)))
            cost_per_hour=databaseConfig['compute']['instance'][machine_type]['cost']['asia-south1']['hour']
            total_cost=((cost_per_hour*running_hours)+(disk*0.12))*(82.74)
            l.append(total_cost);
            print(total_cost);

        else:
            disk=(row['DISK'])
            disk=int(''.join(filter(str.isdigit,disk)))
            total_cost=(disk*0.12)*(82.74)
            print(total_cost);
            l.append(total_cost)
        

            
    except:
        disk=(row['DISK'])
        disk=int(''.join(filter(str.isdigit,disk)))
        machine_type=row['MACHINE_TYPE']
        machine_type_actual=machine_type[:2]
        if(machine_type_actual=="cu"):
            machine_type_actual="n2"
        running_hours=(row['Running_hours'])
        cpu=row['CPU']
        memory=(row['MEMORY'])
        arr_mem=memory.split(".")
        memory=(arr_mem[0])
        print(memory,machine_type_actual,cpu,disk)
        
        url="https://cloudbilling.googleapis.com/v1beta:estimateCostScenario?key=AIzaSyAWSh9ThHqGHvUrcP5Kh4kxYCVEVMI7pX8"
        running_hours=str(running_hours*60*60)+"s";
        data={
            "costScenario": {
            "scenarioConfig": {
            "estimateDuration": running_hours
            },
            "workloads": [
            {
            "name": "vm-example",
"computeVmWorkload": {
"instancesRunning": {
"usageRateTimeline": {
"usageRateTimelineEntries": [
{
"usageRate": 1
}
]
}
},
"machineType": {
"customMachineType":{
"machineSeries": machine_type_actual,
"virtualCpuCount": str(cpu),
"memorySizeGb": str(memory)
}
},

"persistentDisks":[
{
"diskType": "pd-balanced",
"scope":"SCOPE_ZONAL",
"diskSize":{
"usageRateTimeline": {
"unit": "GBy",
"usageRateTimelineEntries": [
{
"usageRate": disk
}
]
}
}
}
],

"region": "asia-south1"
}
}
]
}
}
        response=requests.post(url,json=data)
        response_val=(response.json())
        time.sleep(0.02)
        curr=(response_val['costEstimationResult']['segmentCostEstimates'][0]['workloadCostEstimates'][0]['workloadTotalCostEstimate']['netCostEstimate']['units'])
        paisa=(response_val['costEstimationResult']['segmentCostEstimates'][0]['workloadCostEstimates'][0]['workloadTotalCostEstimate']['netCostEstimate']['nanos'])
        curr=(float(curr))*(82.73)
        paisa1=paisa/1000000000
        total_value=(curr+paisa1)
        l.append(total_value)       
csvFile['total']=l        
csvFile.to_csv('AllCompute5.csv',index = False)





