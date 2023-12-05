# Ronen Dotan - HiredScore Assignment

Notes:

1. The match config object allows a dynamic defenition of search mechanisem to be able to match records from the candidates file to the secondary file.
2. It can be extended, imported from another module or whatever.
3. It defines:
    * an id of each matching mechanisem algorithm,.
    * A key from the candidate (also support a function to extract from the several data points from a candidate)
    * A key from the secondary data source (also support functions)
    * A compare function for both keys. - if not define, equel is used
    * A result_function - which data field should we use if a match was found? if not defined use secondary_data_item["Linkedin"]
    * Priority of the matching config 
4. When we try to match - we always match all the candidates with against all the data in the secondary file - even the matched ones.
5. The algorith will use the priority to first match configs with higher priority.

6. Also, we search for linkedin url in the candidte resume.
7. this field can also particepate in the matching ,mechanisem. in the current configuration - we just take it if we found in the cv. but we can do whatever with that.
