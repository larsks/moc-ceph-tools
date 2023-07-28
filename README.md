This is like the `rook-ceph-tools` Deployment, except it automatically configures credentials in `/etc/ceph.conf` from the `rook-ceph-external-cluster-details-secret`. For example, on our test cluster this results in:

```
bash-4.4$ ls /etc/ceph
ceph.client.healthchecker-nerc-ocp-test-1-rbd.keyring  ceph.conf
ceph.client.node-nerc-ocp-test-1-rbd.keyring           keyring
ceph.client.provisioner-nerc-ocp-test-1-rbd.keyring
```

## Placement

The deployment sets an `affinity` configuration so that you can target particular nodes by labelling the node with `moc-ceph-tools=true`. There is an anti-affinity configuration so that if you increase the number of replicas they should get scheduled on distinct nodes.
