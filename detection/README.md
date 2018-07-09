## Detection

Whilst prevention is a vital part of the security within AWS it also has the potential to impede good work, slowing down delivering and frustrating users. Security teams need to be aware of when prevention is appropriate and when detection may be a better methods to track security across an organisation.

In this module we will explore practices and products to detect changes and security threats and how to generate alerts on that basis. In this module we will use [Amazon Simple Notification Service](https://aws.amazon.com/sns/), [Amazon GuardDuty](https://aws.amazon.com/guardduty/), [AWS CloudTrail](https://aws.amazon.com/cloudtrail/), [AWS Config](https://aws.amazon.com/config/).

## Notification

Since a large part of detection is notifying systems and teams about events we'll start by setting up a notification topic.

<details>
<summary><strong>Setup Amazon SNS</strong></summary><p>

1. From the AWS Console open the SNS dashboard.

1. Click **Create Topic**
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/SNS_topic.png)

1. For the **Topic Name** enter **SecurityWorkshopEvents** and click **Create Topic**

1. Click **Create subscription**

1. Change the **protocol** to **Email** and enter your email address, click **Create subscription**

1. Check your email and click the confirmation to complete the topic setup

</details>

## Using AWS Config Rules and and AWS SNS to detect configuration changes

In this scenario we are going to use one of the AWS supplied configuration rules to monitor Security Group rule configuration; however, it is possible to build your own customer rules.

<details>
<summary><strong>Setup AWS Config</strong></summary><p>

1. In the AWS Console open the Config service, ensuring that you have selected a region where the items you wish to monitor are present

1. Click **Get started**
    ![get started](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-get-started.png)

1. The defaults are useful here but we shall add in monitoring of Identity and Access Management resources (IAM)

1. Under **Resource types to record** check the tick box beside **Include global resources (e.g. AWS IAM resource)**
    ![config settings](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-settings.png)

1. We let Config create the Amazon S3 bucket for us but add in Amazon SNS notification of changes

1. Check the tick box beside **Stream configuration changes and notifications to an Amazon SNS topic.**

1. Choose **Choose a topic from your account** and select the SNS topic create above **SecurityWorkshopEvents**.

1. Let Config create a role for you. Choose a name which matches the naming policy for your organisation

    ![config role](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-role.png)

1. Click **Next**

1. We will not choose any default rules to apply yet, click **Next**

1. On the **Review** screen check that you are satisfied and press **Confirm**.
    ![config confirm](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-confirm.png)

1. After a short period of time, Config will be setup and you will be brought back to the dashboard
    ![config dashboard](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-dash.png)

</p></details>

<details>
<summary><strong>Create a Config Rule in AWS Config (expand for details)</strong></summary><p>

1. In the AWS Console open the Config service, ensuring that you have selected the region where the items you wish to monitor are present

1. Select **Rules** from the left hand menu

1. Press the **Add rule** button ![add rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/add-rule.png)

1. Type **security group** in the search field and click the **restricted-common-ports** card which appears
    ![restrict ports](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/restricted-common-ports.png)

1. Update the **Name** to identify it as part of the workshop, **security-workshop-restricted-common-ports**
    ![name rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-name.png)

1. We shall leave the Trigger section as it is in this case. For creating custom rules where a smaller sub-section of a particular resource should be monitored, or where a periodic check is desired then these [options should be revisited](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html).
AWS have [a repository of custom rules here](https://github.com/awslabs/aws-config-rules).

1. Under **Scope of changes**, select **Tags** and enter **ProjectName** as the **Tag Key** and **Securityworkshop** as the **Tag Value**. This will restrict the rule to only run against the resources we have created in the workshop.
    ![trigger config](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-trigger-config.png)

1. Under **Rule parameters** we want to change **blockedPort3** from 3389 to **80**. The Rule parameters in this case are the TCP ports which should not be permitted. If these rules are added to a security group then the resource will be in breach of compliance.
    ![ports to avoid](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-port-config.png)

1. Click **Save**.

</p></details>

<details>
<summary><strong>Viewing the compliance state (expand for details)</strong></summary><p>

You will now see the Rules section, with the rule you have just created added in and showing a Compliance state of **Evaluating...**.

Evaluation will take a couple of minutes and the UI will update to reflect the new state of **Compliant**. You can click the **Refresh** icon if you do not see the page update.

To see the state of the Security Groups which are being monitored for compliance, click the rule name. In our example here that is **security-workshop-restricted-common-ports**.

![Noncompliant rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_compliant.png)

</p></details>

### Testing the compliance state

We are now going to force a compliance breach by updating the rule to allow port 80 through to our application.

<details>
<summary><strong>Change a security group (expand for details)</strong></summary><p>

1. In the AWS Console open the EC2 service and select **Security Groups** from the left hand menu

1. Place a check next to the **Group ID** for the **securityImmersionDay-loadBalancer**, for example
    ![sg list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_sg_amend.png)

1. Click **Inbound** in the ribbon below

1. Click **Edit** then click **Add Rule**

1. Click **Add rule** and select **HTTP** from the dropdown. 

1. Click **Save**

</details>
<details>
<summary><strong>Check the Compliance breach (expand for details)</strong></summary>

1. In the AWS Console open the Config Service

1. After a short period of time the Compliance state of the **security-workshop-restricted-common-ports** rule will change to **Noncompliant**
    ![sg rule list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_non-compliant.png)

1. Click on the **security-workshop-restricted-common-ports** rule name

1. In the **Resources Evaluated** section, click on the Security Group ID in the **Config Timeline** column for the now **Noncompliant** loadbalancer security group rule

1. Notice the timeline which shows the changes made to the Security Group
    ![sg timeline](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_sg_timeline.png)

1. Click on the **Change** link below the most recent change and note that it reflects the change we made earlier
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_sg_change.png)

