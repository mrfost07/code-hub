# **CodeHub: A Django-Based Collaborative Project Management and Task Tracking System**

**CodeHub** is a robust and flexible project management system built using Django and AdminLTE3. It is designed to enhance team collaboration, streamline task tracking, and simplify project progress monitoring. With its modern interface and rich features, **CodeHub** caters to organizations, teams, and individuals aiming for efficient project workflows.

---

## **Features**
- **Kanban Board**: Drag-and-drop interface for task management.
- **Notifications**: Real-time alerts for task deadlines and updates.
- **Progress Tracking**: Automatic calculation of project progress.
- **Team Collaboration**: Assign roles and manage permissions.
- **Access Levels**: Role-based access control for users.
- **Attachments & Comments**: Upload files and communicate within tasks.
- **AdminLTE3 Integration**: Responsive and user-friendly UI design.
- **Task Deadline Alerts**: Notifications for tasks nearing expiry.
- **Customizable Templates**: Easily modify layout and design.

---

## **Technologies Used**
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, AdminLTE3
- **Database**: SQLite (default), with support for PostgreSQL and MySQL
- **Task Queue**: Celery
- **Notification System**: Redis

---

## **Screenshots**

### Dashboard View with Project Statistics
![Dashboard View](/screenshots/dashboard.png)

### Kanban Board with Tasks in Different Columns
![Kanban Board](/screenshots/kanban_board.png)

### Team View Showing Members
![Team View](/screenshots/team_view.png)

### Notification Panel Displaying Recent Updates
![Notification Panel](/screenshots/notification_panel.png)

### Profile Page with Activity Tracking
![Profile Page](/screenshots/profile_page.png)

---

## **Installation**

### **Prerequisites**
- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

### **Steps**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/mrfost07/code-hub.git
   cd codehub
   ```

   A full list of dependencies is provided in `requirements.txt`.

2. **Creating virtual environment and activating it:**
   
   Linux/macOS:
   ```bash
   python3 -m venv env
   source env/bin/activate 
   ```
   
   Windows:
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

## **Pushing to a GitHub Repository**

If you want to push this project to your own GitHub repository, follow these steps:

1. **Create a new repository** on GitHub without initializing it with a README, license, or .gitignore files.

2. **Initialize a git repository** in your local project folder (if not already done):
   ```bash
   git init
   ```

3. **Add your files** to the git repository:
   ```bash
   git add .
   ```

4. **Commit the changes**:
   ```bash
   git commit -m "Initial commit"
   ```

5. **Add the remote repository URL**:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   ```

6. **Push the changes** to the main branch:
   ```bash
   git push -u origin main
   ```

   Note: If your default branch is named `master` instead of `main`, use that name instead.

---

## **Project Structure**

```
codehub/
├── accounts/       # User authentication and profiles
├── projects/       # Project management 
├── tasks/          # Task tracking and management
├── teams/          # Team collaboration features
├── notifications/  # Notification system
├── static/         # Static files (CSS, JS, images)
├── templates/      # HTML templates
└── media/          # User-uploaded files
```
