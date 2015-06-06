# Princeton Energy

Welcome to the Princeton Energy Repository

## Goals
Using data from PSEG, EIA, EPA, NJ Clean Energy Program and other agencies, develop technology and visualizations that will analyze and display Princeton’s greenhouse gas emissions over time. Create simple quantitative comparisons that will help residents, businesses and other community members understand the impact their efforts to reduce energy consumption can have on Princeton’s greenhouse gas emissions as a whole.


## Dataset Information
Data from 2009 for Gas and Electric usage in Princeton Township and Boro, categorized by Industrial, Commercial, and Residential.

-  Industrial category is not "true" industrial and can be considered Commercial
- Classification of Industrial is based on SIC code
- Includes Princeton University property in the Commercial category
- kWh & Therms are billing information and not actual usage. In the vast majority of cases they are one and the same but they will be instances either because of an estimated bill or a corrected bill where they can be different. This explains negative values in kWh & Therms.
- PSEG can provide data in excel on a Quarterly basis
- No limitations on use of data as it is in aggregate
- Meter to resident or commercial is roughly 1:1
- Data needs to be weather normalized using heating and cooling degree data for the area
- Princeton Hospital closed and moved to Plainsboro on May 23rd 2012 so likely explains drop in Borough Commercial usage
- Princeton Township and Borough consolidated into the Princeton Municipality on January 1st, 2013 but PSEG still records usage separately
- PSEG maintains some streetlights in Princeton but not all. It needs to be determined if the streetlight data is only PSEG owned & maintained. The remaining streetlights are owned and maintained by the Municipality and included in their bill


## Ideas for Data Usage

- Weather normalize data to determine if usage is increasing or decreasing on factors other than weather <a href="http://academic.udayton.edu/kissock/http/Weather/">
http://academic.udayton.edu/kissock/http/Weather/ </a>
- Determine the Greenhouse Gas emissions resulting from the usage data using PSEG energy source data or other proxy
- Create a tool that will show how energy efficiency or conservation measures in Princeton could impact the overall consumption in terms of easier to understand equivalencies <a href ="http://www.epa.gov/cleanenergy/energy-resources/calculator.html"> http://www.epa.gov/cleanenergy/energy-resources/calculator.html </a>

Additional resources:
- EIA (U.S. Energy Information Administration) state energy consumption data
- EPA (Environmental Protection Agency) Greenhouse Gas Equivalencies Calculator
- Weather Depot <a href ="http://www.weatherdatadepot.com/"> http://www.weatherdatadepot.com/ </a> for getting HDD {Heating Degree Days} and CDD (Cooling Degree Days)

## Usage Notes
- Download or fork here to start contributing
- If there are any comments, issues, or suggestions please open an Issue through the tab on the right

## Cleaned Dataset
An attempt to clean the Energy dataset is underway and the first draft is available under <b> cleanDataset </b> in .xls format.
Please make no lossy modifications, add computed columns.

## Original Dataset
The original dataset is located under <b> originalDataset </b>

## Ruby on Rails Commands
You will need to use these commands to run the Application in Ruby on Rails...

- Move in to the 'greengraph' directory
 ```
cd greengraph
```
- Migrate the Development Database (Make it current)
 ```
rake db:migrate RAILS_ENV=development
```
- Seed the newly migrated database (from the input CSV files)
 ```
rake db:seed
```
- Start the Rails Server - this is accessible on http://localhost:3000, if you have used the Rails default settings
 ```
rails s
```
