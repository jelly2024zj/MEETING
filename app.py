from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# 会议模型
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    attendees = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

# 初始化数据库
with app.app_context():
    db.create_all()

# 返回 HTML 页面
@app.route('/')
def index():
    return render_template('index.html')

# 获取所有会议
@app.route('/meetings', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify([{
        'id': m.id, 'name': m.name, 'date': m.date,
        'time': m.time, 'attendees': m.attendees,
        'content': m.content
    } for m in meetings])

# 添加会议
@app.route('/meetings', methods=['POST'])
def add_meeting():
    data = request.json
    new_meeting = Meeting(**data)
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify({'message': '会议已添加'}), 201

# 更新会议
@app.route('/meetings', methods=['PUT'])
def update_meeting():
    data = request.json
    meeting = Meeting.query.get(data['id'])
    if not meeting:
        return jsonify({'error': '会议未找到'}), 404
    for key, value in data.items():
        setattr(meeting, key, value)
    db.session.commit()
    return jsonify({'message': '会议已更新'})

# 删除会议
@app.route('/meetings', methods=['DELETE'])
def delete_meeting():
    data = request.json
    meeting = Meeting.query.get(data['id'])
    if not meeting:
        return jsonify({'error': '会议未找到'}), 404
    db.session.delete(meeting)
    db.session.commit()
    return jsonify({'message': '会议已删除'})

if __name__ == '__main__':
    app.run(debug=True)
