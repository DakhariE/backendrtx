'''================================================================================================================================================
This code is written to get the car details from Carnet.ai using the API. The code is written in Python. The code uses the requests library 
to make a POST request to the Carnet.ai API. The code takes the image path as input and returns the car details as output. 
The code also formats the response from the API to a more readable format. The code is well-documented and easy to understand. 
The code can be used to get car details from Carnet.ai using the API.
====================================================================================================================================================
Author: USF senior project team 2024 - (RTX). 
Assistance: OpenAI. (2024). ChatGPT (4) [Large language model]. https://chat.openai.com. 
Date: 02/13/2024.
====================================================================================================================================================
'''
from .keys import *
import requests
# ==================================================URLs for the requests========================================================================================================================
urls = [
    "https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=all&features=color&region=NA",
    "https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&region=DEF",
    "https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&features=angle&region=DEF"
]
#==========================This function Get the car detals from Carnet.ai useing the API=====================================
def get_car_details(image_path, urls=urls):
    api_key = carnet_apikey  
    headers = {
        'accept': 'application/json',
        'api-key': api_key,
        'Content-Type': 'application/octet-stream'
    }
    combined_response = {'detections': [], 'is_success': True, 'meta': {}}
    
    for url in urls:
        with open(image_path, 'rb') as image_file:
            response = requests.post(url, headers=headers, data=image_file)
            print(response)
        if response.status_code == 200:
            response_json = response.json()
            combined_response['detections'].extend(response_json.get('detections', []))
            combined_response['meta'] = response_json.get('meta', {})  # Assumes last meta is fine
        else:
            combined_response['is_success'] = False
            combined_response['error'] = 'Failed to fetch data'
            combined_response['status_code'] = response.status_code
            break  # Exit if any request fails
    print(combined_response)
    return combined_response

'''==========This code formats the response from the API to a more readable format================================================================================='''
def format_response(response_json):
    response_dict = {}
    if response_json['detections'] == []:
        response_dict['Success'] = False
    else:
        response_dict['Success'] = True
        # Initialize containers for the highest probability results
        max_mmg = None
        max_color = None
        max_angle = None

        # Process each detection to find the max probability items
        for detection in response_json.get('detections', []):
            current_mmg = max(detection.get('mmg', []), key=lambda x: x.get('probability', 0), default=None)
            current_color = max(detection.get('color', []), key=lambda x: x.get('probability', 0), default=None)
            current_angle = max(detection.get('angle', []), key=lambda x: x.get('probability', 0), default=None)

            # Update the max probability items if the current ones are higher
            max_mmg = current_mmg if not max_mmg or (current_mmg and current_mmg.get('probability', 0) > max_mmg.get('probability', 0)) else max_mmg
            max_color = current_color if not max_color or (current_color and current_color.get('probability', 0) > max_color.get('probability', 0)) else max_color
            max_angle = current_angle if not max_angle or (current_angle and current_angle.get('probability', 0) > max_angle.get('probability', 0)) else max_angle

        # Add the highest probability results to the formatted response
        response_dict['Make'] = max_mmg['make_name']
        response_dict['Model'] = max_mmg['model_name']
        response_dict['MM_prob'] = max_mmg['probability']
        response_dict['Color'] = max_color['name']
        response_dict['C_prob'] = max_color['probability']
        response_dict['Angle'] = max_angle['name']
        response_dict['A_prob'] = max_angle['probability']
        #response_dict['Direction']

    return response_dict
'''==========This code is the main code that calls the above functions to get the car details========================================================================================================='''

# image_path = 'madza.jpg'  # Replace with your actual image path
# response_json = get_car_details(image_path, urls)
# formatted_text = format_response(response_json)
