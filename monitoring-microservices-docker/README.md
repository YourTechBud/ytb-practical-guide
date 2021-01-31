# Monitoring Microservices in Docker using Prometheus and Grafana

This app uses the _open source versions_ of the following tools:
- [Prometheus](https://prometheus.io/) as a metric aggregator.
- [Grafana](https://grafana.com/) for visualisation.
- [HA Proxy](https://www.haproxy.com/) as a reverse proxy.
- [cAdvisor](https://github.com/google/cadvisor) to collect container runtime metrics.

> Here's a link to the YouTube video explaining this setup in greater detail - [https://youtu.be/jUhacrwEwDk](https://youtu.be/jUhacrwEwDk)

## Prerequisites
 
- You'll need to have [Docker](https://docs.docker.com/engine/install/) installed. This project uses `docker-compose` to bring the backend components up.

> I was having some issues with making things work when using Docker Desktop using WSL2 on Windows. Not sure what it is.  
> So if you are on Mac or Windows using Docker Desktop, your best bet is to set up an environment on VirtualBox or get yourself a Linux VM on the Cloud like I have.

## How to start the app

- Clone this repo and `cd` into the `monitoring-microservices-docker` directory.
- Simply run `docker-compose -p monitoring up -d` to bring up the monitoring stack along with the services to be monitored. 
- Once all the containers are up, Open `http://IP_ADDRESS:3000` in a browser window to load Grafana.
- Add a Prometheus data source. The Prometheus url is `http://prometheus:9090`. Hit `Save & Test` to add the data source
- Import the dashboard by uploading the `grafana-dashbord.json` file.
- Finally put some load by hitting the `http://IP_ADDRESS:11000/add/1/2` and `https://IP_ADDRESS:11000/greeting/YourTechBud` endpoints.