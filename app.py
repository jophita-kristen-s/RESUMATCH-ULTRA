from flask import Flask, render_template, request, jsonify
import re
import random
import math
import os

app = Flask(__name__)

# ─────────────────────────────────────────────
# DATA: SKILL DATABASE
# ─────────────────────────────────────────────
SKILL_DB = [
    "python","java","javascript","typescript","c++","c#","golang","rust","swift","kotlin","php","ruby","scala","r","dart","elixir",
    "machine learning","deep learning","data science","nlp","computer vision","generative ai","llm","mlops","reinforcement learning","statistics",
    "tensorflow","pytorch","scikit-learn","keras","pandas","numpy","opencv","huggingface","langchain","openai","vector databases",
    "aws","azure","gcp","docker","kubernetes","terraform","ansible","devops","ci/cd","jenkins","github actions","helm","prometheus","grafana",
    "react","vue","angular","next.js","svelte","node","express","django","flask","fastapi","spring boot","laravel","rails","nestjs",
    "postgresql","mysql","mongodb","redis","elasticsearch","kafka","cassandra","sqlite","firebase","supabase","dynamodb","neo4j",
    "rest api","graphql","microservices","agile","scrum","git","linux","bash","powershell","networking","tcp/ip",
    "excel","power bi","tableau","spark","hadoop","airflow","dbt","snowflake","bigquery","looker","databricks","flink",
    "figma","ui/ux","product management","data engineering","cybersecurity","blockchain","web3","solidity",
    "flutter","react native","android","ios","unity","unreal engine",
    "html","css","tailwind","bootstrap","sass","webpack","vite",
    "testing","jest","selenium","cypress","qa","penetration testing","ethical hacking",
    "sap","salesforce","servicenow","jira","confluence",
    "sql",
]

ROLE_SKILLS = {
    "Data Scientist":       {"skills":["python","machine learning","scikit-learn","pandas","numpy","sql","statistics","tensorflow","tableau"],"salary":{"IN":"12–30 LPA","US":"$110–160K","UK":"£60–95K","AU":"A$100–140K"}},
    "ML Engineer":          {"skills":["python","tensorflow","pytorch","mlops","docker","kubernetes","aws","data science","ci/cd"],"salary":{"IN":"18–45 LPA","US":"$130–180K","UK":"£75–110K","AU":"A$120–160K"}},
    "AI Engineer":          {"skills":["python","llm","langchain","huggingface","pytorch","openai","vector databases","mlops","aws","fastapi"],"salary":{"IN":"20–50 LPA","US":"$140–200K","UK":"£80–130K","AU":"A$130–180K"}},
    "Backend Developer":    {"skills":["java","python","rest api","postgresql","docker","kubernetes","microservices","redis","aws","git"],"salary":{"IN":"10–28 LPA","US":"$100–150K","UK":"£55–90K","AU":"A$90–130K"}},
    "Frontend Developer":   {"skills":["javascript","typescript","react","html","css","figma","git","rest api","testing","tailwind"],"salary":{"IN":"8–22 LPA","US":"$90–140K","UK":"£50–80K","AU":"A$80–120K"}},
    "Full Stack Developer": {"skills":["javascript","react","node","postgresql","rest api","docker","git","typescript","html","css"],"salary":{"IN":"12–35 LPA","US":"$110–160K","UK":"£60–95K","AU":"A$100–140K"}},
    "DevOps Engineer":      {"skills":["docker","kubernetes","terraform","aws","ci/cd","linux","bash","git","ansible","prometheus"],"salary":{"IN":"15–40 LPA","US":"$120–170K","UK":"£65–100K","AU":"A$110–150K"}},
    "Data Engineer":        {"skills":["python","spark","airflow","sql","kafka","aws","dbt","snowflake","postgresql","docker"],"salary":{"IN":"14–35 LPA","US":"$115–165K","UK":"£65–95K","AU":"A$105–145K"}},
    "Product Manager":      {"skills":["product management","agile","scrum","figma","sql","excel","jira","roadmapping","user research"],"salary":{"IN":"15–45 LPA","US":"$120–180K","UK":"£65–100K","AU":"A$110–155K"}},
    "Mobile Developer":     {"skills":["react native","flutter","android","ios","kotlin","swift","firebase","rest api","git","testing"],"salary":{"IN":"10–28 LPA","US":"$105–155K","UK":"£55–85K","AU":"A$90–130K"}},
    "Cybersecurity Analyst":{"skills":["cybersecurity","linux","networking","python","bash","penetration testing","ethical hacking","tcp/ip"],"salary":{"IN":"10–30 LPA","US":"$100–155K","UK":"£55–90K","AU":"A$90–130K"}},
    "Data Analyst":         {"skills":["sql","python","excel","tableau","power bi","pandas","statistics","bigquery"],"salary":{"IN":"6–18 LPA","US":"$80–120K","UK":"£40–70K","AU":"A$70–100K"}},
}

