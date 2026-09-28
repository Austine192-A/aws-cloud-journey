# Lab 08 - CloudFront + S3 CDN

## Overview

In this lab, I built a simple static website using Amazon S3 and delivered it through Amazon CloudFront.

The goal was to understand how a CDN can sit in front of an S3 bucket and securely serve website content using HTTPS.

## Architecture

```text
Client
  |
  v
CloudFront
  |
  v
Amazon S3
```

## Objectives

* Host a static website in Amazon S3
* Keep the S3 bucket private
* Create an Amazon CloudFront distribution
* Configure Origin Access Control (OAC)
* Allow CloudFront to access the S3 bucket
* Serve the website through HTTPS
* Test the CloudFront distribution
* Troubleshoot an AccessDenied error
* Clean up AWS resources after the lab

## AWS Services Used

* Amazon S3
* Amazon CloudFront
* CloudFront Origin Access Control (OAC)
* AWS CloudShell

## 1. Create the S3 Bucket

I created an S3 bucket named:

```text
austine-cloudfront-lab-08-2026
```

The bucket was created in the `us-east-1` region.

Block Public Access remained enabled because the website would be accessed through CloudFront rather than directly from S3.

The website files were:

```text
index.html
style.css
```

### Screenshot

![S3 bucket and website files](./screenshots/01-s3-bucket-and-files.png)

## 2. Create the CloudFront Distribution

I created a CloudFront distribution using the S3 bucket as the origin.

CloudFront distribution domain:

```text
d17xfkzizozq8h.cloudfront.net
```

The distribution was configured to use the S3 REST endpoint rather than public S3 website hosting.

### Screenshot

![CloudFront distribution](./screenshots/02-cloudfront-distribution.png)

## 3. Configure Origin Access Control

I configured CloudFront Origin Access Control (OAC) so that CloudFront could securely request objects from the private S3 bucket.

The S3 bucket itself did not need to be publicly accessible.

### Screenshot

![Origin Access Control and bucket policy](./screenshots/03-oac-and-bucket-policy.png)

## 4. Configure the S3 Bucket Policy

The S3 bucket policy allows the CloudFront service principal to retrieve objects from the bucket.

Access is restricted to the specific CloudFront distribution.

This provides the following flow:

```text
User
  |
  v
CloudFront
  |
  v
Private S3 bucket
```

## 5. Troubleshooting AccessDenied

The first CloudFront request returned an `AccessDenied` response.

I checked:

* The S3 objects existed
* The CloudFront origin was correct
* Origin Access Control was configured
* The S3 bucket policy allowed CloudFront access
* The CloudFront distribution had `index.html` configured as the default root object

After correcting the CloudFront configuration, the website became accessible.

## 6. Test the CloudFront Website

The website was successfully opened through the CloudFront domain.

### Browser Test

![CloudFront website](./screenshots/04-cloudfront-website.png)

### Terminal Test

I also tested the CloudFront endpoint from AWS CloudShell:

```bash
curl -I https://d17xfkzizozq8h.cloudfront.net
```

The response returned:

```text
HTTP/2 200
content-type: text/html
server: AmazonS3
x-cache: Miss from cloudfront
```

This confirmed that CloudFront was successfully serving the website.

![CloudFront terminal test](./screenshots/05-cloudfront-terminal-test.png)

## Key Lessons

This lab helped me understand:

* How CloudFront works with Amazon S3
* The difference between public S3 hosting and private S3 origins
* How Origin Access Control improves access to S3 content
* How CloudFront delivers content over HTTPS
* How to troubleshoot CloudFront `AccessDenied` errors
* How to verify CDN responses using HTTP headers
* Why cloud resources should be cleaned up after practice labs

## Evidence

The screenshots in this directory document:

1. S3 bucket and website files
2. CloudFront distribution
3. Origin Access Control and S3 bucket policy
4. Working CloudFront website
5. Successful CloudFront HTTP response

## AWS Resource Cleanup

After completing the lab and capturing the required evidence, the AWS resources were cleaned up to avoid unnecessary ongoing charges.

Resources removed:

* CloudFront distribution
* CloudFront Origin Access Control
* S3 bucket
* S3 bucket contents
* CloudFront-related bucket policy

## Final Status

**Lab 08 - Complete and documented.**

The lab demonstrated a complete S3 + CloudFront delivery workflow, including secure origin access, HTTPS delivery, troubleshooting, testing, documentation, and cleanup.

## Repository

AWS Cloud Learning Journey:

https://github.com/Austine192-A/aws-cloud-journey
