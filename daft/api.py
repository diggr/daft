from flask import Flask, request
from flask_restful import Resource, Api

from daft.dataset_access import load_datasets

app = Flask(__name__)
daft = Api(app)

#get dataset access
datasets = load_datasets()

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
            "entryCount": len(ids)
        }

daft.add_resource(Dataset, '/<string:dataset_name>')
daft.add_resource(Entry, '/<string:dataset_name>/<id_>')

def start_api():
    print("starting api")
    app.run(debug=True)