# UFC Data Project
Practice project for data engineering

## Todo
- Setup dbt
- Calculate more statistics
    - Percentages wins / losses etc.


### Low Priority
- Include other information for fighters
    - Nationality
    - Location
    - Gender
- change from sqlalchemy to raw sql
- Find ways to remove rendundant information
    - Change columns (weight, stance) to an enum
- Update the dates of the dags to reflect after an event has been finished
    - e.g. Run on sunday evenings
- Fix the error output when it finds an existing record
    - The output is too long
- update the table for weight from string to int
    - include a weight class column
- remove fighters who havent fought in the ufc
    - For some reason they are in the ufcstats fighters db