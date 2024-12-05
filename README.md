# remap

## pull image

docker pull ghcr.io/project-osrm/osrm-backend:v5.27.1

## Get pbf data from Geofabrik

<https://download.geofabrik.de/europe/france.html>

# Extract data from the OSM file

docker run -t -v $(pwd):/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-extract -p /opt/car.lua /data/pays-de-la-loire-latest.osm.pbf

# Partition and prepare the data for routing

docker run -t -v $(pwd):/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-partition /osrm-data/pays-de-la-loire-latest.osm.osrm
docker run -t -v $(pwd):/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-customize /osrm-data/pays-de-la-loire-latest.osm.osrm
docker run -t -i -p 5000:5000 -v $(pwd):/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-routed --algorithm mld /data/pays-de-la-loire-latest.osrm

# adapt to my windows

# Extract data from the OSM file

docker run -t -v %cd%/osrm-data:/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-extract -p /opt/car.lua /data/pays-de-la-loire-latest.osm.pbf

# Partition and prepare the data for routing

docker run -t -v %cd%/osrm-data:/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-partition /data/pays-de-la-loire-latest.osrm

docker run -t -v %cd%/osrm-data:/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-customize /data/pays-de-la-loire-latest.osrm

docker run -t -i -p 5000:5000 -v %cd%/osrm-data:/data ghcr.io/project-osrm/osrm-backend:v5.27.1 osrm-routed --algorithm mld /data/pays-de-la-loire-latest.osrm
