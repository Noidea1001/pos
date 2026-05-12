# 🛒 Inventory & POS Management System

A robust Inventory and Point of Sale (POS) management system built with the **Django Framework**. This application is designed to streamline sales, track stock levels, and manage business operations for small to medium enterprises.

## ✨ Key Features
*   **Dynamic Dashboard:** Real-time visualization of sales statistics and stock alerts.
*   **Inventory Management:** Full CRUD operations for products, categories, and suppliers.
*   **Sales & Invoicing:** Seamless checkout process with automated record-keeping.
*   **User Management:** Role-based access for employees and administrators.
*   **Customer Tracking:** Maintain a database of customer history and contact details.

## 🛠️ Tech Stack
*   **Backend:** Python & Django 4.x
*   **Frontend:** HTML5, CSS3 (Bootstrap), JavaScript
*   **Database:** SQLite (Development) / PostgreSQL (Production ready)

## 🚀 Getting Started

### Prerequisites
* Python 3.8 or higher installed.
* Git installed.

### Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd pos
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   # Activate on Windows:
   .\venv\Scripts\activate
   # Activate on Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server:**
   ```bash
   python manage.py runserver
   ```
Visit `http://127.0.0` in your browser.

## 📂 Project Structure
* `inventory_system/` - Core settings and configuration.
* `products/`, `sales/`, `customers/` - Independent Django apps for modular functionality.
* `templates/` - Global HTML UI components.
* `static/` - Assets including CSS, JS, and images.
