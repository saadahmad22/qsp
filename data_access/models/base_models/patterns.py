'''Stores formatting patterns

Fields
    - regex
        python regex pattern (r'') for the string
    - datetime
        format to use in datetime's formatting (strftime, strptime)
    - text
        user friendly text version of the format (e.g., MM/DD/YYYY)
'''

# datetime.date patterns
date_pattern = {"regex" : r"^((0|1)\d{1})\/(((0|1|2)\d{1})|(3(0|1)))\/(\d{4})$",
                 "datetime" : "%m/%d/%Y",
                   "text" : "MM/DD/YYYY"}
# datetime.time patterns
time_pattern = {"regex" : r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$",
                 "datetime" : "%H:%M",
                   "text" : "HH:MM"}