COMPANIES = {
    "India": {
        "Data Scientist":["Flipkart","Swiggy","Zomato","Ola","Paytm","PhonePe","CRED","Razorpay","Meesho","Freshworks","Zoho","Infosys","TCS","Wipro","HCL","Amazon India","Microsoft India","Google India","IBM India","Mu Sigma","LatentView Analytics","Tiger Analytics"],
        "ML Engineer":["Amazon India","Microsoft India","Google India","Flipkart","Swiggy","PhonePe","Razorpay","Ola","CRED","Unacademy","Dream11","MakeMyTrip","Nykaa","Juspay","Sarvam AI","Krutrim","Fractal Analytics"],
        "AI Engineer":["Google India","Microsoft India","Amazon India","Sarvam AI","Krutrim","Yellow.ai","Haptik","Observe.AI","Uniphore","Vernacular.ai","Fractal","LatentView","Juspay","Freshworks"],
        "Backend Developer":["Flipkart","Razorpay","PhonePe","Swiggy","Zomato","Ola","CRED","Meesho","Juspay","Groww","Zepto","Nykaa","MakeMyTrip","Zoho","Freshworks","Infosys","TCS","Wipro"],
        "Frontend Developer":["Flipkart","Swiggy","Zomato","CRED","Meesho","Nykaa","Groww","Zepto","Razorpay","PhonePe","Zoho","Freshworks","Infosys","TCS"],
        "Full Stack Developer":["Flipkart","Razorpay","CRED","Swiggy","Zomato","Meesho","Groww","PhonePe","Zoho","Freshworks","Juspay","Nykaa","Unacademy","BrowserStack"],
        "DevOps Engineer":["Amazon India","Microsoft India","Google India","Flipkart","Razorpay","PhonePe","Swiggy","Infosys","TCS","Wipro","HCL","Juspay","CRED"],
        "Data Engineer":["Amazon India","Flipkart","PhonePe","Razorpay","Swiggy","Mu Sigma","Fractal","LatentView","Meesho","CRED","Dream11","Groww"],
        "Data Analyst":["Amazon India","Flipkart","Swiggy","Zomato","PhonePe","CRED","Meesho","Groww","Nykaa","MakeMyTrip","Mu Sigma","LatentView"],
        "Product Manager":["Flipkart","Amazon India","Razorpay","CRED","PhonePe","Swiggy","Zomato","Meesho","Groww","Nykaa","Dream11","Unacademy"],
        "default":["Infosys","TCS","Wipro","HCL","Tech Mahindra","Capgemini","Accenture India","IBM India","Amazon India","Microsoft India","Google India","Flipkart","Razorpay","PhonePe","Swiggy","Zomato","Freshworks","Zoho"]
    },
    "United States": {"default":["Google","Meta","Apple","Microsoft","Amazon","Netflix","Stripe","Airbnb","Uber","Lyft","Salesforce","Adobe","Nvidia","OpenAI","Anthropic","Palantir","Snowflake","Databricks"]},
    "United Kingdom": {"default":["DeepMind","ARM","Revolut","Monzo","Wise","Ocado","Sky","BT","HSBC Tech","Barclays Tech","Lloyds Banking Group","BP Digital","Darktrace"]},
    "Germany": {"default":["SAP","Siemens","BMW Tech","Volkswagen Digital","Bosch","Deutsche Telekom","Celonis","Personio","N26","HelloFresh Tech","Delivery Hero","Zalando"]},
    "Singapore": {"default":["Sea Limited","Grab","Shopee","Lazada","Gojek","DBS Bank Tech","UOB Tech","Razer","Bytedance Singapore","Stripe APAC","Google APAC"]},
    "default": {"default":["Google","Microsoft","Amazon","Meta","Apple","IBM","Accenture","Deloitte","McKinsey Digital","Goldman Sachs Tech","Stripe","Uber","Airbnb","Nvidia"]},
}

SENIORITY = [
    {"level":"Junior","expYears":"0-2 years","titlePrefix":"Junior"},
    {"level":"Mid",   "expYears":"2-4 years","titlePrefix":""},
    {"level":"Mid",   "expYears":"3-5 years","titlePrefix":""},
    {"level":"Senior","expYears":"4-7 years","titlePrefix":"Senior"},
    {"level":"Senior","expYears":"5-8 years","titlePrefix":"Senior"},
    {"level":"Lead",  "expYears":"6-10 years","titlePrefix":"Lead"},
    {"level":"Mid",   "expYears":"2-5 years","titlePrefix":""},
    {"level":"Senior","expYears":"4-8 years","titlePrefix":"Senior"},
    {"level":"Junior","expYears":"1-3 years","titlePrefix":"Junior"},
    {"level":"Mid",   "expYears":"3-6 years","titlePrefix":""},
]

ROLE_VARIANTS = {
    "ML Engineer":["ML Engineer","Machine Learning Engineer","MLOps Engineer","Applied ML Engineer","ML Platform Engineer","ML Infrastructure Engineer"],
    "AI Engineer":["AI Engineer","Generative AI Engineer","LLM Engineer","AI/ML Engineer","Applied AI Engineer","AI Research Engineer"],
    "Data Scientist":["Data Scientist","Applied Data Scientist","Research Data Scientist","Sr. Data Scientist","Data Science Analyst","Quantitative Data Scientist"],
    "Data Engineer":["Data Engineer","Data Platform Engineer","Analytics Engineer","Data Infrastructure Engineer","Pipeline Engineer","Big Data Engineer"],
    "Data Analyst":["Data Analyst","Business Intelligence Analyst","Analytics Analyst","Insights Analyst","Product Analyst","BI Developer"],
    "Backend Developer":["Backend Engineer","Software Engineer - Backend","API Engineer","Platform Engineer","Backend Software Developer","Server-Side Engineer"],
    "Frontend Developer":["Frontend Engineer","UI Engineer","React Developer","Frontend Software Engineer","Web Developer","UI/UX Engineer"],
    "Full Stack Developer":["Full Stack Engineer","Software Engineer","Full Stack Developer","Web Engineer","Software Development Engineer","SDE II"],
    "DevOps Engineer":["DevOps Engineer","Platform Engineer","SRE","Infrastructure Engineer","Cloud Engineer","DevSecOps Engineer"],
    "Product Manager":["Product Manager","Senior PM","Associate PM","Group PM","Technical PM","Product Lead"],
    "Mobile Developer":["Mobile Engineer","iOS Engineer","Android Engineer","React Native Developer","Flutter Developer","Mobile Software Engineer"],
    "Cybersecurity Analyst":["Security Engineer","Cybersecurity Analyst","AppSec Engineer","Information Security Engineer","Penetration Tester","Security Analyst"],
}

