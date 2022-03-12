from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd

from datafetch import (preprocess_dataframe,
                       load_local_dataframe,
                       load_mongo_dataframe)

from similar_blocks import find_related_blocks_from_blocks

from forecast import forecast

app = Flask(__name__)

# @app.route('/test')
# def get_current_time():
#     return jsonify('flask connection established')


# @app.route('/testcsv/<mode>', methods=['GET'])
# def get_local_csv(mode):
#     print(mode)
    
#     if mode=='local':
#         df_table = load_local_dataframe()
#     else:
#         df_table = load_mongo_dataframe()

#     json_table = df_table.to_json(orient='split')
#     return json_table
    
@app.route('/forecast/', methods=['POST'])
def sample_forecast():
    data = request.json
    # print(data)

    date_field = data['dateField']
    value_field = data['valueField']
    df_data = pd.DataFrame.from_dict(pd.json_normalize(data['data'][0]), orient='columns')
    result = forecast(df_data, date_field , value_field)

    # df_table = load_local_dataframe()
    # json_table = df_table.to_json(orient='split')
    return result

@app.route('/related_blocks/<block_name>', methods=['GET'])
def related_blocks(block_name):
    return find_related_blocks_from_blocks(block_name)


@app.route('/save_network/',methods=['POST'])
def save_network():
    data = request.json
    print(data)
    return '0'

if __name__ == '__main__':
   app.run(port=8000, debug=True)
