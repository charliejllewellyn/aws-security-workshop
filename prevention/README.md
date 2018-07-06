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

1. Finally we force encryption by deleting the HTTP listener. Select the **HTTP: 80** listener and select delete.
    ![Delete HTTP listener](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/LB_delete_listener.png)

</p></details>

If you now access the DVWA over HTTPS e.g.

```
https://secur-loadb-1hhx56x4r3wyy-1780097981.us-east-1.elb.amazonaws.com
```

**Note** you will recieve a certifictae warning in the browser because we used a self signed certificate which the browser will not trust.

You will notice the traffic is now being served over SSL.

### Using S3 bucket policies to deny un-encrypted uploads

We are going to use s3 [bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html) to prevent users.

First we validate we can upload un-encrypted files. Using the cli (configured as part of the pre-reqs) upload a file to s3, for example

```
aws s3 cp YOUR_FILE_NAME s3://YOUR_BUCKET_NAME/
```

The file will upload without issue.

<details>
<summary><strong>Create a new bucket policy (expand for details)</strong></summary><p>

1. In the AWS Console open the S3 service console.

1. Select the bucket name obtained when you setup the workshop

1. In the S3 console select **Permissions** and then **Bucket Policy**

1. Enter the policy below to replacing YOUR_BUCKET_NAME with your bucket name.

```
 {
     "Version": "2012-10-17",
     "Id": "PutObjPolicy",
     "Statement": [
           {
                "Sid": "DenyUnEncryptedObjectUploads",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:PutObject",
                "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*",
                "Condition": {
                        "Null": {
                               "s3:x-amz-server-side-encryption": true
                        }
               }
           }
     ]
 }
```

</details>

Retry the validation using the CLI.

```
aws s3 cp YOUR_FILE_NAME s3://YOUR_BUCKET_NAME/
```

This time the request will fail with **An error occurred (AccessDenied) when calling the PutObject operation: Access Denied**.

If we now request encryption as part of the upload we'll see we can successfully write to the bucket.

```
aws s3 cp YOUR_FILE_NAME s3://YOUR_BUCKET_NAME/ --sse
```

## Web Application Firewall

In this section we are going to use the [AWS Web Application Firewall](https://aws.amazon.com/waf/) to prevent SQL injection attacks against our site.

First we'll prove the vulnerability in DVWA. Browse to the site now served over HTTPS and select **SQL Injection** form the menu on the left.


