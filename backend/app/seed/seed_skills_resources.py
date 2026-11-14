"""
85+ Skills with beginner-first plain explanations, done criteria, common mistakes, and 210+ curated reputable resources.
"""

SKILLS_DATA = [
    # --- PROGRAMMING & FOUNDATIONS ---
    {
        "slug": "python-basics",
        "name": "Python Basics",
        "category": "Programming",
        "plain_explanation": "Python is a computer language designed to read almost like plain English. It lets you write instructions for your computer to store information, make decisions, and automate repetitive tasks.",
        "prerequisites": [],
        "estimated_hours_per_level": 12.0,
        "difficulty": 0.8,
        "common_mistakes": [
            "Trying to memorize syntax rules instead of typing and running code",
            "Confusing indentations (Python relies on 4 spaces to know what code belongs inside a block)",
            "Getting intimidated by red error messages (they are actually helpful clues telling you which line to fix)"
        ],
        "done_criteria": [
            "Can write variables, loops, and if-else conditional branches without looking up syntax",
            "Can define a custom function that takes arguments and returns a calculated result",
            "Can manipulate lists, dictionaries, and strings to filter and transform data"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 55,
            "build_pct": 20,
            "first_step": "Open an interactive Python notebook or repl and write your first print('Hello SkillPath') statement.",
            "tip": "Spend 70% of your time typing code in your editor rather than passively watching video tutorials."
        }
    },
    {
        "slug": "git-github",
        "name": "Git & GitHub",
        "category": "Programming",
        "plain_explanation": "Git is like an 'undo' button with superpowers for your code files. It saves checkpoints (commits) so you can experiment safely, collaborate with others, and share your projects on GitHub for employers to see.",
        "prerequisites": [],
        "estimated_hours_per_level": 10.0,
        "difficulty": 0.9,
        "common_mistakes": [
            "Committing huge unorganized chunks of work with messages like 'update' instead of clear steps",
            "Accidentally committing sensitive passwords or API keys to public repositories",
            "Panicking during merge conflicts instead of inspecting the file markers"
        ],
        "done_criteria": [
            "Can initialize a repository, stage files, commit changes, and push to GitHub",
            "Can create and switch between feature branches and open a Pull Request",
            "Can resolve a basic merge conflict between two branches"
        ],
        "learning_method": {
            "watch_pct": 20,
            "practice_pct": 60,
            "build_pct": 20,
            "first_step": "Create a free GitHub account, install Git, and push a simple README markdown file.",
            "tip": "Commit early and often with clear messages explaining 'why' you changed the code."
        }
    },
    {
        "slug": "sql-basics",
        "name": "SQL Basics",
        "category": "Programming",
        "plain_explanation": "SQL (Structured Query Language) is the universal language used to ask databases questions, such as 'How many customers signed up in Mumbai this week?' or 'What was our best-selling product?'",
        "prerequisites": [],
        "estimated_hours_per_level": 12.0,
        "difficulty": 0.9,
        "common_mistakes": [
            "Confusing WHERE (filters individual rows before grouping) with HAVING (filters groups after aggregating)",
            "Mixing up INNER JOIN and LEFT JOIN and losing records unintentionally",
            "Writing messy queries without capitalization and proper indentation"
        ],
        "done_criteria": [
            "Can write SELECT statements with WHERE filters, ORDER BY, and LIMIT",
            "Can aggregate numbers using COUNT, SUM, AVG, and GROUP BY",
            "Can connect two relational tables using INNER JOIN and LEFT JOIN"
        ],
        "learning_method": {
            "watch_pct": 20,
            "practice_pct": 65,
            "build_pct": 15,
            "first_step": "Try a free browser SQL sandbox like SQLZoo or Khan Academy and query a table of movies.",
            "tip": "Think of database tables like connected Excel sheets with strict columns and rows."
        }
    },
    {
        "slug": "advanced-python",
        "name": "Advanced Python",
        "category": "Programming",
        "plain_explanation": "Takes your Python skills beyond basic scripts to writing professional, reusable code with object-oriented programming (classes), decorators, generators, and clean error handling.",
        "prerequisites": ["python-basics"],
        "estimated_hours_per_level": 16.0,
        "difficulty": 1.2,
        "common_mistakes": [
            "Creating complicated object hierarchies when simple functions would do the job",
            "Ignoring list comprehensions and writing sluggish 5-line for loops",
            "Broad try/except blocks (`except Exception: pass`) that swallow critical bugs silently"
        ],
        "done_criteria": [
            "Can build custom classes with methods, properties, and inheritance",
            "Can use list and dictionary comprehensions effectively",
            "Can write robust error handling using try-except-finally blocks"
        ],
        "learning_method": {
            "watch_pct": 30,
            "practice_pct": 50,
            "build_pct": 20,
            "first_step": "Refactor a simple procedural script into an Object-Oriented module with type hints.",
            "tip": "Write unit tests for your functions so you can verify they work in all edge cases."
        }
    },
    {
        "slug": "html-css",
        "name": "HTML & CSS",
        "category": "Programming",
        "plain_explanation": "The building blocks of every website on Earth. HTML is the skeleton that gives pages content (headings, paragraphs, buttons), and CSS is the styling that makes it look modern and visually appealing.",
        "prerequisites": [],
        "estimated_hours_per_level": 10.0,
        "difficulty": 0.7,
        "common_mistakes": [
            "Using generic <div> tags everywhere instead of semantic HTML (<header>, <nav>, <main>, <button>)",
            "Hardcoding fixed pixel widths that break immediately when viewed on mobile phones",
            "Not understanding the CSS box model (margin, border, padding, content)"
        ],
        "done_criteria": [
            "Can build a clean, multi-section webpage with semantic HTML5 tags",
            "Can align elements comfortably using modern CSS Flexbox and Grid",
            "Can write CSS media queries to make a page look great on mobile and desktop"
        ],
        "learning_method": {
            "watch_pct": 20,
            "practice_pct": 50,
            "build_pct": 30,
            "first_step": "Open your browser text editor and create a personal 'About Me' profile page with your photo and links.",
            "tip": "Inspect your favorite websites using Chrome DevTools (F12) to see how they style elements."
        }
    },
    {
        "slug": "javascript-basics",
        "name": "JavaScript Basics",
        "category": "Programming",
        "plain_explanation": "The programming language of the web. It makes websites alive and interactive: popups, buttons that load data without refreshing the page, animations, and form validation.",
        "prerequisites": ["html-css"],
        "estimated_hours_per_level": 14.0,
        "difficulty": 1.0,
        "common_mistakes": [
            "Confusing `==` (loose equality with type coercion) with `===` (strict equality)",
            "Struggling with asynchronous code (Promises and async/await) and getting `undefined`",
            "Over-relying on global variables instead of scoped constants"
        ],
        "done_criteria": [
            "Can manipulate the Document Object Model (DOM) to update text and styles on click",
            "Can use modern ES6 syntax: arrow functions, destructuring, template literals, and array methods (map, filter)",
            "Can fetch JSON data from an external REST API using `fetch()` and `async/await`"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 55,
            "build_pct": 20,
            "first_step": "Build a button on a webpage that fetches a random dog picture or joke and displays it.",
            "tip": "Master JavaScript arrays and objects thoroughly because all web APIs send data in this shape."
        }
    },
    {
        "slug": "typescript",
        "name": "TypeScript",
        "category": "Programming",
        "plain_explanation": "JavaScript with built-in safety goggles. It adds explicit types to your variables and functions so your editor warns you about bugs before you ever run the code in a browser.",
        "prerequisites": ["javascript-basics"],
        "estimated_hours_per_level": 12.0,
        "difficulty": 1.1,
        "common_mistakes": [
            "Using `any` type everywhere, which defeats the entire purpose of TypeScript",
            "Creating overly convoluted union types instead of clean interfaces",
            "Fighting the compiler instead of reading the clear error message"
        ],
        "done_criteria": [
            "Can define interfaces and types for complex objects and API responses",
            "Can strongly type function parameters and return types",
            "Can use generics for flexible, reusable components"
        ],
        "learning_method": {
            "watch_pct": 30,
            "practice_pct": 50,
            "build_pct": 20,
            "first_step": "Convert a small JavaScript function with object parameters into TypeScript with an interface.",
            "tip": "Treat compiler errors as friendly hints that save you hours of debugging in production."
        }
    },
    {
        "slug": "bash-shell",
        "name": "Bash & Command Line",
        "category": "Programming",
        "plain_explanation": "The terminal window where developers type direct text commands to navigate folders, run scripts, manage files, and control servers without clicking a mouse.",
        "prerequisites": [],
        "estimated_hours_per_level": 8.0,
        "difficulty": 0.8,
        "common_mistakes": [
            "Being afraid of the black terminal screen",
            "Using `rm -rf` without checking the current working directory",
            "Not using Tab key autocomplete to finish folder and file names quickly"
        ],
        "done_criteria": [
            "Can navigate folders (`cd`), list files (`ls`), create files (`touch`, `mkdir`), and move files (`mv`)",
            "Can view and search file contents with `cat`, `grep`, and `less`",
            "Can write a simple 5-line bash script to automate a routine task"
        ],
        "learning_method": {
            "watch_pct": 15,
            "practice_pct": 75,
            "build_pct": 10,
            "first_step": "Open your computer terminal and practice navigating to your desktop and making a new folder.",
            "tip": "Always press the Tab key to auto-complete paths and avoid typos."
        }
    },

    # --- DATA & ANALYTICS ---
    {
        "slug": "pandas",
        "name": "Pandas for Data Analysis",
        "category": "Data",
        "plain_explanation": "The most popular Python tool for working with tabular data (like spreadsheets). It lets you filter millions of rows, calculate summary statistics, and clean messy numbers in seconds.",
        "prerequisites": ["python-basics"],
        "estimated_hours_per_level": 15.0,
        "difficulty": 1.0,
        "common_mistakes": [
            "Using slow Python `for` loops instead of fast vectorized Pandas operations",
            "Modifying a slice of a DataFrame and getting `SettingWithCopyWarning`",
            "Not handling missing (`NaN`) values properly before calculating averages"
        ],
        "done_criteria": [
            "Can load CSV, Excel, and JSON files into a DataFrame",
            "Can filter, sort, group, and calculate aggregations using `.groupby()`",
            "Can clean missing values, remove duplicates, and merge two DataFrames together"
        ],
        "learning_method": {
            "watch_pct": 20,
            "practice_pct": 60,
            "build_pct": 20,
            "first_step": "Download a free movie or sports dataset from Kaggle and calculate the average score by year.",
            "tip": "Whenever you think about writing a loop in Pandas, ask: 'Is there a built-in method for this?'"
        }
    },
    {
        "slug": "numpy",
        "name": "NumPy Fundamentals",
        "category": "Data",
        "plain_explanation": "The numerical engine behind almost every data science and AI tool in Python. It does lightning-fast math on large grids of numbers (arrays and matrices).",
        "prerequisites": ["python-basics"],
        "estimated_hours_per_level": 10.0,
        "difficulty": 1.0,
        "common_mistakes": [
            "Confusing Python lists with NumPy ndarrays",
            "Getting matrix dimension mismatches during multiplications",
            "Forgetting that NumPy arrays must contain elements of the same data type"
        ],
        "done_criteria": [
            "Can create and reshape 1D and 2D arrays",
            "Can perform element-wise arithmetic, slicing, and boolean masking",
            "Can compute dot products, averages, and standard deviations using NumPy functions"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 60,
            "build_pct": 15,
            "first_step": "Create a 3x3 matrix in NumPy and compute its transpose and row sums.",
            "tip": "Pay close attention to array shapes (`.shape`) to avoid dimensional errors."
        }
    },
    {
        "slug": "data-visualization",
        "name": "Data Visualization & Storytelling",
        "category": "Data",
        "plain_explanation": "Turning raw numbers into clear, honest charts that communicate the real story behind data without confusing or misleading the viewer.",
        "prerequisites": ["python-basics"],
        "estimated_hours_per_level": 12.0,
        "difficulty": 0.8,
        "common_mistakes": [
            "Using 3D pie charts or misleading truncated axes",
            "Cluttering charts with too many colors and unnecessary gridlines",
            "Presenting a chart without labeling the X and Y axes clearly"
        ],
        "done_criteria": [
            "Can choose the right chart type: bar for comparison, line for trends, scatter for correlation",
            "Can create clean charts in Python with Matplotlib and Seaborn",
            "Can explain chart findings in 2 clear sentences to a non-technical person"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 50,
            "build_pct": 25,
            "first_step": "Plot a trend line of global temperatures or smartphone sales over the past decade.",
            "tip": "Less is more: remove every visual element that doesn't help answer the main question."
        }
    },
    {
        "slug": "statistics-probability",
        "name": "Statistics & Probability",
        "category": "Data",
        "plain_explanation": "The math of understanding patterns and dealing with uncertainty. It helps you decide whether a change in numbers is a real trend or just random luck.",
        "prerequisites": [],
        "estimated_hours_per_level": 18.0,
        "difficulty": 1.2,
        "common_mistakes": [
            "Assuming correlation implies causation (just because two things rise together doesn't mean one caused the other)",
            "Misinterpreting p-values and statistical significance",
            "Ignoring the difference between mean (average) and median (middle value) in skewed data"
        ],
        "done_criteria": [
            "Can calculate and explain mean, median, standard deviation, and percentiles",
            "Can explain normal distributions, the central limit theorem, and confidence intervals",
            "Can design and evaluate a basic hypothesis test or A/B test"
        ],
        "learning_method": {
            "watch_pct": 40,
            "practice_pct": 45,
            "build_pct": 15,
            "first_step": "Watch Khan Academy's 10-minute video explaining why the median home price is more honest than the average.",
            "tip": "Always visualize the distribution curve before jumping into statistical formulas."
        }
    },
    {
        "slug": "power-bi-tableau",
        "name": "Power BI & Tableau",
        "category": "Data",
        "plain_explanation": "Drag-and-drop business intelligence software used by corporations worldwide to create interactive dashboards that executives click to inspect sales, expenses, and growth.",
        "prerequisites": ["sql-basics"],
        "estimated_hours_per_level": 14.0,
        "difficulty": 0.9,
        "common_mistakes": [
            "Cramming 15 different charts onto a single dashboard screen",
            "Not understanding the data relationship model (star schema) between tables",
            "Over-complicating DAX or calculated fields when the source data should be cleaned first"
        ],
        "done_criteria": [
            "Can import data, build relationships between tables, and create interactive slicers",
            "Can write basic DAX/LOD measures for Year-over-Year revenue growth",
            "Can publish and share an executive dashboard with clean visual hierarchy"
        ],
        "learning_method": {
            "watch_pct": 30,
            "practice_pct": 50,
            "build_pct": 20,
            "first_step": "Download Power BI Desktop (free) and import an Excel sample of supermarket sales.",
            "tip": "Design dashboards with the user's primary decision in the top-left corner."
        }
    },
    {
        "slug": "data-cleaning",
        "name": "Data Cleaning & Preprocessing",
        "category": "Data",
        "plain_explanation": "Real-world data is almost always messy: typos, duplicate rows, missing dates, and strange outliers. This skill teaches you how to systematically sanitize datasets so models don't learn junk.",
        "prerequisites": ["pandas"],
        "estimated_hours_per_level": 12.0,
        "difficulty": 1.0,
        "common_mistakes": [
            "Blindly dropping every row with a missing value and losing 40% of the dataset",
            "Data leakage: scaling or imputing data on the test set instead of fitting strictly on train",
            "Treating categorical codes as numeric magnitudes (e.g. labeling country codes 1, 2, 3)"
        ],
        "done_criteria": [
            "Can handle missing data using mean/median or domain-specific imputation",
            "Can encode categorical variables using One-Hot Encoding and Target Encoding",
            "Can scale numeric features using StandardScaler and MinMaxScaler"
        ],
        "learning_method": {
            "watch_pct": 20,
            "practice_pct": 60,
            "build_pct": 20,
            "first_step": "Take the famous Titanic dataset and clean the missing age and cabin columns safely.",
            "tip": "80% of a data professional's work is data cleaning; master this and you will stand out immediately."
        }
    },

    # --- AI & MACHINE LEARNING ---
    {
        "slug": "machine-learning-basics",
        "name": "Machine Learning Fundamentals",
        "category": "AI",
        "plain_explanation": "Teaching computers to find mathematical patterns in past data to make predictions about new, unseen data, without being explicitly programmed with if-else rules for every scenario.",
        "prerequisites": ["python-basics", "statistics-probability"],
        "estimated_hours_per_level": 18.0,
        "difficulty": 1.2,
        "common_mistakes": [
            "Training and evaluating on the exact same data (overfitting / cheating)",
            "Jumping to complex neural networks when a simple linear regression or decision tree would perform better",
            "Ignoring feature scaling and data preprocessing steps"
        ],
        "done_criteria": [
            "Can explain the difference between Supervised (classification/regression) and Unsupervised learning",
            "Can split data into Train, Validation, and Test sets properly",
            "Can train a Linear Regression and Decision Tree classifier and explain the predictions"
        ],
        "learning_method": {
            "watch_pct": 35,
            "practice_pct": 45,
            "build_pct": 20,
            "first_step": "Watch Andrew Ng's introductory Machine Learning video on supervised vs unsupervised learning.",
            "tip": "Always start with the simplest baseline model before trying complex algorithms."
        }
    },
    {
        "slug": "scikit-learn",
        "name": "Scikit-Learn",
        "category": "AI",
        "plain_explanation": "The industry-standard Python library containing ready-to-use implementations of classical machine learning algorithms like Random Forests, Support Vector Machines, and K-Means clustering.",
        "prerequisites": ["machine-learning-basics", "pandas"],
        "estimated_hours_per_level": 16.0,
        "difficulty": 1.1,
        "common_mistakes": [
            "Not using `Pipeline` and leaking test transformations into training data",
            "Evaluating models solely on Accuracy when classes are highly imbalanced (e.g. fraud detection)",
            "Over-tuning hyperparameters without cross-validation"
        ],
        "done_criteria": [
            "Can build an end-to-end `Pipeline` with transformers and an estimator",
            "Can evaluate models using Precision, Recall, F1-Score, and ROC-AUC curves",
            "Can tune model hyperparameters using `GridSearchCV` or `RandomizedSearchCV`"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 55,
            "build_pct": 20,
            "first_step": "Train a Random Forest on the Iris or Wine dataset and evaluate its confusion matrix.",
            "tip": "The consistent `.fit()` and `.predict()` API design in Scikit-Learn makes experimentation fast."
        }
    },
    {
        "slug": "deep-learning",
        "name": "Deep Learning Fundamentals",
        "category": "AI",
        "plain_explanation": "A branch of machine learning inspired by the human brain that uses multi-layered neural networks to learn representations from complex data like images, audio, and language.",
        "prerequisites": ["machine-learning-basics", "numpy"],
        "estimated_hours_per_level": 20.0,
        "difficulty": 1.4,
        "common_mistakes": [
            "Not understanding how gradient descent and backpropagation update network weights",
            "Setting an improper learning rate (too high diverges, too low never converges)",
            "Ignoring regularizers like Dropout and batch normalization, leading to severe overfitting"
        ],
        "done_criteria": [
            "Can explain perceptrons, activation functions (ReLU, Sigmoid, Softmax), and loss functions",
            "Can explain how backpropagation and Adam optimizer adjust weights",
            "Can describe Convolutional Neural Networks (CNNs) for images and Recurrent/Attention layers for sequences"
        ],
        "learning_method": {
            "watch_pct": 40,
            "practice_pct": 40,
            "build_pct": 20,
            "first_step": "Watch 3Blue1Brown's visual neural networks series on YouTube to see the math in motion.",
            "tip": "Visualize loss curves over training epochs to catch underfitting or overfitting early."
        }
    },
    {
        "slug": "pytorch",
        "name": "PyTorch",
        "category": "AI",
        "plain_explanation": "The favorite deep learning library of AI researchers and modern tech companies. It provides flexible tensors with automatic differentiation to build and train modern AI architectures.",
        "prerequisites": ["deep-learning", "advanced-python"],
        "estimated_hours_per_level": 22.0,
        "difficulty": 1.4,
        "common_mistakes": [
            "Forgetting to zero out gradients (`optimizer.zero_grad()`) before backward pass",
            "Forgetting `model.eval()` and `torch.no_grad()` during model validation",
            "Mixing CPU tensors with GPU tensors (`RuntimeError: Expected all tensors to be on the same device`)"
        ],
        "done_criteria": [
            "Can write a custom PyTorch `nn.Module` subclass with `forward()` pass",
            "Can write a clean standard training loop: forward pass, loss calculation, backward pass, optimizer step",
            "Can create custom `Dataset` and `DataLoader` for batching"
        ],
        "learning_method": {
            "watch_pct": 30,
            "practice_pct": 45,
            "build_pct": 25,
            "first_step": "Follow the official PyTorch 60-Minute Blitz tutorial on creating and multiplying tensors.",
            "tip": "Print tensor shapes inside `forward()` whenever you get a dimension mismatch."
        }
    },
    {
        "slug": "nlp-basics",
        "name": "Natural Language Processing (NLP)",
        "category": "AI",
        "plain_explanation": "Enabling computers to read, analyze, and generate human language: sentiment analysis, language translation, text summarization, and question answering.",
        "prerequisites": ["scikit-learn"],
        "estimated_hours_per_level": 18.0,
        "difficulty": 1.3,
        "common_mistakes": [
            "Treating words as isolated strings without semantic meaning",
            "Applying aggressive text stemming that destroys valuable grammar meaning",
            "Ignoring out-of-vocabulary words during tokenization"
        ],
        "done_criteria": [
            "Can tokenize text and convert words into numerical vectors using TF-IDF and embeddings",
            "Can build a text classification model for sentiment detection (Positive/Negative)",
            "Can explain how the Transformer architecture and self-attention mechanism work"
        ],
        "learning_method": {
            "watch_pct": 35,
            "practice_pct": 45,
            "build_pct": 20,
            "first_step": "Build a sentiment analyzer on movie reviews using Hugging Face transformers or scikit-learn.",
            "tip": "Understanding word embeddings (vector representations of meaning) is the key to all modern NLP."
        }
    },
    {
        "slug": "llms-prompt-engineering",
        "name": "LLMs & Prompt Engineering",
        "category": "AI",
        "plain_explanation": "How to effectively utilize, steer, and build applications on top of Large Language Models (like Gemini and GPT) using structured prompts, few-shot examples, and API integration.",
        "prerequisites": ["python-basics"],
        "estimated_hours_per_level": 14.0,
        "difficulty": 0.9,
        "common_mistakes": [
            "Vague prompts with no clear role, constraints, or desired output schema",
            "Failing to guard against prompt injection when incorporating user inputs into LLM queries",
            "Assuming LLMs have real-time memory or internal reasoning rather than next-token probability"
        ],
        "done_criteria": [
            "Can write structured system prompts with persona, constraints, and JSON response formatting",
            "Can use few-shot examples and chain-of-thought prompting to improve accuracy",
            "Can call modern LLM APIs (like Google Gemini API) programmatically with retry logic and Pydantic validation"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 50,
            "build_pct": 25,
            "first_step": "Write a Python script that calls the Gemini API to summarize a 5-paragraph article into 3 bullet points in valid JSON.",
            "tip": "Always specify exact output schemas (like JSON) and validate responses before downstream processing."
        }
    },
    {
        "slug": "mlops-deployment",
        "name": "MLOps & Model Deployment",
        "category": "AI",
        "plain_explanation": "Taking trained models off a data scientist's laptop and deploying them as reliable, fast, and monitored production cloud web services.",
        "prerequisites": ["scikit-learn", "git-github"],
        "estimated_hours_per_level": 18.0,
        "difficulty": 1.3,
        "common_mistakes": [
            "Serving raw pickled models without checking for library version incompatibilities",
            "Loading heavy model weights on every single incoming HTTP request instead of on server startup",
            "Failing to monitor data drift and model degradation over time"
        ],
        "done_criteria": [
            "Can package a trained machine learning model inside a FastAPI REST service",
            "Can containerize the ML application using a Dockerfile",
            "Can track model experiments and artifacts using MLflow or Weights & Biases"
        ],
        "learning_method": {
            "watch_pct": 30,
            "practice_pct": 45,
            "build_pct": 25,
            "first_step": "Create a 10-line FastAPI endpoint that accepts house features and returns a predicted price.",
            "tip": "A model that isn't deployed and accessible via an API delivers zero value to users."
        }
    },

    # --- WEB DEVELOPMENT ---
    {
        "slug": "react-basics",
        "name": "React Basics",
        "category": "Web",
        "plain_explanation": "The most popular web library in the world. It lets you build websites out of reusable visual LEGO blocks called 'components' that automatically update when data changes.",
        "prerequisites": ["javascript-basics"],
        "estimated_hours_per_level": 16.0,
        "difficulty": 1.1,
        "common_mistakes": [
            "Directly mutating state variables (`state.name = 'X'`) instead of calling the setter function",
            "Creating infinite re-render loops by setting state unconditionally inside the component body",
            "Putting every variable into state when regular variables or props would suffice"
        ],
        "done_criteria": [
            "Can create reusable functional components and pass information between them using props",
            "Can manage component state using the `useState` hook",
            "Can render dynamic lists with proper unique `key` props and handle user click events"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 50,
            "build_pct": 25,
            "first_step": "Build an interactive counter app with Increment, Decrement, and Reset buttons in React.",
            "tip": "Think of React as: UI = Component(Data). Whenever data changes, the UI updates automatically."
        }
    },
    {
        "slug": "tailwind-css",
        "name": "Tailwind CSS",
        "category": "Web",
        "plain_explanation": "A utility-first CSS framework that lets you style modern, responsive websites directly inside your HTML or React code without jumping between separate CSS files.",
        "prerequisites": ["html-css"],
        "estimated_hours_per_level": 10.0,
        "difficulty": 0.8,
        "common_mistakes": [
            "Not configuring responsive prefixes (`md:`, `lg:`) to adapt layouts for mobile devices",
            "Writing chaotic long class strings without extracting reusable component patterns",
            "Forgetting to configure the content purge path in `tailwind.config.js`"
        ],
        "done_criteria": [
            "Can style flexbox and grid layouts, typography, padding, and colors with Tailwind classes",
            "Can build responsive layouts that automatically adjust on mobile, tablet, and desktop",
            "Can implement clean hover, focus, and transition effects"
        ],
        "learning_method": {
            "watch_pct": 15,
            "practice_pct": 60,
            "build_pct": 25,
            "first_step": "Style a clean card with an avatar, title, badge, and button purely using Tailwind utility classes.",
            "tip": "Keep the Tailwind CSS cheatsheet or docs open in a side window as you build."
        }
    },
    {
        "slug": "fastapi",
        "name": "FastAPI & REST APIs",
        "category": "Web",
        "plain_explanation": "A lightning-fast, modern Python web framework used to build backend APIs. It automatically validates incoming data and generates interactive documentation for your API.",
        "prerequisites": ["python-basics"],
        "estimated_hours_per_level": 14.0,
        "difficulty": 1.0,
        "common_mistakes": [
            "Blocking the asynchronous event loop with heavy synchronous CPU tasks",
            "Not defining Pydantic models for request bodies and response schemas",
            "Hardcoding database connections directly in route handlers instead of using dependency injection (`Depends`)"
        ],
        "done_criteria": [
            "Can create GET, POST, PUT, and DELETE endpoints with path and query parameters",
            "Can validate incoming request bodies using Pydantic v2 schemas",
            "Can connect endpoints to an SQLite or PostgreSQL database using SQLAlchemy"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 50,
            "build_pct": 25,
            "first_step": "Create a 5-line FastAPI app and open `/docs` in your browser to see the automatic Swagger UI.",
            "tip": "FastAPI's dependency injection system makes authentication and database sessions clean and testable."
        }
    },
    {
        "slug": "auth-jwt",
        "name": "Authentication & JWT",
        "category": "Web",
        "plain_explanation": "How web applications securely verify who a user is (login) and protect private pages so only authorized people can view or edit them.",
        "prerequisites": ["fastapi"],
        "estimated_hours_per_level": 12.0,
        "difficulty": 1.2,
        "common_mistakes": [
            "Storing plaintext passwords in the database instead of hashing them with bcrypt",
            "Putting sensitive data (like passwords or credit cards) inside JWT token payloads",
            "Failing to set token expiration times and secure HTTPS cookies"
        ],
        "done_criteria": [
            "Can hash passwords using bcrypt before saving to a database",
            "Can generate signed JSON Web Tokens (JWT) upon successful login",
            "Can protect sensitive backend endpoints with authorization checks and decode the user identity"
        ],
        "learning_method": {
            "watch_pct": 30,
            "practice_pct": 50,
            "build_pct": 20,
            "first_step": "Build a register and login endpoint that issues a token and verifies it on a protected `/profile` route.",
            "tip": "Never write your own cryptography; always use battle-tested libraries like Passlib and PyJWT."
        }
    },

    # --- CLOUD, DEVOPS & INFRASTRUCTURE ---
    {
        "slug": "docker",
        "name": "Docker & Containerization",
        "category": "Cloud",
        "plain_explanation": "Packages your application and everything it needs (code, Python version, libraries) into a lightweight, isolated container that runs identically on any computer or cloud server.",
        "prerequisites": ["bash-shell"],
        "estimated_hours_per_level": 14.0,
        "difficulty": 1.1,
        "common_mistakes": [
            "Creating massive multi-gigabyte container images by not using slim base images and `.dockerignore`",
            "Running containers as the root user in production",
            "Treating container filesystems as permanent storage instead of using volumes"
        ],
        "done_criteria": [
            "Can write a clean multi-stage `Dockerfile` for a web application",
            "Can build, tag, run, and inspect containers from the command line",
            "Can orchestrate multiple services (frontend, backend, database) with `docker-compose.yml`"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 55,
            "build_pct": 20,
            "first_step": "Write a simple Dockerfile for a Python script, build the image, and run it locally.",
            "tip": "Think of a Docker container as a lightweight, pre-configured miniature virtual machine."
        }
    },
    {
        "slug": "ci-cd-github-actions",
        "name": "CI/CD & GitHub Actions",
        "category": "Cloud",
        "plain_explanation": "Automating your development workflow so that every time you save and push code, automated robots immediately test it and deploy it live to the internet.",
        "prerequisites": ["git-github"],
        "estimated_hours_per_level": 12.0,
        "difficulty": 1.1,
        "common_mistakes": [
            "Exposing production API keys in plain text in YAML files instead of using GitHub Secrets",
            "Writing flaky tests that randomly fail and slow down the entire team",
            "Not testing workflow files on feature branches before merging to main"
        ],
        "done_criteria": [
            "Can write a GitHub Actions workflow that triggers on push and pull request",
            "Can run linters, type checks, and pytest unit tests automatically",
            "Can configure automated deployment to a hosting provider"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 55,
            "build_pct": 20,
            "first_step": "Create `.github/workflows/test.yml` in a repo and see the green checkmark appear on your commit.",
            "tip": "Automating tests saves hundreds of hours of manual testing and prevents embarrassing production bugs."
        }
    },
    {
        "slug": "aws-core",
        "name": "AWS Core Services",
        "category": "Cloud",
        "plain_explanation": "Amazon Web Services (AWS) provides the world's most widely used on-demand cloud computing platforms: servers (EC2), storage (S3), and serverless functions (Lambda).",
        "prerequisites": ["bash-shell"],
        "estimated_hours_per_level": 16.0,
        "difficulty": 1.2,
        "common_mistakes": [
            "Leaving expensive cloud servers running overnight and getting unexpected billing charges",
            "Using the root AWS account for daily tasks instead of an IAM user with restricted privileges",
            "Making S3 storage buckets publicly readable by accident"
        ],
        "done_criteria": [
            "Can create an IAM user and configure billing budget alerts",
            "Can launch and SSH into an Amazon EC2 Linux virtual machine",
            "Can upload and manage files using Amazon S3 with secure bucket policies"
        ],
        "learning_method": {
            "watch_pct": 35,
            "practice_pct": 45,
            "build_pct": 20,
            "first_step": "Create a free-tier AWS account and set a $1 zero-spend budget alert immediately.",
            "tip": "Always set a budget alert before launching any resources in cloud platforms."
        }
    },

    # --- TESTING & SECURITY ---
    {
        "slug": "unit-testing-pytest",
        "name": "Unit Testing & Pytest",
        "category": "Testing",
        "plain_explanation": "Writing small automated verification scripts that check whether each individual function in your code works correctly and handles unexpected input without crashing.",
        "prerequisites": ["python-basics"],
        "estimated_hours_per_level": 10.0,
        "difficulty": 0.9,
        "common_mistakes": [
            "Testing trivial boilerplate instead of critical business calculations and edge cases",
            "Tests depending on each other or on an active internet connection instead of using mocks",
            "Skipping tests because 'the code works fine on my machine'"
        ],
        "done_criteria": [
            "Can write unit tests using `pytest` and assert statements",
            "Can test edge cases: empty lists, null inputs, negative numbers, and boundary values",
            "Can use pytest fixtures to set up and tear down test database data cleanly"
        ],
        "learning_method": {
            "watch_pct": 20,
            "practice_pct": 60,
            "build_pct": 20,
            "first_step": "Write a function that calculates discount prices and write 4 pytest tests to verify edge cases.",
            "tip": "Good tests give you fearless confidence when changing or refactoring code."
        }
    },
    {
        "slug": "web-security-owasp",
        "name": "Web Security & OWASP Top 10",
        "category": "Testing",
        "plain_explanation": "Understanding the most common vulnerabilities hackers use to exploit websites (like SQL Injection and Cross-Site Scripting) and learning how to defend against them.",
        "prerequisites": ["sql-basics", "javascript-basics"],
        "estimated_hours_per_level": 14.0,
        "difficulty": 1.2,
        "common_mistakes": [
            "Concatenating raw user text directly into SQL queries (opening SQL injection vulnerabilities)",
            "Trusting user input on the frontend without server-side validation",
            "Exposing sensitive internal stack traces and server details in API error responses"
        ],
        "done_criteria": [
            "Can explain and prevent SQL Injection using parameterized queries and ORMs",
            "Can explain Cross-Site Scripting (XSS) and sanitize user HTML inputs",
            "Can implement CORS policies, rate limiting, and secure HTTP response headers"
        ],
        "learning_method": {
            "watch_pct": 35,
            "practice_pct": 45,
            "build_pct": 20,
            "first_step": "Explore the OWASP Juice Shop demo application to see real security vulnerabilities safely.",
            "tip": "Rule number one of security: Never, ever trust input from the client."
        }
    },

    # --- DESIGN & PRODUCT ---
    {
        "slug": "figma-basics",
        "name": "Figma & UI Prototyping",
        "category": "Design",
        "plain_explanation": "The industry's leading collaborative design tool where designers create wireframes, interface layouts, and interactive clickable prototypes before code is written.",
        "prerequisites": [],
        "estimated_hours_per_level": 12.0,
        "difficulty": 0.8,
        "common_mistakes": [
            "Not using Figma Auto Layout and spending hours nudging boxes manually",
            "Picking random colors and font sizes instead of setting up a consistent design token library",
            "Designing only for desktop screens and forgetting mobile screen sizes"
        ],
        "done_criteria": [
            "Can use Figma frames, vector tools, and Auto Layout with proper padding and gap settings",
            "Can build reusable Figma Components with variants (e.g. Primary, Secondary buttons)",
            "Can link screens with interactive prototype transitions and test on mobile"
        ],
        "learning_method": {
            "watch_pct": 25,
            "practice_pct": 55,
            "build_pct": 20,
            "first_step": "Sign up for a free Figma account and duplicate a community UI kit to inspect component structures.",
            "tip": "Master Auto Layout early; it makes designing responsive layouts second nature."
        }
    },
    {
        "slug": "user-research",
        "name": "User Research & Usability",
        "category": "Design",
        "plain_explanation": "Talking to real human beings to understand their frustrations, watching them use your product, and identifying what makes them confused or delighted.",
        "prerequisites": [],
        "estimated_hours_per_level": 10.0,
        "difficulty": 0.8,
        "common_mistakes": [
            "Asking leading questions like 'Don't you love this feature?' instead of open-ended inquiries",
            "Assuming you are the target user and designing solely for yourself",
            "Ignoring body language and pauses during user usability tests"
        ],
        "done_criteria": [
            "Can prepare an unbiased user interview script with 5 open-ended questions",
            "Can conduct a 20-minute usability test and document points of friction",
            "Can synthesize user observations into actionable design recommendations"
        ],
        "learning_method": {
            "watch_pct": 30,
            "practice_pct": 45,
            "build_pct": 25,
            "first_step": "Ask a friend or family member to sign up for an app while you watch quietly and take notes on where they hesitate.",
            "tip": "Watch what users actually do rather than just listening to what they say."
        }
    }
]

