
df = pd.read_csv("sample_data/Ai_Tools_Data.csv")

st.set_page_config("AI Tool Comparison Dashboard", layout="wide")
st.title("🧠 AI Tool Explorer")
st.markdown("Explore and compare AI tools by task, pricing, and use case.")

# Clean pricing column (e.g., convert free/premium to price buckets)
df['pricing_category'] = df['pricing'].fillna('Unknown')
df['primary_task'] = df['primary_task'].fillna('Other')

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
task_filter = st.sidebar.multiselect("Primary Task", options=sorted(df['primary_task'].unique()), default=None)
price_filter = st.sidebar.multiselect("Pricing", options=sorted(df['pricing_category'].unique()), default=None)
search_query = st.sidebar.text_input("Search by Keyword", "")

# Apply filters
filtered_df = df.copy()

if task_filter:
    filtered_df = filtered_df[filtered_df['primary_task'].isin(task_filter)]
if price_filter:
    filtered_df = filtered_df[filtered_df['pricing_category'].isin(price_filter)]
if search_query:
    filtered_df = filtered_df[filtered_df['company_name'].str.contains(search_query, case=False) |
                              filtered_df['short_description'].str.contains(search_query, case=False)]

# Show filtered result count
st.markdown(f"### Showing {len(filtered_df)} tools")

# Table of tools
st.dataframe(filtered_df[['company_name', 'primary_task', 'short_description', 'pricing_category', 'visit_website_url']].sort_values(by='company_name'))

# Charts
st.subheader("📊 Tool Distribution by Task")
task_count = filtered_df['primary_task'].value_counts().reset_index()
task_count.columns = ['Primary Task', 'Tool Count']
fig_task = px.bar(task_count, x='Primary Task', y='Tool Count', title='Number of Tools per Task Type', color='Tool Count')
st.plotly_chart(fig_task, use_container_width=True)

st.subheader("💵 Pricing Distribution")
price_count = filtered_df['pricing_category'].value_counts().reset_index()
price_count.columns = ['Pricing Category', 'Tool Count']
fig_price = px.pie(price_count, names='Pricing Category', values='Tool Count', title='Pricing Categories')
st.plotly_chart(fig_price, use_container_width=True)

# Tool card preview (first 3)
st.subheader("🔎 Featured Tools")
for _, row in filtered_df.head(3).iterrows():
    st.markdown(f"#### [{row['company_name']}]({row['visit_website_url']})")
    st.write(row['short_description'])
    st.markdown(f"**Primary Task**: {row['primary_task']}")
    st.markdown(f"**Pricing**: {row['pricing']}")
    st.markdown("---")

# Notes
with st.expander("ℹ️ How to Extend"):
    st.markdown("""
    - Add scoring columns (e.g., accuracy, latency) to rank tools.
    - Group tools by department or use-case and show comparisons.
    - Add export/download functionality.
    - Include Q&A or pros/cons popup for each tool.
    """)
