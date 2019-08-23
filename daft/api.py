from flask import Flask, request
from flask_restful import Resource, Api

from daft.dataset_access import load_datasets

DAFT_PORT = 6661

app = Flask(__name__)
daft = Api(app)

datasets = {}

class Entry(Resource):
    def get(self, dataset_name, id_):

        if id_.isdigit():
            id_ = str(int(id_))

        ds = datasets[dataset_name]
        data = ds[id_]

        return { 
            "dataset": dataset_name,
            "entry": data
        }

class Dataset(Resource):
    def get(self, dataset_name):

        ds = datasets[dataset_name]
        ids = ds.all_ids()

        return { 
            "dataset": dataset_name,
            "entryCount": len(ids),
            "ids": ids
        }

class MobygamesBySlug(Resource):
    def get(self, slug):
        data = datasets['mobygames'].get_item_by_slug(slug)

        return { 
            "dataset": "mobygames",
            "entry": data
        }

daft.add_resource(Dataset, '/<string:dataset_name>')
daft.add_resource(Entry, '/<string:dataset_name>/<id_>')
daft.add_resource(MobygamesBySlug, '/mobygames/slug/<string:slug>')

def start_api(host, port, debug):
    print("loading datasets ...")
    global datasets 
    datasets = load_datasets()

    print("starting api ...")
    app.run(
        host=host,
        port=port,
        debug=debug
    )
