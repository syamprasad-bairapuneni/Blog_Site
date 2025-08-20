from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from functools import wraps
import re
app = Flask(__name__, template_folder='templates')

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # Change this to your MySQL password
    'database': 'flaskblog'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def init_database():
    """Initialize database and create tables if they don't exist"""
    try:
        # First connect without database to create it
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database')
        
        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS flaskblog")
        cursor.close()
        connection.close()
        
        # Now connect with database and create tables
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Create registration table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registration (
                    username VARCHAR(50) PRIMARY KEY,
                    mobile VARCHAR(20) UNIQUE,
                    email VARCHAR(50) UNIQUE,
                    address VARCHAR(100),
                    password VARCHAR(200)
                )
            """)
            
            # Create posts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200),
                    content TEXT,
                    slug VARCHAR(200)
                )
            """)
            
            connection.commit()
            cursor.close()
            connection.close()
            print("Database initialized successfully!")
            
    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_slug(title):
    """Generate a URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug.strip('-')

@app.route('/')
@app.route('/home')
def home():
    """Homepage route"""
    return render_template('homepage.html')

@app.route('/reg', methods=['GET', 'POST'])
def register():
    """Registration route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([username, mobile, email, address, password]):
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        # Email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            flash('Please enter a valid email address!', 'error')
            return render_template('register.html')
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Database insertion
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO registration (username, mobile, email, address, password) VALUES (%s, %s, %s, %s, %s)",
                    (username, mobile, email, address, hashed_password)
                )
                connection.commit()
                cursor.close()
                connection.close()
                
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
                
            except mysql.connector.IntegrityError as err:
                if 'username' in str(err):
                    flash('Username already exists!', 'error')
                elif 'mobile' in str(err):
                    flash('Mobile number already registered!', 'error')
                elif 'email' in str(err):
                    flash('Email already registered!', 'error')
                else:
                    flash('Registration failed. Please try again.', 'error')
                connection.close()
            except mysql.connector.Error as err:
                flash('Database error occurred. Please try again.', 'error')
                connection.close()
        else:
            flash('Database connection failed!', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return render_template('login.html')
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT password FROM registration WHERE username = %s", (username,))
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if result and check_password_hash(result[0], password):
                    session['username'] = username
                    flash(f'Welcome back, {username}!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid username or password!', 'error')
                    
            except mysql.connector.Error as err:
                flash('Database error occurred. Please try again.', 'error')
                connection.close()
        else:
            flash('Database connection failed!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/addposts', methods=['GET', 'POST'])
@login_required
def add_posts():
    """Add new blog post route"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return render_template('add_post.html')
        
        slug = generate_slug(title)
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO posts (title, content, slug) VALUES (%s, %s, %s)",
                    (title, content, slug)
                )
                connection.commit()
                cursor.close()
                connection.close()
                
                flash('Post added successfully!', 'success')
                return redirect(url_for('view_posts'))
                
            except mysql.connector.Error as err:
                flash('Error adding post. Please try again.', 'error')
                connection.close()
        else:
            flash('Database connection failed!', 'error')
    
    return render_template('add_post.html')

@app.route('/viewpost')
def view_posts():
    """View all blog posts route"""
    connection = get_db_connection()
    posts = []
    
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, title, content, slug FROM posts ORDER BY id DESC")
            posts = cursor.fetchall()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            flash('Error retrieving posts.', 'error')
            connection.close()
    else:
        flash('Database connection failed!', 'error')
    
    return render_template('viewpost.html', posts=posts)

@app.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """Update blog post route"""
    connection = get_db_connection()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('update_post', post_id=post_id))
        
        slug = generate_slug(title)
        
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE posts SET title = %s, content = %s, slug = %s WHERE id = %s",
                    (title, content, slug, post_id)
                )
                connection.commit()
                cursor.close()
                connection.close()
                
                flash('Post updated successfully!', 'success')
                return redirect(url_for('view_posts'))
                
            except mysql.connector.Error as err:
                flash('Error updating post. Please try again.', 'error')
                connection.close()
        else:
            flash('Database connection failed!', 'error')
    
    # GET request - fetch post data
    post = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, title, content FROM posts WHERE id = %s", (post_id,))
            post = cursor.fetchone()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            flash('Error retrieving post.', 'error')
            connection.close()
    
    if not post:
        flash('Post not found!', 'error')
        return redirect(url_for('view_posts'))
    
    return render_template('update.html', post=post)

@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    """Delete blog post route"""
    connection = get_db_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Post deleted successfully!', 'success')
            
        except mysql.connector.Error as err:
            flash('Error deleting post. Please try again.', 'error')
            connection.close()
    else:
        flash('Database connection failed!', 'error')
    
    return redirect(url_for('view_posts'))

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)