import json, numpy
from json import JSONEncoder
import pandas as pd

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


w =  '{ "block_name":"sample_block_0", "channel_tag":["f","e","b"] }'
x =  '{ "block_name":"sample_block_1", "channel_tag":["a","b","c"] }'
y =  '{ "block_name":"sample_block_2", "channel_tag":["c"] }'
z =  '{ "block_name":"sample_block_3", "channel_tag":["d","b","e"] }'

w = json.loads(w)
x = json.loads(x)
y = json.loads(y)
z = json.loads(z)

block1 = pd.DataFrame(w)
block2 = pd.DataFrame(x)
block3 = pd.DataFrame(y)
block4 = pd.DataFrame(z)

blocks = block1.append(block2)
blocks = blocks.append(block3)
blocks = blocks.append(block4)

def find_channel_tags(param):
    channel_tags = blocks[blocks['block_name']==param]['channel_tag'].values.tolist()
    return channel_tags

def find_related_blocks_from_tags(param):
    if type(param) is str:
        related_channels = blocks[blocks['channel_tag'] == param]
    elif type(param) is list:
        related_channels = blocks[blocks['channel_tag'].isin(param)]
    else:
        related_channels = ''
    return related_channels

def find_unique_blocks(df, column, exception):
    related_blocks = df[df[column] != exception]
    return related_blocks[column].unique()

def find_related_blocks_from_blocks(param):
    rel_tags = find_channel_tags(param)
    rel_blocks = find_related_blocks_from_tags(rel_tags)
    rel_blocks = find_unique_blocks(rel_blocks, 'block_name', param)
    return json.dumps(rel_blocks, cls=NumpyArrayEncoder)