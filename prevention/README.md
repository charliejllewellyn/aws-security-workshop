# Prevention

Prevention is a common approach to enforce compliance with security controls.

In this module we will look at some practices and products that can be used to enforce security by restricting  actions and enforcing compliance within AWS.

We'll use the following products to demonstrate these methods, S3, Identity and access management, AWS Certificate Manager, Application load balancer and Web application firewall.

## Identity and Access Management (IAM)
AWS Identity and Access Management (IAM) is a service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources. 

### Creating users

When you first create an AWS account, you begin with a single sign-in identity that has complete access to all AWS services and resources in the account. This identity is called the AWS account root user and is accessed by signing in with the email address and password that you used to create the account. We strongly recommend that you do not use the root user for your everyday tasks, even the administrative ones. Instead, adhere to the best practice of using the root user only to create your first IAM user. Then securely lock away the root user credentials and use them to perform only a few account and service management tasks. [1]

[1] - https://docs.aws.amazon.com/general/latest/gr/aws_tasks-that-require-root.html

<details>
<summary><strong>Create your first user (expand for details)</strong></summary><p>

First we will need to create an IAM User:- 

To create an administrator user for yourself and add the user to an administrators group (console)

1. Use your AWS account email address and password to sign in as the AWS account root user to the IAM console at https://console.aws.amazon.com/iam/.

1. In the navigation pane, choose Users and then choose Add user.
1. For User name, type a user name, such as Administrator. The name can consist of letters, digits, and the following characters: plus (+), equal (=), comma (,), period (.), at (@), underscore (_), and hyphen (-). The name is not case sensitive and can be a maximum of 64 characters in length.

1. Select the check box next to AWS Management Console access, select Custom password, and then type your new password in the text box. If you're creating the user for someone other than yourself, you can optionally select Require password reset to force the user to create a new password when first signing in.

1. Choose Next: Permissions.

1. On the Set permissions for user page, choose Add user to group.

1. Choose Create group.

1. In the Create group dialog box, type the name for the new group. The name can consist of letters, digits, and the following characters: plus (+), equal (=), comma (,), period (.), at (@), underscore (_), and hyphen (-). The name is not case sensitive and can be a maximum of 128 characters in length.

1. In the policy list, select the check box next to AdministratorAccess. Then choose Create group.

1.  Back in the list of groups, select the check box for your new group. Choose Refresh if necessary to see the group in the list.

1. Choose Next: Review to see the list of group memberships to be added to the new user. When you are ready to proceed, choose Create user.

</details>

### Using MFA with IAM and enableing Users to Self Serve

You can enable your users to self-manage their own multi-factor authentication (MFA) devices and credentials. You can use the AWS Management Console to configure credentials (access keys, passwords, signing certificates, and SSH public keys) and MFA devices for your users in small numbers. But that is a task that could quickly become time consuming as the number of users grows. Security best practice specifies that users should regularly change their passwords and rotate their access keys. They should also delete or deactivate credentials that are not needed and use MFA, at the very least, for sensitive operations.

<details>
<summary><strong>Create a policy enforce MFA (expand for details)</strong></summary><p>

To complete this lab you will need to create the following IAM user:- 

User Name | Other instructions
------------ | -------------
MFAUser | Choose only the option for *AWS Management Console access*, and assign a password.


You will also need to create the folowing group:- 

Group Name | Add user as a member | Other instructions
------------- | ------------- | -------------
EC2MFA | MFAUser | Do NOT attach any policies or otherwise grant permissions to this group. 


**Step 1: Create a Policy to Enforce MFA Sign-In**

Create a customer managed policy that prohibits all actions except the few IAM API operations that enable changing credentials and managing MFA devices.
    
**Step 2: Attach Policies to Your Test Group**

Create a group whose members have full access to all Amazon EC2 actions if they sign in with MFA. To create such a group, you attach both the AWS managed policy called AmazonEC2FullAccess and the customer managed policy you created in the first step.
    
