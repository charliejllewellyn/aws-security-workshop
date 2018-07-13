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
