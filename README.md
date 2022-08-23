# sos_otel_cisco_ucs

To run this application in standalone mode.  Simply update the .yaml config files in the ucs-api directory and run "python runner.py" from the ucs-api directory. 


The runner feil pulls in a class from the main.py file.  





Install Docker Compose

change token values in config files. 

In Project root run:  docker-compose build

In Project root run:  docker-compose up -d



This will Launch 2 containers (UCS API Scraper and opentelemtry collector)


To See Logs for these containers, In Project root run:  docker-compose logs
