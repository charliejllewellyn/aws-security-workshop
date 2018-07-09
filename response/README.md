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

1. Click **Save**

</details>
