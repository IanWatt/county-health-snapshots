all: data/final.csv

#################
# File Assemply #
#################

data/final.csv: data/acs.txt
	poetry run python processors/assemble.py

###########
# Sources #
###########

# ACS
data/acs.txt: input/field_config.yaml
	poetry run python processors/acs.py

# setup
setup:
	rm -rf data && mkdir data