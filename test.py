import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# 1. Page setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Passenger Numbers by Train Route",
    layout="wide"
)

st.title("Train Passenger Analysis Dashboard")
st.caption("Analysis question: Which routes have the highest average passenger numbers?")

# ---------------------------------------------------------
# 2. Load the dataset
#    Keep train_journeys.csv in the same folder as this file.
# ---------------------------------------------------------
@st.cache_data
def load_data():
    data_path = Path(__file__).resolve().parent / "train_journeys.csv"
    data = pd.read_csv(data_path)

    required_columns = ["journey_id", "station", "destination", "passengers"]
    missing_columns = [col for col in required_columns if col not in data.columns]

    if missing_columns:
        raise ValueError(
            "The dataset is missing these required columns: "
            + ", ".join(missing_columns)
        )

    data["passengers"] = pd.to_numeric(data["passengers"], errors="coerce")
    data = data.dropna(subset=["station", "destination", "passengers"])
    data["ROUTE"] = (
        data["station"].astype(str).str.strip()
        + " → "
        + data["destination"].astype(str).str.strip()
    )
    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

if df.empty:
    st.warning("There are no valid journey records to analyse.")
    st.stop()

# ---------------------------------------------------------
# 3. Calculate average passenger numbers for each route
# ---------------------------------------------------------
route_passengers = (
    df.groupby("ROUTE")
      .agg(
          TRIPS=("journey_id", "count"),
          TOTAL_PASSENGERS=("passengers", "sum"),
          AVG_PASSENGERS=("passengers", "mean"),
          MAX_PASSENGERS=("passengers", "max")
      )
      .sort_values("AVG_PASSENGERS", ascending=False)
)

# ---------------------------------------------------------
# 4. KPI indicators
# ---------------------------------------------------------
total_journeys = len(df)
total_passengers = int(df["passengers"].sum())
number_of_routes = df["ROUTE"].nunique()
highest_average = route_passengers["AVG_PASSENGERS"].max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total journeys", f"{total_journeys:,}", border=True)
col2.metric("Total passengers", f"{total_passengers:,}", border=True)
col3.metric("Number of routes", f"{number_of_routes:,}", border=True)
col4.metric("Highest average passengers", f"{highest_average:,.1f}", border=True)

st.divider()

# ---------------------------------------------------------
# 5. Top 10 routes by average passenger numbers
# ---------------------------------------------------------
st.header("Top 10 Routes by Average Passenger Numbers")

top_routes = route_passengers.head(10).sort_values("AVG_PASSENGERS")

fig, ax = plt.subplots(figsize=(10, 5.5))

bar_colors = ["darkblue"] * len(top_routes)
bar_colors[-1] = "firebrick"  # Highlight the route with the highest average

bars = ax.barh(
    top_routes.index,
    top_routes["AVG_PASSENGERS"],
    color=bar_colors
)

ax.set_title(
    "TOP 10 ROUTES BY AVERAGE PASSENGER NUMBERS",
    fontsize=13,
    fontweight="bold"
)
ax.set_xlabel("Average number of passengers", fontsize=11)
ax.set_ylabel("Train route", fontsize=11)
ax.grid(axis="x", linestyle="--", alpha=0.7)
ax.set_axisbelow(True)
ax.bar_label(bars, fmt="%.1f", padding=4, fontsize=10)
ax.set_xlim(0, top_routes["AVG_PASSENGERS"].max() * 1.18)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(
    "The chart ranks routes by the mean number of passengers per recorded journey. "
    "The highest-average route is highlighted in red."
)

# ---------------------------------------------------------
# 6. Detailed results for all routes
# ---------------------------------------------------------
st.subheader("Passenger Statistics by Route")

display_table = route_passengers.rename(
    columns={
        "TRIPS": "Number of Journeys",
        "TOTAL_PASSENGERS": "Total Passengers",
        "AVG_PASSENGERS": "Average Passengers",
        "MAX_PASSENGERS": "Maximum Passengers"
    }
).copy()

display_table["Average Passengers"] = display_table["Average Passengers"].round(1)

st.dataframe(
    display_table,
    use_container_width=True
)

# ---------------------------------------------------------
# 7. Automatically generated finding
# ---------------------------------------------------------
top_route = route_passengers.index[0]
top_average = route_passengers.iloc[0]["AVG_PASSENGERS"]
top_trips = int(route_passengers.iloc[0]["TRIPS"])

second_route = route_passengers.index[1] if len(route_passengers) > 1 else None
second_average = (
    route_passengers.iloc[1]["AVG_PASSENGERS"]
    if len(route_passengers) > 1 else None
)

st.subheader("Key Finding")

finding = (
    f"**{top_route}** has the highest average passenger number, "
    f"with **{top_average:,.1f} passengers per journey**, based on "
    f"{top_trips} recorded journey(s)."
)

if second_route is not None:
    finding += (
        f" It is followed by **{second_route}**, with an average of "
        f"**{second_average:,.1f} passengers per journey**."
    )

st.info(finding)

# Highlight the limitation of routes with few observations.
if top_trips == 1:
    st.warning(
        "Interpretation note: The route with the highest average is based on "
        "only one recorded journey. More observations are needed to establish "
        "whether it consistently carries the highest number of passengers."
    )
else:
    st.caption(
        "Interpretation note: Averages are calculated from the journeys available "
        "in the dataset. Routes with fewer recorded journeys should be interpreted "
        "with caution."
    )

st.divider()

st.caption(
    "Method: Average passengers per route = total passengers recorded on the route "
    "divided by the number of recorded journeys on that route."
)
