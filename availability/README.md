# Starlink Availability Cells

This directory contains Starlink availability cells information generated using the public [Geobuf](https://github.com/mapbox/geobuf) file `https://api.starlink.com/public-files/availability-cells.pb` and converted to GeoJSON format.

GitHub WebUI provides a visualization preview of each GeoJSON file. You can also use [geojson.io](https://geojson.io/) to visualize the GeoJSON files and load the RAW URL of each GeoJSON file.

As of January 2025, there are several categories of availability cells:

```
faq
test
blacklisted
waitlisted Expanding in 2025
waitlisted Sold Out
waitlisted Service date is unknown at this time
```

The `.csv` files contains the locations of the centroid of each clustered cell region. The centroid is calculated with the `shapely.geometry` library and might not accurately reflect the shape of clustered cells when the shape is highly irregular. The `.csv` files are only meant to provide a rough estimation and help to locate small cells in the visualized GeoJSON files.

The geolocation results of the coordinates is based on the [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding).
