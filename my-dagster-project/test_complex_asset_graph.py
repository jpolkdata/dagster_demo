import csv
import requests
from dagster import asset
import urllib.request
import zipfile
from dagster import materialize

@asset
def cereals():
    response = requests.get("https://docs.dagster.io/assets/cereal.csv")
    lines = response.text.split("\n")
    return [row for row in csv.DictReader(lines)]

@asset
def nabisco_cereals(cereals):
    """Cereals manufactured by Nabisco"""
    return [row for row in cereals if row["mfr"] == "N"]

@asset
def cereal_protein_fractions(cereals):
    """
    For each cereal, records its protein content as a fraction of its total mass.
    """
    result = {}
    for cereal in cereals:
        total_grams = float(cereal["weight"]) * 28.35
        result[cereal["name"]] = float(cereal["protein"]) / total_grams

    return result

@asset
def highest_protein_nabisco_cereal(nabisco_cereals, cereal_protein_fractions):
    """
    The name of the nabisco cereal that has the highest protein content.
    """
    sorted_by_protein = sorted(
        nabisco_cereals, key=lambda cereal: cereal_protein_fractions[cereal["name"]]
    )
    return sorted_by_protein[-1]["name"]

@asset
def cereal_ratings_zip() -> None:
    urllib.request.urlretrieve(
        "https://dagster-git-tutorial-nothing-elementl.vercel.app/assets/cereal-ratings.csv.zip",
        "cereal-ratings.csv.zip",
    )

@asset(non_argument_deps={"cereal_ratings_zip"})
def cereal_ratings_csv() -> None:
    with zipfile.ZipFile("cereal-ratings.csv.zip", "r") as zip_ref:
        zip_ref.extractall(".")

@asset(non_argument_deps={"cereal_ratings_csv"})
def nabisco_cereal_ratings(nabisco_cereals):
    with open("cereal-ratings.csv", "r") as f:
        cereal_ratings = {
            row["name"]: row["rating"] for row in csv.DictReader(f.readlines())
        }

    result = {}
    for nabisco_cereal in nabisco_cereals:
        name = nabisco_cereal["name"]
        result[name] = cereal_ratings[name]

    return result

def test_nabisco_cereals():
    cereals = [
        {"name": "cereal1", "mfr": "N"},
        {"name": "cereal2", "mfr": "K"},
    ]
    result = nabisco_cereals(cereals)
    assert len(result) == 1
    assert result == [{"name": "cereal1", "mfr": "N"}]

def test_cereal_assets():
    assets = [
        nabisco_cereals,
        cereals,
        cereal_protein_fractions,
        highest_protein_nabisco_cereal,
    ]

    result = materialize(assets)
    assert result.success
    assert result.output_for_node("highest_protein_nabisco_cereal") == "100% Bran"
