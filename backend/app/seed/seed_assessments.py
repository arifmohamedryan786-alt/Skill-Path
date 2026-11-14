"""
Pre-seeded assessments with 5 MCQs and 1 practical task each.
"""

ASSESSMENTS_DATA = {
    "python-basics": {
        "title": "Python Basics Core Proficiency Assessment",
        "description": "Tests your understanding of Python variables, lists, control flow, functions, and error handling.",
        "target_level": 2,
        "questions": [
            {
                "id": 1,
                "question": "What is the output of `type([1, 2, 3])` in Python?",
                "options": ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"],
                "correct_index": 0,
                "explanation": "In Python, square brackets `[...]` denote a standard built-in `list`."
            },
            {
                "id": 2,
                "question": "Which of the following creates a dictionary with keys 'a' and 'b'?",
                "options": ["{'a': 1, 'b': 2}", "['a': 1, 'b': 2]", "('a': 1, 'b': 2)", "<'a'=1, 'b'=2>"],
                "correct_index": 0,
                "explanation": "Curly braces with key:value pairs define a Python dictionary (`dict`)."
            },
            {
                "id": 3,
                "question": "What does `range(1, 6)` produce when converted to a list?",
                "options": ["[1, 2, 3, 4, 5]", "[1, 2, 3, 4, 5, 6]", "[0, 1, 2, 3, 4, 5]", "[2, 3, 4, 5, 6]"],
                "correct_index": 0,
                "explanation": "`range(start, stop)` includes `start` up to but not including `stop`."
            },
            {
                "id": 4,
                "question": "How do you handle potential errors during file or mathematical operations in Python?",
                "options": ["try ... except", "catch ... throw", "do ... while", "validate ... error"],
                "correct_index": 0,
                "explanation": "Python uses `try:` followed by `except Exception:` blocks to handle exceptions gracefully."
            },
            {
                "id": 5,
                "question": "What will `[x * 2 for x in [1, 2, 3]]` return?",
                "options": ["[2, 4, 6]", "[1, 2, 3, 1, 2, 3]", "[2, 2, 2]", "TypeError"],
                "correct_index": 0,
                "explanation": "This is a list comprehension multiplying each element by 2, yielding [2, 4, 6]."
            }
        ],
        "practical_task": {
            "prompt": "Write a Python function `filter_even_numbers(numbers)` that takes a list of integers and returns only the even numbers in the same order.",
            "hint": "Use the modulo operator `x % 2 == 0` or a list comprehension.",
            "evaluation_criteria": "Function must return [2, 4, 6] for input [1, 2, 3, 4, 5, 6] and handle empty lists safely.",
            "starter_code": "def filter_even_numbers(numbers):\n    # Write your solution here\n    pass"
        }
    },
    "statistics-probability": {
        "title": "Statistics & Probability Foundations Assessment",
        "description": "Tests your understanding of central tendency, distributions, standard deviation, and hypothesis testing.",
        "target_level": 2,
        "questions": [
            {
                "id": 1,
                "question": "Given the dataset [2, 3, 5, 7, 100], which measure of central tendency gives the most representative 'typical' value?",
                "options": ["Median (5)", "Mean (23.4)", "Mode", "Standard Deviation"],
                "correct_index": 0,
                "explanation": "Because 100 is an extreme outlier, the median (5) is resilient, whereas the mean is distorted."
            },
            {
                "id": 2,
                "question": "In a standard normal distribution, approximately what percentage of data falls within 1 standard deviation of the mean?",
                "options": ["68%", "95%", "99.7%", "50%"],
                "correct_index": 0,
                "explanation": "According to the empirical rule (68-95-99.7), roughly 68% falls within ±1σ of the mean."
            },
            {
                "id": 3,
                "question": "What does a p-value of 0.03 indicate when testing with a significance threshold of α = 0.05?",
                "options": [
                    "Reject the null hypothesis (the result is statistically significant)",
                    "Accept the null hypothesis (the result is likely chance)",
                    "The test was invalid",
                    "The sample size was too small"
                ],
                "correct_index": 0,
                "explanation": "When p-value < α (0.03 < 0.05), we reject the null hypothesis in favor of the alternative."
            },
            {
                "id": 4,
                "question": "What is the probability of rolling a sum of 7 with two fair 6-sided dice?",
                "options": ["6/36 (1/6)", "7/36", "1/12", "1/7"],
                "correct_index": 0,
                "explanation": "Combinations for 7 are (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 outcomes out of 36."
            },
            {
                "id": 5,
                "question": "What does a correlation coefficient of r = -0.85 imply?",
                "options": [
                    "Strong negative linear relationship",
                    "Weak positive relationship",
                    "No correlation",
                    "Causation between variables"
                ],
                "correct_index": 0,
                "explanation": "r close to -1 indicates that as one variable increases, the other strongly tends to decrease."
            }
        ],
        "practical_task": {
            "prompt": "Write a Python function `compute_summary_stats(values)` that takes a list of numbers and returns a dict with 'mean' and 'median'.",
            "hint": "Sort the list first to find the middle element for the median.",
            "evaluation_criteria": "Correctly returns mean and median for both odd and even length lists.",
            "starter_code": "def compute_summary_stats(values):\n    # Return {'mean': ..., 'median': ...}\n    pass"
        }
    },
    "sql-basics": {
        "title": "SQL Basics & Querying Assessment",
        "description": "Tests your ability to write SELECT statements, filter with WHERE, aggregate with GROUP BY, and join tables.",
        "target_level": 2,
        "questions": [
            {
                "id": 1,
                "question": "Which SQL clause is used to filter rows before any grouping occurs?",
                "options": ["WHERE", "HAVING", "GROUP BY", "ORDER BY"],
                "correct_index": 0,
                "explanation": "WHERE filters individual rows before aggregation; HAVING filters aggregated groups."
            },
            {
                "id": 2,
                "question": "What will `SELECT COUNT(*) FROM students WHERE marks >= 70;` return?",
                "options": [
                    "The number of students who scored 70 or above",
                    "The average mark of passing students",
                    "The list of student names",
                    "A boolean TRUE or FALSE"
                ],
                "correct_index": 0,
                "explanation": "COUNT(*) counts the total number of rows matching the WHERE criteria."
            },
            {
                "id": 3,
                "question": "Which JOIN returns all rows from the left table even if there is no match in the right table?",
                "options": ["LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "CROSS JOIN"],
                "correct_index": 0,
                "explanation": "LEFT JOIN keeps every record from the left table and fills non-matching right columns with NULL."
            },
            {
                "id": 4,
                "question": "How do you sort query results from highest to lowest salary?",
                "options": ["ORDER BY salary DESC", "SORT BY salary DOWN", "ORDER BY salary ASC", "GROUP BY salary DESC"],
                "correct_index": 0,
                "explanation": "ORDER BY with the DESC keyword sorts in descending (highest first) order."
            },
            {
                "id": 5,
                "question": "What keyword eliminates duplicate rows from a SELECT query?",
                "options": ["DISTINCT", "UNIQUE", "DIFFERENT", "SEPARATE"],
                "correct_index": 0,
                "explanation": "SELECT DISTINCT returns only unique values across the specified columns."
            }
        ],
        "practical_task": {
            "prompt": "Write a SQL query that retrieves `department` and the average `salary` as `avg_salary` from an `employees` table, showing only departments with more than 5 employees, ordered by `avg_salary` descending.",
            "hint": "Use GROUP BY, HAVING COUNT(*) > 5, and ORDER BY avg_salary DESC.",
            "evaluation_criteria": "Correct syntax with SELECT, GROUP BY, HAVING, and ORDER BY.",
            "starter_code": "-- Write your SQL query below\nSELECT department, AVG(salary) AS avg_salary FROM employees ..."
        }
    }
}

