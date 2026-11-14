"""
15 Curated, friendly discovery questions covering:
- What they enjoy (building, analyzing data, designing, helping people, solving puzzles)
- Subjects they like
- Work style (alone/team, creative/structured)
- Tiny 'try it' tasks (spot a pattern, logic ordering) to reveal natural aptitude
"""

DISCOVERY_QUESTIONS = [
    {
        "id": 1,
        "category": "enjoyment",
        "question": "When you have free time on a computer, what kind of activity feels most fun or satisfying to you?",
        "help_text": "Pick the one that sounds most exciting. There are no wrong answers!",
        "type": "single",
        "options": [
            {"value": "building_things", "label": "Building things from scratch (apps, games, websites, or 3D models)", "weights": {"full-stack-developer": 4, "frontend-developer": 4, "mobile-app-developer": 4}},
            {"value": "finding_patterns", "label": "Looking at interesting numbers or charts to discover why something happened", "weights": {"data-analyst": 4, "data-scientist": 4, "product-analyst": 4}},
            {"value": "teaching_machines", "label": "Making a computer predict or recognize things automatically (smart AI)", "weights": {"ai-ml-engineer": 5, "data-scientist": 4}},
            {"value": "visual_design", "label": "Choosing colors, fonts, and making things look clean, modern, and easy to use", "weights": {"ui-ux-designer": 5, "frontend-developer": 3}},
            {"value": "protecting_systems", "label": "Investigating how systems work and keeping them secure against attackers", "weights": {"cybersecurity-analyst": 5, "cloud-engineer": 3}}
        ]
    },
    {
        "id": 2,
        "category": "subjects",
        "question": "Which school or college subjects did you find most natural or least painful?",
        "help_text": "Select the one or two that you enjoyed most.",
        "type": "single",
        "options": [
            {"value": "math_logic", "label": "Mathematics, Probability, or Logic Puzzles", "weights": {"ai-ml-engineer": 4, "data-scientist": 4, "data-analyst": 3}},
            {"value": "art_english", "label": "Art, Graphic Design, English, or Creative Writing", "weights": {"ui-ux-designer": 4, "product-analyst": 3, "frontend-developer": 2}},
            {"value": "computer_science", "label": "Computer Science / Basic Programming / Web design", "weights": {"full-stack-developer": 4, "ai-ml-engineer": 3, "cloud-engineer": 3}},
            {"value": "business_economics", "label": "Business, Economics, or Social Science", "weights": {"data-analyst": 4, "product-analyst": 5}},
            {"value": "physics_electronics", "label": "Physics or Hardware / Electronics circuits", "weights": {"cloud-engineer": 4, "devops-engineer": 4}}
        ]
    },
    {
        "id": 3,
        "category": "work_style",
        "question": "How do you prefer to tackle a new project?",
        "help_text": "Think about your ideal daily work environment.",
        "type": "single",
        "options": [
            {"value": "creative_freedom", "label": "High creative freedom: give me an open canvas and let me experiment", "weights": {"ui-ux-designer": 4, "frontend-developer": 3, "data-scientist": 3}},
            {"value": "clear_structure", "label": "Clear structure and logic: I like clear rules, checklists, and predictable order", "weights": {"software-tester-qa": 5, "data-engineer": 4, "devops-engineer": 4}},
            {"value": "investigative", "label": "Detective work: digging into unknown problems to uncover hidden clues", "weights": {"cybersecurity-analyst": 5, "data-analyst": 4, "ai-ml-engineer": 3}},
            {"value": "business_impact", "label": "Strategic and human: talking with people and figuring out what to build next", "weights": {"product-analyst": 5, "ui-ux-designer": 3}}
        ]
    },
    {
        "id": 4,
        "category": "enjoyment",
        "question": "Imagine you are building a new smartphone app for students. Which part would you volunteer to do?",
        "help_text": "Which role sounds like the one you'd naturally gravitate towards?",
        "type": "single",
        "options": [
            {"value": "design_screens", "label": "Sketching how the app looks and how smooth the buttons feel", "weights": {"ui-ux-designer": 5, "frontend-developer": 3}},
            {"value": "code_features", "label": "Writing the code that makes login, chat, and buttons actually work", "weights": {"full-stack-developer": 5, "mobile-app-developer": 5}},
            {"value": "ai_features", "label": "Building the smart AI assistant that gives students personalized advice", "weights": {"ai-ml-engineer": 5, "data-scientist": 3}},
            {"value": "break_and_test", "label": "Trying every crazy scenario to find bugs and ensure it never crashes", "weights": {"software-tester-qa": 5}},
            {"value": "growth_metrics", "label": "Analyzing student feedback and usage data to see which features people love", "weights": {"product-analyst": 5, "data-analyst": 4}}
        ]
    },
    {
        "id": 5,
        "category": "aptitude",
        "question": "Mini Try-It (Pattern Spotting): Look at this sequence of numbers: 3, 6, 11, 18, 27, ___. What comes next?",
        "help_text": "Notice how the gap between each pair of numbers changes: +3, +5, +7, +9...",
        "type": "single",
        "options": [
            {"value": "36", "label": "36", "weights": {}},
            {"value": "38", "label": "38 (Correct! Next gap is +11: 27 + 11 = 38)", "weights": {"ai-ml-engineer": 4, "data-scientist": 4, "data-analyst": 3}},
            {"value": "35", "label": "35", "weights": {}},
            {"value": "40", "label": "40", "weights": {}}
        ]
    },
    {
        "id": 6,
        "category": "aptitude",
        "question": "Mini Try-It (Logic Puzzle): If all Data Analysts know SQL, and Arif knows SQL, does that guarantee Arif is a Data Analyst?",
        "help_text": "Think carefully about circles and categories.",
        "type": "single",
        "options": [
            {"value": "yes", "label": "Yes, absolutely", "weights": {}},
            {"value": "no", "label": "No (Correct! Software engineers and scientists also know SQL)", "weights": {"ai-ml-engineer": 4, "cybersecurity-analyst": 4, "software-tester-qa": 4}},
            {"value": "only_in_tech", "label": "Only if he works in tech", "weights": {}}
        ]
    },
    {
        "id": 7,
        "category": "enjoyment",
        "question": "When you encounter a frustrating bug or obstacle, what is your natural reaction?",
        "help_text": "Be honest about how your brain responds.",
        "type": "single",
        "options": [
            {"value": "tinker_until_fixed", "label": "I get obsessed and keep tinkering until it works; solving it feels amazing", "weights": {"full-stack-developer": 4, "devops-engineer": 4, "ai-ml-engineer": 4}},
            {"value": "step_back_analyze", "label": "I step back, write down possibilities, and test each hypothesis methodically", "weights": {"data-scientist": 4, "cybersecurity-analyst": 4, "software-tester-qa": 4}},
            {"value": "ask_rethink", "label": "I ask: 'Is there a simpler, more user-friendly way to achieve this goal?'", "weights": {"ui-ux-designer": 4, "product-analyst": 4}}
        ]
    },
    {
        "id": 8,
        "category": "work_style",
        "question": "Do you prefer seeing immediate visual results from your work, or working behind the scenes?",
        "help_text": "Both are equally prestigious and rewarding.",
        "type": "single",
        "options": [
            {"value": "immediate_visual", "label": "Immediate visual: I want to change a line of code and see it change on screen right away", "weights": {"frontend-developer": 5, "ui-ux-designer": 5, "mobile-app-developer": 4}},
            {"value": "behind_scenes", "label": "Behind the scenes: I love making systems fast, reliable, and secure without caring about colors", "weights": {"cloud-engineer": 5, "data-engineer": 5, "devops-engineer": 5}},
            {"value": "mix_both", "label": "A healthy mix of both visible results and solid backend logic", "weights": {"full-stack-developer": 5, "ai-ml-engineer": 3}}
        ]
    },
    {
        "id": 9,
        "category": "enjoyment",
        "question": "Which of these headlines would you be proudest to share on LinkedIn in 2 years?",
        "help_text": "Envision your future success.",
        "type": "single",
        "options": [
            {"value": "built_viral_app", "label": "'Our web app just crossed 100,000 active users!'", "weights": {"full-stack-developer": 5, "frontend-developer": 4}},
            {"value": "trained_ai_model", "label": "'Trained a new AI model that detects medical anomalies with 98% precision.'", "weights": {"ai-ml-engineer": 5, "data-scientist": 5}},
            {"value": "stopped_breach", "label": "'Identified and patched a critical vulnerability before any user data was compromised.'", "weights": {"cybersecurity-analyst": 5}},
            {"value": "uncovered_insight", "label": "'Discovered a pricing insight from 1M transactions that increased revenue by 25%.'", "weights": {"data-analyst": 5, "product-analyst": 5}},
            {"value": "redesigned_experience", "label": "'Redesigned our mobile experience, boosting user happiness ratings to 4.9 stars.'", "weights": {"ui-ux-designer": 5}}
        ]
    },
    {
        "id": 10,
        "category": "aptitude",
        "question": "Mini Try-It (Data Interpretation): A website has 1,000 visitors. 200 click a button, and 40 complete a purchase. What is the purchase conversion rate from total visitors?",
        "help_text": "Calculate: 40 out of 1,000 as a percentage.",
        "type": "single",
        "options": [
            {"value": "20%", "label": "20%", "weights": {}},
            {"value": "4%", "label": "4% (Correct! 40 / 1000 = 0.04 = 4%)", "weights": {"data-analyst": 4, "product-analyst": 4, "data-scientist": 3}},
            {"value": "2%", "label": "2%", "weights": {}},
            {"value": "40%", "label": "40%", "weights": {}}
        ]
    },
    {
        "id": 11,
        "category": "work_style",
        "question": "How comfortable are you with mathematics and statistics?",
        "help_text": "Be totally honest; many rewarding tech careers require almost zero advanced math!",
        "type": "single",
        "options": [
            {"value": "love_math", "label": "I genuinely enjoy math, probability, and linear algebra", "weights": {"ai-ml-engineer": 5, "data-scientist": 5}},
            {"value": "practical_math", "label": "I am fine with basic averages, percentages, and formulas if they solve real problems", "weights": {"data-analyst": 4, "product-analyst": 4, "full-stack-developer": 3}},
            {"value": "prefer_no_math", "label": "I prefer logic, visual design, or architecture over calculus and deep formulas", "weights": {"ui-ux-designer": 5, "frontend-developer": 4, "devops-engineer": 3, "cloud-engineer": 3}}
        ]
    },
    {
        "id": 12,
        "category": "enjoyment",
        "question": "Which tool would you feel most excited to master?",
        "help_text": "Pick the one that sparks your curiosity.",
        "type": "single",
        "options": [
            {"value": "python_pytorch", "label": "Python & PyTorch (training neural networks)", "weights": {"ai-ml-engineer": 5, "data-scientist": 4}},
            {"value": "sql_tableau", "label": "SQL & Tableau (pulling numbers and crafting dashboards)", "weights": {"data-analyst": 5, "product-analyst": 4}},
            {"value": "react_tailwind", "label": "React & Tailwind CSS (building modern, slick web apps)", "weights": {"frontend-developer": 5, "full-stack-developer": 5}},
            {"value": "figma", "label": "Figma (wireframing and user experience design)", "weights": {"ui-ux-designer": 5}},
            {"value": "docker_aws", "label": "Docker & AWS Cloud (managing scalable servers and pipelines)", "weights": {"cloud-engineer": 5, "devops-engineer": 5}}
        ]
    },
    {
        "id": 13,
        "category": "work_style",
        "question": "When working in a team, which role do you naturally fall into?",
        "help_text": "Think about past group assignments or hobbies.",
        "type": "single",
        "options": [
            {"value": "the_builder", "label": "The Builder: I quiet down, write the code, and make the thing work", "weights": {"full-stack-developer": 4, "ai-ml-engineer": 4, "data-engineer": 4}},
            {"value": "the_designer", "label": "The Visualizer: I make sure the presentation slides and demo look stunning", "weights": {"ui-ux-designer": 5, "frontend-developer": 4}},
            {"value": "the_analyst", "label": "The Fact-Checker: I check the facts, analyze the results, and ensure calculations are right", "weights": {"data-analyst": 4, "data-scientist": 4, "software-tester-qa": 4}},
            {"value": "the_organizer", "label": "The Coordinator: I define milestones, manage deadlines, and align what we are building", "weights": {"product-analyst": 5}}
        ]
    },
    {
        "id": 14,
        "category": "aptitude",
        "question": "Mini Try-It (System Debugging): A user clicks 'Submit' on a form, but nothing happens. Which step should a developer check first?",
        "help_text": "Think about the sequence of events when a click happens.",
        "type": "single",
        "options": [
            {"value": "buy_new_server", "label": "Buy a bigger cloud server immediately", "weights": {}},
            {"value": "check_console_errors", "label": "Open browser console to see if an error occurred on click (Correct!)", "weights": {"full-stack-developer": 4, "software-tester-qa": 4, "frontend-developer": 4}},
            {"value": "reinstall_os", "label": "Reinstall the computer operating system", "weights": {}}
        ]
    },
    {
        "id": 15,
        "category": "goals",
        "question": "What is your primary goal for the next 6 to 12 months?",
        "help_text": "This helps SkillPath tune your weekly pace and milestone calendar.",
        "type": "single",
        "options": [
            {"value": "explore_options", "label": "I want to explore options and build my very first working project", "weights": {"data-analyst": 3, "full-stack-developer": 3, "ui-ux-designer": 3}},
            {"value": "internship_ready", "label": "I need to become internship-ready for summer campus placements", "weights": {"ai-ml-engineer": 4, "full-stack-developer": 4, "data-analyst": 4}},
            {"value": "job_switch", "label": "I want a clear, step-by-step career transition roadmap to land a full-time job", "weights": {"full-stack-developer": 4, "data-analyst": 4, "cloud-engineer": 4}}
        ]
    }
]

