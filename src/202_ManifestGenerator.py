import sys
import urllib
import json
import argparse
import requests
import os
import shutil
import glob

prefix_1 = "http://gazo.dl.itc.u-tokyo.ac.jp/hiraga2"
prefix_2 = "../docs"
prefix_3 = "https://raw.githubusercontent.com/nakamura196/omekac_hiraga/master/docs"

def get(data_json, data_url):
    # data_json = requests.get(data_url).json()

    data_path = data_url.replace(prefix_1, prefix_2)+".json"

    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    
    with open(data_path, 'w') as outfile:
        json.dump(data_json, outfile, ensure_ascii=False,
                    indent=4, sort_keys=True, separators=(',', ': '))

files = glob.glob(prefix_2+"/api/items/*.json")

manifests = []

for file in files:
    id = file.split("/")[-1].split(".")[0]
    
    manifest_url = prefix_1 + "/iiif/"+str(id)+"/manifest"
    print(manifest_url)

    try:
        manifest_json = requests.get(manifest_url).json()
    except Exception as e:
        print(e)
        continue

    get(manifest_json, manifest_url)

    # --------

    manifests.append({
        "@id": manifest_json["@id"],
        "@type": "sc:Manifest",
        "label": manifest_json["label"]
    })


collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix_3 + "/iiif/top.json",
    "@type": "sc:Collection",
    "label" : "トップコレクション",
    "manifests": manifests
}

get(collection, "../docs/iiif/top.json")

