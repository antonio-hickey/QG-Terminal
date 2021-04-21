# QG-Terminal
An open source finance/trading dashboard (python web app), By defualt this project is tailored to fit my own personal needs for keeping up with financial markets. This platform is mainly python and CSS, making it very easy to customize it to suit your own desired use with little python and web knowledge.

https://i.ibb.co/Cmy092w/2021-04-21-12-48.png


# Data
All open source datasets with mining scripts to keep the datasets up to date.
  - If using linux use crontab jobs to automatically run the data mining script's in the background
     - `crontab -e`
     - `** ** * * * /usr/bin/env python3 /QG-Terminal/Apps/data/USTCurve_Miner.py`
     - ...
     - `ctrl + x`
     - `shft + Y`
     - Output:
     - `crontab: installing new crontab` Done
  - If using windows use task scheduler to automatically run data mining script's in the background

# Contact for help
email: antoniohickey99@gmial.com
