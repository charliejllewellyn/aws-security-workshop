## Detection

Whilst prevention is a vital part of the security within AWS prevention also has the potential to impede good work slowing down delivering and frustrating users. Security teams need to be aware of when prevention is appropriate and when detection may be a better methods to track security across an organisation.

In this module we will explore practices and products to detect changes and security threats and how rto generate alerts on that basis. In this module we will use [Amazon GuardDuty](https://aws.amazon.com/guardduty/), [AWS CloudTrail](https://aws.amazon.com/cloudtrail/), [AWS Config](https://aws.amazon.com/config/).

## Configuration State

A good practice is to monitor the state change of configuration items (CI). This is helpful for change management, fault diagnosis and resolution, training, compliance and of course incident response.

### Using AWS Config Rules and and AWS SNS to detect configuration changes

In this scenario we are going to use one of the AWS supplied configuration rules to monitor Security Group rule configuration.

<details>
<summary><strong>Setup AWS Config</strong></summary><p>

PUT INITIAL CONFIG SETUP IN HERE

</p></details>

<details>
<summary><strong>Create a Config Rule in AWS Config (expand for details)</strong></summary><p>

1. In the AWS Console open the Config service, ensuring that you have selected a region where the items you wish to monitor are present

1. Select **Rules** from the left hand menu

1. Press the **Add rule** button ![add rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/add-rule.png)

1. Type **security group** in the search field and click the **restricted-common-ports** boxout which appears
    ![restrict ports](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/restricted-common-ports.png)

1. Update the **Name** to identify it as part of the workshop, **security-workshop-restricted-common-ports**
    ![name rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-name.png)

1. Under **Scope of changes**, select **Tags** and enter **ProjectName** as the **Tag Key** and **Securityworkshop** as the **Tag Value**. This will restrict the rule to only run against the resources we have created in the workshop.

1. We shall leave the Trigger section as it is in this case. For creating custom rules where a smaller sub-section of a particular resource should be monitored, or where a periodic check is desired then these [options should be revisited].(https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html)
AWS have [a repository of custom rules here].(https://github.com/awslabs/aws-config-rules)
    ![trigger config](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-trigger-config.png)

1. Under **Rule parameters** we want to change **blockedPort3** from 3389 to **80**. The Rule parameters in this case are the TCP ports which should not be permitted. If these rules are added to a security group then the resource will be in breach of compliance.
    ![ports to avoid](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-port-config.png)

1. Click **Save**.

</p></details>

<details>
<summary><strong>Viewing the compliance state (expand for details)</strong></summary><p>

You will now see the Rules section once more, with the rule you have just created added in and showing a Compliance state of **Evaluating...**.

Evaluation will take a couple of minutes and the UI will update to reflect the new state of **Noncompliant**. You can click the **Refresh** icon if you do not see the page update.

To see the state of the Security Groups which are being monitored for compliance, click the rule name. In our example here that is **security-workshop-restricted-common-ports**.

![Noncompliant rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_non-compliant.png)

</p></details>

### Testing the compliance state

We are now going to manually remediate the rules to make sure we no longer allow port 80 through to our application since we have enabled SSL.

<details>
<summary><strong>Change a security group (expand for details)</strong></summary><p>

1. In the AWS Console open the EC2 service and select **Security Groups** from the left hand menu

1. Place a check next to the **Group ID** for the **securityImmersionDay-loadBalancer**, for example
    ![sg list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_sg_amend.png)

1. Click **Inbound** in the ribbon below

1. Click **Edit** then click **Add Rule**

1. Delete the **HTTP** rule by clicking the cross to the right and save the config.
![security group rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/security-group-rule.png)

1. Click **Save**

</details>
<details>
<summary><strong>Check the Compliance breach (expand for details)</strong></summary>

1. In the AWS Console open the Config Service

1. After a short period of time the Compliance state of the **security-workshop-restricted-common-ports** rule will change to **compliant resource(s)**
    ![sg rule list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/compliant-rule-list.png)

1. Click on the **security-workshop-restricted-common-ports** rule name

1. In the **Resources Evaluated** section, click on the Security Group ID in the **Config Timeline** column for the **NonCompliant** resource
    ![sg rule shortlist](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/non-compliant-rule-shortlist.png)

1. Notice the timeline which shows the changes made to the Security Group
    ![sg timeline](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/sg-rule-timeline.png)

1. Click on the **Change** link below the most recent change and note that it reflects the change we made earlier
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/sg-rule-change.png)

</details>
 
## GuardDuty

In order to start processing events with GuardDuty we need to enable the service.

