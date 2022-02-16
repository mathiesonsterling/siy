# siy
A system for quickly creating data pipelines\

Siy means "si y", or Spanish for "yes and".  The basic philosoophy of this system is that data should be placed in a central lake, processed there, and the results returned to that same lake.  This allows modification and evolution of data pipelines over time, instead of having to constantly reconfigure and redevelop data pipelines that are used to feed MLP and other processes.

#Usage
## Platform choice
You'll need to pick out your cloud provider, sources, and the means of delivering data to your customer (Destination)

## Expected infrastructure
### Kubernetes
Some form of Kubernetes, usually running in the cloud (GKE)

### Orchestrator
#### Airflow
This uses Apache Airflow to orchestrate all pipelines.  Simple to understand, can become a bottleneck with large
amounts of interrelated pipelines.  Recommend that you setup Airflow on the Kubernetes cluster you're
going to use for execution.  Use the AirflowWorkflowFactory for this.

#### Kubernetes cron jobs
This uses coordinated cron jobs to remove airflow.  It has eventual consistency.

### Data Lake
- GCP BigQuery
- AWS Snowflake

### Sources
Sources are any mechanism which creates or brings in data.  Extending these is possible as well.
- Airbytes - https://docs.airbyte.com/.  Usually used to pull data from the outside world to the data lake
- Meltano
- dbt - https://www.getdbt.com/.  Used to enable data analysts and scientists to create new models with SQL
- Spark - https://spark.apache.org/

