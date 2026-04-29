import pandas as pd
from db import get_connection

def run_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# 1. Providers & Receivers per city
def providers_receivers_by_city():
    query = """
    SELECT city, 
           COUNT(DISTINCT provider_id) AS total_providers,
           COUNT(DISTINCT receiver_id) AS total_receivers
    FROM (
        SELECT city, provider_id, NULL AS receiver_id FROM providers
        UNION ALL
        SELECT city, NULL, receiver_id FROM receivers
    ) t
    GROUP BY city;
    """
    return run_query(query)

# 2. Type of food provider contributing most
def top_provider_type():
    query = """
    SELECT provider_type, COUNT(*) AS total
    FROM providers
    GROUP BY provider_type
    ORDER BY total DESC
    LIMIT 1;
    """
    return run_query(query)

# 3. Contact info of providers in a specific city
def provider_contacts(city):
    query = "SELECT name, contact FROM providers WHERE city=%s"
    return run_query(query, (city,))

# 4. Receivers who claimed the most food
def top_receivers():
    query = """
    SELECT r.name, COUNT(c.claim_id) AS total_claims
    FROM claims c
    JOIN receivers r ON c.receiver_id=r.receiver_id
    GROUP BY r.name
    ORDER BY total_claims DESC
    LIMIT 5;
    """
    return run_query(query)

# 5. Total food available
def total_food_available():
    query = "SELECT SUM(quantity) AS total_available FROM food_listings"
    return run_query(query)

# 6. City with highest food listings
def city_highest_listings():
    query = """
    SELECT p.city, COUNT(*) AS total_listings
    FROM food_listings f
    JOIN providers p ON f.provider_id = p.provider_id
    GROUP BY p.city
    ORDER BY total_listings DESC
    LIMIT 1;
    """
    return run_query(query)


# 7. Most common food types
def common_food_types():
    query = """
    SELECT food_type, COUNT(*) AS total
    FROM food_listings
    GROUP BY food_type
    ORDER BY total DESC
    LIMIT 5;
    """
    return run_query(query)

# 8. Claims per food item
def claims_per_food():
    query = """
    SELECT f.food_name, COUNT(c.claim_id) AS total_claims
    FROM claims c
    JOIN food_listings f ON c.food_id=f.food_id
    GROUP BY f.food_name
    ORDER BY total_claims DESC;
    """
    return run_query(query)

# 9. Provider with most successful claims
def top_provider_claims():
    query = """
    SELECT p.name, COUNT(c.claim_id) AS total_claims
    FROM claims c
    JOIN food_listings f ON c.food_id=f.food_id
    JOIN providers p ON f.provider_id=p.provider_id
    WHERE c.status='completed'
    GROUP BY p.name
    ORDER BY total_claims DESC
    LIMIT 1;
    """
    return run_query(query)

# 10. Claim status distribution
def claims_status_distribution():
    query = """
    SELECT status, COUNT(*)*100.0/(SELECT COUNT(*) FROM claims) AS percentage
    FROM claims
    GROUP BY status;
    """
    return run_query(query)

# 11. Average quantity per receiver
def avg_claim_quantity():
    query = """
    SELECT r.name, AVG(f.quantity) AS avg_claim
    FROM claims c
    JOIN receivers r ON c.receiver_id=r.receiver_id
    JOIN food_listings f ON c.food_id=f.food_id
    GROUP BY r.name;
    """
    return run_query(query)

# 12. Most claimed meal type
def top_meal_type():
    query = """
    SELECT f.meal_type, COUNT(c.claim_id) AS total
    FROM claims c
    JOIN food_listings f ON c.food_id=f.food_id
    GROUP BY f.meal_type
    ORDER BY total DESC
    LIMIT 1;
    """
    return run_query(query)

# 13. Total quantity donated by each provider
def total_donated_by_provider():
    query = """
    SELECT p.name, SUM(f.quantity) AS total_donated
    FROM food_listings f
    JOIN providers p ON f.provider_id=p.provider_id
    GROUP BY p.name
    ORDER BY total_donated DESC;
    """
    return run_query(query)

# 14. Receiver city with highest claims
def receiver_city_highest_claims():
    query = """
    SELECT r.city, COUNT(c.claim_id) AS total_claims
    FROM claims c
    JOIN receivers r ON c.receiver_id=r.receiver_id
    GROUP BY r.city
    ORDER BY total_claims DESC
    LIMIT 1;
    """
    return run_query(query)

# 15. Monthly donation trends
def monthly_donation_trends():
    query = """
    SELECT DATE_FORMAT(c.timestamp, '%Y-%m') AS month, COUNT(*) AS total_claims
    FROM claims c
    GROUP BY month
    ORDER BY month;
    """
    return run_query(query)