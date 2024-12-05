import json
import matplotlib.pyplot as plt
import folium

def read_csv_trajectory(file_path):
    """
    Reads the trajectory data from a CSV file.
    Returns a list of tuples (latitude, longitude).
    """
    import csv
    trajectory = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            lat, lon = float(row['latitude']), float(row['longitude'])
            trajectory.append((lat, lon))
    return trajectory


def read_matched_results(file_path):
    """
    Reads matched results from the JSON file and extracts the matched coordinates.
    Returns a list of tuples (latitude, longitude).
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    matched_trajectory = []
    for match in data:
        for leg in match.get('matchings', []):
            for coord in leg.get('geometry', {}).get('coordinates', []):
                # Convert GeoJSON lon,lat to lat,lon
                matched_trajectory.append((coord[1], coord[0]))
    return matched_trajectory


def plot_trajectory(original, matched):
    """
    Plots the original and matched trajectory using Matplotlib.
    """
    plt.figure(figsize=(10, 6))
    
    # Original trajectory
    original_lats, original_lons = zip(*original)
    plt.plot(original_lons, original_lats, label="Original Trajectory", marker="o", linestyle="-")

    # Matched trajectory
    matched_lats, matched_lons = zip(*matched)
    plt.plot(matched_lons, matched_lats, label="Matched Trajectory", marker="x", linestyle="--")

    # Labels and legend
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Trajectory Before and After Matching")
    plt.legend()
    plt.grid()

    # Show the plot
    #plt.show()
    plt.savefig("trajectory_plot.png")


def create_interactive_map(original, matched, output_file="trajectory_map.html"):
    """
    Creates an interactive map using Folium to visualize the original and matched trajectory.
    """
    # Center the map on the first point of the original trajectory
    map_center = original[0]

    # Create the map
    m = folium.Map(location=map_center, zoom_start=14)

    # Add original trajectory
    folium.PolyLine(original, color="blue", weight=2, opacity=0.6, tooltip="Original Trajectory").add_to(m)

    # Add matched trajectory
    folium.PolyLine(matched, color="red", weight=1, opacity=0.6, tooltip="Matched Trajectory").add_to(m)

   
    # Save the map to an HTML file
    m.save(output_file)
    print(f"Interactive map saved as {output_file}")


if __name__ == "__main__":
    print("starting")
    # Input files
    input_csv = "trajectory.csv"            # Original trajectory file
    matched_results_json = "matched_results.json"  # Matched results JSON file

    # Read data
    original_trajectory = read_csv_trajectory(input_csv)
    matched_trajectory = read_matched_results(matched_results_json)
    print("len original",len(original_trajectory))
    print("len original_trajectory",len(original_trajectory))
    # Visualize using Matplotlib
    plot_trajectory(original_trajectory, matched_trajectory)

    # Create an interactive map
    create_interactive_map(original_trajectory, matched_trajectory, "trajectory_map.html")
