import csv
import requests

# Input CSV file with domain names
input_csv = "scn_src/news1.csv"
output_csv = "valid_gdelt_domains.csv"

# GDELT API URL template (query for at least one article)
base_url = "https://api.gdeltproject.org/api/v2/doc/doc?query=domain:{}&mode=artlist&maxrecords=1&format=json"

# Read domains from input CSV
with open(input_csv, mode="r", newline="") as infile:
    reader = csv.reader(infile)
    domains = [row[0] for row in reader]  # Extract domain names

# List to store domains that return results
valid_domains = []

# Check each domain in GDELT
for domain in domains:
    url = base_url.format(domain)
    try:
        response = requests.get(url)
        data = response.json()
        if "articles" in data and len(data["articles"]) > 0:
            valid_domains.append(domain)
            print(f"✅ Found results for: {domain}")
        else:
            print(f"❌ No results for: {domain}")
    except Exception as e:
        print(f"⚠️ Error checking {domain}: {e}")

# Write valid domains to a new CSV file
with open(output_csv, mode="w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Valid Domain"])