**Step 3: Test Your User's Access**

Sign in as the test user to verify that access to Amazon EC2 is blocked until the user creates an MFA device and then signs in using that device.

You begin by creating an IAM customer managed policy that denies all permissions except those required for IAM users to manage their own credentials and MFA devices.

1. Sign in to the AWS Management Console as a user with administrator credentials. To adhere to IAM best practices, don’t sign in with your AWS account root user credentials. For more information, see Create individual IAM users.

1. Open the IAM console at https://console.aws.amazon.com/iam/.

1. In the navigation pane, choose Policies, and then choose Create policy.

1. Choose the JSON tab and copy the text from the following JSON policy document. Paste this text into the JSON text box.

    > Note
    > This example policy does not allow users to both sign in and perform a password change. New users and users with an expired password might try to do so. To intentionally allow this, add `iam:ChangePassword` and `iam:CreateLoginProfile` to the statement `BlockMostAccessUnlessSignedInWithMFA`.

```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowAllUsersToListAccounts",
                "Effect": "Allow",
                "Action": [
                    "iam:ListAccountAliases",
                    "iam:ListUsers",
                    "iam:ListVirtualMFADevices",
                    "iam:GetAccountPasswordPolicy",
                    "iam:GetAccountSummary"
                ],
                "Resource": "*"
            },
            {
                "Sid": "AllowIndividualUserToSeeAndManageOnlyTheirOwnAccountInformation",
                "Effect": "Allow",
                "Action": [
                    "iam:ChangePassword",
                    "iam:CreateAccessKey",
                    "iam:CreateLoginProfile",
                    "iam:DeleteAccessKey",
                    "iam:DeleteLoginProfile",
                    "iam:GetLoginProfile",
                    "iam:ListAccessKeys",
                    "iam:UpdateAccessKey",
                    "iam:UpdateLoginProfile",
                    "iam:ListSigningCertificates",
                    "iam:DeleteSigningCertificate",
                    "iam:UpdateSigningCertificate",
                    "iam:UploadSigningCertificate",
                    "iam:ListSSHPublicKeys",
                    "iam:GetSSHPublicKey",
                    "iam:DeleteSSHPublicKey",
                    "iam:UpdateSSHPublicKey",
                    "iam:UploadSSHPublicKey"
                ],
                "Resource": "arn:aws:iam::*:user/${aws:username}"
            },
            {
                "Sid": "AllowIndividualUserToListOnlyTheirOwnMFA",
                "Effect": "Allow",
                "Action": "iam:ListMFADevices",
                "Resource": "arn:aws:iam::*:user/${aws:username}"
            },
            {
                "Sid": "AllowIndividualUserToManageTheirOwnMFA",
                "Effect": "Allow",
                "Action": [
                    "iam:CreateVirtualMFADevice",
                    "iam:DeleteVirtualMFADevice",
                    "iam:EnableMFADevice",
                    "iam:ResyncMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::*:mfa/${aws:username}",
                    "arn:aws:iam::*:user/${aws:username}"
                ]
            },
            {
                "Sid": "AllowIndividualUserToDeactivateOnlyTheirOwnMFAOnlyWhenUsingMFA",
                "Effect": "Allow",
                "Action": [
                    "iam:DeactivateMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::*:mfa/${aws:username}",
                    "arn:aws:iam::*:user/${aws:username}"
                ],
                "Condition": {
                    "Bool": {
                        "aws:MultiFactorAuthPresent": "true"
                    }
                }
            },
            {
                "Sid": "BlockMostAccessUnlessSignedInWithMFA",
                "Effect": "Deny",
                "NotAction": [
                    "iam:CreateVirtualMFADevice",
                    "iam:DeleteVirtualMFADevice",
                    "iam:ListVirtualMFADevices",
                    "iam:EnableMFADevice",
                    "iam:ResyncMFADevice",
                    "iam:ListAccountAliases",
                    "iam:ListUsers",
                    "iam:ListSSHPublicKeys",
                    "iam:ListAccessKeys",
                    "iam:ListServiceSpecificCredentials",
                    "iam:ListMFADevices",
                    "iam:GetAccountSummary",
                    "sts:GetSessionToken"
                ],
                "Resource": "*",
                "Condition": {
                    "BoolIfExists": {
                        "aws:MultiFactorAuthPresent": "false"
                    }
                }
            }
        ]
    }
```
<details>
<summary><strong>What does this policy do? (expand for details)</strong></summary><p>