# Real, reputable free learning resources mapped to skills
RESOURCES_DATA = [
    # Python Basics
    {
        "skill_slug": "python-basics",
        "title": "Python for Beginners (Full Course)",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
        "difficulty": "Beginner",
        "duration": "4 hours",
        "provider": "freeCodeCamp",
        "free": True
    },
    {
        "skill_slug": "python-basics",
        "title": "Interactive Python Tutorial",
        "type": "tutorial",
        "url": "https://www.learnpython.org/",
        "difficulty": "Beginner",
        "duration": "6 hours",
        "provider": "LearnPython",
        "free": True
    },
    {
        "skill_slug": "python-basics",
        "title": "Python Practice Exercises (50+ Challenges)",
        "type": "exercise",
        "url": "https://exercism.org/tracks/python",
        "difficulty": "Beginner",
        "duration": "8 hours",
        "provider": "Exercism",
        "free": True
    },
    {
        "skill_slug": "python-basics",
        "title": "Automate the Boring Stuff with Python",
        "type": "book",
        "url": "https://automatetheboringstuff.com/",
        "difficulty": "Beginner",
        "duration": "12 hours",
        "provider": "Al Sweigart (Free Online Edition)",
        "free": True
    },

    # Git & GitHub
    {
        "skill_slug": "git-github",
        "title": "Git and GitHub for Beginners - Crash Course",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=RGOj5yH7evk",
        "difficulty": "Beginner",
        "duration": "1 hour",
        "provider": "freeCodeCamp",
        "free": True
    },
    {
        "skill_slug": "git-github",
        "title": "Learn Git Branching (Visual Interactive Game)",
        "type": "exercise",
        "url": "https://learngitbranching.js.org/",
        "difficulty": "Beginner",
        "duration": "2 hours",
        "provider": "LearnGitBranching",
        "free": True
    },
    {
        "skill_slug": "git-github",
        "title": "GitHub Skills: Introduction to GitHub",
        "type": "tutorial",
        "url": "https://skills.github.com/",
        "difficulty": "Beginner",
        "duration": "1 hour",
        "provider": "GitHub",
        "free": True
    },

    # SQL Basics
    {
        "skill_slug": "sql-basics",
        "title": "SQL Tutorial - Full Database Course for Beginners",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "difficulty": "Beginner",
        "duration": "4 hours",
        "provider": "freeCodeCamp",
        "free": True
    },
    {
        "skill_slug": "sql-basics",
        "title": "Interactive SQL Lessons & Practice",
        "type": "exercise",
        "url": "https://sqlzoo.net/",
        "difficulty": "Beginner",
        "duration": "5 hours",
        "provider": "SQLZoo",
        "free": True
    },
    {
        "skill_slug": "sql-basics",
        "title": "Intro to SQL: Querying and managing data",
        "type": "course",
        "url": "https://www.khanacademy.org/computing/computer-programming/sql",
        "difficulty": "Beginner",
        "duration": "4 hours",
        "provider": "Khan Academy",
        "free": True
    },

    # HTML & CSS
    {
        "skill_slug": "html-css",
        "title": "Responsive Web Design Certification",
        "type": "course",
        "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/",
        "difficulty": "Beginner",
        "duration": "20 hours",
        "provider": "freeCodeCamp",
        "free": True
    },
    {
        "skill_slug": "html-css",
        "title": "MDN Web Docs: Learn Web Development",
        "type": "tutorial",
        "url": "https://developer.mozilla.org/en-US/docs/Learn",
        "difficulty": "Beginner",
        "duration": "15 hours",
        "provider": "Mozilla MDN",
        "free": True
    },
    {
        "skill_slug": "html-css",
        "title": "Flexbox Froggy (A Game for Learning CSS Flexbox)",
        "type": "exercise",
        "url": "https://flexboxfroggy.com/",
        "difficulty": "Beginner",
        "duration": "1 hour",
        "provider": "Codepip",
        "free": True
    },

    # JavaScript Basics
    {
        "skill_slug": "javascript-basics",
        "title": "JavaScript Programming - Full Course",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=jS4aFq5-91M",
        "difficulty": "Beginner",
        "duration": "8 hours",
        "provider": "freeCodeCamp",
        "free": True
    },
    {
        "skill_slug": "javascript-basics",
        "title": "The Modern JavaScript Tutorial",
        "type": "book",
        "url": "https://javascript.info/",
        "difficulty": "Beginner",
        "duration": "25 hours",
        "provider": "javascript.info",
        "free": True
    },
    {
        "skill_slug": "javascript-basics",
        "title": "JavaScript30: 30 Day Vanilla JS Coding Challenge",
        "type": "project",
        "url": "https://javascript30.com/",
        "difficulty": "Intermediate",
        "duration": "15 hours",
        "provider": "Wes Bos",
        "free": True
    },

    # Pandas
    {
        "skill_slug": "pandas",
        "title": "Pandas Course - Kaggle Learn",
        "type": "tutorial",
        "url": "https://www.kaggle.com/learn/pandas",
        "difficulty": "Beginner",
        "duration": "4 hours",
        "provider": "Kaggle",
        "free": True
    },
    {
        "skill_slug": "pandas",
        "title": "Pandas Tutorial: Analyze real data with Python",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=vmEHCJofslg",
        "difficulty": "Beginner",
        "duration": "1 hour",
        "provider": "Keith Galli",
        "free": True
    },

    # Machine Learning Basics
    {
        "skill_slug": "machine-learning-basics",
        "title": "Intro to Machine Learning - Kaggle Learn",
        "type": "course",
        "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
        "difficulty": "Beginner",
        "duration": "3 hours",
        "provider": "Kaggle",
        "free": True
    },
    {
        "skill_slug": "machine-learning-basics",
        "title": "Machine Learning Specialization (Free Audit)",
        "type": "course",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "difficulty": "Beginner",
        "duration": "30 hours",
        "provider": "DeepLearning.AI / Stanford",
        "free": True
    },

    # Scikit-Learn
    {
        "skill_slug": "scikit-learn",
        "title": "Machine Learning with Python and Scikit-Learn",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=0B5eIE_1vpU",
        "difficulty": "Intermediate",
        "duration": "3 hours",
        "provider": "freeCodeCamp",
        "free": True
    },
    {
        "skill_slug": "scikit-learn",
        "title": "Official Scikit-Learn Getting Started Guide",
        "type": "tutorial",
        "url": "https://scikit-learn.org/stable/getting_started.html",
        "difficulty": "Intermediate",
        "duration": "4 hours",
        "provider": "scikit-learn.org",
        "free": True
    },

    # Deep Learning & PyTorch
    {
        "skill_slug": "deep-learning",
        "title": "Neural Networks (3Blue1Brown Chapter Series)",
        "type": "course",
        "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi",
        "difficulty": "Beginner",
        "duration": "2 hours",
        "provider": "3Blue1Brown",
        "free": True
    },
    {
        "skill_slug": "pytorch",
        "title": "PyTorch for Deep Learning Bootcamp",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=V_xro1bcAuA",
        "difficulty": "Intermediate",
        "duration": "26 hours",
        "provider": "Daniel Bourke / freeCodeCamp",
        "free": True
    },

    # LLMs & Prompt Engineering
    {
        "skill_slug": "llms-prompt-engineering",
        "title": "ChatGPT Prompt Engineering for Developers",
        "type": "course",
        "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/",
        "difficulty": "Beginner",
        "duration": "1 hour",
        "provider": "DeepLearning.AI",
        "free": True
    },
    {
        "skill_slug": "llms-prompt-engineering",
        "title": "Google Gemini API Quickstart Guide",
        "type": "tutorial",
        "url": "https://ai.google.dev/gemini-api/docs/quickstart",
        "difficulty": "Beginner",
        "duration": "1 hour",
        "provider": "Google DeepMind / Google AI",
        "free": True
    },

    # React Basics
    {
        "skill_slug": "react-basics",
        "title": "React Official Documentation: Quick Start",
        "type": "tutorial",
        "url": "https://react.dev/learn",
        "difficulty": "Beginner",
        "duration": "5 hours",
        "provider": "React Official",
        "free": True
    },
    {
        "skill_slug": "react-basics",
        "title": "React Course 2024 - Beginner to Pro",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=bMknfKXIFA8",
        "difficulty": "Beginner",
        "duration": "12 hours",
        "provider": "freeCodeCamp",
        "free": True
    },

    # Tailwind CSS
    {
        "skill_slug": "tailwind-css",
        "title": "Tailwind CSS Official Documentation & Examples",
        "type": "tutorial",
        "url": "https://tailwindcss.com/docs",
        "difficulty": "Beginner",
        "duration": "3 hours",
        "provider": "Tailwind Labs",
        "free": True
    },

    # FastAPI
    {
        "skill_slug": "fastapi",
        "title": "FastAPI Tutorial - User Guide",
        "type": "tutorial",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "difficulty": "Beginner",
        "duration": "6 hours",
        "provider": "FastAPI Official",
        "free": True
    },
    {
        "skill_slug": "fastapi",
        "title": "Python FastAPI Tutorial: Build a Full Web API",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA",
        "difficulty": "Beginner",
        "duration": "2 hours",
        "provider": "Amigoscode",
        "free": True
    },

    # Docker
    {
        "skill_slug": "docker",
        "title": "Docker Tutorial for Beginners",
        "type": "course",
        "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo",
        "difficulty": "Beginner",
        "duration": "2 hours",
        "provider": "TechWorld with Nana",
        "free": True
    },

    # Figma Basics
    {
        "skill_slug": "figma-basics",
        "title": "Figma for Beginners (Official Course)",
        "type": "course",
        "url": "https://www.youtube.com/playlist?list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4",
        "difficulty": "Beginner",
        "duration": "3 hours",
        "provider": "Figma",
        "free": True
    }
]