ROLE_DESCRIPTIONS = {
    "ML Engineer":    lambda s: f"Build and deploy machine learning models using {s[0] if s else 'Python'} and {s[1] if len(s)>1 else 'TensorFlow'} at scale. Maintain ML pipelines, model versioning, and production infrastructure for real-time inference.",
    "AI Engineer":    lambda s: f"Design and ship AI-powered features using {s[0] if s else 'Python'} and LLM frameworks including {s[1] if len(s)>1 else 'LangChain'}. Integrate generative AI capabilities into production products with low latency.",
    "Data Scientist": lambda s: f"Apply {s[0] if s else 'Python'} and {s[1] if len(s)>1 else 'machine learning'} to extract insights from large datasets and drive business decisions. Build predictive models and communicate findings to stakeholders.",
    "Data Engineer":  lambda s: f"Design and maintain data pipelines using {s[0] if s else 'Python'} and {s[1] if len(s)>1 else 'Spark'} to move and transform data at scale. Build reliable ETL workflows and data warehouse solutions.",
    "Data Analyst":   lambda s: f"Analyse large datasets using {s[0] if s else 'SQL'} and {s[1] if len(s)>1 else 'Python'} to surface actionable business insights. Create dashboards, reports, and visualisations for cross-functional teams.",
    "Backend Developer": lambda s: f"Build scalable REST APIs and microservices using {s[0] if s else 'Python'} and {s[1] if len(s)>1 else 'PostgreSQL'}. Design backend architecture to handle high traffic and ensure system reliability.",
    "Frontend Developer": lambda s: f"Create responsive, performant UIs using {s[0] if s else 'React'} and {s[1] if len(s)>1 else 'TypeScript'}. Collaborate closely with designers and backend engineers to ship product features.",
    "Full Stack Developer": lambda s: f"Build end-to-end features using {s[0] if s else 'React'} on the frontend and {s[1] if len(s)>1 else 'Node.js'} on the backend. Own features from database schema to deployed UI.",
    "DevOps Engineer": lambda s: f"Manage cloud infrastructure using {s[0] if s else 'AWS'} and containerisation with {s[1] if len(s)>1 else 'Docker'} and Kubernetes. Build CI/CD pipelines and ensure system reliability and security.",
    "Product Manager": lambda s: f"Define and drive product roadmap using {s[0] if s else 'Agile'} methodologies and data-driven decision making. Work cross-functionally to ship features that improve user engagement.",
    "default":        lambda s: f"Work with {s[0] if s else 'modern technologies'} and {s[1] if len(s)>1 else 'cloud platforms'} to build and maintain production systems. Collaborate with cross-functional teams to deliver high-quality software.",
}

SALARY_RANGES = {
    "India":{
        "Junior":"₹4-9 LPA","Mid":"₹10-22 LPA","Senior":"₹22-45 LPA","Lead":"₹40-80 LPA",
        "ML Engineer":{"Junior":"₹6-12 LPA","Mid":"₹14-28 LPA","Senior":"₹28-55 LPA","Lead":"₹50-90 LPA"},
        "AI Engineer":{"Junior":"₹8-15 LPA","Mid":"₹18-35 LPA","Senior":"₹35-65 LPA","Lead":"₹60-1.2 Cr"},
        "Data Scientist":{"Junior":"₹6-12 LPA","Mid":"₹12-28 LPA","Senior":"₹28-55 LPA","Lead":"₹50-90 LPA"},
    },
    "United States":{
        "Junior":"$70-100K","Mid":"$110-150K","Senior":"$150-200K","Lead":"$190-280K",
        "ML Engineer":{"Junior":"$90-120K","Mid":"$130-170K","Senior":"$170-230K","Lead":"$220-320K"},
        "AI Engineer":{"Junior":"$100-130K","Mid":"$140-190K","Senior":"$190-260K","Lead":"$250-380K"},
    },
    "United Kingdom":{"Junior":"£35-55K","Mid":"£60-90K","Senior":"£90-130K","Lead":"£120-180K"},
    "Germany":{"Junior":"€45-60K","Mid":"€65-90K","Senior":"€90-130K","Lead":"€120-170K"},
    "Singapore":{"Junior":"S$50-80K","Mid":"S$90-130K","Senior":"S$130-180K","Lead":"S$170-250K"},
    "default":{"Junior":"Market rate","Mid":"Market rate","Senior":"Senior rate","Lead":"Lead rate"},
}

# ─────────────────────────────────────────────
# PYTHON LOGIC FUNCTIONS
# ─────────────────────────────────────────────
def extract_skills(text):
    lower = text.lower()
    found = []
    for s in SKILL_DB:
        pattern = r'\b' + re.escape(s) + r'\b'
        if re.search(pattern, lower, re.IGNORECASE):
            if s not in found:
                found.append(s)
    return found

def detect_role(skills):
    best_role = None
    best_score = -1
    for role, data in ROLE_SKILLS.items():
        overlap = sum(1 for s in data["skills"] if s in skills)
        score = overlap / len(data["skills"])
        if score > best_score:
            best_score = score
            best_role = role
    return {"role": best_role, "confidence": best_score}

def get_missing(role, user_skills):
    if not role or role not in ROLE_SKILLS:
        return []
    return [s for s in ROLE_SKILLS[role]["skills"] if s not in user_skills]

def score_job(user_skills, resume, job_text):
    j_skills = extract_skills(job_text)
    matched = [s for s in user_skills if s in j_skills]

    # Skill overlap: matched user skills vs all skills required by this job
    sk = len(matched) / len(j_skills) if j_skills else 0

    def tok(t):
        return [w for w in re.sub(r'[^a-z0-9 ]', ' ', t.lower()).split() if len(w) > 3]
    rs = set(tok(resume))
    jt = tok(job_text)

    if rs and jt:
        # Full keyword + skill blend when resume text is present
        kw = min(sum(1 for w in jt if w in rs) / len(jt) * 3, 1)
        score = 0.55 * kw + 0.45 * sk
    else:
        # No resume text: score on skill overlap + small deterministic variance per job
        # so cards show different percentages instead of all being identical
        noise = (hash(job_text[:50]) % 17) / 100  # 0.00 – 0.16 spread
        score = min(max(sk + noise * (0.5 - sk), 0.05), 0.97)

    return {
        "score": round(score, 3),
        "skillScore": round(sk, 3),
        "matched": matched,
        "missing": [s for s in j_skills if s not in user_skills],
    }

def get_salary(country, role, level):
    c = SALARY_RANGES.get(country, SALARY_RANGES["default"])
    if isinstance(c.get(role), dict) and level in c[role]:
        return c[role][level]
    return c.get(level, c.get("Mid", "Market rate"))