* The first statement enables the user to see basic information about the account and its users in the IAM console. These permissions must be in their own statement because they do not support or do not need to specify a specific resource ARN, and instead specify "Resource" : "*".

* The second statement enables the user to manage his or her own user, password, access keys, signing certificates, SSH public keys, and MFA information in the IAM console. The resource ARN limits the use of these permissions to only the user's own IAM user entity.

* The third statement enables the user to see information about MFA devices, and which are associated with his or her IAM user entity.

* The fourth statement allows the user to provision or manage his or her own MFA device. Notice that the resource ARNs in the fourth statement allow access to only an MFA device or user that has the exact same name as the currently signed-in user. Users can't create or alter any MFA device other than their own.

* The fifth statement allows the user to deactivate only his or her own MFA device and only if the user signed in using MFA. This prevents others with only the access keys (and not the MFA device) from deactivating the MFA device and replacing it with their own.

* The sixth and final statement uses a combination of "Deny" and "NotAction" to deny all actions for all other AWS services if the user is not signed-in with MFA. If the user is signed-in with MFA, then the "Condition" test fails and the final "deny" statement has no effect and other permissions granted to the user can take effect. This last statement ensures that when the user is not signed-in with MFA that they can perform only the IAM actions allowed in the earlier statements. The ...IfExists version of the Bool operator ensures that if the aws:MultiFactorAuthPresent key is missing, the condition returns true. This means that a user accessing an API with long-term credentials, such as an access key, is denied access to the non-IAM API operations.
</p></details>


1. When you are finished, choose Review policy. The Policy Validator reports any syntax errors.

    >Note
    >You can switch between the Visual editor and JSON tabs any time. However, the policy above includes the NotAction element, which is not supported in the visual editor. For this policy, you will see a notification on the Visual editor tab. Return to the JSON tab to continue working with this policy.

1. On the Review page, type Force_MFA for the policy name. For the policy description, type This policy allows users to manage their own passwords and MFA devices but nothing else unless they authenticate with MFA. Review the policy Summary to see the permissions granted by your policy, and then choose Create policy to save your work.

The new policy appears in the list of managed policies and is ready to attach.

Step 2: Attach Policies to Your Test Group

Next you attach two policies to the test IAM group, which will be used to grant the MFA-protected permissions.

1. In the navigation pane, choose Groups.

1. In the search box, type EC2MFA, and then choose the group name (not the check box) in the list.

1. On the Permissions tab, and click Attach Policy.

1. On the Attach Policy page, in the search box, type EC2Full and then select the check box next to AmazonEC2FullAccess in the list. Don't save your changes yet.

1. In the search box, type Force, and then select the check box next to Force_MFA in the list.

Choose Attach Policy.

Step 3: Test Your User's Access

In this part of the tutorial, you sign in as the test user and verify that the policy works as intended.

1. Sign in to your AWS account as MFAUser with the password you assigned in the previous section. Use the URL: https://<alias or account ID number>.signin.aws.amazon.com/console

1. Choose EC2 to open the Amazon EC2 console and verify that the user has no permissions to do anything.

1. On the navigation bar, choose Services, and then choose IAM to open the IAM console.

1. In the navigation pane, choose Users, and then choose the user (not the check box) MFAUser. If the Groups tab appears by default, note that it says that you don't have permissions to see your group memberships.

1. Now add an MFA device. Choose the Security credentials tab. Next to Assigned MFA device, choose the edit icon ( ).

