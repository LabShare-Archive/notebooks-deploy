## Test deployment

For a simple testing, you can use the following chart values to simplify and remove most of the complexity.

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

## Production deployment

### Configure ingress

### Configure LS Auth

Make sure that LS Auth redirect URL is pointing to ingress URL
