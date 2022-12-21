![ATU Header](images/ATU_Logo.jpg)

***

#### Student: Sam Tracey
#### Student ID: G00398245
#### Module: Data Representation
#### Topic: Big Project

***

### Introduction

<p> The purpose of this project is to demonstrate an understanding of the creation and consumption of RESTful APIs.
    
This project uses Flask in conjunction with a MySQL database to create a web application that allows a user to consume the API to perform CRUD operations on the stored data.</p>

<p>This project is centered around the provision of an Analytics web application which can be used by my current employer.
</p>

### Overview of Zeus Industrial Products

<p> <a href="https://www.zeusinc.com/company/">Zeus Industrial Products</a> is a global leader in advanced polymer solutions, helping customers overcome complex design and engineering challenges for over 50 years. With manufacturing and sales facilities across three continents and a presence in 180 countries worldwide, Zeus develops and delivers customized polymer solutions for companies in the medical, automotive, aerospace, fiber optics, energy, and fluid management markets.
    
Headquartered in Orangeburg, SC, USA, Zeus employs over 1,800 people worldwide across its facilities in Aiken, Columbia, Gaston, and Orangeburg, South Carolina; Branchburg, New Jersey; Chattanooga, Tennessee; San Jose, California; Guangzhou, China; and Letterkenny, Ireland.
    
Like many large corporations primarily based in the USA, employee attrition has become of greater concern in the past number of years.</p>

### Purpose of This Project

<p>The primary purpose of this project is to provide our leadership team with insights into the employee attrition rate at the company as well as trends in macro economic data that could be correlated.
    
**Please note: Since the employee attrition rate is confidential information we will be using synthetic data for the purpose of this project**</p>

### Data Sources

<p> Our synthetic employee attrition data is initially stored in a .csv file before being read into our MySQL database. We also extract the following macro economic data:

* <a href="https://fred.stlouisfed.org/series/SCUR">Unemployment Rate in South Carolina</a> 
* <a href="https://fred.stlouisfed.org/series/SCMFG">All Employees: Manufacturing in South Carolina</a>
* <a href="https://fred.stlouisfed.org/series/JTS00SOQUL">Quits: Total Nonfarm in South Census Region</a>
* <a href="https://fred.stlouisfed.org/series/JTS00SOJOL">Job Openings: Total Nonfarm in South Census Region</a>

These data sets are extracted directly from the <a href="https://fred.stlouisfed.org/docs/api/fred/">FRED API</a> and stored in our MySQL database.</p>
    
### Repository Contents

<p> This repository contains the following files:
    
* <code>app.py</code> Python Flask server application program.
* <code>config.py</code> Python configuration file with credentials for the MySQL database and FRED API.
* <code>dataDAO.py</code> Python file which enables interaction with the MySQL database.
* <code>init_db.sql</code> SQL file which allows the datarepresentation schema and relevant MySQL tables to be initilised.
* <code>local_quits.csv</code> CSV file which contains the syntetic data for local employee attrition</code>
* <code>README.md</code> Readme file.
* <code>requirements.txt</code> File containing the Python packages required to run the application.
* <code>static</code> Folder containing the images used in the webpages (images folder) and css styles used for the webpages (styles folder).
* <code>templates</code> Folder containing 10 .html pages used for the web application.
* <code>images</code> Folder containing the images used in this Readme document.
 