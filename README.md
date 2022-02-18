# siy
"See ee" - A turnkey solution for Data Engineering, that allows an organization to quickly get data processing, with long term maintenance
and augmentation being done with just domain experts and data scientist.  Unlike many solutions, this one can integrate with 
any technology that can be triggered by a Docker container.

Siy means "si y", or Spanish for "yes and".  The basic philosophy of this system is that data should be placed in a 
central lake, processed there, and the results returned to that same lake in a new table/object.  This allows modification and evolution of 
data pipelines over time, instead of having to constantly reconfigure and redevelop data pipelines that are used to 
feed ML and other processes.  Meanwhile, making this data available to the outside world is done easily through configurable Destinations,
which can automatically generate such common methods as REST API, GraphQL, Snowflake, and Looker dashboards out of the box.

This allows modification and evolution of data pipelines over time, instead of having to constantly reconfigure and redevelop data pipelines that are used to feed MLP and other processes.
![Yes, and_ model - User Control](https://user-images.githubusercontent.com/3457836/154697220-12359616-d198-41a2-bb10-ace448415deb.png)
![Yes, and_ model - Basic Data Flow](https://user-images.githubusercontent.com/3457836/154697228-46adb2a3-2265-4d36-b8cd-f9ae5d8dae1a.png)


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
- Custom Docker Image - arbitrary code that runs in a docker image.  The user will need to tell the system which tables will be created here

