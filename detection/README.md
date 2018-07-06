# Prevention

Detection is a common approach to understand where security controls have failed.

In this module we will look at some practices and products that can be used to detect changes which have been made to your configurations and how to generate alerts on that basis.

We'll use the following products to demonstrate these methods, AWS Config, AWS SNS, AWS CloudTrail and Amazon CloudWatch.

## Configuration State

A good practice is to monitor the state change of configuration items (CI). This is helpful for change management, fault diagnosis and resolution, training, compliance and of course incident response.

### Using AWS Config Rules and and AWS SNS to detect configuration changes

In this scenario we are going to use one of the AWS supplied configuration rules to monitor Security Group rule configuration.

<details>
<summary><strong>Create a Config Rule in AWS Config (expand for details)</strong></summary><p>

1. In the AWS Console open the Config service, ensuring that you have selected a region where the items you wish to monitor are present

1. Select **Rules** from the left hand menu

1. Press the **Add rule** button
    ![add rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/add-rule.png)

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

(https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-evaluating.png)

Evaluation will take a couple of minutes and the UI will update to reflect the new state of **Compliant**. You can click the **Refresh** icon if you do not see the page update.

To see the state of the Security Groups which are being monitored for compliance, click the rule name. In our example here that is **myOrg-security-groups-restrict-common-ports**.

(https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-compliant.png)

You will now see that we have two groups in compliance.
(https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/rule-detail-compliant.png)

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
2. **Type** - Custom TCP
3. **Protocol** - TCP
4. **Port Range** - 3389
5. **Source** Anywhere
6. **Description** RDesktop for everything
    ![new sg rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/security-group-rule.png)

1. Click **Save**

</details>
<details>
<summary><strong>Check the Compliance breach (expand for details)</strong></summary>

1. In the AWS Console open the Config Service

1. After a short period of time the Compliance state of the **myOrg-security-groups-restrict-common-ports** rule will change to **1 noncompliant resource(s)**
    ![sg rule list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/non-compliant-rule-list.png)

1. Click on the **myOrg-security-groups-restrict-common-ports** Rule name

1. In the **Resources Evaluated** section, click on the Security Group ID in the **Config Timeline** column for the **NonCompliant** resource
    ![sg rule shortlist](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/non-compliant-rule-shortlist.png)

1. Notice the timeline which shows the changes made to the Security Group
    ![sg timeline](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/sg-rule-timeline.png)

1. Click on the **Change** link below the most recent change and note that it reflects the change we made earlier
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/sg-rule-change.png)

</details>
