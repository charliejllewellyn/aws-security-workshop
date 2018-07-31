# AWS Security Workshop

This workshop will guide you through four modules building up a multi-stage protection stratgey. Each module builds on the previous module to provide an understanding of how AWS security services can be used to provide holistic controls encompassing the entire security lifecycle. We will deploy a simple ethical hacking application that enables users to explore vulnerabilities. The deployment uses [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to deploy the [Damn Vulnerable Web Application (DVWA)](http://www.dvwa.co.uk/).

The application architecture uses [Amazon EC2](https://aws.amazon.com/ec2/), [AWS Auto Scaling](https://aws.amazon.com/autoscaling/) and [Amazon Relational Database Service (Amazon RDS)](https://aws.amazon.com/rds/).

See the diagram below for a description of the core infrastructure.

<p align="center">
  <img width="300" src="https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/secuirty_immersion_day.jpg">
</p>

## Prerequisites

### AWS Account

In order to complete this workshop you'll need an AWS Account with access to create AWS IAM, S3, EC2, VPC, CloudTrail, GuardDuty and WAF resources. The code and instructions in this workshop assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you may run into naming conflicts for certain resources. You can work around these by appending a unique suffix to the resources that fail to create due to conflicts, but the instructions do not provide details on the changes required to make this work.

Many of the resources you will launch as part of this workshop are eligible for the AWS free tier if your account is less than 12 months old. See the [AWS Free Tier page](https://aws.amazon.com/free/) for more details.

### Browser

We recommend you use the latest version of Chrome to complete this workshop.

## AWS CLI

Some of the modules use the CLI to access AWS resources. Follow the guide [here](https://docs.aws.amazon.com/lambda/latest/dg/setup-awscli.html) to get setup.

## Generate a keypair

To access the servers that are deployed in the workshop you'll need to generate a keypair. Follow this [guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair) to complete the setup.

Record the name of the keypair as you will need it to deploy the lab.

### OpenSSL client

During the lab you will generate a self-signed SSL certificate, to do this we use openssl. You can download the tool for Windows, Linux and Mac [here](https://wiki.openssl.org/index.php/Binaries).

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

**Note:** You will be prompted to supply the keypair you generated in the pre-reqs above.

## Record stack parameters

Once the stack has successfully deployed we need capture a couple of variables generated during the setup for use in the modules. In the AWS console open the CloudFormation service. You will see a stack (**not** NESTED) called "aws-security-workshop", place a check in the box next to it and in the ribbon below select "Output". Here you will find the URL for the DVWA and the bucket name for S3. Record them both.

![DVWA URL](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/dvwa_url.png)

## DVWA configuration

Use the DVWA url obtained above to access the site by entering it into your browser. Once the page returns click the "Create / Reset database" button at the bottom of the page.

![DVWA](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/dvwa.png)

Login with:

```
Username: admin
Password: password
```

In the left hand menu select **DVWA Security**, in the dropdown select **Low** and click **Submit**.

![DVWA Security](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/dvwa_security.png)

## Modules

The workshop has been modelled around a common pattern for security lifecycle.

<p align="center">
  <img width="300" src="https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/security_lifecycle.png">
</p>

1. [Prevention](prevention) - common techniques to enforce desired controls in AWS
2. [Detection](detection) - products that help monitor and surface information about security and change across AWS
3. [Response](response) - techniques to automatically remmdiate against information surfaced through detection 
4. [Analysis](analysis) - techniques to audit information gathered across AWS
