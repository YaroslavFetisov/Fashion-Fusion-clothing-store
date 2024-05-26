# Fashion Fusion Clothing Store

## Project Description
Fashion Fusion is an online clothing store developed as a group project for university. The website allows users to browse, search, and purchase clothing items. The frontend is built with React, and the backend is powered by Flask.

## Prerequisites
Before you begin, ensure you have the following installed:
- **Node.js**: [Download Node.js](https://nodejs.org/)
- **npm**: This is included with Node.js
- **Python 3**: [Download Python](https://www.python.org/)
- **pip**: Python package installer
- **Git**: [Download Git](https://git-scm.com/)
  
## Installation
### Backend (Flask)
Clone the repository:
```bash
git clone https://github.com/your-username/FashionFusion.git
```
Navigate to the backend directory:
```bash
cd FashionFusion/backend
```
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```
Install the dependencies:
```bash
pip install -r requirements.txt
```
Create a config.py file in the backend directory with the following content:
```python
class Config:
SECRET_KEY = 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
```