1. For this tutorial, we use a virtual (software-based) MFA device, such as the Google Authenticator app on a mobile phone. Choose A virtual MFA device, and then click Next Step.
    IAM generates and displays configuration information for the virtual MFA device, including a QR code graphic. The graphic is a representation of the secret configuration key that is available for manual entry on devices that do not support QR codes.

1. Open your virtual MFA app. (For a list of apps that you can use for hosting virtual MFA devices, see Virtual MFA Applications.) If the virtual MFA app supports multiple accounts (multiple virtual MFA devices), choose the option to create a new account (a new virtual MFA device).

1. Determine whether the MFA app supports QR codes, and then do one of the following:

    * Use the app to scan the QR code. For example, you might choose the camera icon or choose an option similar to Scan code, and then use the device's camera to scan the code.

    * In the Manage MFA Device wizard, choose Show secret key for manual configuration, and then type the secret configuration key into your MFA app.

    When you are finished, the virtual MFA device starts generating one-time passwords.

1. In the Manage MFA Device wizard, in the Authentication Code 1 box, type the one-time password that currently appears in the virtual MFA device. Wait up to 30 seconds for the device to generate a new one-time password. Then type the second one-time password into the Authentication Code 2 box. Choose Active Virtual MFA.

    > Important
    > Submit your request immediately after generating the codes. If you generate the codes and then wait too long to submit the request, the MFA device is successfully associated with the user. However,t the MFA device is out of sync. This happens because time-based one-time passwords (TOTP) expire after a short period of time. If this happens, you can resync the device.

    The virtual MFA device is now ready to use with AWS.

1. Sign out of the console and then sign in as MFAUser again. This time AWS prompts you for an MFA code from your phone. When you get it, type the code in the box and then choose Submit.

1. Choose EC2 to open the Amazon EC2 console again. Note that this time you can see all the information and perform any actions you want. If you go to any other console as this user, you see access denied messages because the policies in this tutorial grant access only to Amazon EC2.

## Encryption

A good best practice is to use both encryption in transit and encryption at rest. Whilst the details about how to enforce this may change between AWS products the approach to protect data remains consistent.

### Using AWS Certificate Manager and Application Load Balancing to protect data in transit

In this scenario we're going to use a self-signed SSL certificate however the process can be used to import official SSL certificates or ACM can be used to generate certificates for domains you own.

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

1. Place a check next to the security-workshop load balancer and in the ribbon below select **Listeners**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/LB_listners.png)

1. Click **Add Listener**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/LB_listners.png)

1. Change the protocol to **HTTPS**

1. Select **Add Action**, **Forward to...** under Default Action(s) and select the security workshop target group.

1. Change **Default SSL Certificate** to **Import**

1. Copy and paste the contents of server.key (created earlier) to **Certificate Private Key**

1. Copy and paste the contents of server.crt (created earlier) to **Certificate Body**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/LB_listner_protocal.png)

1. Finally we force encryption by removing port 80 from the security group.

    1. In the AWS Console open the EC2 service and select **Security Groups** from the left hand menu

    1. Place a check next to the **Group ID** for the **securityImmersionDay-loadBalancer**, for example
    ![sg list](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_sg_amend.png)

    1. Click **Inbound** in the ribbon below

    1. Click **Edit** then click **Add Rule**

    1. Delete the **HTTP** rule by clicking the cross to the right and save the config.
        ![security group rule](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/detection/Config_sg_delete.png)

1. Click **Save**
</p></details>

If you now access the DVWA over HTTPS e.g.

```
https://secur-loadb-1hhx56x4r3wyy-1780097981.us-east-1.elb.amazonaws.com
```

**Note** you will receive a certificate warning in the browser because we used a self-signed certificate which the browser will not trust.

You will notice the traffic is now being served over SSL.

### Using S3 bucket policies to deny un-encrypted uploads

We are going to use s3 [bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html) to prevent users.

First we validate we can upload un-encrypted files. Using the cli (configured as part of the pre-reqs) upload a file to s3, for example

