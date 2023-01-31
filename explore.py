#/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st


st.title("Individualism vs Collectivism (IDV)")
st.markdown("## Does culture correlate with development?")

df = pd.read_csv("results.csv")

p_value_cutoff = st.sidebar.slider('P-value cutoff', 0.00, 1.00, 0.05, 0.01)

size_cutoff = st.sidebar.slider('Sample Size cutoff', 0, 61, 50, 1)

rsquared_cutoff = st.sidebar.slider('Adj R-squared cutoff', 0.00, 1.00, 0.5, 0.05)

year_from = st.sidebar.slider('Year From', 1960, 2021, 2000)
year_to = st.sidebar.slider('Year To', 1960, 2021, 2020)

df_filter = df[(df["Year"] >= year_from) & (df["Year"] <= year_to) & (df["Pearson P-value"] <= p_value_cutoff) & (df["Countries"] >= size_cutoff) & (df["R_Squared_Adj"] >= rsquared_cutoff )]

topic_list = list(df_filter["Topic"].unique())
topic = st.selectbox('Select a Topic', topic_list)

df_topic = df_filter[df_filter["Topic"] == topic]

indicator_list = list(df_topic["Indicator Code"].unique())

indicator = st.selectbox('Select an Indicator', indicator_list)
df_series = pd.read_csv("WDISeries.csv")
indicator_row = df_series[df_series["Series Code"] == indicator].head(1)
indicator_name = indicator_row["Indicator Name"].values[0]
long_definition = indicator_row["Long definition"].values[0]
topic = indicator_row["Topic"].values[0]
#st.markdown("**Topic:**")
#st.markdown(topic)
st.markdown("**Name:**")
st.markdown(indicator_name)
st.markdown("**Definition:**")
st.markdown(long_definition)

df_fig = df_topic[(df_topic["Indicator Code"] == indicator)]
df_fig["Year"] = df_fig["Year"].astype(str)
fig = px.bar(df_fig, 
             x="Year", 
             y="Pearson R", 
             color="Year",
             title = f"Pearson's R (Correlation Coefficient) between IDV and {indicator}"
             )
fig.update_xaxes(dtick="Y1")
fig.update_layout(showlegend=False)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

