# Flask Blog Application

A modern, full-stack web blogging platform built with Flask, MySQL, and Bootstrap. This application provides a complete content management system with user authentication, responsive design, and secure CRUD operations for blog posts.

![Flask](https://img.shields.io/badge/Flask-3.0.3-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![Python](https://img.shields.io/badge/Python-3.7+-green)

## 🌟 Features

- **User Authentication**: Secure registration and login system with password hashing
- **Blog Management**: Create, read, update, and delete blog posts
- **Responsive Design**: Mobile-first design using Bootstrap 5
- **Security**: SQL injection prevention, secure password hashing, session management
- **Modern UI**: Clean, gradient-based interface with card layouts
- **Input Validation**: Comprehensive form validation and error handling

## 🏗️ System Architecture

The application follows the **Model-View-Controller (MVC)** pattern:

- **Model**: MySQL database with user registration and blog posts tables
- **View**: Jinja2 templates for dynamic HTML rendering
- **Controller**: Flask routes handling HTTP requests and business logic

## 📊 Database Schema

```sql
-- User Registration Table
CREATE TABLE registration (
    username VARCHAR(50) PRIMARY KEY,
    mobile VARCHAR(20) UNIQUE,
    email VARCHAR(50) UNIQUE,
    address VARCHAR(100),
    password VARCHAR(200)
);

-- Blog Posts Table
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    slug VARCHAR(200)
);
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- MySQL Server 8.0 or higher
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/syamprasadbairapuneni/Blog_Site.git
   cd Blog_Site
   ```

2. **Create virtual environment**
   ```bash
   python -m venv blog_env
   
   # On Linux/Mac
   source blog_env/bin/activate
   
   # On Windows
   blog_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install Flask==3.0.3 mysql-connector-python==9.0.0 Werkzeug==3.0.3
   ```

4. **Configure database**
   - Start your MySQL server
   - Update the `DB_CONFIG` in `app.py` with your MySQL credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'your_database'
   }
   ```

5. **Create database tables**
   ```sql
   -- Run these commands in your MySQL client
   CREATE DATABASE your_database;
   USE your_database;
   
   CREATE TABLE registration (
       username VARCHAR(50) PRIMARY KEY,
       mobile VARCHAR(20) UNIQUE,
       email VARCHAR(50) UNIQUE,
       address VARCHAR(100),
       password VARCHAR(200)
   );
   
   CREATE TABLE posts (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(200),
       content TEXT,
       slug VARCHAR(200)
   );
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
flask-blog/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # Jinja2 templates
│   ├── homepage.html     # Base template and homepage
│   ├── navbar.html       # Navigation component
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── add_post.html     # Create post form
│   ├── viewpost.html     # Display all posts
│   └── update.html       # Edit post form
└── blog_env/             # Virtual environment (created during setup)
```

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Backend Framework | Flask | 3.0.3 |
| Database | MySQL | 8.0+ |
| Frontend | Bootstrap | 5.3.0 |
| Template Engine | Jinja2 | Built into Flask |
| Password Security | Werkzeug | 3.0.3 |
| Database Connector | mysql-connector-python | 9.0.0 |

## 🔐 Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **SQL Injection Prevention**: Parameterized queries for all database operations
- **Session Management**: Secure Flask sessions with proper logout handling
- **Input Validation**: Comprehensive form validation and sanitization
- **Authentication Protection**: Login required decorator for protected routes

## 📱 Routes

### Public Routes
- `GET /` or `/home` - Homepage
- `GET /register` - Registration form
- `POST /register` - Process registration
- `GET /login` - Login form
- `POST /login` - Process login
- `GET /viewpost` - View all blog posts

### Protected Routes (Login Required)
- `GET /addposts` - Create new post form
- `POST /addposts` - Process new post creation
- `GET /update_post/<id>` - Edit post form
- `POST /update_post/<id>` - Process post update
- `POST /delete_post/<id>` - Delete post
- `GET /logout` - Logout user

## 🧪 Testing

To test the application:

1. **User Registration**: Create a new account with valid credentials
2. **Authentication**: Test login/logout functionality
3. **Blog Operations**: Create, view, edit, and delete posts
4. **Security**: Verify protection on authenticated routes
5. **Responsive Design**: Test on different screen sizes

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use environment variables for sensitive data
   ```python
   import os
   
   DB_CONFIG = {
       'host': os.getenv('DB_HOST', 'localhost'),
       'user': os.getenv('DB_USER', 'root'),
       'password': os.getenv('DB_PASSWORD'),
       'database': os.getenv('DB_NAME')
   }
   
   app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')
   ```

2. **HTTPS**: Enable SSL/TLS for production
3. **Database**: Use connection pooling for better performance
4. **Logging**: Implement proper error logging and monitoring

## 🔮 Future Enhancements

- [ ] User roles and permissions system
- [ ] Comment system for blog posts
- [ ] Post categories and tags
- [ ] Search functionality
- [ ] User profile management
- [ ] Email notifications
- [ ] RESTful API implementation
- [ ] Unit and integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you encounter any problems or have suggestions, please [open an issue](https://github.com/yourusername/flask-blog/issues).

## 📞 Support

For support and questions:
- Create an issue in this repository
- Contact: [syamprasadbairapuneni@gmail.com](mailto:syamprasadbairapuneni@gmail.com)

---

**Built with ❤️ using Flask, MySQL, and Bootstrap**
