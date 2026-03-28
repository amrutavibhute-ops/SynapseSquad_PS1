# SynapseSquad_PS1
Green Auditor - Python-based UI tool that analyzes product descriptions to detect greenwashing using NLP techniques and certification checks.

a. Datasets Used and Preprocessing
 Datasets Used:
  The system uses a combination of:
    Custom dataset (brands.csv)
    Contains brand names and their certifications
 Used for brand and certification matching
   Keyword-based dataset
    Buzzwords: eco-friendly, natural, green, sustainable, organic
    Certification keywords: ISO, FSSAI, FDA, AYUSH, B-Corp, etc.
  Dynamic Input Data
    Product descriptions entered by the user
    OR extracted from URLs using web scraping

 Preprocessing Steps:
  Lowercasing
    Converts all text to lowercase for uniform comparison
  Text Cleaning
    Removes special characters using regex:
    re.sub(r'[^a-zA-Z0-9]', '', text)
  Sentence Tokenization
    Splits text into sentences using ., !, ?
  Keyword Detection
  Identifies:
    Marketing buzzwords
    Certification terms
  Brand Matching
    Cleans text and compares with brands in CSV
    Handles variations (spacing, symbols)

b. Model Used and Accuracy / Performance Metrics 
   Model Used:
     The system uses a Rule-Based NLP Model
   Techniques Used:
     Regular Expressions (Regex)
       Detects patterns like percentages and certifications
     Keyword Matching
       Identifies marketing buzzwords
    Performance Metrics:
    No formal accuracy metrics (like accuracy, precision, recall)
      Because:
        No machine learning model is used
        No labeled dataset for evaluation
    Performance Observation:
      Works well for:
       Clear marketing claims
       Certification-based statements

c. Key Features
🔍 Real-time Greenwashing Detection
Identifies misleading environmental claims
 URL-Based Analysis
Extracts product descriptions from websites using web scraping
 Sentence Classification
Categorizes text into:
Marketing Fluff
Evidence-Based
Neutral
 Certification Verification
Detects certifications using:
CSV dataset
Keyword matching
 Explainable Results
Shows:
Why a product is not trustworthy
Detected buzzwords
 Detailed Output
Fluff vs Evidence count
Final verdict
 Audit History
Stores previous results in a table
 User-Friendly Interface
Built using Tkinter
Simple and interactive UI