def build_job_url(title, skills, location, country):
    from urllib.parse import quote
    title_skills = f"{title} {' '.join(skills[:4])}".strip()
    kw = quote(title_skills)
    loc = quote(location or country)
    kw_plain = re.sub(r'[^\w\s.+#]', ' ', title_skills).replace(' ', '+')
    loc_plain = (location or country).replace(',', ' ').replace(' ', '+')
    return {
        "linkedinUrl":  f"https://www.linkedin.com/jobs/search/?keywords={kw}&location={loc}&sortBy=R&f_TPR=r604800",
        "indeedUrl":    f"https://www.indeed.com/jobs?q={kw}&l={loc}&sort=date&fromage=14",
        "googleJobsUrl":f"https://www.google.com/search?q={kw_plain}+jobs+{loc_plain}&ibp=htl;jobs",
        "glassdoorUrl": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={kw}&locT=N&locId=0&jobType=all",
        "naukri":       f"https://www.naukri.com/jobs?k={kw}&l={loc}&sort=1" if country == "India" else None,
        "wellfoundUrl": f"https://wellfound.com/jobs?q={kw}&l={loc}",
    }

def ai_review(job):
    pct = round(job["score"] * 100)
    matched = job.get("matched", [])
    missing = job.get("missing", [])
    if pct >= 70:
        verdict = f"Strong fit — your {matched[0] if matched else 'core skills'} align directly with this {job['title']} role."
    elif pct >= 45:
        verdict = f"Decent fit — you cover the fundamentals but some gaps ({', '.join(missing[:3])}) may affect shortlisting."
    else:
        verdict = f"Stretch role — you have transferable skills but {', '.join(missing[:3]) if missing else 'key skills'} are heavily weighted in this JD."
    if matched:
        asset = f"Your strongest asset here is {matched[0]}{' combined with '+matched[1] if len(matched)>1 else ''}—exactly what {job['company']} is hiring for."
    else:
        asset = "Your general technical background gives you a foundation, though you'll need to demonstrate domain depth."
    if missing:
        action = f"In the next 30 days, focus on {missing[0]}—even a small project or certification will move you past the ATS filter for this role."
    else:
        action = "You have the skills—now tailor your resume to use the exact keywords from this JD and apply directly on the company's careers page."
    return {"review": f"{verdict} {asset} {action}", "prioritySkills": missing[:3]}

SKILL_ROADMAP = {
    "python":            {"priority":95,"weeks":8, "why":"Core language for nearly all data/ML roles"},
    "machine learning":  {"priority":90,"weeks":12,"why":"Foundation of the entire ML/AI field"},
    "sql":               {"priority":88,"weeks":6, "why":"Essential for any data role — queried in nearly every interview"},
    "tensorflow":        {"priority":82,"weeks":10,"why":"Industry-standard deep learning framework"},
    "pytorch":           {"priority":82,"weeks":10,"why":"Research-preferred framework, increasingly used in production"},
    "docker":            {"priority":80,"weeks":5, "why":"Required for packaging and deploying any ML or backend service"},
    "kubernetes":        {"priority":75,"weeks":8, "why":"Orchestrates containerised services at scale — critical for MLOps"},
    "aws":               {"priority":78,"weeks":10,"why":"Most in-demand cloud platform globally"},
    "azure":             {"priority":70,"weeks":8, "why":"Dominant in enterprise and Microsoft-stack companies"},
    "react":             {"priority":85,"weeks":8, "why":"Most demanded frontend framework by job count"},
    "typescript":        {"priority":78,"weeks":5, "why":"Expected alongside React in most modern frontend roles"},
    "node":              {"priority":75,"weeks":6, "why":"Enables full-stack JS development, very common in startups"},
    "spark":             {"priority":80,"weeks":10,"why":"Standard for large-scale data processing"},
    "kafka":             {"priority":72,"weeks":7, "why":"Core real-time streaming infrastructure skill"},
    "airflow":           {"priority":74,"weeks":6, "why":"De-facto workflow orchestration tool for data pipelines"},
    "dbt":               {"priority":70,"weeks":5, "why":"Rapidly adopted for analytics engineering and data modelling"},
    "mlops":             {"priority":85,"weeks":12,"why":"Bridges the gap between ML research and production deployment"},
    "langchain":         {"priority":83,"weeks":6, "why":"Most adopted framework for building LLM-powered applications"},
    "llm":               {"priority":88,"weeks":10,"why":"Generative AI is the fastest-growing segment in tech hiring"},
    "vector databases":  {"priority":75,"weeks":5, "why":"Core component of RAG pipelines and semantic search"},
    "terraform":         {"priority":73,"weeks":7, "why":"Infrastructure as code — expected in all DevOps/cloud roles"},
    "ci/cd":             {"priority":77,"weeks":5, "why":"Expected skill in any modern engineering role"},
    "figma":             {"priority":65,"weeks":4, "why":"Standard design tool — expected in product and frontend roles"},
    "postgresql":        {"priority":80,"weeks":6, "why":"Most popular open-source relational database"},
    "redis":             {"priority":72,"weeks":4, "why":"Standard caching and session store in production systems"},
    "microservices":     {"priority":75,"weeks":8, "why":"Architecture pattern used in every large-scale system"},
}

