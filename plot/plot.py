import os
import re
import sys
import json
import ipaddress

import pycountry
import numpy as np

from pprint import pprint
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from brokenaxes import brokenaxes
from matplotlib import pyplot as plt


GEOIP_FEED_DIR = "../feed"
GEOIP_DIR = "../geoip"
ATLAS_DIR = "../atlas"


def get_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def count_ipv6_56_subnets(subnet: str):
    net = ipaddress.IPv6Network(subnet)
    num48subnets = 2 ** (56 - net.prefixlen)
    assert num48subnets >= 1
    return num48subnets


def count_subnet(filename):
    with open(filename, "r") as f:
        ipv4_subnets = 0
        ipv6_subnets = 0
        ipv4_ips = 0
        ipv6_56_subnet_count = 0
        for line in f:
            # 65.181.1.0/24,AU,AU-NSW,Sydney,
            subnet = line.split(",")[0]
            try:
                ipaddress.IPv6Network(subnet).hosts()
                # count how many /48 subnets are available in this subnet
                ipv6_56_subnet_count += count_ipv6_56_subnets(subnet)
                ipv6_subnets += 1
            except ipaddress.AddressValueError:
                try:
                    ipaddress.IPv4Network(subnet).hosts()
                    ipv4_subnets += 1
                    ipv4_ips += ipaddress.IPv4Network(subnet).num_addresses
                except:
                    continue
    return ipv4_subnets, ipv6_subnets, ipv4_ips, ipv6_56_subnet_count


def plot_subnet_count():
    print("Plotting Subnet Count")
    subnet_count = {
        "ipv4": {},
        "ipv6": {},
        "ipv4_ips": {},
        "ipv6_56_subnet_count": {},
    }

    for dirpath, _, filenames in os.walk(GEOIP_FEED_DIR):
        for filename in filenames:
            if filename.startswith("feed-") and filename.endswith(".csv"):
                if "latest" in filename:
                    continue
                date_time = "-".join(filename.split(".")[0].split("-")[1:])
                date = datetime.strptime(date_time, "%Y%m%d-%H%M")
                # skip historical data
                if date < datetime(2024, 1, 1):
                    continue
                v4_count, v6_count, v4_ips, ipv6_56_subnet_count = count_subnet(Path(dirpath).joinpath(filename))
                subnet_count["ipv4"][date] = v4_count
                subnet_count["ipv6"][date] = v6_count
                subnet_count["ipv4_ips"][date] = v4_ips / 1000
                subnet_count["ipv6_56_subnet_count"][date] = ipv6_56_subnet_count / 1000000

    fig = plt.figure(figsize=(8, 6))
    # ax = fig.add_subplot(111)
    bax = brokenaxes(ylims=((200, 600), (1200, 1800)), hspace=.1)

    subnet_count["ipv4"] = dict(sorted(subnet_count["ipv4"].items()))
    subnet_count["ipv6"] = dict(sorted(subnet_count["ipv6"].items()))

    bax.plot(subnet_count["ipv4"].keys(), subnet_count["ipv4"].values(), label="IPv4")
    bax.plot(subnet_count["ipv6"].keys(), subnet_count["ipv6"].values(), label="IPv6")
    bax.legend()
    bax.set_xlabel("Date")
    bax.set_ylabel("Subnet Count")
    plt.title("No. of IPv4 and IPv6 Subnets as Planned in Starlink GeoIP Feed")
    plt.figtext(0.99, 0.01, "Date: {}".format(get_date()), horizontalalignment='right')
    # plt.tight_layout()
    plt.savefig("figures/geoip-subnet-count.png")
    plt.close()

    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    subnet_count["ipv4_ips"] = dict(sorted(subnet_count["ipv4_ips"].items()))

    ax.plot(subnet_count["ipv4_ips"].keys(), subnet_count["ipv4_ips"].values(), label="IPv4 Usable IP Addresses")
    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("Usable IP Address Count (Thousands)")
    plt.title("No. of Usable IPv4 Addresses as Planned in Starlink GeoIP Feed")
    plt.figtext(0.99, 0.01, "Date: {}".format(get_date()), horizontalalignment='right')
    plt.tight_layout()
    plt.savefig("figures/geoip-subnet-ip-count.png")
    plt.close()

    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    subnet_count["ipv6_56_subnet_count"] = dict(sorted(subnet_count["ipv6_56_subnet_count"].items()))

    ax.plot(subnet_count["ipv6_56_subnet_count"].keys(), subnet_count["ipv6_56_subnet_count"].values(), label="IPv6 /56 Subnet Count")
    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("No. of /56 Subnets (Millions)")
    plt.title("No. of /56 Subnets as Planned in Starlink GeoIP Feed")
    plt.figtext(0.99, 0.01, "Date: {}".format(get_date()), horizontalalignment='right')
    plt.tight_layout()
    plt.savefig("figures/geoip-v6_56_subnet-count.png")
    plt.close()


def count_country_city(filename):
    country_list = []
    city_list = []
    with open(filename, "r") as f:
        for line in f:
            # 65.181.1.0/24,AU,AU-NSW,Sydney,
            country = line.split(",")[1]
            city = line.split(",")[3]
            country = pycountry.countries.get(alpha_2=country)
            if country is not None:
                country_list.append(country.name)
            city_list.append(city)

    return len(list(set(country_list))), len(list(set(city_list)))