```
aws s3 cp securityThreatList.txt s3://YOUR_BUCKET_NAME/
```

The file will upload without issue.

<details>
<summary><strong>Create a new bucket policy (expand for details)</strong></summary><p>

1. In the AWS Console open the S3 service console.

1. Select the bucket name obtained when you setup the workshop

1. In the S3 console select **Permissions** and then **Bucket Policy**
  ![DVWA Security](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/s3_bucket_policy.png)

1. Enter the policy below, replacing YOUR_BUCKET_NAME with your bucket name.

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
aws s3 cp securityThreatList.txt s3://YOUR_BUCKET_NAME/
```

This time the request will fail with **An error occurred (AccessDenied) when calling the PutObject operation: Access Denied**.

If we now request encryption as part of the upload we'll see we can successfully write to the bucket.

```
aws s3 cp securityThreatList.txt s3://YOUR_BUCKET_NAME/ --sse
```

## Web Application Firewall

In this section we are going to use the [AWS Web Application Firewall](https://aws.amazon.com/waf/) to prevent SQL injection attacks against our site.

First we'll prove the vulnerability in DVWA. Browse to the site now served over HTTPS and select **SQL Injection** form the menu on the left.

**Note** you can skip the detailed steps if you are not interested in understanding the exploit and just run the last command to prove you can dump data from the database.

<details>
<summary><strong>Exploit the site (expand for details)</strong></summary><p>

1. First we'll check if the site is vulnerable to SQL injection, in the input enter the following and click submit.

```
1'
```

The site responds with a SQL error indicating it tried to execute what we entered.

1. Now we'll see what information we can return

```
1' or 1 = 1#
```

This dumps content from the table

1. We'll now work out how many columns are selected in the original statement

```
1' order by 3#
```

This generates an error showing us that the query selects 3 or less columns.

```
1' order by 2#
```

This tells us the query has two columns in.

1. Lets now return the table name

```
1' or 1 = 1 union select null, table_name from information_schema.tables#
```

If we search down the list of tables we'll discover one called **users**

1. We'll now see what columns are available in the table

```
1' or 1 = 1 union select null, column_name from information_schema.columns where table_name = "users"#
```

Here we can see a users user and password column....interesting ;-)

</details>

Finally, we'll dump the data

```
1' or 1 = 1 union select user,password from users#
```

This returns a list of usernames and what look like hashed passwords

Using a site to reverse the hash such as https://md5.gromweb.com/ we prove that we can exploit the site to return the password.

<details>
<summary><strong>Setup AWS WAF to prevent SQL injection (expand for details)</strong></summary><p>

1. In the AWS console open the WAF

1. Select **Go to AWS WAF** under **AWS WAF**

1. Click **Configure ACL** and select **Next** at the bottom of the page.

1. Enter **Security workshop** in "Web ACL name" and select the **region** you deployed your stack to and select the security loadbalancer as the **resource**, click **Next**

1. Scroll down to **SQL injection match conditions** and choose **Create condition**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/WAF_acl.png)

1. Enter **Security workshop SQLinjection** for the **Name**

1. Select **URI** for the **Part of the request to filter on** and **Url Decode** for the **Transformation**, click **Add filter** and click **Create**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/WAF_sqli.png)

1. Select **Create rule** and enter **Security workshop rule**

1. Under **Add conditions** change the dropdown for **match at least one of the filters in the cross-site scripting match condition** to **match at least one of the filters in the SQL injection match condition** and select the condition **Security workshop SQLinjection**, click **Create**
    ![provision certificates](https://github.com/charliejllewellyn/aws-security-workshop/blob/master/images/WAF_rule.png)

1. Select **Allow all requests that don't match any rules**.

1. Click **Review and create** and **Confirm and create**

</details>

Attempt to re-run the exploit above and you will see your requests are denied.

## Conclusion

This concludes some examples of how security policies can be enforced through prevention in the [next module](../detection), we'll look at methods and tools that can be used to detect security events within your systems.
