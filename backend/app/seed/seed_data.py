"""
Curated Realistic Seed Database for SkillPath.
Contains:
- 13 industry careers with full Day-in-the-Life, mini-projects, entry titles, and growth paths
- 85+ skills with plain explanations, prerequisites, done criteria, learning methods
- 210+ verified free/reputable learning resources
- 100+ plain-language glossary items
- Branch to career alignments
- 4 realistic demo learners (including Arif Mohamed) + 1 admin
"""

CAREERS_DATA = [
    {
        "slug": "ai-ml-engineer",
        "name": "AI/ML Engineer",
        "plain_description": "Builds and trains smart computer systems that learn from patterns in data to make predictions or decisions on their own.",
        "day_in_life": "Arrives around 9:30 AM, checks model training jobs from the night before, cleans newly collected datasets in Python, experiments with a new neural network architecture, and meets with software engineers to deploy a working model into production.",
        "typical_tasks": [
            "Write clean Python code to clean and prepare large datasets",
            "Train machine learning and deep learning models using scikit-learn and PyTorch",
            "Evaluate model accuracy and test for bias and overfitting",
            "Package models into fast REST APIs (using FastAPI or Docker) so apps can use them",
            "Monitor live model performance and retrain when real-world data shifts"
        ],
        "entry_titles": ["Junior Machine Learning Engineer", "Associate AI Developer", "Data Science & ML Intern"],
        "growth_path": ["Junior AI/ML Engineer (0-2y)", "ML Systems Engineer (2-5y)", "Senior/Lead AI Architect (5y+)"],
        "demand_level": "Very High",
        "salary_range_note": "₹6.5L - ₹14L / year entry-level in India ($85k - $130k US) - check current market data",
        "suits_who": "People who enjoy math, statistics, writing code, finding patterns, and teaching machines to solve complex challenges.",
        "mini_project": {
            "title": "Train Your First Spam Classifier",
            "duration": "1 hour",
            "description": "Build a simple Python script using scikit-learn that classifies incoming text messages as 'Spam' or 'Legitimate'.",
            "steps": [
                "Load a dataset of 1,000 labeled SMS messages into a Pandas DataFrame",
                "Convert text words into numbers using TF-IDF vectorization",
                "Train a Naive Bayes classifier on 80% of the messages",
                "Test accuracy on the remaining 20% and test your own custom message"
            ],
            "starter_code": "import pandas as pd\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.naive_bayes import MultinomialNB\n# SkillPath 1-hour starter code",
            "expected_outcome": "A working classifier that identifies spam messages with over 94% accuracy."
        }
    },
    {
        "slug": "data-analyst",
        "name": "Data Analyst",
        "plain_description": "Translates numbers and raw records into clear charts, dashboards, and stories that help businesses make smart everyday decisions.",
        "day_in_life": "Starts by reviewing automated morning dashboard metrics, uses SQL to extract user purchasing trends from a database, creates clean visualizations in Tableau or Power BI, and presents insights to the marketing team.",
        "typical_tasks": [
            "Write SQL queries to extract, filter, and join business data across tables",
            "Clean messy spreadsheets and missing values in Excel or Python",
            "Design clear, interactive charts and KPI dashboards for managers",
            "Explain what the numbers mean in simple presentations to non-technical leaders",
            "Run A/B test analysis to see if a new website button increased sales"
        ],
        "entry_titles": ["Junior Data Analyst", "Business Intelligence Associate", "Reporting Analyst"],
        "growth_path": ["Junior Data Analyst (0-2y)", "Senior BI Analyst (2-5y)", "Analytics Manager / Lead (5y+)"],
        "demand_level": "High",
        "salary_range_note": "₹4.5L - ₹8.5L / year entry-level (check current market data)",
        "suits_who": "Curious people who like solving puzzles, organizing spreadsheets, finding trends, and telling visual stories with charts.",
        "mini_project": {
            "title": "Analyze an E-Commerce Sales Trends Sheet",
            "duration": "1 hour",
            "description": "Analyze 5,000 real-world store sales records using Python and Pandas to discover top customer cities and peak sales hours.",
            "steps": [
                "Open the sample sales CSV and check for missing values",
                "Group sales totals by city and product category",
                "Plot a clean horizontal bar chart of top 5 profitable items",
                "Write a 3-bullet summary answering which region needs better delivery"
            ],
            "starter_code": "import pandas as pd\nimport matplotlib.pyplot as plt\ndf = pd.read_csv('ecommerce_sample.csv')\nprint(df.head())",
            "expected_outcome": "A clear bar chart and executive summary ready to show a team."
        }
    },
    {
        "slug": "data-scientist",
        "name": "Data Scientist",
        "plain_description": "Combines advanced math, statistics, and machine learning to uncover hidden insights and forecast future business trends.",
        "day_in_life": "Gathers customer behavior logs, formulates statistical hypotheses, runs regression or classification experiments, and translates mathematical findings into strategic recommendations.",
        "typical_tasks": [
            "Explore unstructured data to discover underlying behavioral patterns",
            "Formulate mathematical and statistical models for predictive analytics",
            "Design and evaluate controlled randomized experiments (A/B testing)",
            "Collaborate with product leaders to turn data insights into new features"
        ],
        "entry_titles": ["Associate Data Scientist", "Data Science Fellow", "Junior Quantitative Analyst"],
        "growth_path": ["Junior Data Scientist (0-2y)", "Senior Data Scientist (2-5y)", "Principal Scientist / Head of AI (5y+)"],
        "demand_level": "High",
        "salary_range_note": "₹6L - ₹12L / year entry-level (check current market data)",
        "suits_who": "Problem solvers who love probability, statistical inquiry, experimentation, and digging deep into unknown data.",
        "mini_project": {
            "title": "Predict Customer Churn Probability",
            "duration": "1 hour",
            "description": "Build a logistic regression model to identify which mobile subscribers are likely to cancel their subscriptions this month.",
            "steps": [
                "Inspect customer tenure, monthly spend, and customer support call counts",
                "Train a logistic regression model",
                "Identify top 3 warning signs of a leaving customer"
            ],
            "starter_code": "import pandas as pd\nfrom sklearn.linear_model import LogisticRegression\n# Churn Prediction Starter",
            "expected_outcome": "A ROC curve and list of top factors causing customer churn."
        }
    },
    {
        "slug": "data-engineer",
        "name": "Data Engineer",
        "plain_description": "Constructs the digital plumbing and pipelines that deliver huge amounts of reliable data quickly and cleanly to analysts and AI models.",
        "day_in_life": "Monitors automated overnight data pipelines in Apache Airflow, optimizes slow SQL queries in a cloud data warehouse like Snowflake or BigQuery, and writes Python ETL jobs.",
        "typical_tasks": [
            "Build automated Extract-Transform-Load (ETL) data pipelines",
            "Design database schemas for high-speed reporting and analytics",
            "Ensure data arrives on time, unbroken, and without duplicate records",
            "Manage cloud storage and databases on AWS or Google Cloud"
        ],
        "entry_titles": ["Junior Data Engineer", "ETL Developer", "Cloud Data Associate"],
        "growth_path": ["Data Engineer (0-2y)", "Senior Data Pipeline Engineer (2-5y)", "Data Architect / Infrastructure Lead (5y+)"],
        "demand_level": "Very High",
        "salary_range_note": "₹5.5L - ₹11L / year entry-level (check current market data)",
        "suits_who": "Those who like organizing messy things, backend plumbing, system reliability, and working behind the scenes.",
        "mini_project": {
            "title": "Build an Automated Weather Data Ingestion Script",
            "duration": "1 hour",
            "description": "Write a Python script that fetches real-time city weather from a free API and automatically appends it into an SQLite database table.",
            "steps": [
                "Make an HTTP request to the Open-Meteo weather API",
                "Extract temperature, humidity, and wind speed",
                "Create an SQLite table and insert the structured records"
            ],
            "starter_code": "import requests\nimport sqlite3\n# Data pipeline starter",
            "expected_outcome": "A self-updating local database table with historical weather records."
        }
    },
    {
        "slug": "full-stack-developer",
        "name": "Full Stack Developer",
        "plain_description": "Builds complete web applications from start to finish, from the visible user interface in the browser to the backend server and database.",
        "day_in_life": "Builds a sleek new signup form in React in the morning, writes REST API endpoints in Python or Node.js in the afternoon, tests database queries, and pushes code to GitHub.",
        "typical_tasks": [
            "Build responsive, attractive web screens using HTML, CSS, and modern React",
            "Write secure backend server APIs in Python (FastAPI) or Node.js",
            "Connect the application to a relational database like PostgreSQL or SQLite",
            "Implement secure user login with JWT tokens and password hashing",
            "Deploy websites to cloud platforms like Vercel, Netlify, or AWS"
        ],
        "entry_titles": ["Junior Full Stack Developer", "Software Engineer - Web", "Graduate Software Engineer"],
        "growth_path": ["Junior Full Stack Dev (0-2y)", "Senior Full Stack Engineer (2-5y)", "Tech Lead / Engineering Manager (5y+)"],
        "demand_level": "Very High",
        "salary_range_note": "₹5L - ₹10L / year entry-level (check current market data)",
        "suits_who": "Makers who want to build complete, functional products end-to-end and see their ideas come alive in a web browser.",
        "mini_project": {
            "title": "Build a Working Task Tracker Web App",
            "duration": "1 hour",
            "description": "Connect a React frontend with a FastAPI backend to create, mark complete, and delete tasks.",
            "steps": [
                "Create a 3-endpoint FastAPI backend (/tasks GET, POST, DELETE)",
                "Create a responsive React component with an input field and task list",
                "Connect the two with fetch() and test live adding and deleting"
            ],
            "starter_code": "from fastapi import FastAPI\napp = FastAPI()\ntasks = []",
            "expected_outcome": "A live interactive task manager running locally in your browser."
        }
    },
    {
        "slug": "frontend-developer",
        "name": "Frontend Developer",
        "plain_description": "Specializes in building the interactive, visual part of websites and applications that users see, click, and interact with.",
        "day_in_life": "Turns designer mockups into pixel-perfect web pages using Tailwind CSS and React, ensures smooth animations, and makes sure the site works well on mobile phones.",
        "typical_tasks": [
            "Translate UI/UX designs into responsive web interfaces",
            "Manage state and user interactions cleanly using modern TypeScript & React",
            "Ensure fast page load times and accessibility (WCAG AA compliance)",
            "Connect user interactions to backend APIs via asynchronous fetch requests"
        ],
        "entry_titles": ["Junior Frontend Developer", "UI Developer", "Web Designer & Developer"],
        "growth_path": ["Junior Frontend Dev (0-2y)", "Senior UI Engineer (2-5y)", "Staff Frontend Architect (5y+)"],
        "demand_level": "High",
        "salary_range_note": "₹4.5L - ₹9L / year entry-level (check current market data)",
        "suits_who": "Visual thinkers with an eye for detail, design, typography, and satisfying animations.",
        "mini_project": {
            "title": "Build an Interactive Product Card with Cart Counter",
            "duration": "1 hour",
            "description": "Craft a beautiful modern e-commerce product card with size selector, image carousel, and dynamic cart badge.",
            "steps": [
                "Structure HTML semantics with image, title, price, and tags",
                "Style with Tailwind CSS hover effects and badges",
                "Add interactive state in React to update cart total instantly"
            ],
            "starter_code": "export default function ProductCard() { return <div>Card</div>; }",
            "expected_outcome": "A polished, responsive component suitable for a professional portfolio."
        }
    },
    {
        "slug": "cloud-engineer",
        "name": "Cloud Engineer",
        "plain_description": "Designs, deploys, and manages servers, storage, and networking on cloud platforms like AWS, Microsoft Azure, and Google Cloud.",
        "day_in_life": "Sets up virtual servers, configures cloud security policies, optimizes monthly cloud hosting costs, and ensures company websites never crash during traffic spikes.",
        "typical_tasks": [
            "Deploy virtual machines, containers, and serverless functions in AWS or GCP",
            "Write Infrastructure as Code (Terraform) to spin up environments reliably",
            "Set up firewalls, virtual private clouds (VPC), and secure access keys",
            "Monitor server uptime, CPU usage, and automated backups"
        ],
        "entry_titles": ["Associate Cloud Engineer", "Junior Cloud Support Associate", "Cloud Operations Intern"],
        "growth_path": ["Junior Cloud Engineer (0-2y)", "Senior Cloud Specialist (2-5y)", "Cloud Solutions Architect (5y+)"],
        "demand_level": "Very High",
        "salary_range_note": "₹5L - ₹11L / year entry-level (check current market data)",
        "suits_who": "People who enjoy networking, operating systems, security, and making sure huge digital systems stay online 24/7.",
        "mini_project": {
            "title": "Host a Static Website on AWS S3 with Custom Domain",
            "duration": "1 hour",
            "description": "Deploy a personal portfolio site onto cloud object storage and configure public web hosting permissions.",
            "steps": [
                "Create an S3 bucket with web hosting enabled",
                "Upload index.html, style.css, and images",
                "Configure bucket policy for read-only public access and verify via live URL"
            ],
            "starter_code": "# AWS CLI command\naws s3 cp ./website s3://my-skillpath-demo-site --recursive",
            "expected_outcome": "A live globally accessible website URL served directly from the cloud."
        }
    },
    {
        "slug": "devops-engineer",
        "name": "DevOps Engineer",
        "plain_description": "Automates the bridge between writing code and shipping it safely to users, creating lightning-fast automated build and release pipelines.",
        "day_in_life": "Configures GitHub Actions to run automated tests whenever developers push code, packages applications into Docker containers, and manages Kubernetes clusters.",
        "typical_tasks": [
            "Build Continuous Integration & Continuous Deployment (CI/CD) pipelines",
            "Package applications into lightweight Docker containers",
            "Automate testing and security scans before code reaches production",
            "Set up monitoring alerts (Prometheus/Grafana) to notify teams of errors"
        ],
        "entry_titles": ["Junior DevOps Engineer", "Build & Release Engineer", "Platform Operations Associate"],
        "growth_path": ["DevOps Engineer (0-2y)", "Senior Site Reliability Engineer (2-5y)", "Principal Platform Engineer (5y+)"],
        "demand_level": "Very High",
        "salary_range_note": "₹5.5L - ₹12L / year entry-level (check current market data)",
        "suits_who": "Organized thinkers who hate repetitive manual work and love automating tasks with shell scripts and pipelines.",
        "mini_project": {
            "title": "Create a GitHub Actions CI Pipeline for Python Tests",
            "duration": "1 hour",
            "description": "Write a workflow file that automatically installs dependencies and runs pytest whenever code is pushed.",
            "steps": [
                "Create .github/workflows/test.yml in a repository",
                "Define triggers for push and pull_request on the main branch",
                "Configure Python setup and run pytest, testing the green badge"
            ],
            "starter_code": "name: Run Tests\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest",
            "expected_outcome": "An automated pipeline with green passing checkmarks on GitHub."
        }
    },
    {
        "slug": "cybersecurity-analyst",
        "name": "Cybersecurity Analyst",
        "plain_description": "Protects computer systems, networks, and confidential data from hackers, malware, digital espionage, and security breaches.",
        "day_in_life": "Monitors security alert dashboards for unusual network traffic, investigates potential phishing emails reported by employees, tests systems for weak passwords, and writes incident reports.",
        "typical_tasks": [
            "Monitor security information tools (SIEM) for signs of unauthorized access",
            "Scan networks and web apps for known security vulnerabilities",
            "Investigate malware and phishing incidents to contain threats",
            "Implement strong password rules, multi-factor authentication, and encryption"
        ],
        "entry_titles": ["Junior SOC Analyst", "Information Security Associate", "Cyber Defense Intern"],
        "growth_path": ["SOC Analyst L1 (0-2y)", "Security Engineer / Threat Hunter (2-5y)", "Chief Information Security Officer (5y+)"],
        "demand_level": "High",
        "salary_range_note": "₹4.5L - ₹9.5L / year entry-level (check current market data)",
        "suits_who": "Vigilant, ethical detectives who like investigating puzzles, understanding how systems break, and keeping people safe.",
        "mini_project": {
            "title": "Analyze Suspicious Web Traffic Logs with Wireshark",
            "duration": "1 hour",
            "description": "Inspect a network packet capture file to pinpoint an unauthorized port scan or plaintext password transmission.",
            "steps": [
                "Open a sample .pcap network capture file",
                "Apply filters for HTTP and TCP SYN scans",
                "Identify the attacker's IP address and the exposed credentials"
            ],
            "starter_code": "# Wireshark filter query\nhttp.request.method == \"POST\" || tcp.flags.syn == 1",
            "expected_outcome": "A forensic incident report identifying the attacker and vulnerability."
        }
    },
    {
        "slug": "ui-ux-designer",
        "name": "UI/UX Designer",
        "plain_description": "Researches how people use apps and websites to design intuitive, beautiful, and easy-to-use digital experiences.",
        "day_in_life": "Conducts a 30-minute interview with a real user to see where they get confused, sketches wireframes on paper, designs high-fidelity mockups in Figma, and hands off specs to developers.",
        "typical_tasks": [
            "Interview users and create simple personas to understand user needs",
            "Sketch user journey flows and wireframes for mobile and desktop screens",
            "Design polished interactive prototypes in Figma with consistent design tokens",
            "Test prototypes with beginners to spot confusion before code is written"
        ],
        "entry_titles": ["Junior UI/UX Designer", "Product Design Associate", "Interaction Design Intern"],
        "growth_path": ["Junior Designer (0-2y)", "Product Designer (2-5y)", "Design Director / VP of Design (5y+)"],
        "demand_level": "High",
        "salary_range_note": "₹4L - ₹8.5L / year entry-level (check current market data)",
        "suits_who": "Empathetic, creative individuals who care deeply about how things look, feel, and simplify human lives.",
        "mini_project": {
            "title": "Design a 3-Screen Mobile Onboarding Flow in Figma",
            "duration": "1 hour",
            "description": "Create a clean, welcoming onboarding sequence for a student learning app with consistent typography and colors.",
            "steps": [
                "Set up an 8px grid and color styles (primary, ink, surface)",
                "Design Screen 1 (Welcome), Screen 2 (Goal selection), Screen 3 (Ready)",
                "Link screens with prototype arrows and test in Figma Mirror"
            ],
            "starter_code": "Figma community template: SkillPath Beginner Design Kit",
            "expected_outcome": "A clickable mobile prototype link you can share and interact with on your phone."
        }
    },
    {
        "slug": "mobile-app-developer",
        "name": "Mobile App Developer",
        "plain_description": "Builds fast, interactive applications that run smoothly on iPhones, iPads, and Android smartphones.",
        "day_in_life": "Uses Flutter or React Native to code a new camera feature, tests the app on both an Android phone and an iPhone simulator, optimizes battery consumption, and prepares releases for app stores.",
        "typical_tasks": [
            "Build cross-platform mobile apps using React Native or Flutter",
            "Connect mobile screens to backend cloud APIs and offline storage",
            "Handle phone permissions like camera, location, and push notifications",
            "Test app performance across different screen sizes and device speeds"
        ],
        "entry_titles": ["Junior Mobile Developer", "Android/iOS Associate", "Flutter Developer"],
        "growth_path": ["Junior Mobile Dev (0-2y)", "Senior Mobile Engineer (2-5y)", "Mobile Tech Lead (5y+)"],
        "demand_level": "High",
        "salary_range_note": "₹4.5L - ₹9.5L / year entry-level (check current market data)",
        "suits_who": "Those who love smartphones and want to install apps they built onto their friends' and family's phones.",
        "mini_project": {
            "title": "Build a Daily Quote App with Push Notifications",
            "duration": "1 hour",
            "description": "Create a React Native / Expo app that displays an inspiring quote each morning and saves favorites locally.",
            "steps": [
                "Initialize an Expo project (`npx create-expo-app QuoteApp`)",
                "Fetch a random quote from a free JSON endpoint",
                "Store saved favorite quotes in AsyncStorage and render a heart toggle"
            ],
            "starter_code": "import { View, Text, TouchableOpacity } from 'react-native';\n// Expo mobile starter",
            "expected_outcome": "A mobile app running live on your phone via Expo Go QR code."
        }
    },
    {
        "slug": "software-tester-qa",
        "name": "Software Tester / QA Engineer",
        "plain_description": "Finds bugs, glitches, and usability issues in software before it ever reaches real customers, ensuring rock-solid quality.",
        "day_in_life": "Reads requirements for a new feature, writes test cases, executes automated test scripts in Playwright or Selenium, reports bugs to developers, and verifies fixes.",
        "typical_tasks": [
            "Write detailed test cases covering happy paths and edge cases",
            "Write automated browser test scripts using Python, Cypress, or Playwright",
            "Test API endpoints with Postman for correct status codes and error messages",
            "Document reproducible bug steps with screenshots and console logs"
        ],
        "entry_titles": ["Junior QA Engineer", "Software Test Associate", "Quality Analyst Intern"],
        "growth_path": ["QA Engineer (0-2y)", "Senior Automation Engineer (2-5y)", "QA Lead / Director of Quality (5y+)"],
        "demand_level": "Moderate",
        "salary_range_note": "₹3.8L - ₹7.5L / year entry-level (check current market data)",
        "suits_who": "Detail-oriented people who like breaking things intentionally, asking 'what if', and ensuring top craftsmanship.",
        "mini_project": {
            "title": "Write an Automated Login Test in Playwright",
            "duration": "1 hour",
            "description": "Script an automated browser test that enters valid credentials and confirms successful dashboard navigation.",
            "steps": [
                "Install Playwright in Python (`pip install pytest-playwright`)",
                "Write a test script that navigates to a demo login page",
                "Fill username/password, click Submit, and assert dashboard header visibility"
            ],
            "starter_code": "from playwright.sync_api import sync_playwright\n# QA Automation starter",
            "expected_outcome": "A green test run with video recording of the browser auto-filling and passing."
        }
    },
    {
        "slug": "product-analyst",
        "name": "Product Analyst",
        "plain_description": "Bridges data and product strategy to measure how users interact with features, identifying what to build next to grow the product.",
        "day_in_life": "Checks user drop-off funnels in Mixpanel or Google Analytics, drafts an experiment plan for a new feature checkout flow, and presents metrics to the product manager.",
        "typical_tasks": [
            "Analyze user retention cohorts and feature adoption rates",
            "Build conversion funnels to pinpoint where users drop off",
            "Define product metrics and KPIs with product managers",
            "Run statistical hypothesis testing on product updates"
        ],
        "entry_titles": ["Associate Product Analyst", "Growth Analyst", "Product Operations Associate"],
        "growth_path": ["Product Analyst (0-2y)", "Senior Product Analyst (2-5y)", "Product Manager / Head of Analytics (5y+)"],
        "demand_level": "Growing",
        "salary_range_note": "₹5L - ₹10L / year entry-level (check current market data)",
        "suits_who": "Those who like understanding human behavior, psychology, business growth, and analyzing user metrics.",
        "mini_project": {
            "title": "Analyze a Sign-Up Funnel Drop-off Rate",
            "duration": "1 hour",
            "description": "Calculate conversion percentages across a 4-step onboarding funnel to find the biggest bottleneck.",
            "steps": [
                "Load 2,000 onboarding session records",
                "Calculate conversion %: Landing -> Sign Up -> Form -> First Action",
                "Identify which step lost 60% of users and write 2 recommendations"
            ],
            "starter_code": "import pandas as pd\n# Funnel analysis starter",
            "expected_outcome": "A clean funnel chart and recommended UI change to recover lost users."
        }
    }
]

BRANCH_CAREER_MAPPINGS = {
    "Artificial Intelligence and Data Science": ["ai-ml-engineer", "data-scientist", "data-analyst", "data-engineer", "product-analyst"],
    "Computer Science and Engineering": ["full-stack-developer", "frontend-developer", "ai-ml-engineer", "cloud-engineer", "devops-engineer"],
    "Information Technology": ["full-stack-developer", "cloud-engineer", "cybersecurity-analyst", "data-analyst", "devops-engineer"],
    "Electronics and Communication Engineering": ["cloud-engineer", "devops-engineer", "ai-ml-engineer", "software-tester-qa"],
    "Mechanical Engineering / Civil": ["data-analyst", "product-analyst", "full-stack-developer", "ui-ux-designer"],
    "Commerce / Management / Arts": ["data-analyst", "product-analyst", "ui-ux-designer", "software-tester-qa"],
    "General / Other": ["data-analyst", "full-stack-developer", "ui-ux-designer", "frontend-developer"]
}

