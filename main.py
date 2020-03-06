# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, jsonify, request

from alg.wind_max_calculate import *
from alg.windguru import windguru_get
from alg.function import *
from alg.outlier import *

import pandas as pd
import datetime
import warnings
from werkzeug.utils import secure_filename
warnings.simplefilter(action="ignore", category=FutureWarning)
app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static/file/input'
ALLOWED_EXTENSIONS = set(['csv', 'xls'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/favicon.ico')
def get_fav():
    print(__name__)
    return app.send_static_file('../static/img/favicon.png')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/disaster')
@app.route('/disaster.html')
def disaster():
    return render_template('disaster.html')

@app.route('/measures.html')
def get_measures_html():
    return render_template("measures.html")


@app.route('/weather.html')
def get_weather_html():
    return render_template("weather.html")

@app.route('/windpower.html')
def get_windpower_html():
    return render_template("windpower.html")

@app.route('/earthquake')
@app.route('/earthquake.html')
def get_earthquake_html():
    return render_template("earthquake.html")

@app.route('/flood')
@app.route('/flood.html')
def get_flood_html():
    return render_template("flood.html")

@app.route('/seawave')
@app.route('/seawave.html')
def get_seawave_html():
    return render_template("seawave.html")

@app.route('/meteorology')
@app.route('/meteorology.html')
def get_meteorology_html():
    return render_template("meteorology.html")

@app.route('/newpneumonia')
@app.route('/newpneumonia.html')
def get_newpneumonia_html():
    return render_template("newpneumonia.html")



@app.route('/weather', methods=['GET', 'POST'])
def weather():
    r = get_weather()
    if r['status'] != 0:
        return "get weather fail"
    else:
        result = r['result']
        out = ""
        out += result['city'] + ': '
        out += result['date'] + " " + result['week'] + ', '
        out += "天气" + result['weather'] + "，当前温度" + result['temp'] + "℃, 整日温度范围:" \
               + result['templow'] + '~' + result['temphigh'] + "℃ ,"
        out += "风速：" + result['windspeed'] + "，风向：" + result['winddirect'] + " " + result['windpower']
        # print(out)
        return jsonify(out)

@app.route('/windcalc', methods=['GET', 'POST'])
def windcalc():
    parent_path = os.getcwd()
    web_path = '/static/file'
    filename = 'config.json'
    encode = 'utf-8'
    f = open(filename, mode='r', encoding=encode, errors='ignore')#ISO-8859-1
    text = f.read()
    f.close()
    cfg = json.loads(text)
    folder = cfg['datafolder']
    datapath = parent_path + web_path+ '/' + folder + '/'
    df_origin = readAXX(datapath)
    df = wind_calc(df_origin)
    df_fault = pd.read_excel('ExcelInfo/故障列表提示内容.xls')
    error_df = outliersDetectin(df_origin)
    ###############################结果输出到文件夹#######################
    ouputpath = parent_path + web_path + '/' + cfg['output'] + '/'
    if not os.path.exists(ouputpath):
        os.makedirs(ouputpath)
    filetime = str(df['时间'].min())
    ouputfile_name = ouputpath + '/' + filetime + '-output_max.xlsx'
    df.to_excel(ouputfile_name,index=False)  # 将该对象按照Excel输出，Excel文件名为参数，默认保存到当前路径下
    # 异常值保存
    outlierfile_name = ouputpath + '/' + filetime + '-error_info.xlsx'
    error_df.to_excel(outlierfile_name, index=False)  # 将该对象按照Excel输出，Excel文件名为参数，默认保存到当前路径下

    cfg['ouputfile_name'] = ouputfile_name
    cfg['outlierfile_name'] = outlierfile_name
    with open(filename, 'w', encoding=encode, errors='ignore') as f:#ISO-8859-1
        json.dump(cfg, f)
    f.close()
    error_info = fixinfo(df_origin, df_fault)
    result = {}
    result['error_info'] = error_info
    result['filename'] = filetime + '-output_max.xlsx'
    return jsonify(result)

@app.route('/winddir', methods=['GET', 'POST'])
def winddir():
    result = windguru_get()
    return jsonify(result)

@app.route('/workinfo', methods=['GET', 'POST'])
def workinfo():
    df = pd.read_excel('ExcelInfo/风电场日常工作提醒内容.xls')
    today = datetime.date.today()
    tmp = df[df['日期'] == str(today)]['定期工作']
    rr = str(tmp.values[0]).replace("\n", '</br>')
    return jsonify(rr)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload.html', methods=['GET'])
def upload_html():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        for file in request.files.getlist('file'):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)