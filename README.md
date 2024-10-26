# Starlink GeoIP Dataset

[![Refresh GeoIP](https://github.com/clarkzjw/starlink-geoip/actions/workflows/geoip_feed_refresh.yaml/badge.svg)](https://github.com/clarkzjw/starlink-geoip/actions/workflows/geoip_feed_refresh.yaml) [![Update GEOIP Map](https://github.com/clarkzjw/starlink-geoip/actions/workflows/update_map.yaml/badge.svg)](https://github.com/clarkzjw/starlink-geoip/actions/workflows/update_map.yaml) [![Refresh Atlas Probe List](https://github.com/clarkzjw/starlink-geoip/actions/workflows/refresh_atlas_probe.yaml/badge.svg)](https://github.com/clarkzjw/starlink-geoip/actions/workflows/refresh_atlas_probe.yaml)

📝 See the list of our related research work at https://oac.uvic.ca/starlink.

📍 Checkout the GeoIP visualization map at https://pan.uvic.ca/~clarkzjw/starlink.

<a href="https://pan.uvic.ca/~clarkzjw/starlink" target="_blank"><img alt="Starlink GeoIP Map" src="https://github.com/clarkzjw/clarkzjw/blob/master/geoip.jpg?raw=true"></a>

## Code

The source code used to generated this repository is available at [clarkzjw/starlink-geoip](https://github.com/clarkzjw/starlink-geoip).

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/geoip-subnet-count.png)

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/geoip-subnet-ip-count.png)

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/geoip-country-city-count.png)

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/geoip-pop-density.png)

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/atlas-active-probes.png)

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/atlas-active-probes-per-pop.png)

## Data

This repository contains the following components:

### [GeoIP Feed](./feed/)

This directory contains raw snapshots of Starlink's GeoIP feed: https://geoip.starlinkisp.net/feed.csv

Example:

```
14.1.64.0/24,PH,PH-00,Manila,
2a0d:3340:f400::/38,DE,DE-BE,Berlin,
```

Each line in the GeoIP feed represents a subnet allocated to a region of Starlink users, with the following fields:

`<IPv4 or IPv6 subnet CIDR>,<ISO 3166-2 Alpha 2 Country Code>,<Region or State Code>,<City>,`

Note that the `city` concept in the GeoIP feed does not necessarily correspond to an actual single city. For example, a Starlink dish within the Canadian Arctic circle is assigned with the public IPv4 address `170.203.201.xx`, which is associated with the Seattle PoP, belongs to `170.203.201.0/24,CA,CA-BC,Vancouver,` in the GeoIP feed.

### [DNS PTR Records](./geoip/)

This directory contains the corresponding DNS PTR records for the raw GeoIP feed.

