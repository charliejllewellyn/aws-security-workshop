# AWS Security Workshop

In this workshop we will deploy a simple ethical hacking application that enables users to explore vunerabilites. The deployment uses [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to deploy the [Damn Vunerable Web Application (DVWA)](http://www.dvwa.co.uk/).

The application architecture uses [Amazon EC2](https://aws.amazon.com/ec2/), [AWS Auto Scaling](https://aws.amazon.com/autoscaling/) and [Amazon Relational Database Service (Amazon RDS)](https://aws.amazon.com/rds/).

See the diagram below for a description of the core infrastrure.

<p align="center">
  <img width="300" src="https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/secuirty_immersion_day.jpg">
</p>

## Prerequisites

### AWS Account

In order to complete this workshop you'll need an AWS Account with access to create AWS IAM, S3, EC2, VPC, CloudTrail, GuardDuty resources. The code and instructions in this workshop assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you may run into naming conflicts for certain resources. You can work around these by appending a unique suffix to the resources that fail to create due to conflicts, but the instructions do not provide details on the changes required to make this work.

Many of the resources you will launch as part of this workshop are eligible for the AWS free tier if your account is less than 12 months old. See the [AWS Free Tier page](https://aws.amazon.com/free/) for more details.

### Browser

We recommend you use the latest version of Chrome to complete this workshop.

### OpenSSL client

During the lab you will generate a self signed SSL certificate so need access to openssl. You can download the tool for Windows, Linux and Mac [here](https://wiki.openssl.org/index.php/Binaries).

## Application setup

The application can be launched in the following regions by clicking the launch stack icons below.

Stack| Launch
------|-----
US East (N. Virginia) | [![Launch AWS Security Workshop in us-east-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
US East (Ohio) | [![Launch AWS Security Workshop in us-east-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
US West (Oregon) | [![Launch AWS Security Workshop in us-west-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
EU (Frankfurt) | [![Launch AWS Security Workshop in eu-central-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
EU (Ireland) | [![Launch AWS Security Workshop in eu-west-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
Asia Pacific (Tokyo) | [![Launch AWS Security Workshop in ap-northeast-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
Asia Pacific (Sydney) | [![Launch AWS Security Workshop in ap-southeast-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)

## Record stack parameters

Once the stack has successfully deployed we need capture a couple of variables generated during the setup for use in the modules. From the CloudFormation click the checkbox for the stack "aws-security-workshop" and in the ribbon below select "Output". Here you will find the URL for the DVWA and the bucket name for S3. Record them both.

![DVWA URL](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/dvwa_url.png)

## DVWA configuration

Use the DVWA url obtained above to access the site by entering it into your browser. Once the page returns click the "Create / Reset database" button at the bottom of the page.

![DVWA](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/dvwa.png)

Login with:

```
Username: admin
Password: password
```

## Modules

There are four modules aligned to a common IT security lifecycle model.

1. [Prevention](prevention)
2. [Detection](detection)
3. [Response](reponse)
4. [Analysis](analysis)
