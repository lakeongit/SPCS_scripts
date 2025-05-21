from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import json

# -- Snowflake connection parameters --
connection_parameters = {
    "account": "<your_account>",
    "user": "<your_user>",
    "password": "<your_password>",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "MY_DATABASE",
    "schema": "PUBLIC"
}

session = Session.builder.configs(connection_parameters).create()

# 1. Get current user
current_user = session.sql("SELECT CURRENT_USER()").collect()[0][0]
print(f"Current User: {current_user}")

# 2. Get current role and privileges
current_role = session.sql("SELECT CURRENT_ROLE()").collect()[0][0]
print(f"Current Role: {current_role}")

role_grants = session.sql(f"SHOW GRANTS TO USER {current_user}").collect()
print("Grants to user:")
for row in role_grants:
    print(row)

# 3. Get network policies
network_policies = session.sql("SHOW NETWORK POLICIES").collect()
print("Network Policies:")
for policy in network_policies:
    print(policy)

# 4. Get default warehouse for current user
user_info = session.sql(f"SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.USERS WHERE NAME = '{current_user}'").collect()
if user_info:
    print("Default Warehouse:", user_info[0]["DEFAULT_WAREHOUSE"])
else:
    print("No user info found in ACCOUNT_USAGE view.")

# 5. Create and apply a masking policy
# Replace with actual table and column
table_name = "MY_TABLE"
column_name = "EMAIL"

# Create masking policy
session.sql("""
    CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING) 
    RETURNS STRING ->
        CASE 
            WHEN CURRENT_ROLE() IN ('FULL_ACCESS_ROLE') THEN val
            ELSE CONCAT('****@', SPLIT_PART(val, '@', 2))
        END
""").collect()
print("Masking policy 'mask_email' created.")

# Apply masking policy to a column
session.sql(f"""
    ALTER TABLE {table_name} 
    MODIFY COLUMN {column_name} 
    SET MASKING POLICY mask_email
""").collect()
print(f"Masking policy applied to {table_name}.{column_name}.")

session.close()