Each Starlink customer IP address allocated by the GeoIP feed is assigned a [DNS PTR record](https://www.cloudflare.com/learning/dns/dns-records/dns-ptr-record/), which reflects the associated Point of Presence (PoP) location of this IP address.

For example, for the GeoIP feed entry `98.97.32.0/24,US,US-WA,Seattle`,

`nslookup 98.97.32.1` or `dig -x 98.97.32.1` returns:

```
1.32.97.98.in-addr.arpa name = customer.sttlwax1.pop.starlinkisp.net.
```

which means the Starlink users assigned with public IPv4 addresses within the subnet `98.97.32.0/24` are associated with the `sttlwax1` (Seattle) PoP.

The PoP naming scheme is related to [CLLI code](https://en.wikipedia.org/wiki/CLLI_code).

  + For PoPs in the USA, the naming scheme is `<4-letter-city><2-letter-state>x<number>`.
  + For other PoPs around the world, the naming scheme is `<4-letter-city><3-letter-country><number>`.

    However, the following records are likely exceptions:

    ```
    customer.pthpakx.pop.starlinkisp.net.

    customer.rcxship1.pop.starlinkisp.net.
    customer.rcxship2.pop.starlinkisp.net.
    customer.spxship1.pop.starlinkisp.net.

    customer.rdmdwax3rk3.pop.starlinkisp.net.
    ```

    Note that `rdmdwax3` **sometimes seems to be** a placeholder for new PoPs to be launched in the future.

For the data in this repository, we only started checking DNS PTR records automatically and generating reports by GitHub Actions after `2024-08-05`.

**Note that**: It is only meaningful to check the corresponding DNS PTR records for the GeoIP feed at the time of the GeoIP feed data collection. The DNS PTR records for a given subnet may change over time.

The structure of the `geoip-{date}.json` file is as follows:

```json
{
  "valid": {
    "<2 letter country code>": {
      "<Region or state code>": {
        "<City>": {
          "ips": [
            [
              "IPv4 or IPv6 subnet CIDR",
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

This directory contains snapshots of raw JSON metrics for https://www.starlink.com/map?view=latency, which contains monthly snapshots of the global latency and download/upload speed released by Starlink.

* https://api.starlink.com/public-files/metrics_residential.json
* https://api.starlink.com/public-files/metrics_maritime.json

## [Data for GeoIP Map](./map/)

The [`map`](./map) directory contains the data used to render the GeoIP map available at [https://pan.uvic.ca/~clarkzjw/starlink/](https://pan.uvic.ca/~clarkzjw/starlink/).

## [RIPE Atlas Probe List](./atlas/)

The [`atlas`](./atlas/) directory contains the list of [RIPE Atlas probes](https://atlas.ripe.net/probes/public) connected to Starlink networks.

[`probes.json`](./atlas/probes.json) contains the list of all probes associated with Starlink networks, filtered based on `ASN 14593` and `ASN 45700` (In Indonesia).

[`active_probes.csv`](./atlas/active_probes.csv) contains the list of active probes with the status of `Connected` at the time of checking.
For active probes, the corresponding DNS PTR records of the public IP is checked with `dig -x <ip> +short` to get the corresponding PoP location.

## [PeeringDB](./peeringdb/)

The [`peeringdb`](./peeringdb/) directory contains the information about Starlink networks ([18747/ASN 14593](https://www.peeringdb.com/net/18747), [36005/ASN 45700](https://www.peeringdb.com/net/36005)) available from https://www.peeringdb.com.

It mainly contains the lists of Public Peering Exchange Points (`netixlan`) and Interconnection Facilities (`netfac`).

## [Plot](./plot/)

This directory contains the script to generate the figures in this README file as shown above. The figures are available in the [`figures`](https://github.com/clarkzjw/starlink-geoip-data/tree/figures) branch of this repository.

## Update Frequency

The repository is automatically update by GitHub Actions in https://github.com/clarkzjw/starlink-geoip/tree/master/.github/workflows.

* GeoIP feed: [`"0 * * * *"`](https://crontab.guru/#0_*_*_*_*)
* DNS PTR records: [`"15 */3 * * *"`](https://crontab.guru/#15_*/3_*_*_*)
* GeoIP map refresh: [`"30 */6 * * *"`](https://crontab.guru/#30_*/6_*_*_*)
* Monthly latency snapshots: [`"0 0 */7 * *"`](https://crontab.guru/#0_0_*/7_*_*)
* RIPE Atlas probe list: [`"0 0 * * *"`](https://crontab.guru/#0_0_*_*_*)
* PeeringDB info: [`"45 0 * * *"`](https://crontab.guru/#45_0_*_*_*)

*Whenever the GeoIP feed is updated, DNS PTR records refresh is also triggered.*

## Note

1. The GeoIP feed only represents the planned naming and addressing scheme of the Starlink ISP. It may not reflect the actual deployment status of Starlink ground stations or the availability of Starlink service in a given region.
2. Some subnets listed in the GeoIP feed **may** not have been announced by BGP.
3. Some subnets **might** be associated with outdated or inaccurate DNS PTR records, which does not reflect the actual PoP association.

## TODO

- [ ] Verify subnet IP allocation with BGP announcements.
- [ ] Test subnet IP external reachability.

## Disclaimer

This repository is not affiliated with, endorsed by, or in any way connected to Starlink, SpaceX Inc., or any of their subsidiaries. All content provided here is either independently developed or obtained from publicly available sources on the Internet and is for educational and informational purposes only.
