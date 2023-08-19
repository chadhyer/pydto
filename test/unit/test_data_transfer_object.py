import pytest

from dto import DTO

from jsonschema.exceptions import ValidationError

class ExampleClass(DTO):
    def __init__(self, d: dict | str | None = None, **kwargs) -> None:
        s = {
            "type":"object",
            "required":["b","s","i","a","o"],
            "properties":{
                "b":{"type":"boolean"},
                "s":{"type":"string"},
                "i":{"type":"integer"},
                "a":{"type":"array"},
                "o":{"type":"object"}
            }
        }
        super().__init__(d, s, **kwargs)

parameters = ["input_","output_"]
# Test data, json, yaml method output
expected_output = [
    {'a': [1], 'b': True, 'i': 0, 'o': {'f': 'f'}, 's': 'string'},
    '{"a": [1], "b": true, "i": 0, "o": {"f": "f"}, "s": "string"}',
    '''a:
- 1
b: true
i: 0
o:
  f: f
s: string
'''
]
tests = [
    ({'a':[1],'b':True,'i':0,'o':{'f':'f'},'s':'string'},
    expected_output),
    ('{"a": [1], "b": true, "i": 0, "o": {"f": "f"}, "s": "string"}',
    expected_output),
    ('''a:
- 1
b: true
i: 0
o:
  f: f
s: string
''', expected_output),
    ("{'a':[1],'b':True,'i':0,'o':{'f':'f'},'s':'string'}",
    expected_output)
]
@pytest.mark.parametrize(", ".join(parameters), tests)
def test_DataTransferObject_data_json_yaml_output(input_, output_):
    test_class = ExampleClass(input_)
    assert test_class.data() == output_[0]
    assert test_class.json() == output_[1]
    assert test_class.yaml() == output_[2]

# Test exception
value_error = 'Valid python dictionary or JSON/YAML formatted string required!'
tests = [
    ({'b':True,'i':0,'o':{'f':'f'},'s':'string'},
    [ValidationError,"'a' is a required property"]),
    ('{"b":true,"i":0,"o":{"f":"f"},"s":"string"}',
    [ValidationError,"'a' is a required property"]),
    ('''b: true
i: 0
o:
  f: f
s: string''', [ValidationError,"'a' is a required property"]),
    ({'a':[1,2,3],'i':0,'o':{'f':'f'},'s':'string'},
    [ValidationError,"'b' is a required property"]),
    ('{"a":[1,2,3],"i":0,"o":{"f":"f"},"s":"string"}',
    [ValidationError,"'b' is a required property"]),
    ('''a:
- 1
i: 0
o:
  f: f
s: string''', [ValidationError,"'b' is a required property"]),
    ({'a':[1,2,3],'b':True,'o':{'f':'f'},'s':'string'},
    [ValidationError,"'i' is a required property"]),
    ('{"a":[1,2,3],"b":true,"o":{"f":"f"},"s":"string"}',
    [ValidationError,"'i' is a required property"]),
    ('''a:
- 1
b: true
o:
  f: f
s: string''', [ValidationError,"'i' is a required property"]),
    ({'a':[1,2,3],'b':True,'i':0,'s':'string'},
        [ValidationError,"'o' is a required property"]),
    ('{"a":[1,2,3],"b":true,"i":0,"s":"string"}',
        [ValidationError,"'o' is a required property"]),
    ('''a:
- 1
b: true
i: 0
s: string''', [ValidationError,"'o' is a required property"]),
    ({'a':[1,2,3],'b':True,'i':0,'o':{'f':'f'}},
        [ValidationError,"'s' is a required property"]),
    ('{"a":[1,2,3],"b":true,"i":0,"o":{"f":"f"}}',
        [ValidationError,"'s' is a required property"]),
    ('''a:
- 1
b: true
i: 0
o:
  f: f''', [ValidationError,"'s' is a required property"]),
    ("{a:[1,2,3],b:True,i:0,o:{f:f},s:string}",
    (ValidationError,"'b' is a required property")),
    ({'a':1,'b':True,'i':0,'o':{'f':'f'},'s':'string'},
    (ValidationError,"1 is not of type 'array'")),
    ('''a: 1
b: true
i: 0
o:
  f: f
s: s
''', (ValidationError,"1 is not of type 'array'")),
    ({'a':[1,2,3],'b':1,'i':0,'o':{'f':'f'},'s':'string'},
    (ValidationError,"1 is not of type 'boolean'")),
    ('''a:
- 1
b: 1
i: 0
o:
  f: f
s: s
''', (ValidationError,"1 is not of type 'boolean'")),
    ({'a':[1,2,3],'b':True,'i':'1','o':{'f':'f'},'s':'string'},
    (ValidationError,"'1' is not of type 'integer'")),
    ('''a:
- 1
b: true
i: '1'
o:
  f: f
s: s
''', (ValidationError,"'1' is not of type 'integer'")
    ),
    ({'a':[1,2,3],'b':True,'i':0,'o':1,'s':'string'},
    (ValidationError,"1 is not of type 'object'")),
    ('''a:
- 1
b: true
i: 1
o: 1
s: s
''', (ValidationError,"1 is not of type 'object'")),
    ({'a':[1,2,3],'b':True,'i':0,'o':{'f':'f'},'s':1},
    (ValidationError,"1 is not of type 'string'")),
    ('''a:
- 1
b: true
i: 1
o:
  f:
s: 1
''', (ValidationError,"1 is not of type 'string'")),
    ('''a:1
b:true
i:0
o:
s:s
'''
        "'a':[1,2,3],'b':True,'i':0,'o':{'f':'f'},'s':1",
        (ValueError,value_error)),
    ('''a:,
- 1
- 2
- 3
b: true
i: 0
o:
  f: f
s: string
''', (ValueError,value_error)),
    ('a:[1,2,3],b:True,i:0,o:{f:f},s:s',
    (ValueError,value_error)),
]
@pytest.mark.parametrize(", ".join(parameters), tests)
def test_DataTransferObject_error(input_, output_):
    with pytest.raises(Exception) as exception:
        ExampleClass(input_)
    assert exception.type == output_[0]
    assert exception.value.args[0] == output_[1]


