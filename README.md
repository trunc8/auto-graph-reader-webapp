# Automated Graph Reader Web-app

### Demo
![Auto-graph Reader Demo](assets/auto-graph-reader-demo.gif)

### Interface
![Auto-graph Reader Interface](assets/auto-graph-reader-demo.png)

### Instructions to Use
The user uploads a simple graph snippet from any document/research paper. The app automatically reads the X and Y labels after cleaning the X, Y and graph titles. It allows you to query Y-values for desired X-values. It also alerts the user when the graph is too complex for it to process.

### Steps to Run Locally on your System
1. `git clone https://github.com/trunc8/auto-graph-reader-webapp.git`
2. `sudo apt install tesseract-ocr tesseract-ocr-eng libgl1` (Use `.exe` installer for `Tesseract` on Windows)
3. `pip install -r requirements.txt`
4. `streamlit run graph_reader_app.py`

### Deployment
The web-app ([link](https://auto-graph-reader.herokuapp.com/)) is deployed on a Heroku server and live!  
(The server may take up to 5 seconds to load the page. Heroku restarts the server after periods of inactivity)

### Authors

* **Siddharth Saha** - [trunc8](https://github.com/trunc8)

<p align='center'>Created with :heart: by <a href="https://www.linkedin.com/in/sahasiddharth611/">Siddharth</a></p>