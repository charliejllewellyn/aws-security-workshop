# Analysis

Analaysis is a vital part in the security lifecycle, once we have detected and responded to a security event we need to diagnose exactly what happened.

In this module we will look at some techniques to start investigtaing the issues that could have led up to compromise of the server. We'll be using [Amazon CloudWatch](https://aws.amazon.com/cloudwatch) and [AWS CloudTrail](https://aws.amazon.com/cloudtrail/).

## CloudWatch

CloudWatch is a service that allows us to capture logs, metrics and events which allow us to analysis the state across our systems.

In this scenario we were alerted that one of our servers was making callouts to a know bad actor defined on a custom threat list. If you study the CloudFormation template we used to deploy the application you'll notice that the servers were configured with the [CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-on-first-instance.html) which captured all commands issued on the server and passed them to CloudWatch. This same agent can be used to capture any system or application logs on the server to give us visibilty into the activity on the server.

It is also possible to capture [custom metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html) from your application to get greater visibilty into bespoke applications you may be running.

<details>
<summary><strong>Review logs (expand for details)</strong></summary><p>

1. From the AWS Console open the CloudWatch dashboard

1. Click **Logs** from the left hand menu

1. From the notification email you recieved alerting you to the event you will be able to obtain the instance ID, e.g. "i-036c394ba8fe4cd39"

1. In the CloudWatch dashboard enter the search instance ID
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/CloudWatch_log_filter.png)

1. Click into the log group and then into the log stream and you will see a list of all shell commands executed on the server.
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/CloudWatch_log.png)

1. The CloudFormation also enables VPC flow logs when setting up the infrastructure which allows us to query the packets sent and recieved by the server. Click on **Logs** again in the left hand menu and enter **securityGroupVpcFlowLogs** in the filter
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/CloudWatch_flowlog_filter.png)

1. Click into the log group and click **Search Log Group**

1. Enter **209.85.202.94** in the filter to return a list of packets matching the IP
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/CloudWatch_flowlog.png)

1. Click the **eni-xxxxxxxxxx** to the right under **Show in stream**

1. This returns the highlighted packet in context of the rest of the stream and just above we can see the IP address of the user that connected shortly before the command was executed.
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/CloudWatch_flowlog.png)

</details>

Whilst this is a forced example it shows how system and infrastructure logs can be easily aggregated to start building a picture of exactly what was going on around the time of the event. It is also possible to stream the logs to other tools like splunk or (Elasticsearch)[https://aws.amazon.com/elasticsearch-service/] to visulaise the data.

## CloudTrail

CloudTrail allows us to record and query all API requests made to the AWS Service APIs. In this case we are going to look at any events recorded that might give insight into actions taken against our instances.

<details>
<summary><strong>Query CloudTrail logs (expand for details)</strong></summary><p>

1. From the AWS Console open the CloudTrail dashboard

1. From the left hand menu select **Event History**

1. In the filter dropdown select **Resource Name**

1. In the Enter lookup value enter the resource id of the instance obtained above, e.g. "i-036c394ba8fe4cd39"

1. This returns a list of all API actions listed against the resource.
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/CloudTrail_event_filtering.png)

</details>

## Athena

Athena is an AWS service that allows us to query data stored in S3. CloudTrail logs data to S3 which means we can configure a schema that allows us to write more complex queries to interigate the data.

<details>
<summary><strong>Configure Athena to query CloudTrail logs (expand for details)</strong></summary><p>

1. From the AWS Console open the CloudTrail dashboard

1. From the left hand menu select **Event History**

1. Click **Run advanced queries in Amazon Athena**

1. Select the **securityimmersionday-s3Bucket-xxxxxxxxxx** as the Storage Location

1. Click **Create Table**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/Athena_table.png)

1. Click **Go to Athena**

1. Click **Get Started**

1. In the Query window enter the following updating the query with your table name and your instance id

```
WITH newdata AS (
  select 
    eventtime, 
    resources as resource, 
    useridentity,
    eventname,
    requestparameters
    
  from YOUR_ATHENA_TABLE_NAME where cardinality(resources) >= 1
  )
  select eventtime, eventname, useridentity, requestparameters, resource from newdata where resource[1].arn like '%YOUR_INSTANCE_ID%'
```

1. This will return the actions taken against the instance as well as the paraemeters of the calls
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/analysis/Athena_query.png)

</details>

# Summary

This concludes the workshop. We have learnt about different AWS products that can support various stages of the security lifecycle.

The suggested next steps would be review the risks that have been highlighted during the security review of the platform and start thinking about how the products and methodologies we have used during the workshop could be used to control the risks that are highlighted.
