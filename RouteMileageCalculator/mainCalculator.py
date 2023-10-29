import math
import gpxpy
import numpy as np
import haversine as hs
import csv

def toFeet(num) -> float:
    return num * 3.280839895

def haversine_distance(lat1,lon1,lat2,lon2) -> float:
    distance = hs.haversine(point1=(lat1, lon1),point2=(lat2,lon1),unit=hs.Unit.METERS
    )
    return np.round(distance, 2)

def openGPX(file) -> list:
    listo = []
    with open(file,'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for route in gpx.routes:
            for point in route.points:
                listo.append({
                    'latitude' : point.latitude,
                    'longitude' : point.longitude,
                    'elevation' : point.elevation
            })
    return listo

def routeCalc(list1) -> list:
    distances = []
    for x in range(len(list1) - 1):
        distances.append(toFeet(haversine_distance(
        list1[x]['latitude'],
        list1[x]['longitude'],
        list1[x + 1]['latitude'],
        list1[x + 1]['longitude']
        )))
    
    elevation_diffs = []
    for x in range(len(list1) - 1):
        diff = list1[x + 1]['elevation'] - list1[x]['elevation']
        elevation_diffs.append(toFeet(diff))
    
    route_prime = []
    unusable_index = []
    for x in range(len(distances)):
        route_prime.append({
            'distance' : distances[x],
            'elevation_diff' : elevation_diffs[x],
            'gradient' : elevation_diffs[x]/distances[x] * 100
        })
        if route_prime[x]['distance'] == 0:
            unusable_index.append(x)

    length = len(unusable_index)
    while length != 0:
        route_prime.pop(unusable_index[0])
        unusable_index.pop(0)
        length -= 1
        for y in range(length):
            unusable_index[y] -= 1

    return route_prime 

def extractSimData(file):
    with open(file,'r') as txtfile:
        csvOb = csv.reader(txtfile)
        returnDict = {}
        speed_key = []
        consumption_key = []
        gradients = []
        for row in csvOb:
            speed_key.append({
                'gradient' : float(row[0]),
                'speed' : float(row[2])
            })
            if float(row[4]) < 0:
                row[4] = 0
            consumption_key.append({
                'gradient' : float(row[0]),
                'consumption' : float(row[4])
            })
            gradients.append(float(row[0]))
        returnDict['speedList'] = speed_key
        returnDict['consumptionList'] = consumption_key
        returnDict['gradientList'] = gradients
        return returnDict
    
def roundGradients(list1) -> list:
    returnList = []
    for value in list1:
        lowDiff = abs(value - math.floor(value))
        midDiff = abs(value - (math.floor(value) + 0.5))
        highDiff = abs(value - math.ceil(value))
        if lowDiff < midDiff and lowDiff < highDiff:
            returnList.append(math.floor(value))
        elif midDiff < lowDiff and midDiff < highDiff:
            returnList.append(math.floor(value) + 0.5)
        else:
            returnList.append(math.ceil(value))
    return returnList

def extractValuesFromListOfDictionaries(list,key) -> list:
    returnList = []
    for x in list:
       returnList.append(x[key]) 
    return returnList

def assignValuesFromListMirroringListOfDictionaries(mirror,data,list1,key) -> list:
    returnList = []
    for x in list1:
        index = mirror.index(x)
        returnList.append(data[index][key])
    return returnList

def listValuesMiToFt(list1,num):
    if num == 0:
        for i in range(len(list1)):
            list1[i] = list1[i] / 5280
    elif num == 1:
        for i in range(len(list1)):
            list1[i] = list1[i] * 5280


route_prime = routeCalc(openGPX('route.gpx'))
key = extractSimData('wattage.txt')
consumptionBetweenPoints = []
roundedGradients = roundGradients(key['gradientList'])
givenGradients = extractValuesFromListOfDictionaries(route_prime,'gradient')
assignedGradients = roundGradients(givenGradients)

for i in range(len(assignedGradients)):
    if assignedGradients[i] > 30:
        assignedGradients[i] = 30
    elif assignedGradients[i] < -30:
        assignedGradients[i] = -30

assignedConsumption = assignValuesFromListMirroringListOfDictionaries(roundedGradients,key['consumptionList'],assignedGradients,'consumption')
listValuesMiToFt(assignedConsumption,0)
totalConsumption = 0.0

for i in range(len(assignedConsumption)):
    totalConsumption += assignedConsumption[i] * route_prime[i]['distance']

print("\n--------------------------------------------------------------------------------------\n")
print(f'The total consumption of energy by the bike is {totalConsumption:.3f} Watt Hours')
assignedSpeed = assignValuesFromListMirroringListOfDictionaries(roundedGradients,key['speedList'],assignedGradients,'speed')
listValuesMiToFt(assignedSpeed,1)
totalTime = 0.0

for i in range(len(assignedSpeed)):
    totalTime += route_prime[i]['distance'] / assignedSpeed[i]

print(f'The total time it would take to cycle nonstop to the destination is {int(totalTime)} Hours and {totalTime % 1 * 60:.0f} Minutes')
batteryVoltage = float(input("What is the voltage of the battery? "))
batteryAmperage = float(input("What is the Amp Hours of the battery? "))
batteryWattHours = batteryVoltage * batteryAmperage
print(f'The total capacity of the battery is {batteryWattHours:.3f} Watt Hours')
print(f'The bike will go through {totalConsumption/batteryWattHours:.2f} charges to get to the destination')

if (totalConsumption < batteryWattHours):
    print("The bike will make the journey on one charge")
else:
    print("The bike will not make the journey on one charge")
    