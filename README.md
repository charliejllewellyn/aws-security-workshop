# AWS Security Workshop

In this workshop we will deploy a simple ethical hacking application that enables users to explore vunerabilites. The deployment uses [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to deploy the [Damn Vunerable Web Application (DVWA)](http://www.dvwa.co.uk/).

The application architecture uses [Amazon EC2](https://aws.amazon.com/ec2/), [AWS Auto Scaling](https://aws.amazon.com/autoscaling/) and [Amazon Relational Database Service (Amazon RDS)](https://aws.amazon.com/rds/).

See the diagram below for a description of the core infrastrure.

<p align="center">
  <img width="300" src="https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/secuirty_immersion_day.jpg">
</p>

Stack| Launch
------|-----
US East (N. Virginia) | [![Launch AWS Security Workshop in us-east-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
US East (Ohio) | [![Launch AWS Security Workshop in us-east-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
US West (Oregon) | [![Launch AWS Security Workshop in us-west-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
EU (Frankfurt) | [![Launch AWS Security Workshop in eu-central-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
EU (Ireland) | [![Launch AWS Security Workshop in eu-west-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
EU (London) | [![Launch AWS Security Workshop in eu-west-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
Asia Pacific (Tokyo) | [![Launch AWS Security Workshop in ap-northeast-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
Asia Pacific (Seoul) | [![Launch AWS Security Workshop in ap-northeast-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
Asia Pacific (Sydney) | [![Launch AWS Security Workshop in ap-southeast-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
Asia Pacific (Mumbai) | [![Launch AWS Security Workshop in ap-south-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=aws-security-workshop&templateURL=https://s3-eu-west-1.amazonaws.com/cjl-cloudformation-stack-templates/application_deployment.yaml)
