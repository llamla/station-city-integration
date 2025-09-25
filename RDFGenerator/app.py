from flask import Flask, render_template, request, send_file, jsonify, url_for
import os
from convert_functions import env_csv_to_rdf, energy_csv_to_rdf, flow_csv_to_rdf, struct_csv_to_rdf

app = Flask(__name__)

# 配置文件上传和下载路径
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# 设置 secret_key，用于 session 和 flash 消息的加密
app.config['SECRET_KEY'] = 'your_secret_key'  # 确保使用一个强的秘钥，这里

# 确保上传目录和输出目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 转换文件函数调用的映射
convert_map = {
    "env": env_csv_to_rdf.create_owl_from_csv,
    "struct": struct_csv_to_rdf.create_owl_from_csv,
    "flow": flow_csv_to_rdf.create_owl_from_csv,
    "energy": energy_csv_to_rdf.create_owl_from_csv,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert/<type>', methods=['POST'])
def convert(type):
    if type not in convert_map:
        return jsonify({'status': 'error', 'message': '无效的转换类型！'})

    # 获取上传的文件
    file = request.files.get(f'{type}_file')
    if not file:
        return jsonify({'status': 'error', 'message': '没有文件部分！'})
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '没有选择文件！'})
    if not file.filename.endswith('.csv'):
        return jsonify({'status': 'error', 'message': '仅支持CSV文件！'})

    # 保存文件
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # 转换文件
    output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{file.filename}.rdf")
    try:
        convert_map[type](filename, output_file)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"转换失败：{str(e)}"})

    # 返回成功消息和下载链接
    return jsonify({'status': 'success', 'message': '文件转换成功！', 'file_url': url_for('download', filename=f"{file.filename}.rdf")})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
