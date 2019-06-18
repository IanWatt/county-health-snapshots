acs_url = "https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/5_year_by_state/Texas_All_Geographies_Not_Tracts_Block_Groups.zip"


###########
# Sources #
###########

# ACS
acs: data/acs.zip
	unzip $^ -d data/acs

# Download the summary file. It's big (300mb), so grab some coffee!
data/acs.zip:
	curl $(acs_url) -o $@

# setup
setup:
	rm -rf data && mkdir data