# Starlink GeoIP Dataset

📝 See the list of our related research work at https://oac.uvic.ca/starlink.

📍 Check out the GeoIP visualization map at https://pan.uvic.ca/~clarkzjw/starlink.

<a href="https://pan.uvic.ca/~clarkzjw/starlink" target="_blank"><img alt="Starlink GeoIP Map" src="https://github.com/clarkzjw/clarkzjw/blob/master/geoip.jpg?raw=true"></a>

## Code

The source code used to generate this repository is available at [clarkzjw/starlink-geoip](https://github.com/clarkzjw/starlink-geoip).

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/geoip-subnet-count.png)

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/geoip-subnet-ip-count.png)

![](https://raw.githubusercontent.com/clarkzjw/starlink-geoip-data/refs/heads/figures/geoip-v6_56_subnet-count.png)

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

Historical GeoIP feeds earlier than `2024` were retrieved from the [Wayback Machine](https://web.archive.org/web/*/https://geoip.starlinkisp.net/feed.csv).

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
  },
  "bgp_not_active": [
    "list of GeoIP entries with no active BGP announcement in AS14593/45700",
  ]
}
```

**Note that**: Starting from `2024-11-25`, we are checking whether the subnets in the GeoIP feed are announced in the BGP table of AS 14593/45700. The BGP data is retrieved from [BGP.tools](https://bgp.tools/). See also [#bgp](#bgp).

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
For active probes, the corresponding DNS PTR records of the public IPs are checked with `dig -x <ip> +short` to get the corresponding PoP location.

## [PeeringDB](./peeringdb/)

The [`peeringdb`](./peeringdb/) directory contains the information about Starlink networks ([18747/ASN 14593](https://www.peeringdb.com/net/18747), [36005/ASN 45700](https://www.peeringdb.com/net/36005)) available from https://www.peeringdb.com.

It mainly contains the lists of Public Peering Exchange Points (`netixlan`) and Interconnection Facilities (`netfac`).

## [BGP](./bgp/)

The [`bgp`](./bgp/) directory contains the BGP announcements from Starlink ASN 14593/45700. Some subnets planned in GeoIP feed might not appear in BGP announcement yet.

The BGP data is retrieved from [BGP.tools](https://bgp.tools/kb/api).

## [Availability](./availability/)

See the [README](./availability/README.md) file in the [`availability`](./availability/) directory for more information.

## [Plot](./plot/)

This directory contains the script to generate the figures in this README file as shown above. The figures are available in the [`figures`](https://github.com/clarkzjw/starlink-geoip-data/tree/figures) branch of this repository.

## Update Frequency

The repository is automatically updated by GitHub Actions at https://github.com/clarkzjw/starlink-geoip/tree/master/.github/workflows.

## Note

1. The GeoIP feed only represents the planned naming and addressing scheme of the Starlink ISP. It may not reflect the actual deployment status of Starlink ground stations or the availability of Starlink service in a given region.
2. Some subnets listed in the GeoIP feed **may** not have been announced by BGP.
3. Some subnets **might** be associated with outdated or inaccurate DNS PTR records, which do not reflect the actual PoP association.

## Disclaimer

This repository is not affiliated with, endorsed by, or in any way connected to Starlink, SpaceX Inc., or any of their subsidiaries. All content provided here is either independently developed or obtained from publicly available sources on the Internet and is for educational and informational purposes only.
