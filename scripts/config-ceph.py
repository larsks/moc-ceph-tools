import json
import os
import jinja2

CLUSTER_DETAILS_PATH = os.getenv("CLUSTER_DETAILS_PATH", "external_cluster_details")
CEPH_CONFIG_PATH = os.getenv("CEPH_CONFIG_PATH", ".")

ceph_keyring_template = jinja2.Template(
    """[client.{{ userid }}]
key = {{ key }}

"""
)

with open(CLUSTER_DETAILS_PATH) as fd:
    details = json.load(fd)

detailmap = {x["name"]: x for x in details}

creds = detailmap["rook-ceph-operator-creds"]
userid = creds["data"]["userID"].split(".")[1]
key = creds["data"]["userKey"]
with open(os.path.join(CEPH_CONFIG_PATH, f"ceph.client.{userid}.keyring"), "w") as fd:
    fd.write(ceph_keyring_template.render(userid=userid, key=key))

for key in ["rook-csi-rbd-node", "rook-csi-rbd-provisioner"]:
    creds = detailmap[key]
    userid = creds["data"]["userID"]
    key = creds["data"]["userKey"]
    with open(
        os.path.join(CEPH_CONFIG_PATH, f"ceph.client.{userid}.keyring"), "w"
    ) as fd:
        fd.write(ceph_keyring_template.render(userid=userid, key=key))

os.execvp("sleep", ["sleep", "inf"])
