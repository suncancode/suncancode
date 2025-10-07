# Practice with dictionary for mapping

# Create a dictionary with country code mappings
country_codes = {
    "AU": "Australia",
    "US": "United States",
    "UK": "United Kingdom",
    "JP": "Japan"
}

# Access and print mapped values
print("Full name for AU:", country_codes["AU"])
print("Full name for JP:", country_codes["JP"])

# Update an existing value
country_codes["UK"] = "United Kingdom of Great Britain"
print("Updated country code:", country_codes)
# Output: {'AU': 'Australia', 'US': 'United States', 'UK': 'United Kingdom of Great Britain', 'JP': 'Japan'}

# Add a new mapping
country_codes["CN"] = "China"
print("Added new mapping:", country_codes)  # Output: {'AU': 'Australia', 'US': 'United States', 'UK': 'United Kingdom of Great Britain', 'JP': 'Japan', 'CN': 'China'}