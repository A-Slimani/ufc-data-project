# UFC Data Project
Practice project for data engineering. 

## Todo
- Calculate more statistics
    - Percentages wins / losses etc.
    - most amount of x wins e.g. submissions 
- Display the data with a visualisation tool e.g. Power BI
- Fix so that dbt can run on airflow (currently cant)

### Low Priority
- Include other information for fighters (will need to scrape other websites)
    - Nationality
    - Location
    - Gender
- change from sqlalchemy to raw sql
    - To practice my sql skills
- Find ways to remove rendundant information
    - Change columns (weight, stance, method) to an enum
- Update the dates of the dags to reflect after an event has been finished
    - e.g. Run on sunday evenings after ufc events are finished
- Fix the error output when it finds an existing record
    - The output is too long
- update the table for weight from string to int
    - include a weight class column
- remove fighters who havent fought in the ufc 
    - For some reason they are in the ufcstats fighters db
    - Or not im not sure
- create a new scraper that scrapes only newer stuff
    - Currently scrapes everything from the beginning

## Notes
Saving table space / size with enums
- Currently the size of the fighter table is `432kb` 
- Check the all the distinct stances with command `SELECT DISTINCT(stance) FROM fighters;`
    - The stances are `Switch, Orthodox, Open Stance, Southpaw, Sideways, EmptyString???`
- Script used to convert the column into an enum

Missing one ufc event?
- Currently on a google search there is 714 events however my db only has 713
- Try to find the missing event

## Issues and resolutions
- Issue with not having a tmp folder when running scrapy with airflow
    - Real issue was airflow unable to use the URI in the .env file stored in the project folder
    - Resolved by including the line `environment={'URI':'{{ var.value.URI}}'}` in the docker operator task
    - Add the db uri link in the admin -> variables headers

