from flask import Flask, request, render_template_string
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

DATA_FILE = "output/return_predictions.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


@app.route("/")
def dashboard():

    df = load_data()

    # ---------------- FILTERS ----------------

    category = request.args.get("category", "All")
    region = request.args.get("region", "All")
    channel = request.args.get("channel", "All")
    risk = request.args.get("risk", "All")

    filtered_df = df.copy()

    if category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == category
        ]

    if region != "All":
        filtered_df = filtered_df[
            filtered_df["Region"] == region
        ]

    if channel != "All":
        filtered_df = filtered_df[
            filtered_df["Marketing_Channel"] == channel
        ]

    if risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk_Level"] == risk
        ]

    # ---------------- KPIs ----------------

    total_orders = len(filtered_df)

    returned_orders = int(
        filtered_df["Returned"].sum()
    )

    if total_orders > 0:
        return_rate = (
            returned_orders / total_orders
        ) * 100

        average_delivery = filtered_df[
            "Delivery_Days"
        ].mean()

    else:
        return_rate = 0
        average_delivery = 0

    high_risk_orders = len(
        filtered_df[
            filtered_df["Risk_Level"] == "High"
        ]
    )

    # ---------------- CATEGORY CHART ----------------

    category_data = (
        filtered_df
        .groupby("Category")["Returned"]
        .mean()
        .reset_index()
    )

    category_data["Returned"] *= 100

    category_chart = px.bar(
        category_data,
        x="Category",
        y="Returned",
        color="Returned",
        color_continuous_scale="Turbo",
        title="Return Rate by Category"
    )

    category_chart.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    category_html = pio.to_html(
        category_chart,
        full_html=False,
        include_plotlyjs="cdn"
    )

    # ---------------- REGION CHART ----------------

    region_data = (
        filtered_df
        .groupby("Region")["Returned"]
        .mean()
        .reset_index()
    )

    region_data["Returned"] *= 100

    region_chart = px.bar(
        region_data,
        x="Region",
        y="Returned",
        color="Returned",
        color_continuous_scale="Viridis",
        title="Return Rate by Region"
    )

    region_chart.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    region_html = pio.to_html(
        region_chart,
        full_html=False,
        include_plotlyjs=False
    )

    # ---------------- MARKETING CHANNEL ----------------

    channel_data = (
        filtered_df
        .groupby("Marketing_Channel")["Returned"]
        .mean()
        .reset_index()
    )

    channel_data["Returned"] *= 100

    channel_chart = px.bar(
        channel_data,
        x="Marketing_Channel",
        y="Returned",
        color="Returned",
        color_continuous_scale="Plasma",
        title="Return Rate by Marketing Channel"
    )

    channel_chart.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    channel_html = pio.to_html(
        channel_chart,
        full_html=False,
        include_plotlyjs=False
    )

    # ---------------- RISK CHART ----------------

    risk_data = (
        filtered_df["Risk_Level"]
        .value_counts()
        .reset_index()
    )

    risk_data.columns = [
        "Risk_Level",
        "Orders"
    ]

    risk_chart = px.pie(
        risk_data,
        names="Risk_Level",
        values="Orders",
        hole=0.45,
        title="Return Risk Distribution",
        color="Risk_Level",
        color_discrete_map={
            "Low": "#22c55e",
            "Medium": "#f59e0b",
            "High": "#ef4444"
        }
    )

    risk_chart.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    risk_html = pio.to_html(
        risk_chart,
        full_html=False,
        include_plotlyjs=False
    )

    # ---------------- DELIVERY CHART ----------------

    delivery_data = (
        filtered_df
        .groupby("Delivery_Days")["Returned"]
        .mean()
        .reset_index()
    )

    delivery_data["Returned"] *= 100

    delivery_chart = px.line(
        delivery_data,
        x="Delivery_Days",
        y="Returned",
        markers=True,
        title="Delivery Days vs Return Rate"
    )

    delivery_chart.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    delivery_html = pio.to_html(
        delivery_chart,
        full_html=False,
        include_plotlyjs=False
    )

    # ---------------- FILTER OPTIONS ----------------

    categories = [
        "All"
    ] + sorted(
        df["Category"].dropna().unique().tolist()
    )

    regions = [
        "All"
    ] + sorted(
        df["Region"].dropna().unique().tolist()
    )

    channels = [
        "All"
    ] + sorted(
        df["Marketing_Channel"].dropna().unique().tolist()
    )

    risks = [
        "All",
        "Low",
        "Medium",
        "High"
    ]

    # =====================================================
    # HTML
    # =====================================================

    html = """
<!DOCTYPE html>

<html>

<head>

<title>
E-Commerce Return Risk Dashboard
</title>

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family: Arial, sans-serif;

    background:
    linear-gradient(
        135deg,
        #eef2ff,
        #fdf2f8,
        #ecfeff
    );

    color: #1f2937;
}


/* HEADER */

.header {

    background:
    linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed,
        #db2777
    );

    color: white;

    padding: 30px;

    border-radius:
    0 0 30px 30px;

    box-shadow:
    0 10px 30px
    rgba(79, 70, 229, 0.25);
}

.header h1 {

    margin: 0;

    font-size: 32px;
}

.header p {

    margin-top: 10px;

    opacity: 0.9;
}


/* CONTAINER */

.container {

    max-width: 1400px;

    margin: auto;

    padding: 25px;
}


/* FILTERS */

.filters {

    background: white;

    padding: 22px;

    border-radius: 18px;

    margin-bottom: 25px;

    box-shadow:
    0 8px 25px
    rgba(0,0,0,0.08);
}

.filters h2 {

    color: #4f46e5;

    margin-top: 0;
}

.filter-row {

    display: grid;

    grid-template-columns:
    repeat(4, 1fr);

    gap: 15px;
}

.filter-group label {

    display: block;

    font-weight: bold;

    margin-bottom: 7px;
}

select {

    width: 100%;

    padding: 12px;

    border-radius: 10px;

    border:
    1px solid #d1d5db;
}

button {

    margin-top: 18px;

    background:
    linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    color: white;

    border: none;

    padding: 12px 25px;

    border-radius: 10px;

    font-weight: bold;

    cursor: pointer;
}


/* KPI */

.kpi-grid {

    display: grid;

    grid-template-columns:
    repeat(5, 1fr);

    gap: 18px;

    margin-bottom: 25px;
}

.kpi {

    padding: 25px;

    border-radius: 18px;

    color: white;

    min-height: 140px;

    box-shadow:
    0 8px 25px
    rgba(0,0,0,0.12);
}

.kpi h3 {

    margin: 0;

    font-size: 15px;
}

.kpi-value {

    font-size: 32px;

    font-weight: bold;

    margin-top: 18px;
}

.blue {

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #06b6d4
    );
}

.purple {

    background:
    linear-gradient(
        135deg,
        #7c3aed,
        #c026d3
    );
}

.pink {

    background:
    linear-gradient(
        135deg,
        #db2777,
        #f43f5e
    );
}

.orange {

    background:
    linear-gradient(
        135deg,
        #ea580c,
        #f59e0b
    );
}

.green {

    background:
    linear-gradient(
        135deg,
        #059669,
        #22c55e
    );
}


/* CHARTS */

.chart-grid {

    display: grid;

    grid-template-columns:
    repeat(2, 1fr);

    gap: 22px;
}

.chart-card {

    background: white;

    border-radius: 18px;

    padding: 10px;

    box-shadow:
    0 8px 25px
    rgba(0,0,0,0.08);
}

.full {

    grid-column:
    span 2;
}


/* FOOTER */

.footer {

    text-align: center;

    margin-top: 30px;

    padding: 20px;

    color: #6b7280;
}


/* RESPONSIVE */

@media(max-width: 1100px) {

    .kpi-grid {

        grid-template-columns:
        repeat(2, 1fr);
    }

    .filter-row {

        grid-template-columns:
        repeat(2, 1fr);
    }
}

@media(max-width: 700px) {

    .kpi-grid {

        grid-template-columns: 1fr;
    }

    .filter-row {

        grid-template-columns: 1fr;
    }

    .chart-grid {

        grid-template-columns: 1fr;
    }

    .full {

        grid-column: span 1;
    }
}

</style>

</head>


<body>


<div class="header">

<div class="container">

<h1>
🛒 E-Commerce Return Risk Dashboard
</h1>

<p>
Data Analytics • Machine Learning • Return Prediction
</p>

</div>

</div>


<div class="container">


<div class="filters">

<h2>
🔎 Dashboard Filters
</h2>

<form method="get">

<div class="filter-row">


<div class="filter-group">

<label>
Category
</label>

<select name="category">

{% for item in categories %}

<option
value="{{ item }}"
{% if item == category %}
selected
{% endif %}
>

{{ item }}

</option>

{% endfor %}

</select>

</div>


<div class="filter-group">

<label>
Region
</label>

<select name="region">

{% for item in regions %}

<option
value="{{ item }}"
{% if item == region %}
selected
{% endif %}
>

{{ item }}

</option>

{% endfor %}

</select>

</div>


<div class="filter-group">

<label>
Marketing Channel
</label>

<select name="channel">

{% for item in channels %}

<option
value="{{ item }}"
{% if item == channel %}
selected
{% endif %}
>

{{ item }}

</option>

{% endfor %}

</select>

</div>


<div class="filter-group">

<label>
Risk Level
</label>

<select name="risk">

{% for item in risks %}

<option
value="{{ item }}"
{% if item == risk %}
selected
{% endif %}
>

{{ item }}

</option>

{% endfor %}

</select>

</div>


</div>


<button type="submit">
✨ Apply Filters
</button>

</form>

</div>


<div class="kpi-grid">


<div class="kpi blue">

<h3>
📦 Total Orders
</h3>

<div class="kpi-value">
{{ total_orders }}
</div>

</div>


<div class="kpi purple">

<h3>
↩️ Returned Orders
</h3>

<div class="kpi-value">
{{ returned_orders }}
</div>

</div>


<div class="kpi pink">

<h3>
📊 Return Rate
</h3>

<div class="kpi-value">
{{ "%.2f"|format(return_rate) }}%
</div>

</div>


<div class="kpi orange">

<h3>
⚠️ High Risk Orders
</h3>

<div class="kpi-value">
{{ high_risk_orders }}
</div>

</div>


<div class="kpi green">

<h3>
🚚 Avg Delivery Days
</h3>

<div class="kpi-value">
{{ "%.2f"|format(average_delivery) }}
</div>

</div>


</div>


<div class="chart-grid">


<div class="chart-card">

{{ category_html|safe }}

</div>


<div class="chart-card">

{{ region_html|safe }}

</div>


<div class="chart-card">

{{ channel_html|safe }}

</div>


<div class="chart-card">

{{ risk_html|safe }}

</div>


<div class="chart-card full">

{{ delivery_html|safe }}

</div>


</div>


<div class="footer">

E-Commerce Return Rate Reduction Analysis

<br>

Developed using Python, Pandas,
Scikit-learn, Flask and Plotly

</div>


</div>


</body>

</html>
"""

    return render_template_string(
        html,
        categories=categories,
        regions=regions,
        channels=channels,
        risks=risks,
        category=category,
        region=region,
        channel=channel,
        risk=risk,
        total_orders=total_orders,
        returned_orders=returned_orders,
        return_rate=return_rate,
        high_risk_orders=high_risk_orders,
        average_delivery=average_delivery,
        category_html=category_html,
        region_html=region_html,
        channel_html=channel_html,
        risk_html=risk_html,
        delivery_html=delivery_html
    )


if __name__ == "__main__":

    print()
    print("==============================================")
    print(" E-COMMERCE RETURN RISK DASHBOARD")
    print("==============================================")
    print()
    print("Dashboard URL:")
    print("http://127.0.0.1:5000")
    print()
    print("Press CTRL + C to stop the dashboard.")
    print()

    app.run(debug=True)