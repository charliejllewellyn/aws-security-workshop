# AWS Security Workshop

In this workshop we will deploy a simple ethical hacking application that enables users to explore vunerabilites. The deployment uses [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to deploy the [Damn Vunerable Web Application (DVWA)](http://www.dvwa.co.uk/).

The application architecture uses [Amazon EC2](https://aws.amazon.com/ec2/), [AWS Auto Scaling](https://aws.amazon.com/autoscaling/) and [Amazon Relational Database Service (Amazon RDS)](https://aws.amazon.com/rds/).

See the diagram below for a description of the core infrastrure.

<p align="center">
  <img width="300" src="https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/secuirty_immersion_day.jpg">
</p>

Stack| Launch
------|-----
AWS Security Workshop | [![Launch DVWA](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
