from flask import Flask, request, jsonify, send_file, render_template
import os
import csv

app = Flask(__name__)

data_file = 'attendance_data.csv'

# 初始化 CSV 檔案（如果不存在）並添加初始數據
def initialize_csv():
    if not os.path.exists(data_file):
        with open(data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['姓名', '狀態'])
            # 預設10個學生
            initial_students = [
                ['王小明', '未點名'],
                ['李小華', '未點名'],
                ['張大衛', '未點名'],
                ['林美美', '未點名'],
                ['陳志強', '未點名'],
                ['黃曉東', '未點名'],
                ['趙小雨', '未點名'],
                ['孫小婷', '未點名'],
                ['周偉豪', '未點名'],
                ['吳依琳', '未點名']
            ]
            writer.writerows(initial_students)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_students', methods=['GET'])
def get_students():
    if not os.path.exists(data_file):
        initialize_csv()

    students = []
    with open(data_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        students = [{'name': row[0], 'status': row[1]} for row in reader]
    return jsonify(students)

@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': '未提供任何數據'}), 400

        with open(data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['姓名', '狀態'])
            for student in data:
                writer.writerow([student['name'], student['status']])

        return jsonify({'message': '數據已成功保存！'}), 200
    except Exception as e:
        return jsonify({'message': f'發生錯誤: {str(e)}'}), 500

@app.route('/export', methods=['GET'])
def export_data():
    try:
        if not os.path.exists(data_file):
            return jsonify({'message': '沒有找到數據檔案，請先保存數據！'}), 404

        return send_file(data_file, as_attachment=True, download_name='attendance_report.csv', mimetype='text/csv')
    except Exception as e:
        return jsonify({'message': f'發生錯誤: {str(e)}'}), 500

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': '請提供學生姓名！'}), 400

        name = data['name']
        with open(data_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, '未點名'])

        return jsonify({'message': f'學生 {name} 已成功新增！'}), 200
    except Exception as e:
        return jsonify({'message': f'發生錯誤: {str(e)}'}), 500

@app.route('/delete_student', methods=['POST'])
def delete_student():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': '請提供學生姓名！'}), 400

        name = data['name']
        if not os.path.exists(data_file):
            return jsonify({'message': '數據檔案不存在！'}), 404

        students = []
        deleted = False
        with open(data_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == name:
                    deleted = True
                else:
                    students.append(row)

        if not deleted:
            return jsonify({'message': f'未找到學生 {name}，無法刪除！'}), 404

        with open(data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(students)

        return jsonify({'message': f'學生 {name} 已成功刪除！'}), 200
    except Exception as e:
        return jsonify({'message': f'發生錯誤: {str(e)}'}), 500

if __name__ == '__main__':
    initialize_csv()
    app.run(debug=True)
