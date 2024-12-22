from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

data_file = 'students.xlsx'

# 初始化 Excel 檔案（如果不存在）並添加初始數據
def initialize_excel():
    if not os.path.exists(data_file):
        data = {'姓名': ['王小明', '李小華', '張大衛', '林美美', '陳志強', 
                       '黃曉東', '趙小雨', '孫小婷', '周偉豪', '吳依琳'],
                '狀態': ['未點名'] * 10}
        df = pd.DataFrame(data)
        df.to_excel(data_file, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_students', methods=['GET'])
def get_students():
    if not os.path.exists(data_file):
        initialize_excel()

    df = pd.read_excel(data_file)
    students = df.to_dict(orient='records')  # 轉換為列表形式
    return jsonify(students)

@app.route('/update_students', methods=['POST'])
def update_students():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': '未提供任何數據'}), 400

        df = pd.DataFrame(data)
        df.to_excel(data_file, index=False)

        return jsonify({'message': '點名數據已成功保存！'}), 200
    except Exception as e:
        return jsonify({'message': f'發生錯誤: {str(e)}'}), 500

@app.route('/export', methods=['GET'])
def export_data():
    try:
        if not os.path.exists(data_file):
            return jsonify({'message': '數據檔案不存在！'}), 404

        return send_file(data_file, as_attachment=True, download_name='attendance_report.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        return jsonify({'message': f'發生錯誤: {str(e)}'}), 500

if __name__ == '__main__':
    initialize_excel()
    app.run(debug=True)