</details>
 
## GuardDuty

In this section we're going to review the results we get from GuardDuty. In order to start processing events with GuardDuty we need to enable the service.

<details>
<summary><strong>Setup AWS GuardDuty (expand for details)</strong></summary>

1. In the AWS Console open the GuardDuty Service

1. Select **Get Started** and then **Enable GuardDuty**.
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/GuardDuty.png)

1. We are now going to create a fake threat list for GuardDuty so we can force our hosts to generate events. To do this we need to change the permissions on the threat list we uploaded previously.

```
aws s3api put-object-acl --bucket YOUR_BUCKET_NAME --key securityThreatList.txt --acl public-read
```

1. In the GuardDuty console on the left menu select **Lists** 

1. Select **Add a threat list**, enter a name of **SecurityWorkshop**, enter the URL formated as follows

```
https://s3.amazonaws.com/YOUR_BUCKET_NAME/securityThreatList.txt
```

select **Plaintext** for the **Format**, finally check **I agree** and click **Add List**
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/GuardDuty_list_add.png)

1. Place a check in the **Activate** box to enable the list
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/GuardDuty_list_activate.png)

</details>

## CloudWatch

Whilst GuardDuty is useful we really want to be in a position to notify our security team or systems rather than checking an interface. To aid with this we'll setup a CloudWatch event to notify the SNS topic we created earlier to alert the security team.

<details>
<summary><strong>Generate events (expand for details)</strong></summary>

1. From the EC2 console open the CloudWatch dashboard.

1. Click on **Rules** in the left menu

1. Click **Create Rule**

1. Click **Edit** in the **Event Pattern Preview** and enter the JSON below

```
{
  "source": [
    "aws.guardduty"
  ],
  "detail-type": [
    "GuardDuty Finding"
  ],
  "detail": {
    "type": [
      "Backdoor:EC2/C&CActivity.B!DNS"
    ]
  }
}
```

Click **Save**

1. On the right hand side click **Add target**

1. Change the dropdown from **Lambda Function** to **SNS topic**

1. Enter the SNS from earlier **SecurityWorkshopEvents**

1. Click **Configure Details**, enter the name **SecurityWorkshopEventRule** and click **Create Rule**

</details>

## Test detection

<details>
<summary><strong>Generate events to trigger GuardDuty (expand for details)</strong></summary>

1. We are now going logon to one of the application instances to generate some alerts. To do this we need the public address of one of the instances. From the AWS console open the EC2 dashboard. In the left hand menu select **Instances**

1. In the search enter **ProjectName** and select the tag in the value select **securityImmersionDay**. 

1. Check one of the hosts and from the bottom window copy the **Public DNS (IPv4)**
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/GuardDuty_ec2_host.png)

1. Open an SSH terminal and run

```
ssh -A -i LOCATION_OF_PRIVATE_KEYPAIR ec2-user@YOUR_EC@_PUBLIC_DNS
```

1. Once logged on run the following command

```
dig GuardDutyC2ActivityB.com any
curl -s http://com.minergate.pool/dkjdjkjdlsajdkljalsskajdksakjdksajkllalkdjsalkjdsalkjdlkasj  > /dev/null &
curl -s http://xdn-xmr.pool.minergate.com/dhdhjkhdjkhdjkhajkhdjskahhjkhjkahdsjkakjasdhkjahdjk  > /dev/null &
curl -s http://209.85.202.94 > /dev/null &
```

This will access the site we have defined as a threat.

1. Go back to the GuardDuty console and select **Findings** from the left menu. After about 5 minutes you should see notifications that the bad host was accessed.
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/GuardDuty_finding.png)

</details>
