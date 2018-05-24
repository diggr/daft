import zipfile
import json


class MobygamesData(object):

    def __init__(self, filepath):
        self._filepath = filepath

    def __getitem__(self, id_):
        """
        Returns mobygames dataset with id :id_:
        """
        with zipfile.ZipFile(self._filepath) as zf:
            filename = "{}.json".format(id_)
            with zf.open(filename) as f:
                data = f.read().decode("utf-8")
                return json.loads(data)

    def __iter__(self):
        """
        Iterator over mobygames dataset
        """
        with zipfile.ZipFile(self._filepath) as zf:
            for filename in zf.namelist():
                with zf.open(filename) as f:
                    data = f.read().decode("utf-8")
                    yield json.loads(data)

    def source_file(self):
        return self._filepath
        