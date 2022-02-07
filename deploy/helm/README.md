For a simple testing on AWS EKS, you can use the following chart values to simplify and remove most of the complexity.

```
hub:
    storageClass: aws-efs
    service:
        type: LoadBalancer
    ingress:
        enabled: false
    wipp:
        enabled: false
    polusNotebooksHub:
        enabled: false
postgresql:
  enabled: true
```
