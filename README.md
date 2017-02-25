# blight-compliance

Starter scripts for the [https://inclass.kaggle.com/c/detroit-blight-ticket-compliance](MDST Blight Ticket Compliance Challenge)

### Instructions

- Install dependencies: `pip install numpy pandas sklearn`
- Clone the repo: `git clone git@github.com:MichiganDataScienceTeam/blight-compliance.git`

#### To run `starter_script.py`

- Make a data directory: `mkdir data`
- Download `train.csv` and `test.csv` from the Kaggle page into `data`
- Run the script: `python starter_script.py`
- Submit the benchmark submission: `data/submission_RF_R.csv`

#### To run `starter_heatmap.py`

- Make a data directory: `mkdir data`
- Download `addresses.csv` and `latlons.csv` from the Kaggle page into `data`
- Run the script: `python starter_heatmap.py`
- Open in your browser `data/blight_tickets.html` 
