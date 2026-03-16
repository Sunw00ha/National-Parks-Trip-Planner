# /parkboundaries
# Names: Irene Ha, Ejean Kuo, Henron Ruan

import json
import math
import requests
import os

def calculate_area(coordinates):
    RADIUS = 6371.0 # radius of earth in km
    area = 0.0
    n = len(coordinates)

    for i in range(n):
        lon1, lat1 = coordinates[i]
        lon2, lat2 = coordinates[(i+1)%n]

        x1 = math.radians(lon1) * math.cos(math.radians(lat1)) * RADIUS
        y1 = math.radians(lat1) * RADIUS
        x2 = math.radians(lon2) * math.cos(math.radians(lat2)) * RADIUS
        y2 = math.radians(lat2) * RADIUS

        area += (x1*y2) - (x2*y1)
    
    return abs(area) / 2.0

def lambda_handler(event, context):
   # call NPS park boundaries endpoint
    try:
        print("**Call to NPS park boundaries")
        parameters = event["pathParameters"]
        if "sitecode" not in parameters:
            raise Exception("request has no key 'sitecode'")
        
        sitecode = parameters["sitecode"].lower()
        
        api_key = os.environ.get("API_KEY")
        nps_url = f"https://developer.nps.gov/api/v1/mapdata/parkboundaries/{sitecode}?api_key={api_key}"
        
        # make GET request to NPS
        response = requests.get(nps_url)
        nps_body = response.json()
        #print("**NPS data:")
        #print(nps_body)

        # extract geometric coordinates as a nested list
        features = nps_body["features"]
        if not features:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": f"park '{sitecode}' not found"
                })
            }

        poly_coords = features[0]["geometry"]["coordinates"]
        total_park_area = 0
        print(poly_coords[0])

        for polygon in poly_coords:
            # calculate exterior ring area
            exterior_area = calculate_area(polygon[0])

            # subtract inner rings (holes, eg. lakes)
            hole_area_sum = 0
            for hole in polygon[1:]:
                hole_area_sum += calculate_area(hole)

            total_park_area += (exterior_area - hole_area_sum)

        body = {
            "parkname": features[0]["properties"]["name"],
            "sitecode": sitecode,
            "parkareakm": f"{round(total_park_area,4)} km^2",
            "parkareaacres": f"{round(total_park_area*247.105,4)} acres"
        }

        return {
            "statusCode": 200,
            "body": json.dumps(body)
        }


    except Exception as e:
        print("**Exception:")
        print(str(e))
        body = {
            "message": str(e),
            "parkname": "N/A",
            "sitecode": "N/A",
            "parkareakm": -1000,
            "parkareaacres": -1000
        }
        return {
            "statusCode": 500,
            "body": json.dumps(body)
        }
        
        
