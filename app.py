import streamlit as st
import pandas as pd
from db import get_connection
import reports
import io

# App Title
st.set_page_config(page_title="Food Donation CRUD & Reports", layout="wide")
#st.title("🍴 Food Donation Management System")
# Custom CSS for heading & sidebar style
st.markdown(
    """
    <style>
    /* App Title */
    .app-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #ff9800; /* Orange accent */
        font-family: 'Trebuchet MS', sans-serif;
        margin-top: -30px;
        margin-bottom: 20px;
    }

    /* Main content card style */
    div[data-testid="stMain"] {
        background-color: #ffffff; /* Solid white */
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    /* Sidebar style */
    section[data-testid="stSidebar"] {
        background-color: #2c2c2c; /* Dark sidebar */
        color: white;
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 16px;
        font-weight: 600;
    }

    /* Sidebar radio button labels */
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Display heading
st.markdown('<div class="app-title">🍴 Food Donation Management System</div>', unsafe_allow_html=True)


menu = ["Providers", "Receivers", "Food Listings", "Claims", "Reports"]
choice = st.sidebar.radio("📂 Select Table", menu)

# ==========================================================
# PROVIDERS CRUDE
# ==========================================================
if choice == "Providers":
    st.subheader("👨‍🌾 Manage Providers")

    # Create
    with st.form("add_provider", clear_on_submit=True):
        st.write("➕ Add Provider")
        pid = st.number_input("Provider ID", step=1, format="%d")
        name = st.text_input("Name")
        ptype = st.text_input("Provider Type")
        address = st.text_input("Address")
        city = st.text_input("City")
        contact = st.text_input("Contact")
        submit = st.form_submit_button("Add")

        if submit:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO providers (provider_id, name, provider_type, address, city, contact) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (pid, name, ptype, address, city, contact))
            conn.commit()
            conn.close()
            st.success("Provider Added ✅")

    # Read
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM providers", conn)
    st.dataframe(df)
    conn.close()

    # Update
    if not df.empty:
        st.write("✏️ Update Contact")
        update_id = st.selectbox("Select Provider", df['provider_id'])
        new_contact = st.text_input("New Contact")
        if st.button("Update Contact"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE providers SET contact=%s WHERE provider_id=%s", 
                        (new_contact, update_id))
            conn.commit()
            conn.close()
            st.success("Updated ✅")

    # Delete
    if not df.empty:
        del_id = st.selectbox("❌ Delete Provider", df['provider_id'])
        if st.button("Delete Provider"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM providers WHERE provider_id=%s", (del_id,))
            conn.commit()
            conn.close()
            st.success("Deleted ✅")

# ==========================================================
# RECEIVERS CRUD
# ==========================================================
elif choice == "Receivers":
    st.subheader("🏢 Manage Receivers")

    # Create
    with st.form("add_receiver", clear_on_submit=True):
        st.write("➕ Add Receiver")
        rid = st.number_input("Receiver ID", step=1, format="%d")
        name = st.text_input("Name")
        rtype = st.text_input("Receiver Type")
        city = st.text_input("City")
        contact = st.text_input("Contact")
        submit = st.form_submit_button("Add")

        if submit:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO receivers (receiver_id, name, receiver_type, city, contact) 
                VALUES (%s, %s, %s, %s, %s)
            """, (rid, name, rtype, city, contact))
            conn.commit()
            conn.close()
            st.success("Receiver Added ✅")

    # Read
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM receivers", conn)
    st.dataframe(df)
    conn.close()

    # Update
    if not df.empty:
        st.write("✏️ Update Contact")
        update_id = st.selectbox("Select Receiver", df['receiver_id'])
        new_contact = st.text_input("New Contact")
        if st.button("Update Contact"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE receivers SET contact=%s WHERE receiver_id=%s", 
                        (new_contact, update_id))
            conn.commit()
            conn.close()
            st.success("Updated ✅")

    # Delete
    if not df.empty:
        del_id = st.selectbox("❌ Delete Receiver", df['receiver_id'])
        if st.button("Delete Receiver"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM receivers WHERE receiver_id=%s", (del_id,))
            conn.commit()
            conn.close()
            st.success("Deleted ✅")

# ==========================================================
# FOOD LISTINGS CRUD
# ==========================================================
elif choice == "Food Listings":
    st.subheader("🥗 Manage Food Listings")

    # Create
    with st.form("add_listing", clear_on_submit=True):
        st.write("➕ Add Food Listing")
        fid = st.number_input("Food ID", step=1, format="%d")
        fname = st.text_input("Food Name")
        qty = st.number_input("Quantity", step=1, format="%d")
        expiry = st.date_input("Expiry Date")
        pid = st.number_input("Provider ID", step=1, format="%d")
        ptype = st.text_input("Provider Type")
        location = st.text_input("Location")
        ftype = st.text_input("Food Type")
        mtype = st.text_input("Meal Type")
        submit = st.form_submit_button("Add")

        if submit:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO food_listings 
                (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (fid, fname, qty, expiry, pid, ptype, location, ftype, mtype))
            conn.commit()
            conn.close()
            st.success("Food Listing Added ✅")

    # Read
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings", conn)
    st.dataframe(df)
    conn.close()

    # Update
    if not df.empty:
        st.write("✏️ Update Quantity")
        update_id = st.selectbox("Select Food Item", df['food_id'])
        new_qty = st.number_input("New Quantity", step=1, format="%d")
        if st.button("Update Quantity"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE food_listings SET quantity=%s WHERE food_id=%s", 
                        (new_qty, update_id))
            conn.commit()
            conn.close()
            st.success("Updated ✅")

    # Delete
    if not df.empty:
        del_id = st.selectbox("❌ Delete Food Item", df['food_id'])
        if st.button("Delete Food Item"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM food_listings WHERE food_id=%s", (del_id,))
            conn.commit()
            conn.close()
            st.success("Deleted ✅")

# ==========================================================
# CLAIMS CRUD
# ==========================================================
elif choice == "Claims":
    st.subheader("📦 Manage Claims")

    # Create
    with st.form("add_claim", clear_on_submit=True):
        st.write("➕ Add Claim")
        cid = st.number_input("Claim ID", step=1, format="%d")
        fid = st.number_input("Food ID", step=1, format="%d")
        rid = st.number_input("Receiver ID", step=1, format="%d")
        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
        ts = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")
        submit = st.form_submit_button("Add")

        if submit:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO claims (claim_id, food_id, receiver_id, status, timestamp) 
                VALUES (%s, %s, %s, %s, %s)
            """, (cid, fid, rid, status, ts))
            conn.commit()
            conn.close()
            st.success("Claim Added ✅")

    # Read
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM claims", conn)
    st.dataframe(df)
    conn.close()

    # Update
    if not df.empty:
        st.write("✏️ Update Claim Status")
        update_id = st.selectbox("Select Claim", df['claim_id'])
        new_status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])
        if st.button("Update Claim"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE claims SET status=%s WHERE claim_id=%s", 
                        (new_status, update_id))
            conn.commit()
            conn.close()
            st.success("Updated ✅")

    # Delete
    if not df.empty:
        del_id = st.selectbox("❌ Delete Claim", df['claim_id'])
        if st.button("Delete Claim"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM claims WHERE claim_id=%s", (del_id,))
            conn.commit()
            conn.close()
            st.success("Deleted ✅")

# ==========================================================
# REPORTS & ANALYSIS
# ==========================================================
elif choice == "Reports":
    st.subheader("📊 Reports & Analysis")

    report_options = {
        "Providers & Receivers per city": (
            reports.providers_receivers_by_city,
            """
            SELECT city,
                   COUNT(DISTINCT p.provider_id) AS total_providers,
                   COUNT(DISTINCT r.receiver_id) AS total_receivers
            FROM providers p
            LEFT JOIN receivers r ON p.city = r.city
            GROUP BY city;
            """
        ),
        "Top contributing provider type": (
            reports.top_provider_type,
            """
            SELECT provider_type, COUNT(*) AS total_contributions
            FROM food_listings
            GROUP BY provider_type
            ORDER BY total_contributions DESC
            LIMIT 1;
            """
        ),
        "Provider contacts in a city": (
            reports.provider_contacts,
            """
            SELECT name, contact
            FROM providers
            WHERE city = %s;
            """
        ),
        "Top receivers by claims": (
            reports.top_receivers,
            """
            SELECT r.name, COUNT(c.claim_id) AS total_claims
            FROM receivers r
            JOIN claims c ON r.receiver_id = c.receiver_id
            GROUP BY r.name
            ORDER BY total_claims DESC;
            """
        ),
        "Total food available": (
            reports.total_food_available,
            """
            SELECT SUM(quantity) AS total_quantity
            FROM food_listings;
            """
        ),
        "City with highest food listings": (
            reports.city_highest_listings,
            """
            SELECT location AS city, COUNT(*) AS total_listings
            FROM food_listings
            GROUP BY location
            ORDER BY total_listings DESC
            LIMIT 1;
            """
        ),
        "Most common food types": (
            reports.common_food_types,
            """
            SELECT food_type, COUNT(*) AS count
            FROM food_listings
            GROUP BY food_type
            ORDER BY count DESC;
            """
        ),
        "Claims per food item": (
            reports.claims_per_food,
            """
            SELECT f.food_name, COUNT(c.claim_id) AS claim_count
            FROM food_listings f
            LEFT JOIN claims c ON f.food_id = c.food_id
            GROUP BY f.food_name;
            """
        ),
        "Provider with most successful claims": (
            reports.top_provider_claims,
            """
            SELECT p.name, COUNT(c.claim_id) AS successful_claims
            FROM providers p
            JOIN food_listings f ON p.provider_id = f.provider_id
            JOIN claims c ON f.food_id = c.food_id
            WHERE c.status = 'Completed'
            GROUP BY p.name
            ORDER BY successful_claims DESC
            LIMIT 1;
            """
        ),
        "Claim status distribution": (
            reports.claims_status_distribution,
            """
            SELECT status, COUNT(*) AS count
            FROM claims
            GROUP BY status;
            """
        ),
        "Average quantity per receiver": (
            reports.avg_claim_quantity,
            """
            SELECT r.name, AVG(f.quantity) AS avg_quantity
            FROM receivers r
            JOIN claims c ON r.receiver_id = c.receiver_id
            JOIN food_listings f ON c.food_id = f.food_id
            GROUP BY r.name;
            """
        ),
        "Most claimed meal type": (
            reports.top_meal_type,
            """
            SELECT meal_type, COUNT(*) AS claim_count
            FROM food_listings f
            JOIN claims c ON f.food_id = c.food_id
            GROUP BY meal_type
            ORDER BY claim_count DESC
            LIMIT 1;
            """
        ),
        "Total donated by provider": (
            reports.total_donated_by_provider,
            """
            SELECT p.name, SUM(f.quantity) AS total_donated
            FROM providers p
            JOIN food_listings f ON p.provider_id = f.provider_id
            GROUP BY p.name;
            """
        ),
        "Receiver city with highest claims": (
            reports.receiver_city_highest_claims,
            """
            SELECT r.city, COUNT(c.claim_id) AS total_claims
            FROM receivers r
            JOIN claims c ON r.receiver_id = c.receiver_id
            GROUP BY r.city
            ORDER BY total_claims DESC
            LIMIT 1;
            """
        ),
        "Monthly donation trends": (
            reports.monthly_donation_trends,
            """
            SELECT DATE_FORMAT(expiry_date, '%Y-%m') AS month, SUM(quantity) AS total_quantity
            FROM food_listings
            GROUP BY month
            ORDER BY month;
            """
        ),
    }

    report_choice = st.selectbox("📌 Select Report", list(report_options.keys()))
    query_func, sql_code = report_options[report_choice]

    df = None  # initialize

    if report_choice == "Provider contacts in a city":
        city = st.text_input("Enter City")
        if not city:
           st.info("✍️ Please enter a city name to view provider contacts.")
        else:
           df = query_func(city)
    else:
        df = query_func()

    if df is not None:
        if not df.empty:
           st.markdown("**🔍 Executed SQL Query:**")
           st.code(sql_code, language="sql")

           st.markdown("**📊 Query Results:**")
           st.dataframe(df, use_container_width=True)

           if df.shape[1] >= 2:
               try:
                  st.bar_chart(df.set_index(df.columns[0]))
               except Exception:
                   pass
        else:
            st.warning("⚠️ No results found for this query.")


