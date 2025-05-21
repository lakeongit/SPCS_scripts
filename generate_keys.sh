#!/bin/bash

# Script: generate_keys.sh
# Description: Generates EC key pair and outputs contents to easily copyable files.

# Instructions ###
# Save the script above as generate_keys.sh.
# Run it with: 
# chmod +x generate_keys.sh
# ./generate_keys.sh
# Open the copy_keys.txt file to copy both keys quickly.




# Step 1: Generate a new EC private key (temp)
openssl ecparam -name secp521r1 -genkey -noout -out private_key_temp.pem

# Step 2: Convert to PKCS#8 format
openssl pkcs8 -nocrypt -topk8 -in private_key_temp.pem -out private_key.pem

# Step 3: Extract and save the public key
openssl ec -in private_key.pem -pubout -out public_key.pem

# Step 4: Save easily copyable versions
echo "==== Public Key ====" > copy_keys.txt
cat public_key.pem >> copy_keys.txt

echo -e "\n==== Private Key ====" >> copy_keys.txt
cat private_key.pem >> copy_keys.txt

# Cleanup
rm private_key_temp.pem

echo "Keys generated. See 'copy_keys.txt' for quick copy-paste."
