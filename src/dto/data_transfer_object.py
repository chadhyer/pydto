import json
import yaml

from jsonschema import validate

from json.decoder import JSONDecodeError


class DataTransferObject:
    def __init__(
            self,
            d: dict | str | None = None,
            s: dict = {},
            sk: list[str] = [],
            **kwargs
        ) -> None:
        """Inherit to create a object capable of dict, JSON, YAML input/output

        Args:
            d (dict | str | None, optional):
                Python dictionary, JSON string, or YAML string data that will
                    construct the object
                Defaults to None
            s (dict, optional):
                Dictionary that describes objects data structure and validates
                    via jsonschema.validate
                Defaults to {}
            sk (list[str], optional):
                List of strings that indicate what keys in the d to skip
                Defaults to []
        """
        if d:
            d = self._convert(d)
            self._ingest(d, sk)
            validate(d,s)
        if not d:
            sk.append('d')
            self._ingest(kwargs, sk=sk)
            validate(self.data(),s)

    def _convert(self, d: dict | str) -> dict:
        if isinstance(d,str):
            try:
                d = yaml.safe_load(d)
            except Exception:
                pass
        if isinstance(d,str):
            try:
                d = json.loads(d)
            except JSONDecodeError:
                raise ValueError('Valid python dictionary or JSON/YAML \
formatted string required!')
        if isinstance(d,str):
            raise ValueError('Failed to convert d to a dictionary')
        return d

    def _ingest_dto(self, k,v) -> None:
        pass

    def _ingest(self, d: dict, sk: list[str] = []) -> None:
        for k,v in d.items():
            if k in sk:
                continue
            self.__dict__[k] = v
            self._ingest_dto(k,v)

    def _build(self, sk: list[str] = []) -> dict:
        d = {}
        for k,v in self.__dict__.items():
            if k in sk or k == 'sk':
                continue
            if isinstance(v,DataTransferObject):
                v = v.data()
            if isinstance(v,list):
                if [True for i in v if isinstance(i,DataTransferObject)]:
                    v = self._list_data(v)
            d[k] = v
        return d

    @staticmethod
    def _list_data(lt: list) -> list:
        return [i.data() for i in lt if isinstance(i,DataTransferObject)]

    def data(self) -> dict:
        """Dump object data into a python dictionary
        Returns: dict"""
        return self._build()
    
    def json(self) -> str:
        """Dump object data into a JSON formatted string
        Returns: str"""
        return json.dumps(self._build())
    
    def yaml(self) -> str:
        """Dump object data into a YAML formatted string
        Returns: str"""
        return yaml.dump(self._build())
