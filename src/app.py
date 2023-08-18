import pandas as pd
from shiny import App, ui, render
from sqlalchemy import select, func, distinct
from schema import engine, tbl_solar
import matplotlib.pyplot as plt
from datetime import datetime


# DATABASE
def get_distinct_sorted_years():
    with engine.connect() as conn:
        stmt = (
            select(distinct(tbl_solar.c.year))\
            .order_by(tbl_solar.c.year)
        )
        results = conn.execute(stmt).fetchall()
    years_list = [row[0] for row in results]
    return years_list


def get_distinct_sorted_months(yr):
    with engine.connect() as conn:
        stmt = (
            select(distinct(tbl_solar.c.month))\
            .where(tbl_solar.c.year == yr)\
            .order_by(tbl_solar.c.year)
        )
        results = conn.execute(stmt).fetchall()
    years_list = [row[0] for row in results]
    return years_list


def get_generation_per_year():
    with engine.connect() as conn:
        stmt = (
            select(tbl_solar.c.year, func.sum(tbl_solar.c.solar))
            .group_by(tbl_solar.c.year)
            .order_by(tbl_solar.c.year)
        )
        results = conn.execute(stmt).fetchall()
    df = pd.DataFrame(results, columns=['time', 'solar'])
    return df


def get_generation_per_month(yr):
    with engine.connect() as conn:
        stmt = (
            select(tbl_solar.c.month, func.sum(tbl_solar.c.solar))
            .where(tbl_solar.c.year == yr)
            .group_by(tbl_solar.c.month)
            .order_by(tbl_solar.c.month)
        )
        results = conn.execute(stmt).fetchall()
    df = pd.DataFrame(results, columns=['time', 'solar'])
    return df


def get_generation_per_day(yr, mo):
    with engine.connect() as conn:
        stmt = (
            select(tbl_solar.c.day, tbl_solar.c.solar)
            .where((tbl_solar.c.year == yr) & (tbl_solar.c.month == mo))
            .order_by(tbl_solar.c.day)
        )
        results = conn.execute(stmt).fetchall()
    df = pd.DataFrame(results, columns=['time', 'solar'])
    return df


# SHINY
app_ui = ui.page_fluid(
    ui.panel_title(title="Growatt solar power generation charts"),
    ui.navset_pill(
        ui.nav("Year",
               ui.output_plot("plot_year"),
               ),
        ui.nav("Month",
               ui.output_plot("plot_month"),
               ui.input_slider("sl_month_year", "Year", get_distinct_sorted_years()[0], get_distinct_sorted_years()[-1],
                               get_distinct_sorted_years()[-1]),
               ),
        ui.nav("Day",
                ui.output_plot("plot_day"),
               ui.input_slider("sl_day_year", "Year", get_distinct_sorted_years()[0], get_distinct_sorted_years()[-1],
                               get_distinct_sorted_years()[-1]),
               ui.input_slider("sl_day_month", "Month", get_distinct_sorted_months(datetime.now().year)[0],
                               get_distinct_sorted_months(datetime.now().year)[-1],
                               get_distinct_sorted_months(datetime.now().year)[-1]),
               ),
    ),
)


def server(input, output, session):
    @output
    @render.plot(alt="Solar power barchart")
    def plot_year():
        df = get_generation_per_year()
        bars = plt.bar(df.time, df.solar)
        plt.bar_label(bars)
        plt.xlabel('Year')
        plt.ylabel('Generation (kWh)')

    @output
    @render.plot(alt="Solar power barchart")
    def plot_month():
        df = get_generation_per_month(input.sl_month_year())
        bars = plt.bar(df.time, df.solar)
        plt.bar_label(bars)
        plt.xlabel('Month')
        plt.ylabel('Generation (kWh)')

    @output
    @render.plot(alt="Solar power barchart")
    def plot_day():
        df = get_generation_per_day(input.sl_day_year(),
                                    input.sl_day_month())
        bars = plt.bar(df.time, df.solar)
        plt.bar_label(bars)
        plt.xlabel('Day')
        plt.ylabel('Generation (kWh)')

app = App(app_ui, server, debug=False)