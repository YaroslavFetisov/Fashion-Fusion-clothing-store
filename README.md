# Fashion Fusion Clothing Store

## Project Description
Fashion Fusion is an online clothing store developed as a group project for university. The website allows users to browse and search for clothing items. The frontend is built with React, and the backend is powered by Flask.

## Prerequisites
Before you begin, ensure you have the following installed:
- **Node.js**: [Download Node.js](https://nodejs.org/)
- **npm**: This is included with Node.js
- **Python 3**: [Download Python](https://www.python.org/)
- **pip**: Python package installer
- **Git**: [Download Git](https://git-scm.com/)
  
## Installation
### Backend (Flask)
1.Clone the repository:
```bash
git clone https://github.com/your-username/FashionFusion.git
```
2.Navigate to the backend directory:
```bash
cd FashionFusion/backend
```
3.Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```
4.Install the dependencies:
```bash
pip install -r requirements.txt
```
5.Create a config.py file in the backend directory with the following content:
```python
class Config:
SECRET_KEY = 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
```
### Frontend (React)
1.Navigate to the frontend directory:
```bash
cd FashionFusion/frontend
```
2.Install the dependencies:
```bash
npm install
```
3.To handle requests to the Flask backend during development, add the following proxy to your package.json file in the frontend directory:
```json
"proxy": "http://localhost:5000"
```
## Running the Project
### Backend
1.Ensure you are in the FashionFusion/backend directory and the virtual environment is activated.
2.Run the Flask server:
```bash
flask run
```
### Frontend
1.Ensure you are in the FashionFusion/frontend directory.
2.Start the React development server:
```bash
npm start
```
## Accessing the Application
1.Open your browser and navigate to http://localhost:3000 to view the React frontend.
2.The backend API can be accessed at http://localhost:5000.

## Usage
Once the project is set up and running, you can:

- Browse the clothing catalog
- Search for specific items
- Filter items by brand, size, price and so on
- Add items to the cart

## Contributing
#### To contribute to this project, follow these steps:

1. Fork this repository.
2. Create a branch: git checkout -b <branch_name>.
3. Make your changes and commit them: git commit -m '<commit_message>'.
4. Push to the original branch: git push origin <branch_name>.
5. Create the pull request.
6. Alternatively, see the GitHub documentation on creating a pull request.

## License
This project is licensed under the MIT License.


