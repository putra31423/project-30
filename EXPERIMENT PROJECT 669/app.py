from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import db
from models import Inquiry, AuditLog
import os

app = Flask(__name__)
# SECURITY WARNING: Keep the secret key used in production secret!
# In a real application, use: os.environ.get('SECRET_KEY', 'default_dev_key')
app.secret_key = 'your_secret_key_here'

# Admin Credentials
# SECURITY WARNING: Do not hardcode passwords in production!
# Use environment variables or a database for user management.
ADMIN_USERNAME = 'Putra1944'
ADMIN_PASSWORD = 'YeSSir1866'

# Use an absolute path for the database to avoid issues
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'surf_instructor.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for static files

db.init_app(app)

# Create database tables within app context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/admin/api/emails', methods=['GET', 'POST'])
def admin_emails():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)

        query = Inquiry.query
        if search:
            query = query.filter(
                (Inquiry.name.ilike(f'%{search}%')) |
                (Inquiry.message.ilike(f'%{search}%')) |
                (Inquiry.email.ilike(f'%{search}%'))
            )
        
        pagination = query.order_by(Inquiry.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'emails': [email.to_dict() for email in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })

    if request.method == 'POST':
        data = request.get_json()
        try:
            new_email = Inquiry(
                name=data['name'],
                email=data['email'],
                level=data.get('level', 'Beginner'),
                message=data['message']
            )
            db.session.add(new_email)
            
            # Log Audit
            log = AuditLog(action='ADD', details=f"Added email for {data['email']}")
            db.session.add(log)
            
            db.session.commit()
            return jsonify({'message': 'Email added successfully', 'email': new_email.to_dict()}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/admin/api/emails/<int:id>', methods=['DELETE'])
def delete_email_api(id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    inquiry = Inquiry.query.get_or_404(id)
    try:
        email_addr = inquiry.email
        db.session.delete(inquiry)
        
        # Log Audit
        log = AuditLog(action='DELETE', details=f"Deleted email from {email_addr}")
        db.session.add(log)
        
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/audit-logs', methods=['GET'])
def get_audit_logs():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(50).all()
    return jsonify([log.to_dict() for log in logs])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/inquiry', methods=['POST'])
def create_inquiry():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'email', 'level']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        new_inquiry = Inquiry(
            name=data['name'],
            email=data['email'],
            level=data['level'],
            message=data.get('message', '')
        )
        db.session.add(new_inquiry)
        db.session.commit()
        return jsonify({'message': 'Inquiry received successfully!', 'data': new_inquiry.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)