def plot_country_city_count():
    print("Plotting Country and City Count")
    count = {
        "country": {},
        "city": {},
    }
    for dirpath, _, filenames in os.walk(GEOIP_FEED_DIR):
        for filename in filenames:
            if filename.startswith("feed-") and filename.endswith(".csv"):
                if "latest" in filename:
                    continue
                date_time = "-".join(filename.split(".")[0].split("-")[1:])
                date = datetime.strptime(date_time, "%Y%m%d-%H%M")
                # skip historical data
                if date < datetime(2024, 1, 1):
                    continue
                country_count, city_count = count_country_city(Path(dirpath).joinpath(filename))
                count["country"][date] = country_count
                count["city"][date] = city_count

    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    count["country"] = dict(sorted(count["country"].items()))
    count["city"] = dict(sorted(count["city"].items()))

    ax.plot(count["country"].keys(), count["country"].values(), label="Country")
    ax.plot(count["city"].keys(), count["city"].values(), label="City")
    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    plt.title("No. of Countries, Territories and Cities as Planned in Starlink GeoIP Feed")
    plt.figtext(0.99, 0.01, "Date: {}".format(get_date()), horizontalalignment='right')
    plt.tight_layout()
    plt.savefig("figures/geoip-country-city-count.png")
    plt.close()


def plot_pop_density():
    print("Plotting PoP Serving Subnet Count")
    with open(Path(GEOIP_DIR).joinpath("geoip-latest.json"), "r") as f:
        data = json.load(f)
        pop_subnet_count = data["pop_subnet_count"]
        pop_density = {}
        for pop, count in pop_subnet_count:
            if re.match(r"customer\.[a-z0-9]+\.pop\.starlinkisp\.net\.", pop):
                pop_code = pop.split('.')[1]
                pop_density[pop_code] = count

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)

        pop_density = dict(sorted(pop_density.items(), key=lambda x: x[1], reverse=True))

        x = np.arange(len(pop_density))
        ax.bar(x, pop_density.values())
        ax.set_xticks(x)
        ax.set_xticklabels(pop_density.keys(), rotation=45, ha="right")
        ax.set_xlabel("PoP")
        ax.set_ylabel("Subnet Count")
        plt.title("No. of Subnets Served per PoP as Planned in Starlink GeoIP Feed")
        plt.figtext(0.99, 0.01, "Date: {}".format(get_date()), horizontalalignment='right')
        plt.tight_layout()
        plt.savefig("figures/geoip-pop-density.png")
        plt.close()


def plot_active_atlas_probes():
    print("Plotting Active Atlas Probes Distribution")
    with open(Path(ATLAS_DIR).joinpath("probes.json"), "r") as f:
        data = json.load(f)
        probe_count = defaultdict(int)
        for probe in data:
            if probe["status"]["name"] == "Connected":
                country_name = pycountry.countries.get(alpha_2=probe["country_code"]).name
                probe_count[country_name] += 1

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        probe_count = dict(sorted(probe_count.items(), key=lambda x: x[1], reverse=True))

        x = np.arange(len(probe_count))
        ax.bar(x, probe_count.values())
        for i, v in enumerate(probe_count.values()):
            ax.text(i, v + 0.1, str(v), ha="center")

        ax.set_xticks(x)
        ax.set_xticklabels(probe_count.keys(), rotation=45, ha="right")
        ax.set_xlabel("Country")
        ax.set_ylabel("Probe Count")
        plt.title("No. of Active RIPE Atlas Probes per Country")
        plt.figtext(0.99, 0.01, "Date: {}".format(get_date()), horizontalalignment='right')
        plt.tight_layout()
        plt.savefig("figures/atlas-active-probes.png")
        plt.close()


def plot_active_atlas_probe_per_pops():
    print("Plotting Active Atlas Probes per PoP")
    with open(Path(ATLAS_DIR).joinpath("active_probes.csv"), "r") as f:
        probe_count = defaultdict(int)
        for line in f:
            _, dns, _, _ = line.split(",")
            if len(dns) > 0:
                pop_code = dns.split('.')[1]
                probe_count[pop_code] = probe_count[pop_code] + 1

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        probe_count = dict(sorted(probe_count.items(), key=lambda x: x[1], reverse=True))

        x = np.arange(len(probe_count))
        ax.bar(x, probe_count.values())
        for i, v in enumerate(probe_count.values()):
            ax.text(i, v + 0.1, str(v), ha="center")

        ax.set_xticks(x)
        ax.set_xticklabels(probe_count.keys(), rotation=45, ha="right")
        ax.set_xlabel("PoP")
        ax.set_ylabel("Probe Count")
        plt.title("No. of Active RIPE Atlas Probes per PoP")
        plt.figtext(0.99, 0.01, "Date: {}".format(get_date()), horizontalalignment='right')
        plt.tight_layout()
        plt.savefig("figures/atlas-active-probes-per-pop.png")
        plt.close()


if __name__ == "__main__":
    plot_subnet_count()
    plot_country_city_count()
    plot_pop_density()
    plot_active_atlas_probes()
    plot_active_atlas_probe_per_pops()