class ChildExampleClass(DTO):
    def __init__(self, d: dict | str | None = None, **kwargs) -> None:
        s = {
            "type":"object",
            "required":["i"],
            "properties":{
                "i":{"type":"integer"}
            }
        }
        super().__init__(d, s, **kwargs)


class ParentExampleClass(DTO):
    def __init__(self, d: dict | str | None = None, **kwargs) -> None:
        s = {
            "type":"object",
            "required":["ChildExampleClass","Childs"],
            "properties":{
                "ChildExampleClass":{"type":"object"},
                "Childs":{"type":"array"}
            }
        }
        super().__init__(d, s, **kwargs)
    
    def _ingest_dto(self, k, v):
        if k == 'ChildExampleClass':
            self.ChildExampleClass = ChildExampleClass(d=v)
        if k == 'Childs':
            self.Childs = []
            for i in v:
                self.Childs.append(ChildExampleClass(d=i))

tests = [
    (
        {'i':1},
        [
            {'ChildExampleClass': {'i': 1}, 'Childs': [{'i': 1}, {'i': 1}]},
            '{"ChildExampleClass": {"i": 1}, "Childs": [{"i": 1}, {"i": 1}]}',
            '''ChildExampleClass:
  i: 1
Childs:
- i: 1
- i: 1
'''
        ]
    ),
]
@pytest.mark.parametrize(", ".join(parameters), tests)
def test_DataTransferObject_data_json_yaml_child_output(input_, output_):
    print('input_',input_)
    print('output_',output_)
    child = ChildExampleClass(input_)
    data = {
        'ChildExampleClass':child.data(),'Childs':[child.data(),child.data()]
    }
    parent = ParentExampleClass(d=data)

    assert parent.data() == output_[0]
    assert parent.ChildExampleClass.data() == output_[0]['ChildExampleClass']
    assert parent.Childs[0].data() == output_[0]['Childs'][0]
    assert parent.json() == output_[1]
    assert parent.yaml() == output_[2]

    parent = ParentExampleClass(
        ChildExampleClass=ChildExampleClass(input_).data(),
        Childs=[
            ChildExampleClass(input_).data(),
            ChildExampleClass(input_).data()
        ]
    )

    assert parent.data() == output_[0]
    assert parent.ChildExampleClass.data() == output_[0]['ChildExampleClass']
    assert parent.Childs[0].data() == output_[0]['Childs'][0]
    assert parent.json() == output_[1]
    assert parent.yaml() == output_[2]