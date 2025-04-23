import csv
from datetime import datetime, timedelta

# Define input and output file names
input_csv = "scn_src/news1.csv"      # Input file with 435 domain names
output_csv = "gdelt_urls.csv"  # Output file with generated URLs

# GDELT API URL template with monthly filtering
base_url = "https://api.gdeltproject.org/api/v2/doc/doc?query=domain:{}&mode=artlist&maxrecords=250&format=json&DATE={}"

# Generate the past 12 months in YYYYMM format
today = datetime.today()
dates = [(today - timedelta(days=i * 30)).strftime("%Y%m") for i in range(12)]

# Read domain names from the input CSV
with open(input_csv, mode="r", newline="") as infile:
    reader = csv.reader(infile)
    domains = [row[0] for row in reader]  # Extract domain names

# Generate URLs and write to a new CSV
with open(output_csv, mode="w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Domain", "Month", "GDELT_URL"])  # Write header row

    for domain in domains:
        for date in dates:
            month_name = datetime.strptime(date, "%Y%m").strftime("%B %Y")  # Convert YYYYMM to Month Year
            url = base_url.format(domain, date)
            writer.writerow([domain, month_name, url])  # Write domain, month, and URL

print(f"✅ Successfully created {output_csv} with {len(domains) * 12} GDELT URLs.")