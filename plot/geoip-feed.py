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

from matplotlib import pyplot as plt


GEOIP_FEED_DIR = "../feed"
GEOIP_DIR = "../geoip"


def count_subnet(filename):
    with open(filename, "r") as f:
        ipv4_subnets = 0
        ipv6_subnets = 0
        for line in f:
            # 65.181.1.0/24,AU,AU-NSW,Sydney,
            subnet = line.split(",")[0]
            try:
                subnet_ips = ipaddress.IPv6Network(subnet).hosts()
                ipv6_subnets += 1
            except ipaddress.AddressValueError:
                try:
                    subnet_ips = ipaddress.IPv4Network(subnet).hosts()
                    ipv4_subnets += 1
                except:
                    continue
    return ipv4_subnets, ipv6_subnets


def plot_subnet_count():
    print("Plotting Subnet Count")
    subnet_count = {
        "ipv4": {},
        "ipv6": {},
    }

    for dirpath, _, filenames in os.walk(GEOIP_FEED_DIR):
        for filename in filenames:
            if filename.startswith("feed-") and filename.endswith(".csv"):
                if "latest" in filename:
                    continue
                date_time = "-".join(filename.split(".")[0].split("-")[1:])
                date = datetime.strptime(date_time, "%Y%m%d-%H%M")
                v4_count, v6_count = count_subnet(Path(dirpath).joinpath(filename))
                subnet_count["ipv4"][date] = v4_count
                subnet_count["ipv6"][date] = v6_count

    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    subnet_count["ipv4"] = dict(sorted(subnet_count["ipv4"].items()))
    subnet_count["ipv6"] = dict(sorted(subnet_count["ipv6"].items()))

    ax.plot(subnet_count["ipv4"].keys(), subnet_count["ipv4"].values(), label="IPv4")
    ax.plot(subnet_count["ipv6"].keys(), subnet_count["ipv6"].values(), label="IPv6")
    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("Subnet Count")
    plt.title("No. of IPv4 and IPv6 Subnets as Planned in Starlink GeoIP Feed")
    plt.tight_layout()
    plt.savefig("figures/geoip-subnet-count.png")
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
        plt.tight_layout()
        plt.savefig("figures/geoip-pop-density.png")
        plt.close()


if __name__ == "__main__":
    plot_subnet_count()
    plot_country_city_count()
    plot_pop_density()
