## Response

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
