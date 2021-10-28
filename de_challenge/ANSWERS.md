# Answers
---
### Question 1
```
The claims data comes with duplicates and NDCs are messy.
Please write a script to de- deduplicate the data
(Note:rows identical to each other in every single column is considered duplicate)
and clean the NDC into standard format (11 digits and matchable
to the format in tab ndc)
```
###Solution:
The test solution for processing the data and get the resultant patients is provided in [question1.py](https://github.com/devdasgupta/DE_Challenge/blob/initial-setup/de_challenge/question1.py)

* The de-duplication logic after reading the data into pandas dataframe is provided [here](https://github.com/devdasgupta/DE_Challenge/blob/01e01c527a31dbaea83a57fed343e4e877a5eab2/de_challenge/question1.py#L15)
* Cleaning/Normalizing the NDC records is provided [here](https://github.com/devdasgupta/DE_Challenge/blob/01e01c527a31dbaea83a57fed343e4e877a5eab2/de_challenge/question1.py#L86)
* The solution also provides the final patients list as a CSV format and is saved in the location [output_data](https://github.com/devdasgupta/DE_Challenge/blob/initial-setup/de_challenge/output_data/patients.csv)


### Question 2
```
In production, we deal with data at scale ingested from various data sources.
How would you go about designing a testing framework to ensure that this data
is clean after being processed? Please describe your plan as granular and
operation-able as you can. Feel free to start high-level, zoom into one data
field, e.g. NDC, and flesh it out to show how you would design it, using it as
an example.
```
###Solution:
While dealing with production and using a large scale data my first assumption is that we won't be getting the data in excel.
Instead these would be varied data coming from various sources with varied data format.
For diving into the solution I propose the following flow for the data ingestion. The QA framework strategy will be applied in each of these layer to ensure data quality.

####Data Flow design
