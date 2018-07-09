## Response

In this module we will explore practices and products to automate the response the events we detect in the previous [module](../detection). We will use [AWS Lambda](https://aws.amazon.com/lambda/), [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/), [Amazon GuardDuty](https://aws.amazon.com/guardduty/), [AWS Config](https://aws.amazon.com/config/).

## Lambda

In this module we use Lambda as a serverless compute to automate responses to some of the security notifications we configured previously. This improves the response times to for standard activies whilst still giving the visibilty we need into security operations on the platform.

<details>
<summary><strong>Setup GuardDuty Lambda</strong></summary><p>

1. From the AWS Console open the Lambda dashboard.

1. Click **Create a function**
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/response/Lambda.png)

1. Update the **Name** with **securityWorkshopGuardDutyLambda**

1. Select **Python 3.6** as the **runtime**

1. Under **Role** select **Create custom role**

1. On the IAM page that opens select **View Policy Document** and click **edit**, click **OK** to acknoweldge reading the documentation

1. Enter the following policy:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Action": "ec2:*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

1. Click **Allow**

1. When you are returned to the Lambda console click **Create Function**
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/response/Lambda_setup.png)

1. Scroll down to the **Function Code** and replace the **lambda_function** code with the code in response/lambda/GuardDuty/lambda_function.py
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/response/Lambda_function.png)

1. Under **Basic Settings** change the **Timeout** to **5 minutes**

1. Click **Save**

</details>

## CloudWatch

Building on our previous detection event in CloudWatch we're now going to configure the event to not only notify the security via SNS but also invoke the Lambda we created above. 

The Lambda code will capture the name of the infected resource, take a snapshot and terminate the instance.

<details>
<summary><strong>Update CloudWatch event ton notify Lambda</strong></summary><p>

1. From the AWS Console open the CloudWatch dashboard.

1. Select **Events** from the left hand menu. Select the **SecurityWorkshopEventRule** event rule we created earlier and in the top right corner select **Actions** then **Edit**.

1. Click **Add Target** choose **Lambda Function** and select the Lambda function we just created **securityWorkshopGuardDutyLambda**
    ![sg change](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/response/CloudWatch_trigger.png)

1. Click **Configure Details** and then **Update Rule**

</details>

## Generate test events

Follow the previous modules instructions to [Test Detection](https://github.com/charliejllewellyn/aws-security-workshop/tree/master/detection#test-detection).
