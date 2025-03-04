
<body>
  <h1>Student ID Card Information Extraction using SVM</h1>

  <h2>Overview</h2>
  <p>
    This project aims to build an automated system for extracting key information from student ID cards using the Support Vector Machine (SVM) approach. The system is applied in the attendance process at Hue University of Science, and it helps:
  </p>
  <ul>
    <li>Save time in processing student information.</li>
    <li>Reduce errors caused by manual operations.</li>
    <li>Improve efficiency in student management and attendance.</li>
  </ul>


  <h2>Process description</h2>
  <p>
    The following images provide visual guidance:
  </p>
  <ul>
    <li>
      <strong>Diagram of the process for extracting the information regions from the student ID card, illustrating the process from image pre-processing to region extraction:</strong> .<br>
      <img src="https://i.ibb.co/8D9Kn7dS/image.png" alt="Extraction Process Diagram" border="0" />
    </li>
    <li>
      <strong>Diagram of the SVM-based information extraction process, describing the training and testing phases of the model:</strong> .<br>
      <img src="https://i.ibb.co/4gSWcbw9/image.png" alt="SVM Training and Testing Diagram" border="0">
    </li>
        <li>
      <strong>Shows the input and output of the problem (original student ID card image and the Word file containing the extracted information)</strong> .<br>
      <img src="https://i.ibb.co/jZh9Mvfd/image.png" alt="Input and Output Example" border="0">
    </li>
  </ul>

  <h2>Installation and Usage</h2>
  <h3>1. Setting up the Environment</h3>
  <p><strong>Requirements:</strong> Python 3.8 or higher.</p>
  <p><strong>Libraries:</strong> Install the required libraries using the <code>requirements.txt</code> file:</p>
  <pre><code>pip install -r requirements.txt</code></pre>

  <h3>2. Running the Demo Interface</h3>
  <p>Run the Streamlit application:</p>
  <p><strong>Option 1: Run locally</strong></p>
  <pre><code>streamlit run streamlit_app.py</code></pre>
  <p><strong>Option 2: Access the online demo</strong></p>
  <p>Click the link below to access the deployed Streamlit application:</p>
  <p><a href="https://extract-student-card-information-using-svm-junldfg4vabu2obgs8d.streamlit.app/" target="_blank">Open Streamlit App</a></p>

  <p><strong>Usage instructions for the demo interface:</strong></p>
  <ul>
    <li>Click the <strong>"Browse files"</strong> button to upload one or more student ID card images.</li>
    <li>Once uploaded, the extracted results (such as name, date of birth, class, student ID, and card image) will be displayed on the interface.</li>
    <li>Click the <strong>"Download Word File"</strong> button to save the extracted information into the <code>thong_tin_sinh_vien.doc</code> file.</li>
  </ul>


  <h2>Conclusion</h2>
  <p>
    The SVM-based student ID card information extraction system is an effective solution for automating attendance and student management. This project not only demonstrates the feasibility of the SVM approach for image processing but also paves the way for future applications in educational management.
  </p>

  <h2>Contact</h2>
  <p>
    If you have any questions or suggestions, please contact: 
    <a href="tranhoang0320@gmail.com">tranhoang0320@gmail.com</a>
  </p>
</body>
</html>


## Link to Google Drive Dataset
([link to dataset](https://drive.google.com/file/d/1RJSvMqz0HKN9VNgjGc4qM8jk-iwgqKSz/view?usp=drive_link))
