# National Parks Trip Planner
National Parks Trip Planner is a backend API project that helps users explore and compare U.S. national parks using data from the National Park Service API ((https://www.nps.gov/subjects/developer/index.htm)).

The project supports three main features:

1. **Compare park sizes** by computing land area from official park boundary polygons.
2. **Visualize activities** by generating bar charts showing how many activity categories each park offers.
3. **Download park image galleries** by bundling National Park Service gallery photos into a ZIP file.

Stack is **Python** on **AWS Lambda** + **API Gateway**, with **S3** for charts and ZIPs and **RDS (MySQL)** to cache where each park’s ZIP lives so we don’t rebuild it on every request.

**Team:** Irene Ha, Ejean Kuo, Henron Ruan  

---

### Pieces in this repo

- **`parkAreasComputation.py`** — Lambda for `GET …/parkboundaries/{sitecode}`. Pulls GeoJSON from NPS, adds up polygon areas (subtracting holes), returns km² and acres.
- **`activityChart.py`** — Lambda for a `POST` that accepts `parkCodes`. Calls NPS for each park, counts activities, renders a bar chart through [QuickChart](https://quickchart.io/), uploads the PNG to S3, returns the file URL and counts.
- **`getImagesZip.py`** — Lambda for `GET …/parkimages/{park}`. Fetches gallery images, zips them, uploads to S3, stores the object key in MySQL on first use, returns a presigned download link.
- **`schema.sql`** — MySQL schema for that cache table.
- **`client.py`** — Tiny CLI to exercise the three flows against a deployed API.
- **`readme.txt`** — Longer AWS console walkthrough (layers, Gateway paths, env vars, IAM).

---

### Run the client

```bash
pip install requests
python3 client.py
```

Set `baseurl` in `client.py` to your API Gateway stage URL, then choose task `1`, `2`, or `3`. Use `list` at prompts to print NPS site codes.

---

### Deploying

Provision MySQL (RDS), run `schema.sql`, deploy each `.py` as a Lambda with the right **layers** (`requests`, `boto3`, `pymysql`, …), hook them up with **API Gateway** using Lambda proxy integration, and set **env vars** (NPS key, buckets, DB credentials, etc.) in the console or your IaC—never commit secrets.

Exact clicks and example layer zip commands are in **`readme.txt`**.

---

### Expected Behavior

Areas use the NPS boundaries endpoint and a bit of geometry on the coordinates. Charts aggregate NPS “activities” and stash the rendered image in S3. The ZIP path hits NPS multimedia galleries, compresses up to a configurable limit, uploads once per park code, then reuses the stored S3 key for faster follow-up requests.
