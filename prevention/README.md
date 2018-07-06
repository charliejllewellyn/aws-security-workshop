# Prevention

Prevention is a common approach to enforce compliance with security controls.

In this module we will look at some practices and products that can be used to enforce security by restircting actions and enforcing compliance within AWS.

We'll use the following products to demonstrate these methods, S3, Identity and access managment, AWS Certificate Manager, Application load balancer, Web application firewall.

## Encryption

A good best practice is to use both encryption in transit and encryption at rest. Whilst the details about how to enforce this may change between AWS products the approach to protect data remains consistent.

### Using AWS Certificate Manager and Application Load Balancing to protect data in transit

In this scenario we're going to use a self signed SSL certifcate however the process can be used to import offical SSL certificates or ACM can be used to generate certificates for domains you own.

<details>
<summary><strong>Create a new certificate in AWS Certificate Manager (expand for details)</strong></summary><p>

1. Generate a certificate using OpenSSL by running

```
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
```

Complete the details entering the DVWA load balancer URL obtained when setting up the application for example

```
Country Name (2 letter code) [AU]:GB
State or Province Name (full name) [Some-State]:Somerset
Locality Name (eg, city) []:Wells
Organization Name (eg, company) [Internet Widgits Pty Ltd]:AWS   
Organizational Unit Name (eg, section) []:AWS Security Workshop
Common Name (e.g. server FQDN or YOUR name) []:secur-loadb-1hhx56x4r3wyy-1780097981.us-east-1.elb.amazonaws.com        
Email Address []:email@example.com
```

1. In the AWS Console open the EC2 service

1. Select **Load Balancers** from the left hand menu

1. Place a check next to the security-workshop load balancer and in the ribbon below select **Listners**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/LB_listners.png)

1. Click **Add Listner**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/LB_listners.png)

1. Change the protocal to **HTTPS**

1. Select **Add Action**, **Forward to...** under Default Action(s) and select the security workshop target group.

1. Change **Default SSL Certificate** to **Import**

1. Copy can paste the contents of server.key (created earlier) to **Certificate Private Key**

1. Copy can paste the contents of server.crt (created earlier) to **Certificate Body**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/LB_listner_protocal.png)

</p></details>

If you now access the DVWA over HTTPS e.g.

```
https://secur-loadb-1hhx56x4r3wyy-1780097981.us-east-1.elb.amazonaws.com
```

**Note** you will recieve a certifictae warning in the browser because we used a self signed certificate which the browser will not trust.
You will notice the traffic is now being served over SSL.

first enabling encryption at rest for our s3 bucket file stoarge


