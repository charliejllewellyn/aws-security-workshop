## Detection

Whilst prevention is a vital part of the security within AWS prevention also has the potential to impede good work slowing down delivering and frustrating users. Security teams need to be aware of when prevention is appropriate and when detection may be a better methods to track security across an organisation.

In this module we will explore practices and products to detect changes and security threats and how rto generate alerts on that basis. In this module we will use [Amazon GuardDuty](https://aws.amazon.com/guardduty/), [AWS CloudTrail](https://aws.amazon.com/cloudtrail/), [AWS Config](https://aws.amazon.com/config/).

## Configuration State

A good practice is to monitor the state change of configuration items (CI). This is helpful for change management, fault diagnosis and resolution, training, compliance and of course incident response.

### Using AWS Config Rules and and AWS SNS to detect configuration changes

In this scenario we are going to use one of the AWS supplied configuration rules to monitor Security Group rule configuration.

<details>
<summary><strong>Setup AWS Config</strong></summary><p>

1. In the AWS Console open the Config service, ensuring that you have selected a region where the items you wish to monitor are present

1. Press **Get started**
    ![get started](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-get-started.png)

1. The defaults are useful here but we shall add in monitoring of Identity and Access Management resources (IAM)

1. Under **Resource types to record** check the tick box beside **Include global resources (e.g. AWS IAM resource)**
    ![config settings](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-settings.png)

1. We shall let Config create the Amazon S3 bucket for us but we shall add in Amazon SNS notification of changes

1. Check the tick box beside **Stream configuration changes and notifications to an Amazon SNS topic.**

1. Let Config create the topic and choose a name which matches the naming policy for your organisation

    ![config topic](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-topic.png)

1. Let Config create a role for you. Choose a name which matches the naming policy for your organisation

    ![config role](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-role.png)

1. Press **Next**

1. We will not choose any default rules to apply yet, so press **Next**

1. On the **Review** screen check that you are satisfied and press **Confirm** if so. If not, press **Previous** to go back a screen and make changes to your satisfaction.
    ![config confirm](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-confirm.png)

1. After a short period of time, Config will be setup and you will be brought to the dashboard
    ![config dashboard](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/config-dash.png)

</p></details>

<details>
<summary><strong>Create a Config Rule in AWS Config (expand for details)</strong></summary><p>

1. In the AWS Console open the Config service, ensuring that you have selected a region where the items you wish to monitor are present

1. Select **Rules** from the left hand menu

1. Press the **Add rule** button ![add rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/add-rule.png)

1. Type **security group** in the search field and click the **restricted-common-ports** boxout which appears
    ![restrict ports](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/restricted-common-ports.png)

1. Give the rule a name which fits the naming pattern in use at your organisation and a helpful description.
    ![name rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-name.png)

1. We shall leave the Trigger section as it is in this case. For creating custom rules where a smaller sub-section of a particular resource should be monitored, or where a periodic check is desired then these [options should be revisited].(https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html)
AWS have [a repository of custom rules here].(https://github.com/awslabs/aws-config-rules)
    ![trigger config](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-trigger-config.png)

1. The Rule parameters in this case are the TCP ports which should not be permitted. If these rules are added to a security group then the resource will be in breach of compliance.
    ![ports to avoid](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-port-config.png)


1. Click **Save**.

</p></details>

<details>
<summary><strong>Viewing the compliance state (expand for details)</strong></summary><p>

You will now see the Rules section once more, with the rule you have just created added in and showing a Compliance state of **Evaluating...**.

![rule evaluation](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-evaluating.png)

Evaluation will take a couple of minutes and the UI will update to reflect the new state of **Compliant**. You can click the **Refresh** icon if you do not see the page update.

To see the state of the Security Groups which are being monitored for compliance, click the rule name. In our example here that is **myOrg-security-groups-restrict-common-ports**.

![compliant rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-compliant.png)

You will now see that we have two groups in compliance.
![compliant groups](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-detail-compliant.png)

</p></details>

### Testing the compliance state

We are now going to make one of our resources breach compliance.

<details>
<summary><strong>Change a security group (expand for details)</strong></summary><p>

1. In the AWS Console open the EC2 service and select **Security Groups** from the left hand menu

1. Place a check next to the **Group ID** for the Security Group you want to update
    ![sg list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/security-group-list.png)

1. Click **Inbound** in the ribbon below

1. Click **Edit** then click **Add Rule**

1. Use the following rule configuration:
  * **Type** - Custom TCP
  * **Protocol** - TCP
  * **Port Range** - 3389
  * **Source** Anywhere
  * **Description** RDesktop for everything

![security group rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/security-group-rule.png)

1. Click **Save**

</details>
<details>
<summary><strong>Check the Compliance breach (expand for details)</strong></summary>

1. In the AWS Console open the Config Service

1. After a short period of time the Compliance state of the **myOrg-security-groups-restrict-common-ports** rule will change to **1 noncompliant resource(s)**
    ![sg rule list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/non-compliant-rule-list.png)

1. Click on the **myOrg-security-groups-restrict-common-ports** rule name

1. In the **Resources Evaluated** section, click on the Security Group ID in the **Config Timeline** column for the **NonCompliant** resource
    ![sg rule shortlist](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/non-compliant-rule-shortlist.png)

1. Notice the timeline which shows the changes made to the Security Group
    ![sg timeline](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/sg-rule-timeline.png)

1. Click on the **Change** link below the most recent change and note that it reflects the change we made earlier
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/sg-rule-change.png)

</details>
 
## GuardDuty

In order to start processing events with GuardDuty we need to enable the service.

