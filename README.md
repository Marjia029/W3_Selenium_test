# 🌐 Vacation Rental Home Page Selenium Automation Testing 🏠

## Project Overview
🚀 This project automates testing for a vacation rental details page using Selenium WebDriver in Python. The script performs comprehensive checks on various aspects of the webpage to ensure quality and SEO compliance.

## Table of Contents
- [Features](#features)
- [Test Cases Covered](#test-cases-covered)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Reporting](#reporting)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Features
✨ **Key Features**:
- 🤖 Automated web testing for vacation rental websites
- ✅ Validates critical webpage elements
- 📊 Generates detailed Excel reports of test results

## Test Cases Covered
1. **📝 H1 Tag Existence Test**  
   - Checks if the H1 tag is present on the page  
   - 🚫 Fails if H1 tag is missing  

2. **🔤 HTML Tag Sequence Test**  
   - Validates [H1-H6] tag sequence  
   - 🚫 Fails if tag sequence is broken or tags are missing  

3. **🖼️ Image Alt Attribute Test**  
   - Checks for alt attributes on images  
   - 🚫 Fails if alt attributes are missing  

4. **🌐 URL Status Code Test**  
   - Verifies all URLs are accessible  
   - 🚫 Fails for 404 status codes  

5. **💱 Currency Filter Test**  
   - Ensures property tile currencies update correctly  

6. **📋 Script Data Scraping**  
   - Extracts key information:  
     - 🔗 Site URL  
     - 🆔 Campaign ID  
     - 🏷️ Site Name  
     - 🌍 Browser  
     - 🇺🇸 Country Code  
     - 📶 IP Address  

## Prerequisites
📌 **Requirements**:
- 🐍 Python 3+
- 🛠️ Selenium WebDriver
- 🐼 Pandas
- ⚙️ WebDriver Manager
- 🌐 Chrome Browser

## Project Structure

```bash
W3_Selenium_test/
│
├── main.py                 # Main test execution script
├── utils/
│   ├── driver_setup.py     # WebDriver configuration
│   └── test_utils.py       # Test utility functions
│
├── tests/
│   ├── test_h1_tag.py
│   ├── test_html_tag_sequence.py
│   ├── test_image_alt_attribute.py
│   ├── test_url_status.py
│   ├── test_currency_filter.py
│   └── test_scrape_data.py
│
├── reports/                # Test reports directory
│   └── test_report.xlsx
│
├── requirements.txt        # Project dependencies
├── .gitignore              # Git ignore file
└── README.md               # Project documentation

```

## Installation
⚙️ **Follow these steps**:

1. **📥 Clone the repository**:
    ```bash
    git clone https://github.com/Marjia029/W3_Selenium_test.git
    cd W3_Selenium_test
    ```

2. **🌟 Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux
    venv\Scripts\activate     # For Windows
    ```

3. **📦 Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **▶️ Run the tests**:
    ```bash
    python main.py  # Run tests with visible browser
    python main.py --headless  # Run tests in headless mode
    ```

## Reporting

- 📋 **Test results are logged in** `reports/test_report.xlsx`.  
- Each test generates a row with the following details:  
    - **🔗 Page URL**: The URL of the page tested  
    - **📝 Test Case Name**: The name or description of the specific test case  
    - **✅ Pass/Fail Status**: The outcome of the test (Pass or Fail)  
    - **💬 Detailed Comments**: Additional information about the test results, such as error details or observations  

📊 This report structure ensures that all test cases are tracked and can be reviewed systematically.

## Customization

🛠️ **Steps for modification**:  
- Edit `main.py` to add or remove test cases.  
- Update `utils/driver_setup.py` for browser configuration.  
- Adjust test scripts in the `tests/` directory for specific requirements.

## Troubleshooting

❓ **Common Issues**:  
- 🖥️ Ensure WebDriver is compatible with your browser version.  
- 🌐 Check network connectivity.  
- 🐍 Verify Python and package dependencies.

## Contributing

🤝 **How to contribute**:
1. Fork the repository.
2. Create your feature branch:  
   ```bash
   git checkout -b feature/AmazingFeature
   git commit -m 'Add some AmazingFeature'
   git push origin feature/AmazingFeature
   ```
3. Open a Pull Request

## Acknowledgments

🎉 Special Thanks To:

- Selenium WebDriver
- Python
- Pandas Library