LEARNING_RESOURCES = {
    "python":         [{"name":"Python for Everybody","platform":"Coursera","url":"https://www.coursera.org/specializations/python"},{"name":"Automate the Boring Stuff","platform":"Free Book","url":"https://automatetheboringstuff.com"}],
    "machine learning":[{"name":"ML Specialization","platform":"Coursera","url":"https://www.coursera.org/specializations/machine-learning-introduction"},{"name":"Fast.ai","platform":"Fast.ai","url":"https://www.fast.ai"}],
    "react":          [{"name":"React Docs","platform":"React.dev","url":"https://react.dev"},{"name":"React Course","platform":"Scrimba","url":"https://scrimba.com/learn/learnreact"}],
    "docker":         [{"name":"Docker Getting Started","platform":"Docker","url":"https://docs.docker.com/get-started/"},{"name":"Docker & Kubernetes","platform":"Udemy","url":"https://www.udemy.com/course/docker-kubernetes-the-practical-guide"}],
    "kubernetes":     [{"name":"Kubernetes Basics","platform":"k8s.io","url":"https://kubernetes.io/docs/tutorials/kubernetes-basics/"},{"name":"CKA Prep","platform":"Linux Foundation","url":"https://training.linuxfoundation.org"}],
    "aws":            [{"name":"AWS Cloud Practitioner","platform":"AWS","url":"https://aws.amazon.com/certification/certified-cloud-practitioner/"},{"name":"AWS Solutions Architect","platform":"Udemy","url":"https://www.udemy.com/course/aws-certified-solutions-architect-associate"}],
    "sql":            [{"name":"Mode SQL Tutorial","platform":"Mode","url":"https://mode.com/sql-tutorial/"},{"name":"SQLZoo","platform":"SQLZoo","url":"https://sqlzoo.net"}],
    "tensorflow":     [{"name":"TF Developer Certificate","platform":"TensorFlow","url":"https://www.tensorflow.org/certificate"},{"name":"Deep Learning Specialization","platform":"Coursera","url":"https://www.coursera.org/specializations/deep-learning"}],
    "pytorch":        [{"name":"PyTorch Tutorials","platform":"PyTorch.org","url":"https://pytorch.org/tutorials/"},{"name":"Deep Learning with PyTorch","platform":"Udemy","url":"https://www.udemy.com/course/pytorch-for-deep-learning-in-python-bootcamp"}],
    "typescript":     [{"name":"TypeScript Handbook","platform":"TS Docs","url":"https://www.typescriptlang.org/docs/handbook/"},{"name":"TS with React","platform":"Scrimba","url":"https://scrimba.com/learn/typescript"}],
    "figma":          [{"name":"Figma Official Course","platform":"Figma","url":"https://www.figma.com/resources/learn-design/"},{"name":"UI/UX Design","platform":"Coursera","url":"https://www.coursera.org/learn/wireframes-low-fidelity-prototypes"}],
    "golang":         [{"name":"Tour of Go","platform":"go.dev","url":"https://go.dev/tour/welcome/1"},{"name":"Go by Example","platform":"gobyexample.com","url":"https://gobyexample.com"}],
    "llm":            [{"name":"LLM University","platform":"Cohere","url":"https://docs.cohere.com/docs/llmu"},{"name":"LangChain Docs","platform":"LangChain","url":"https://python.langchain.com/docs/get_started/introduction"}],
}

def get_resources(skill):
    return LEARNING_RESOURCES.get(skill.lower(), [{"name":f"Learn {skill}","platform":"Google","url":f"https://www.google.com/search?q=learn+{skill.replace(' ','+')}+tutorial"}])

def ai_auto_find_jobs(skills, role, country, city):
    country_companies = COMPANIES.get(country, COMPANIES["default"])
    role_companies = country_companies.get(role, country_companies.get("default", COMPANIES["default"]["default"]))
    variants = ROLE_VARIANTS.get(role, [role, f"Senior {role}", f"Lead {role}"])
    desc_fn = ROLE_DESCRIPTIONS.get(role, ROLE_DESCRIPTIONS["default"])
    role_skills = ROLE_SKILLS.get(role, {}).get("skills", skills[:8])

    shuffled = role_companies[:]
    random.shuffle(shuffled)
    location = f"{city}, {country}" if city and city != "Any City" else country

    jobs = []
    for i, sen in enumerate(SENIORITY):
        company = shuffled[i % len(shuffled)]
        variant_title = variants[i % len(variants)]
        prefix = sen["titlePrefix"]
        title = f"{prefix} {variant_title}".strip() if prefix else variant_title

        # Vary demanded skills by seniority so match scores differ across cards
        demand_count = {"Junior": 4, "Mid": 5, "Senior": 7, "Lead": 8}.get(sen["level"], 5)
        shuffled_role = role_skills[:]
        random.shuffle(shuffled_role)
        needed = shuffled_role[:demand_count]

        nice_to_have = [s for s in role_skills if s not in needed][:2]
        description = desc_fn(skills)
        salary_range = get_salary(country, role, sen["level"])
        company_rating = round(3.8 + random.random() * 1.1, 1)
        is_remote = random.random() > 0.5

        urls = build_job_url(title, skills, location, country)
        j_text = f"{title} {description} {' '.join(needed)}"
        # Pass skills as resume proxy so keyword scoring produces real signal
        scored = score_job(skills, " ".join(skills), j_text)

        job = {
            "title": title,
            "company": company,
            "location": location,
            "salary": salary_range,
            "companyRating": company_rating,
            "remote": is_remote,
            "experience": sen["expYears"],
            "description": description,
            "requiredSkills": needed,
            "niceToHave": nice_to_have,
            "score": scored["score"],
            "skillScore": scored["skillScore"],
            "matched": scored["matched"],
            "missing": [s for s in needed if s not in skills],
            "snippet": description,
            **urls,
        }
        jobs.append(job)

    return sorted(jobs, key=lambda j: j["companyRating"], reverse=True)

def ai_roadmap(role, missing_skills):
    result = []
    for i, s in enumerate(missing_skills[:7]):
        d = SKILL_ROADMAP.get(s.lower(), {"priority": 70 - i*5, "weeks": 6, "why": f"Core skill for {role} roles"})
        result.append({"skill": s, **d, "resources": get_resources(s)})
    return sorted(result, key=lambda x: x["priority"], reverse=True)

