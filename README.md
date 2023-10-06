
# Welcome to your Monitor DB Activity Streams project!

## Pre-requisites:
1. To work with the AWS CDK, you must have an AWS account and credentials and have installed Node.js and the AWS CDK Toolkit. 

2. Python AWS CDK applications require Python 3.6 or later. If you don't already have it installed, download a compatible version 
for your operating system at python.org.

3. You need to have SSM session manager installed on your local machine to do port forwarding to access Opensearch Dashboard.
Refer to this link: https://guide.aws.dev/articles/ARhePEPiT4SY2ezumYiqFVbQ/port-forwarding-with-aws-session-manager

## Infrastructure
This template will deploy the following components:
1. VPC with 3 public & 3 private subnets (Need to do it in region where there is at least 3 AZs)
2. Aurora Postgresql
3. BastionHost
4. Opensearch Cluster



This is a project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Next, deploy!
```
$ cdk deploy
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Other Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
