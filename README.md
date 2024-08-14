# Starlink GeoIP Dataset

## Data

This repository contains three components:

### [GeoIP Feed](./feed/)

Raw snapshots of Starlink's GeoIP feed: https://geoip.starlinkisp.net/feed.csv

### [DNS PTR Records](./geoip/)

Corresponding DNS PTR records for the raw GeoIP feed, which reflects the associated PoP location for a given subnet, i.e., users in a given city/region.

<details>
  <summary>Example</summary>

The GeoIP feed lists `98.97.32.0/24,US,US-WA,Seattle`.

Using `nslookup 98.97.32.1` returns

```
1.32.97.98.in-addr.arpa name = customer.sttlwax1.pop.starlinkisp.net.
```

which means the Starlink users with public IPv4 addresses within the subnet `98.97.32.0/24` are associated with the PoP location in Seattle.
</details>

We only started checking DNS PTR records automatically and generate this report by GitHub Actions after `2024-08-05`.

**Note that**: It is only meaningful to check the corresponding DNS PTR records for the GeoIP feed at the time of the original data collections. The DNS PTR records for a given subnet may change over time.

The structure of the `geoip-{date}.json` file is as follows:

```json
{
  "valid": {
    "Two letter country code": {
      "Region or state code": {
        "City": {
          "ips": [
            [
              "subnet CIDR",
              "DNS PTR record of the first resolvable IP, usually the first IP in the subnet"
            ]
          ]
        }
      }
    }
  },
  "nxdomain": [
    "list of GeoIP entries with NXDOMAIN response",
  ],
  "servfail": [
    "list of GeoIP entries with SERVFAIL response",
  ],
  "pop_subnet_count": {
    [
      "DNS PTR record for a PoP",
      "the number of subnets associated with this PoP"
    ]
  }
}
```

### [Raw Data for Starlink Latency Map](./latency/)

Snapshots of raw JSON metrics for https://www.starlink.com/map?view=latency, which contains monthly snapshots of global latency and download/upload speed released by Starlink.

* https://api.starlink.com/public-files/metrics_residential.json
* https://api.starlink.com/public-files/metrics_maritime.json

## Update Frequency

The GeoIP feed is checked every 30 minutes by a GitHub Actions Workflow. Only if any new updates in the GeoIP feed are detected, the feed is downloaded and the corresponding DNS PTR records are checked by `nslookup` and the `geoip-{date}.json` file is generated.

The raw data for the Starlink latency map is updated at the beginning of each month.

## Note

1. The GeoIP feed only represents the planned naming and addressing scheme of the Starlink ISP. It does not reflect the actual deployment status of Starlink ground stations or the availability of Starlink service in a given region.
2. Some subnets listed in the GeoIP feed **may** not have been announced by BGP.
3. Some subnets **might** be associated with outdated or inaccurate DNS PTR records, which does not reflect the actual PoP association.

## Disclaimer

This repository is not affiliated with, endorsed by, or in any way connected to Starlink, SpaceX Inc., or any of their subsidiaries. All content provided here is either independently developed or obtained from publicly available sources on the Internet and is for educational and informational purposes only.