# ─────────────────────────────────────────────
# COUNTRIES DATA (for frontend rendering)
# ─────────────────────────────────────────────
COUNTRIES_DATA = {
    "South Asia":[
        {"code":"IN","flag":"🇮🇳","name":"India","currency":"₹","salaryUnit":"LPA",
         "cities":["Bangalore","Mumbai","Hyderabad","Pune","Chennai","Delhi","Noida","Gurgaon","Gurugram","Kolkata","Kochi","Ahmedabad","Jaipur","Chandigarh","Indore","Nagpur","Coimbatore","Vadodara","Surat","Lucknow","Bhubaneswar","Thiruvananthapuram","Mysore","Vizag","Remote"],
         "boards":[
             {"name":"Naukri","icon":"🔶","color":"#ff6600","rating":4.5,"desc":"India's #1 job portal · 70M+ users","urlTemplate":"https://www.naukri.com/jobs?k={skills}&l={loc}"},
             {"name":"LinkedIn India","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network + jobs","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location={loc}"},
             {"name":"Indeed India","icon":"🔍","color":"#2557a7","rating":4.2,"desc":"Salary comparisons & company reviews","urlTemplate":"https://in.indeed.com/jobs?q={skills}&l={loc}"},
             {"name":"Glassdoor IN","icon":"⭐","color":"#0caa41","rating":4.4,"desc":"Salary insights + company culture","urlTemplate":"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={skills}&locT=N&locId=0"},
             {"name":"Instahyre","icon":"🌟","color":"#7c3aed","rating":4.3,"desc":"AI matching · Top tech companies","urlTemplate":"https://www.instahyre.com/search-jobs/?skill={skills}&location={loc}"},
             {"name":"Hirist.tech","icon":"💻","color":"#0ea5e9","rating":4.2,"desc":"Curated IT & tech-only jobs","urlTemplate":"https://www.hirist.tech/search?q={skills}&loc={loc}"},
             {"name":"Cutshort","icon":"✂️","color":"#f97316","rating":4.3,"desc":"Referral-based · vetted candidates","urlTemplate":"https://cutshort.io/jobs?keywords={skills}"},
             {"name":"AngelList/Wellfound","icon":"🚀","color":"#ff5733","rating":4.3,"desc":"Startup jobs + ESOPs","urlTemplate":"https://wellfound.com/jobs?q={skills}&l={loc}"},
             {"name":"Upwork India","icon":"🟢","color":"#14a800","rating":4.2,"desc":"Freelance & contract projects","urlTemplate":"https://www.upwork.com/nx/search/jobs/?q={skills}&sort=recency"},
             {"name":"Google Jobs 🇮🇳","icon":"🌐","color":"#4285f4","rating":4.8,"desc":"All boards combined · live ratings","urlTemplate":"https://www.google.com/search?q={skills}+jobs+{loc}&ibp=htl;jobs"},
         ]},
        {"code":"PK","flag":"🇵🇰","name":"Pakistan","currency":"PKR","salaryUnit":"K/mo",
         "cities":["Karachi","Lahore","Islamabad","Rawalpindi","Remote"],
         "boards":[
             {"name":"Rozee.pk","icon":"🔵","color":"#0057a8","rating":4.2,"desc":"Pakistan's leading job portal","urlTemplate":"https://www.rozee.pk/job/jsearch/q/{skills}"},
             {"name":"LinkedIn","icon":"💼","color":"#0077b5","rating":4.6,"desc":"Professional network + jobs","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Pakistan"},
             {"name":"Indeed PK","icon":"🔍","color":"#2557a7","rating":4.0,"desc":"Job listings & salary data","urlTemplate":"https://pk.indeed.com/jobs?q={skills}&l=Pakistan"},
         ]},
        {"code":"BD","flag":"🇧🇩","name":"Bangladesh","currency":"BDT","salaryUnit":"K/mo",
         "cities":["Dhaka","Chittagong","Remote"],
         "boards":[{"name":"LinkedIn","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network + jobs","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Bangladesh"}]},
        {"code":"LK","flag":"🇱🇰","name":"Sri Lanka","currency":"LKR","salaryUnit":"K/mo",
         "cities":["Colombo","Kandy","Remote"],
         "boards":[{"name":"LinkedIn","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network + jobs","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Sri+Lanka"}]},
    ],
    "East Asia":[
        {"code":"JP","flag":"🇯🇵","name":"Japan","currency":"¥","salaryUnit":"M JPY/yr",
         "cities":["Tokyo","Osaka","Fukuoka","Remote"],
         "boards":[
             {"name":"Jobs in Japan","icon":"⛩️","color":"#bc002d","rating":4.3,"desc":"English jobs in Japan","urlTemplate":"https://www.jobsinjapan.com/jobs/?q={skills}"},
             {"name":"LinkedIn JP","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Japan"},
         ]},
        {"code":"SG","flag":"🇸🇬","name":"Singapore","currency":"S$","salaryUnit":"K/yr",
         "cities":["Singapore"],
         "boards":[
             {"name":"MyCareersFuture","icon":"🦁","color":"#e63946","rating":4.4,"desc":"Singapore government jobs portal","urlTemplate":"https://www.mycareersfuture.gov.sg/search?search={skills}&sortBy=new_posting_date"},
             {"name":"JobStreet SG","icon":"🌴","color":"#e91e63","rating":4.2,"desc":"Leading SEA job portal","urlTemplate":"https://www.jobstreet.com.sg/jobs?q={skills}"},
             {"name":"LinkedIn SG","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Singapore"},
         ]},
        {"code":"KR","flag":"🇰🇷","name":"South Korea","currency":"₩","salaryUnit":"M KRW/yr",
         "cities":["Seoul","Busan","Remote"],
         "boards":[{"name":"LinkedIn KR","icon":"💼","color":"#0077b5","rating":4.6,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=South+Korea"}]},
        {"code":"HK","flag":"🇭🇰","name":"Hong Kong","currency":"HK$","salaryUnit":"K/mo",
         "cities":["Hong Kong"],
         "boards":[
             {"name":"JobsDB HK","icon":"🏙️","color":"#e63946","rating":4.2,"desc":"HK's top job portal","urlTemplate":"https://hk.jobsdb.com/jobs?q={skills}"},
             {"name":"LinkedIn HK","icon":"💼","color":"#0077b5","rating":4.6,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Hong+Kong"},
         ]},
    ],
    "Southeast Asia":[
        {"code":"MY","flag":"🇲🇾","name":"Malaysia","currency":"RM","salaryUnit":"K/mo",
         "cities":["Kuala Lumpur","Penang","Remote"],
         "boards":[
             {"name":"JobStreet MY","icon":"🌺","color":"#e91e63","rating":4.3,"desc":"Malaysia's top job portal","urlTemplate":"https://www.jobstreet.com.my/jobs?q={skills}"},
             {"name":"LinkedIn MY","icon":"💼","color":"#0077b5","rating":4.6,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Malaysia"},
         ]},
        {"code":"PH","flag":"🇵🇭","name":"Philippines","currency":"₱","salaryUnit":"K/mo",
         "cities":["Metro Manila","Cebu","Remote"],
         "boards":[{"name":"LinkedIn PH","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Philippines"}]},
        {"code":"TH","flag":"🇹🇭","name":"Thailand","currency":"฿","salaryUnit":"K/mo",
         "cities":["Bangkok","Chiang Mai","Remote"],
         "boards":[{"name":"LinkedIn TH","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Thailand"}]},
        {"code":"ID","flag":"🇮🇩","name":"Indonesia","currency":"Rp","salaryUnit":"M IDR/mo",
         "cities":["Jakarta","Surabaya","Remote"],
         "boards":[
             {"name":"Jobstreet ID","icon":"🌊","color":"#e91e63","rating":4.1,"desc":"Indonesia's top job portal","urlTemplate":"https://www.jobstreet.co.id/jobs?q={skills}"},
             {"name":"LinkedIn ID","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Indonesia"},
         ]},
        {"code":"VN","flag":"🇻🇳","name":"Vietnam","currency":"₫","salaryUnit":"M VND/mo",
         "cities":["Ho Chi Minh City","Hanoi","Remote"],
         "boards":[{"name":"LinkedIn VN","icon":"💼","color":"#0077b5","rating":4.4,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Vietnam"}]},
    ],
    "Middle East":[
        {"code":"AE","flag":"🇦🇪","name":"UAE","currency":"AED","salaryUnit":"K/mo",
         "cities":["Dubai","Abu Dhabi","Sharjah","Remote"],
         "boards":[
             {"name":"Bayt","icon":"🏛️","color":"#cc7722","rating":4.3,"desc":"Leading MENA job portal","urlTemplate":"https://www.bayt.com/en/uae/jobs/?q={skills}"},
             {"name":"GulfTalent","icon":"🌟","color":"#e63946","rating":4.1,"desc":"Gulf region specialist","urlTemplate":"https://www.gulftalent.com/jobs?q={skills}&country=uae"},
             {"name":"LinkedIn AE","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=United+Arab+Emirates"},
         ]},
        {"code":"SA","flag":"🇸🇦","name":"Saudi Arabia","currency":"SAR","salaryUnit":"K/mo",
         "cities":["Riyadh","Jeddah","Dammam","Remote"],
         "boards":[
             {"name":"Bayt SA","icon":"🕌","color":"#006c35","rating":4.2,"desc":"KSA leading job portal","urlTemplate":"https://www.bayt.com/en/saudi-arabia/jobs/?q={skills}"},
             {"name":"LinkedIn SA","icon":"💼","color":"#0077b5","rating":4.6,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Saudi+Arabia"},
         ]},
        {"code":"QA","flag":"🇶🇦","name":"Qatar","currency":"QAR","salaryUnit":"K/mo",
         "cities":["Doha","Remote"],
         "boards":[{"name":"LinkedIn QA","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Qatar"}]},
    ],
    "Europe":[
        {"code":"GB","flag":"🇬🇧","name":"United Kingdom","currency":"£","salaryUnit":"K/yr",
         "cities":["London","Manchester","Edinburgh","Birmingham","Remote"],
         "boards":[
             {"name":"Reed.co.uk","icon":"🌹","color":"#c41e3a","rating":4.3,"desc":"UK's largest job board","urlTemplate":"https://www.reed.co.uk/jobs?keywords={skills}&location={loc}"},
             {"name":"Totaljobs","icon":"🇬🇧","color":"#003087","rating":4.2,"desc":"UK jobs aggregator","urlTemplate":"https://www.totaljobs.com/jobs?q={skills}"},
             {"name":"LinkedIn UK","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=United+Kingdom"},
             {"name":"Glassdoor UK","icon":"⭐","color":"#0caa41","rating":4.4,"desc":"Salary insights + culture","urlTemplate":"https://www.glassdoor.co.uk/Job/jobs.htm?sc.keyword={skills}&locT=N&locId=0"},
         ]},
        {"code":"DE","flag":"🇩🇪","name":"Germany","currency":"€","salaryUnit":"K/yr",
         "cities":["Berlin","Munich","Hamburg","Frankfurt","Remote"],
         "boards":[
             {"name":"StepStone","icon":"🟠","color":"#ff6600","rating":4.3,"desc":"Germany's top job portal","urlTemplate":"https://www.stepstone.de/jobs?q={skills}"},
             {"name":"Indeed DE","icon":"🔍","color":"#2557a7","rating":4.2,"desc":"Job aggregator","urlTemplate":"https://de.indeed.com/jobs?q={skills}"},
             {"name":"LinkedIn DE","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Germany"},
         ]},
        {"code":"NL","flag":"🇳🇱","name":"Netherlands","currency":"€","salaryUnit":"K/yr",
         "cities":["Amsterdam","Rotterdam","The Hague","Remote"],
         "boards":[{"name":"LinkedIn NL","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Netherlands"}]},
        {"code":"FR","flag":"🇫🇷","name":"France","currency":"€","salaryUnit":"K/yr",
         "cities":["Paris","Lyon","Bordeaux","Remote"],
         "boards":[
             {"name":"Welcome to Jungle","icon":"🌿","color":"#3dba90","rating":4.4,"desc":"France's top startup jobs","urlTemplate":"https://www.welcometothejungle.com/en/jobs?query={skills}&where=France"},
             {"name":"LinkedIn FR","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=France"},
         ]},
        {"code":"IE","flag":"🇮🇪","name":"Ireland","currency":"€","salaryUnit":"K/yr",
         "cities":["Dublin","Cork","Limerick","Remote"],
         "boards":[{"name":"LinkedIn IE","icon":"💼","color":"#0077b5","rating":4.6,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Ireland"}]},
        {"code":"PL","flag":"🇵🇱","name":"Poland","currency":"PLN","salaryUnit":"K/mo",
         "cities":["Warsaw","Kraków","Wrocław","Remote"],
         "boards":[{"name":"LinkedIn PL","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Poland"}]},
    ],
    "North America":[
        {"code":"US","flag":"🇺🇸","name":"United States","currency":"$","salaryUnit":"K/yr",
         "cities":["New York","San Francisco","Seattle","Austin","Chicago","Boston","Remote"],
         "boards":[
             {"name":"LinkedIn US","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location={loc}&f_WT=2"},
             {"name":"Indeed US","icon":"🔍","color":"#2557a7","rating":4.3,"desc":"Largest US job board","urlTemplate":"https://www.indeed.com/jobs?q={skills}&l={loc}&sort=date&fromage=14"},
             {"name":"Glassdoor","icon":"⭐","color":"#0caa41","rating":4.4,"desc":"Salary insights + culture","urlTemplate":"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={skills}&remoteWorkType=1"},
             {"name":"Wellfound","icon":"🚀","color":"#ff5733","rating":4.3,"desc":"Startup jobs + ESOPs","urlTemplate":"https://wellfound.com/jobs?q={skills}"},
             {"name":"Dice","icon":"🎲","color":"#e63946","rating":4.0,"desc":"Tech-only jobs board","urlTemplate":"https://www.dice.com/jobs?q={skills}&countryCode=US"},
         ]},
        {"code":"CA","flag":"🇨🇦","name":"Canada","currency":"CA$","salaryUnit":"K/yr",
         "cities":["Toronto","Vancouver","Montreal","Calgary","Remote"],
         "boards":[
             {"name":"Indeed CA","icon":"🔍","color":"#2557a7","rating":4.2,"desc":"Canada's top job board","urlTemplate":"https://ca.indeed.com/jobs?q={skills}&l={loc}"},
             {"name":"LinkedIn CA","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location={loc}"},
         ]},
    ],
    "Oceania":[
        {"code":"AU","flag":"🇦🇺","name":"Australia","currency":"A$","salaryUnit":"K/yr",
         "cities":["Sydney","Melbourne","Brisbane","Perth","Remote"],
         "boards":[
             {"name":"Seek AU","icon":"🦘","color":"#003c8f","rating":4.4,"desc":"Australia's #1 job board","urlTemplate":"https://www.seek.com.au/jobs?q={skills}&where={loc}"},
             {"name":"LinkedIn AU","icon":"💼","color":"#0077b5","rating":4.7,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location={loc}"},
             {"name":"Indeed AU","icon":"🔍","color":"#2557a7","rating":4.1,"desc":"Job aggregator","urlTemplate":"https://au.indeed.com/jobs?q={skills}"},
         ]},
        {"code":"NZ","flag":"🇳🇿","name":"New Zealand","currency":"NZ$","salaryUnit":"K/yr",
         "cities":["Auckland","Wellington","Remote"],
         "boards":[
             {"name":"Seek NZ","icon":"🥝","color":"#003c8f","rating":4.2,"desc":"NZ's top job board","urlTemplate":"https://www.seek.co.nz/jobs?q={skills}"},
             {"name":"LinkedIn NZ","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=New+Zealand"},
         ]},
    ],
    "Latin America":[
        {"code":"BR","flag":"🇧🇷","name":"Brazil","currency":"R$","salaryUnit":"K/mo",
         "cities":["São Paulo","Rio de Janeiro","Brasília","Remote"],
         "boards":[{"name":"LinkedIn BR","icon":"💼","color":"#0077b5","rating":4.6,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Brazil"}]},
        {"code":"MX","flag":"🇲🇽","name":"Mexico","currency":"MXN","salaryUnit":"K/mo",
         "cities":["Mexico City","Guadalajara","Monterrey","Remote"],
         "boards":[{"name":"LinkedIn MX","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Mexico"}]},
        {"code":"CO","flag":"🇨🇴","name":"Colombia","currency":"COP","salaryUnit":"M/mo",
         "cities":["Bogotá","Medellín","Remote"],
         "boards":[{"name":"LinkedIn CO","icon":"💼","color":"#0077b5","rating":4.4,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Colombia"}]},
    ],
    "Africa":[
        {"code":"NG","flag":"🇳🇬","name":"Nigeria","currency":"₦","salaryUnit":"K/mo",
         "cities":["Lagos","Abuja","Port Harcourt","Remote"],
         "boards":[{"name":"LinkedIn NG","icon":"💼","color":"#0077b5","rating":4.4,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Nigeria"}]},
        {"code":"ZA","flag":"🇿🇦","name":"South Africa","currency":"R","salaryUnit":"K/mo",
         "cities":["Cape Town","Johannesburg","Durban","Remote"],
         "boards":[{"name":"LinkedIn ZA","icon":"💼","color":"#0077b5","rating":4.5,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=South+Africa"}]},
        {"code":"KE","flag":"🇰🇪","name":"Kenya","currency":"KES","salaryUnit":"K/mo",
         "cities":["Nairobi","Mombasa","Remote"],
         "boards":[{"name":"LinkedIn KE","icon":"💼","color":"#0077b5","rating":4.3,"desc":"Professional network","urlTemplate":"https://www.linkedin.com/jobs/search/?keywords={skills}&location=Kenya"}]},
    ],
}

# ─────────────────────────────────────────────
# FLASK ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", countries=COUNTRIES_DATA)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.json
    resume = data.get("resume", "")
    country_name = data.get("country", "")
    city = data.get("city", "")

    if not resume.strip():
        return jsonify({"error": "No resume provided"}), 400

    skills = extract_skills(resume)
    if not skills:
        return jsonify({"error": "No tech skills detected. Add keywords like Python, React, AWS, Docker, SQL, etc."}), 400

    role_result = detect_role(skills)
    role = role_result["role"]
    confidence = role_result["confidence"]

    missing = get_missing(role, skills)
    jobs = ai_auto_find_jobs(skills, role, country_name, city)

    salary_ref = None
    if role and role in ROLE_SKILLS:
        country_obj = next(
            (c for region in COUNTRIES_DATA.values() for c in region if c["name"] == country_name), None
        )
        if country_obj:
            salary_ref = ROLE_SKILLS[role]["salary"].get(country_obj["code"])

    return jsonify({
        "skills": skills,
        "role": role,
        "confidence": round(confidence * 100),
        "missing": missing,
        "jobs": jobs,
        "salaryRef": salary_ref,
    })

@app.route("/api/roadmap", methods=["POST"])
def roadmap():
    data = request.json
    role = data.get("role", "")
    missing_skills = data.get("missingSkills", [])
    result = ai_roadmap(role, missing_skills)
    return jsonify(result)

@app.route("/api/review", methods=["POST"])
def review():
    job = request.json
    result = ai_review(job)
    return jsonify(result)

@app.route("/api/countries")
def get_countries():
    return jsonify(COUNTRIES_DATA)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
