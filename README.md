# Starlink GeoIP Dataset

## Data

This repository contains three components:

### [GeoIP Feed](./feed/)

Raw snapshots of Starlink's GeoIP feed: https://geoip.starlinkisp.net/feed.csv

### [DNS PTR Records](./geoip/)

Corresponding DNS PTR records for the raw GeoIP feed, which reflects the associated PoP location for a given subnet.

We only started checking DNS PTR records automatically and generate this report by GitHub Actions after `2024-08-05`.

**Note that**: It is only meaningful to check the corresponding DNS PTR records for the GeoIP feed at the time of the original data collections. The DNS PTR records for a given subnet may change over time.

### [Raw Data for Starlink Latency Map](./latency/)

Snapshots of raw JSON metrics for https://www.starlink.com/map?view=latency, which contains monthly snapshots of global latency and download/upload speed released by Starlink.

## Update Frequency

The GeoIP feed is checked every 1 hour by a GitHub Actions Workflow. If any new updates in the GeoIP feed are detected, the feed is downloaded and the corresponding DNS PTR records are checked by `nslookup` and the `geoip-{date}.json` file is generated.

## Note

The GeoIP feed only represents the planned naming and addressing of Starlink ISP. It does not reflect the actual deployment status of Starlink ground stations or the availability of Starlink service in a given region.
