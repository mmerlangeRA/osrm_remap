import csv
import json
import logging
import os
import numpy as np
import requests

# Define the OSRM API endpoint
OSRM_API_URL = "http://127.0.0.1:5000/match/v1/driving"

# Convert GPS coordinates to the required format for OSRM API
def format_coordinates(coordinates):
    """
    Converts a numpy array of coordinates to a list of formatted strings
    for the OSRM API.
    """
    return [f"{lon},{lat}" for _, lat, lon in coordinates]  # Extract lat, lon from array

# Send GPS coordinates to OSRM API
def send_to_osrm_api(coordinates, timestamps):
    """
    Sends GPS coordinates and timestamps to the OSRM /match API.
    """
    # OSRM expects "lon,lat" format for coordinates
    formatted_coords = ";".join([f"{lon},{lat}" for lat, lon in coordinates])
    timestamps_in_seconds = [int(ts // 1000) for ts in timestamps]
    # OSRM expects a semicolon-separated list of timestamps
    formatted_timestamps = ";".join(map(str, timestamps_in_seconds))
    print("Formatted Coordinates:", formatted_coords)
    print("Formatted Timestamps:", formatted_timestamps)


    # Parameters for the API request
    params = {
        "steps": "true",         # Include navigation steps
        "geometries": "geojson", # Return GeoJSON formatted geometry
        "timestamps": formatted_timestamps  # Add timestamps
    }
    query_string = f"{OSRM_API_URL}/{formatted_coords}?timestamps={formatted_timestamps}"
    print("Query string length:", len(query_string))
    # Send the request
    response = requests.get(f"{OSRM_API_URL}/{formatted_coords}", params=params)

    # Check for successful response
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def read_meta_from_file(file_path: str) -> dict:
    """
    Reads metadata from a file and stores it as a dictionary.
    """
    try:
        with open(file_path, "r") as file:
            metadata = {}
            for line in file:
                if ":" in line:  # Parse key-value metadata
                    key, value = line.strip().split(":", 1)
                    metadata[key.strip()] = value.strip()

        return metadata
    except Exception as e:
        logging.error(f"Error reading metadata: {e}")
        return None


    
# Read GPS coordinates from CSV
def read_trajectory_from_file(file_path):
    """
    Reads the trajectory CSV file and returns coordinates and timestamps.
    """
    import csv
    coordinates = []
    timestamps = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            timestamp = int(row['datetime'])
            coordinates.append((lat, lon))
            timestamps.append(timestamp)

    return coordinates, timestamps

# Save matched results to a new file
def save_matched_results(data, output_file):
    with open(output_file, mode='w') as file:
        json.dump(data, file, indent=4)

# Main function
if __name__ == "__main__":
    input_csv = "trajectory.csv"            # Path to your input CSV
    output_file = "matched_results.json"    # Path to save the matched results

    # Read GPS data and timestamps
    coordinates, timestamps = read_trajectory_from_file(input_csv)
    # Ensure the lengths of coordinates and timestamps match
    if len(coordinates) != len(timestamps):
        raise ValueError(f"Mismatch between coordinates ({len(coordinates)}) and timestamps ({len(timestamps)})")

    print("Read GPS coordinates and timestamps:", coordinates, timestamps)

    # Limit to avoid URL length restrictions
    MAX_COORDINATES_PER_REQUEST = 50
    chunks = [
        (coordinates[i:i + MAX_COORDINATES_PER_REQUEST],
         timestamps[i:i + MAX_COORDINATES_PER_REQUEST])
        for i in range(0, len(coordinates), MAX_COORDINATES_PER_REQUEST)
    ]

    matched_results = []

    # Process each chunk
    for coords_chunk, timestamps_chunk in chunks:
        result = send_to_osrm_api(coords_chunk, timestamps_chunk)
        if result:
            matched_results.append(result)

    # Save results
    save_matched_results(matched_results, output_file)

    print("Matched results saved to", output_file)

