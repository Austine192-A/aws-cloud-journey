# Lab 01 — Static Website Hosting with Amazon S3

## Overview

As part of my AWS Cloud Learning Journey, I built and deployed a simple static website using **Amazon S3**.

The goal of this lab was to understand the fundamentals of AWS object storage, S3 buckets, static website hosting, object management, and basic cloud deployment.

## Objective

* Create and configure an Amazon S3 bucket
* Upload static website files to S3
* Configure static website hosting
* Deploy a website using an S3 website endpoint
* Test the deployed website
* Practice managing and cleaning up AWS resources

## AWS Services Used

* **Amazon S3** — Object storage and static website hosting

## Architecture

```text
Local Website
     │
     │ Upload
     ▼
Amazon S3 Bucket
     │
     │ Static Website Hosting
     ▼
S3 Website Endpoint
     │
     ▼
     Browser
```

## What I Built

I created a simple static website containing:

* HTML structure
* Custom CSS styling
* AWS Cloud Learning Journey information
* A section describing what I was learning
* Responsive layout for different screen sizes

The website was then uploaded to an Amazon S3 bucket and configured for static website hosting.

## Implementation Steps

### 1. Created an S3 Bucket

I created a dedicated S3 bucket for the lab and configured it in my selected AWS Region.

### 2. Created the Website

The website was built locally using:

* HTML
* CSS

The main files were:

```text
index.html
style.css
```

### 3. Uploaded the Website to S3

The website files were uploaded directly into the S3 bucket.

The final bucket structure was:

```text
Bucket
├── index.html
└── style.css
```

### 4. Enabled Static Website Hosting

I configured the S3 bucket for static website hosting and specified:

```text
Index document: index.html
```

### 5. Tested the Deployment

After configuration, I opened the S3 website endpoint in a browser and verified that the website was successfully served from Amazon S3.

## Challenge Encountered

During deployment, the initial website endpoint returned:

```text
404 Not Found
Code: NoSuchKey
```

The issue was caused by the website files not being located at the expected root level of the S3 bucket.

I corrected the bucket structure so that `index.html` was directly inside the bucket rather than inside a folder.

After correcting the file structure, the website loaded successfully.

## Key Learnings

This lab helped me understand:

* How S3 buckets work
* How objects are stored in S3
* How S3 can be used for static website hosting
* The importance of correct object paths and file names
* How AWS resources can be configured through the AWS Management Console
* How to troubleshoot basic S3 deployment errors
* The difference between developing a website locally and deploying it to the cloud
* The importance of cleaning up temporary cloud resources after completing a lab

## Result

The static website was successfully deployed and accessed through an Amazon S3 website endpoint.

**Status: Completed**

## Cost & Resource Management

This was a learning environment using the AWS Free account.

After documenting and testing the deployment, the temporary S3 resources will be removed to avoid unnecessary ongoing resource usage.

## Cleanup Plan

After completing the documentation:

1. Delete the website objects from the S3 bucket.
2. Delete the S3 bucket.
3. Verify that the bucket has been removed.
4. Confirm that no additional AWS resources were created for this lab.

## Next Lab

**Lab 02 — Deploying a Node.js API on Amazon EC2**

The next stage of the AWS Cloud Learning Journey will move from static website hosting to deploying a backend application on an EC2 instance.
