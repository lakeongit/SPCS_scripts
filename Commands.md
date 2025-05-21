#Replace your_table_name and email_address with actual table and column names.
#Make sure the role executing these queries has appropriate permissions (e.g., ACCOUNTADMIN or SECURITYADMIN for masking/network policies).
#Use SNOWFLAKE.ACCOUNT_USAGE views or INFORMATION_SCHEMA as needed depending on your role’s access.




-- 1. Current user
SELECT CURRENT_USER();

-- 2. Current role and granted privileges
-- Current Role
SELECT CURRENT_ROLE();

-- All Roles Granted to Current User
SHOW GRANTS TO USER CURRENT_USER();

-- 3. Network rules and policies
-- List all network policies
SHOW NETWORK POLICIES;

-- To view the network policy assigned to the current user or account:
SELECT SYSTEM$GET_ACCOUNT_POLICY();

-- 4. Default warehouse for the current user
-- You can retrieve the user's default warehouse setting
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.USERS 
WHERE NAME = CURRENT_USER();

-- 5. Setup masking policy (example: mask email address)
-- Create masking policy
CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING) 
RETURNS STRING ->
  CASE 
    WHEN CURRENT_ROLE() IN ('FULL_ACCESS_ROLE') THEN val
    ELSE CONCAT('****@', SPLIT_PART(val, '@', 2))
  END;

-- Example: Apply the masking policy to a column
ALTER TABLE your_table_name 
MODIFY COLUMN email_address 
SET MASKING POLICY mask_email;
