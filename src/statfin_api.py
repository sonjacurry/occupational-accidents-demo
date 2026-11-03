import requests
import pandas as pd

# This section retrieves accident statistics from the StatFin PXWeb API. 
# The requests are batched by year to avoid exceeding the API request limit.

url = "https://statfin.stat.fi/PXWeb/api/v1/en/StatFin/ttap/129s.px"

years = [str(year) for year in range(2008, 2025)]

all_dfs = []

for year in years:

    print(f"Fetching {year}...")

    query = {
        "query": [
            {
                "code": "Timeperiod_y",
                "selection": {
                    "filter": "item",
                    "values": [year]
                }
            },
            {
                "code": "ammattiasema_13_19960101",
                "selection": {
                    "filter": "item",
                    "values": [
                        "0",
                        "1",
                        "3"
                    ]
                }
            },
            {
                "code": "henkilovahinko_47_19960101",
                "selection": {
                    "filter": "item",
                    "values": [
                        "4-",
                        "0-3",
                        "4-6",
                        "7-14",
                        "15-30",
                        "31-90",
                        "91-180",
                        "181-",
                        "997",
                        "998"
                    ]
                }
            },
            {
                "code": "toimiala_79_20180101",
                "selection": {
                    "filter": "item",
                    "values": [
                        "A", "A01", "A02", "A03",
                        "B", "B05", "B06", "B07", "B08", "B09",
                        "C", "C10", "C11", "C12", "C13", "C14",
                        "C15", "C16", "C17", "C18", "C19", "C20",
                        "C21", "C22", "C23", "C24", "C25", "C26",
                        "C27", "C28", "C29", "C30", "C31", "C32",
                        "C33",
                        "D", "D35",
                        "E", "E36", "E37", "E38", "E39",
                        "F", "F41", "F42", "F43",
                        "G", "G45", "G46", "G47",
                        "H", "H49", "H50", "H51", "H52", "H53",
                        "I", "I55", "I56",
                        "J", "J58", "J59", "J60", "J61", "J62", "J63",
                        "K", "K64", "K65", "K66",
                        "L", "L68",
                        "M", "M69", "M70", "M71", "M72", "M73",
                        "M74", "M75",
                        "N", "N77", "N78", "N79", "N80", "N81", "N82",
                        "O", "O84",
                        "P", "P85",
                        "Q", "Q86", "Q87", "Q88",
                        "R", "R90", "R91", "R92", "R93",
                        "S", "S94", "S95", "S96",
                        "T", "T97", "T98",
                        "U", "U99",
                        "S1313",
                        "X"
                    ]
                }
            },
            {
                "code": "ikaryhma_10_20180101",
                "selection": {
                    "filter": "item",
                    "values": [
                        "15-24",
                        "25-34",
                        "35-44",
                        "45-54",
                        "55-64",
                        "X"
                    ]
                }
            },
            {
                "code": "sukupuoli_9_20180101",
                "selection": {
                    "filter": "item",
                    "values": [
                        "1",
                        "2"
                    ]
                }
            },
            {
                "code": "contentscode",
                "selection": {
                    "filter": "item",
                    "values": [
                        "Tapaturmia"
                    ]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    # POST request
    resp = requests.post(
        url,
        json=query,
        timeout=120
    )

    # 200 = POST worked
    print(f"{year}: HTTP {resp.status_code}")

    # Show StatFin response if request failed
    if not resp.ok:
        print(resp.text)
        resp.raise_for_status()

    data = resp.json()

    # Convert JSON-stat2 cube to DataFrame
    names = data["id"]

    categories = [
        list(
            data["dimension"][code]["category"]["label"].values()
        )
        for code in names
    ]

    index = pd.MultiIndex.from_product(
        categories,
        names=names
    )

    df_year = pd.DataFrame(
        {
            "value": pd.array(
                data["value"],
                dtype="Float64"
            )
        },
        index=index
    ).reset_index()

    print(f"{year}: {len(df_year):,} rows")

    # Save this year's DataFrame
    all_dfs.append(df_year)


# Combine all years
df = pd.concat(
    all_dfs,
    ignore_index=True
)