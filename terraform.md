Questions:
---

1).I have provisioned the aws resources using terraform the infra is in place but someone from my team has modified the infra manually (instance type from t2.large to m5.xlarge) from console how can i identify and ensure the state file is upto date?
This is a classic Terraform drift scenario 👍 Let’s break it down clearly, step-by-step, and then I’ll give you best practices to prevent this in future.

What happened (Problem)
Infrastructure was provisioned using Terraform

Someone manually modified the resource from AWS Console

Example: t2.large → m5.xlarge
Terraform state file still thinks the instance is t2.large
<img width="1039" height="511" alt="image" src="https://github.com/user-attachments/assets/6823078f-c6cd-47e1-aa52-726a9088ab85" />