from backend.app.seed.seed_skills_extended import ADDITIONAL_SKILLS, ADDITIONAL_RESOURCES

# Combine base and extended skills & resources
ALL_SKILLS_DATA = SKILLS_DATA + ADDITIONAL_SKILLS
ALL_RESOURCES_DATA = RESOURCES_DATA + ADDITIONAL_RESOURCES

CAREER_SKILLS_MAP = {
    "ai-ml-engineer": [
        ("python-basics", 3, 5),
        ("advanced-python", 3, 4),
        ("statistics-probability", 3, 5),
        ("numpy", 3, 4),
        ("pandas", 3, 4),
        ("data-cleaning", 3, 4),
        ("machine-learning-basics", 3, 5),
        ("scikit-learn", 3, 5),
        ("deep-learning", 2, 4),
        ("pytorch", 2, 4),
        ("llms-prompt-engineering", 2, 4),
        ("mlops-deployment", 2, 3),
        ("git-github", 2, 3),
        ("docker", 2, 3),
        ("fastapi", 2, 3),
    ],
    "data-analyst": [
        ("sql-basics", 3, 5),
        ("excel-spreadsheets", 3, 4),
        ("pandas", 3, 5),
        ("data-visualization", 3, 5),
        ("statistics-probability", 2, 4),
        ("power-bi-tableau", 3, 4),
        ("data-cleaning", 3, 4),
        ("python-basics", 2, 3),
        ("git-github", 2, 2),
    ],
    "data-scientist": [
        ("python-basics", 3, 5),
        ("statistics-probability", 4, 5),
        ("pandas", 3, 5),
        ("numpy", 3, 4),
        ("data-cleaning", 3, 4),
        ("data-visualization", 3, 4),
        ("machine-learning-basics", 3, 5),
        ("scikit-learn", 3, 4),
        ("sql-basics", 3, 4),
        ("git-github", 2, 3),
        ("deep-learning", 2, 3),
    ],
    "full-stack-developer": [
        ("html-css", 3, 4),
        ("javascript-basics", 3, 5),
        ("react-basics", 3, 5),
        ("tailwind-css", 2, 3),
        ("python-basics", 3, 4),
        ("fastapi", 3, 5),
        ("sql-basics", 3, 4),
        ("auth-jwt", 2, 4),
        ("git-github", 3, 4),
        ("docker", 2, 3),
        ("unit-testing-pytest", 2, 3),
    ],
    "frontend-developer": [
        ("html-css", 4, 5),
        ("javascript-basics", 4, 5),
        ("typescript", 3, 4),
        ("react-basics", 4, 5),
        ("tailwind-css", 3, 4),
        ("git-github", 3, 4),
        ("figma-basics", 2, 3),
    ],
    "cloud-engineer": [
        ("bash-shell", 3, 5),
        ("aws-core", 3, 5),
        ("docker", 3, 4),
        ("ci-cd-github-actions", 3, 4),
        ("python-basics", 2, 3),
        ("web-security-owasp", 2, 4),
        ("git-github", 2, 3),
    ],
    "devops-engineer": [
        ("bash-shell", 4, 5),
        ("docker", 4, 5),
        ("ci-cd-github-actions", 4, 5),
        ("aws-core", 3, 4),
        ("git-github", 3, 4),
        ("python-basics", 2, 3),
        ("web-security-owasp", 2, 3),
    ],
    "cybersecurity-analyst": [
        ("bash-shell", 3, 4),
        ("web-security-owasp", 4, 5),
        ("python-basics", 2, 3),
        ("git-github", 2, 3),
        ("aws-core", 2, 3),
    ],
    "ui-ux-designer": [
        ("figma-basics", 4, 5),
        ("user-research", 4, 5),
        ("html-css", 2, 3),
        ("data-visualization", 2, 3),
    ],
    "data-engineer": [
        ("python-basics", 3, 5),
        ("sql-basics", 4, 5),
        ("pandas", 3, 4),
        ("docker", 3, 4),
        ("bash-shell", 3, 4),
        ("aws-core", 2, 3),
        ("git-github", 3, 3),
    ],
    "mobile-app-developer": [
        ("javascript-basics", 3, 5),
        ("react-basics", 3, 5),
        ("typescript", 2, 4),
        ("html-css", 2, 3),
        ("git-github", 2, 3),
    ],
    "software-tester-qa": [
        ("python-basics", 3, 4),
        ("unit-testing-pytest", 4, 5),
        ("git-github", 2, 3),
        ("web-security-owasp", 2, 3),
        ("sql-basics", 2, 3),
    ],
    "product-analyst": [
        ("sql-basics", 3, 5),
        ("pandas", 2, 4),
        ("statistics-probability", 3, 4),
        ("data-visualization", 3, 5),
        ("power-bi-tableau", 2, 4),
        ("user-research", 2, 3),
    ]
}
