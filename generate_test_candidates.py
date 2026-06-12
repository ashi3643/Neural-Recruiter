#!/usr/bin/env python3
"""
generate_test_candidates.py
Generates a realistic set of 101 candidate profiles representing:
- Group 1: AI Superstars (Tier A, rich semantic search details) - 15 candidates
- Group 2: Keyword Stuffers (Non-tech HR/Ops with false AI skills) - 15 candidates
- Group 3: Consulting firm candidates (100% career in outsourcing giants) - 15 candidates
- Group 4: Honeypot traps (Impossible timelines, expert 0 months, future dates) - 12 candidates
- Group 5: Behavioral ghosts (Brilliant CVs, but inactive/unreachable) - 12 candidates
- Group 6: Plain-language seekers (Great backend search experience, but no buzzwords) - 12 candidates
- Group 7: Normal tech candidates (Average backend developers/Data scientists) - 30 candidates
Total: 101 Candidates. Meets evaluation standards.
"""

import json

def get_test_candidates():
    candidates = []

    product_companies = ['Razorpay', 'Flipkart', 'InMobi', 'PhonePe', 'Dunzo', 'Myntra', 'Ola Cabs', 'Swiggy', 'Zomato', 'Cred', 'Slack', 'Stripe', 'Atlassian']
    consulting_companies = ['Tata Consultancy Services', 'Infosys', 'Wipro Digital', 'Accenture', 'Cognizant Technology Solutions', 'Capgemini India', 'HCL Technologies', 'Tech Mahindra']
    
    locations = [
        {"city": "Bengaluru", "country": "India"},
        {"city": "Noida", "country": "India"},
        {"city": "Pune", "country": "India"},
        {"city": "Hyderabad", "country": "India"},
        {"city": "Gurugram", "country": "India"},
        {"city": "Mumbai", "country": "India"}
    ]

    first_names = ['Arjun', 'Priya', 'Aditya', 'Sneha', 'Rohan', 'Ananya', 'Vikram', 'Divya', 'Sandeep', 'Deepika', 'Kunal', 'Neha', 'Rahul', 'Tanvi', 'Abhishek']
    last_names = ['Sharma', 'Iyer', 'Patel', 'Nair', 'Mehta', 'Reddy', 'Verma', 'Sen', 'Choudhury', 'Joshi', 'Gupta', 'Rao', 'Singh', 'Deshmukh', 'Mishra']

    # GROUP 1: AI SUPERSTARS (15 candidates)
    for i in range(15):
        fn = first_names[i]
        ln = last_names[i]
        loc = locations[i % len(locations)]
        cid = f"CAND_{1000000 + i}"
        yoe = 6 + (i % 3) # 6, 7, 8 years
        comp = product_companies[i % len(product_companies)]
        prev_comp = product_companies[(i + 1) % len(product_companies)]
        
        skills = [
            {"name": "Python", "proficiency": "expert", "endorsements": 44, "duration_months": yoe * 12},
            {"name": "Sentence Transformers", "proficiency": "expert", "endorsements": 32, "duration_months": 36},
            {"name": "Pinecone", "proficiency": "advanced", "endorsements": 28, "duration_months": 30},
            {"name": "RAG", "proficiency": "expert", "endorsements": 35, "duration_months": 32},
            {"name": "NDCG", "proficiency": "expert", "endorsements": 21, "duration_months": 28},
            {"name": "PyTorch", "proficiency": "advanced", "endorsements": 41, "duration_months": 48},
            {"name": "FAISS", "proficiency": "advanced", "endorsements": 18, "duration_months": 24}
        ]
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": f"{fn} {ln}",
                "current_title": "Senior AI Engineer" if i % 2 == 0 else "Machine Learning Engineer",
                "current_company": comp,
                "headline": f"Senior Machine Learning & Retrieval Specialist | ex-{comp}",
                "summary": f"Passionate engineer with {yoe}+ years shipping information retrieval and recommendation systems at scale. Experienced in neural networks, dense embeddings, hybrid search, and ranking evaluation metrics. Built dense index systems handling millions of daily query hits.",
                "years_of_experience": yoe,
                "location": f"{loc['city']}, India",
                "country": "India"
            },
            "career_history": [
                {
                    "company": comp,
                    "title": "Senior ML Engineer" if i % 2 == 0 else "Machine Learning Engineer",
                    "duration_months": 41,
                    "description": "Designed and deployed end-to-end multi-stage hybrid ranking system. Integrated dense vector similarity (Sentence-Transformers + Pinecone) alongside classical hybrid sparse models. Leveraged Learning-to-Rank (LTR LambdaMART) resulting in a 14% lift in Search NDCG@10 metrics. Monitored online production performance through continuous split A/B testing."
                },
                {
                    "company": prev_comp,
                    "title": "Machine Learning Engineer",
                    "duration_months": 33,
                    "description": "Built candidate text embedding pipelines to parse, match and rank semantic compatibility scores. Optimized search latency below 45ms. Deployed real-time query vector index caches based on FAISS library."
                }
            ],
            "skills": skills,
            "education": [{"institution": "IIT Bombay", "degree": "B.Tech", "field_of_study": "Computer Science", "end_year": 2018}],
            "certifications": [{"name": "TensorFlow Developer Certificate", "issuer": "Google", "year": 2021}],
            "redrob_signals": {
                "open_to_work_flag": i % 2 == 0,
                "last_active_date": "2026-06-10",
                "recruiter_response_rate": 0.88 + (i * 0.008),
                "notice_period_days": 15 + (i * 2),
                "github_activity_score": 82 + i,
                "interview_completion_rate": 0.95,
                "skill_assessment_scores": {"Python": 98, "Machine Learning": 95},
                "willing_to_relocate": True
            }
        })

    # GROUP 2: KEYWORD STUFFERS (15 candidates)
    stuffer_first = ['Rajesh', 'Sunita', 'Anil', 'Kiran', 'Manish', 'Kavita', 'Sanjay', 'Alok', 'Amit', 'Pooja', 'Suresh', 'Geeta', 'Ramesh', 'Harish', 'Ritu']
    stuffer_titles = ['HR Operations Partner', 'Senior Operations Manager', 'Finance Lead', 'Customer Success Associate', 'Logistics Analyst', 'Talent Scout Coordinator', 'Sales Specialist']
    for i in range(15):
        fn = stuffer_first[i]
        ln = last_names[(i + 3) % len(last_names)]
        cid = f"CAND_{1000100 + i}"
        yoe = 8 + (i % 4)
        title = stuffer_titles[i % len(stuffer_titles)]
        
        skills = [
            {"name": "Python", "proficiency": "expert", "endorsements": 1, "duration_months": 6},
            {"name": "Sentence Transformers", "proficiency": "expert", "endorsements": 0, "duration_months": 3},
            {"name": "Pinecone", "proficiency": "expert", "endorsements": 0, "duration_months": 3},
            {"name": "RAG", "proficiency": "expert", "endorsements": 1, "duration_months": 4},
            {"name": "NDCG", "proficiency": "advanced", "endorsements": 0, "duration_months": 2},
            {"name": "Operations Management", "proficiency": "expert", "endorsements": 45, "duration_months": 120}
        ]
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": f"{fn} {ln}",
                "current_title": title,
                "current_company": "Global Retail Corp",
                "headline": "Supercharged Operations & Tech Enthusiast | Python | RAG | Pinecone | OpenAI embeddings | Generative AI expert",
                "summary": f"Results-driven operations professional now specializing in AI capabilities. Experience in Python scripts, RAG pipelines, Prompt engineering, embeddings matching, and LLM orchestration. Levering neural net embeddings for workflow efficiency.",
                "years_of_experience": yoe,
                "location": "Chandigarh, India",
                "country": "India"
            },
            "career_history": [
                {
                    "company": "Global Retail Corp",
                    "title": title,
                    "duration_months": 64,
                    "description": "Coordinates logistics workflows, managing a team of 15 logistics associates. Integrated tiny Python scripts and OpenAI API ChatGPT tokens to draft automated email responses, enhancing office throughput metrics. Explored vector storage conceptually."
                }
            ],
            "skills": skills,
            "education": [{"institution": "Kurukshetra University", "degree": "B.Com", "field_of_study": "Business Commerce", "end_year": 2017}],
            "certifications": [{"name": "Prompt Engineering Bootcamp Certificate", "issuer": "Online Academy", "year": 2025}],
            "redrob_signals": {
                "open_to_work_flag": True,
                "last_active_date": "2026-06-11",
                "recruiter_response_rate": 0.95,
                "notice_period_days": 0,
                "github_activity_score": 12,
                "interview_completion_rate": 1.0,
                "skill_assessment_scores": {"Python": 35},
                "willing_to_relocate": True
            }
        })

    # GROUP 3: CONSULTING CANDIDATES (15 candidates)
    consult_first = ['Vikash', 'Aishwarya', 'Karthik', 'Swati', 'Hari', 'Pallavi', 'Vijay', 'Sumit', 'Jaya', 'Shankar', 'Nidhi', 'Madhuri', 'Tarun', 'Shalini', 'Nikhil']
    for i in range(15):
        fn = consult_first[i]
        ln = last_names[(i + 6) % len(last_names)]
        cid = f"CAND_{1000200 + i}"
        yoe = 7 + (i % 3)
        firm = consulting_companies[i % len(consulting_companies)]
        prev_firm = consulting_companies[(i + 2) % len(consulting_companies)]
        
        skills = [
            {"name": "Python", "proficiency": "advanced", "endorsements": 18, "duration_months": 48},
            {"name": "RAG", "proficiency": "advanced", "endorsements": 12, "duration_months": 24},
            {"name": "Pinecone", "proficiency": "intermediate", "endorsements": 5, "duration_months": 18},
            {"name": "Sentence Transformers", "proficiency": "intermediate", "endorsements": 3, "duration_months": 12},
            {"name": "Project Management", "proficiency": "expert", "endorsements": 85, "duration_months": 80}
        ]
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": f"{fn} {ln}",
                "current_title": "AI Architect & Delivery Lead",
                "current_company": firm,
                "headline": f"Lead Consultant | AI-ML Delivery Lead at {firm}",
                "summary": f"Accomplished AI Solutions Consultant with {yoe} years delivery management expertise in banking, healthcare and insurance clients. Implemented diverse enterprise RAG databases using out-of-the-box pipeline connectors. Skilled Scrum Master and customer stakeholder catalyst.",
                "years_of_experience": yoe,
                "location": "Hyderabad, India",
                "country": "India"
            },
            "career_history": [
                {
                    "company": firm,
                    "title": "Lead AI Engineer",
                    "duration_months": 50,
                    "description": "Supervises client delivery architectures on cloud. Orchestrates vendor AI frameworks. Implemented LangChain connectors to feed knowledge documents into default third-party vector databases. Supported client demo pitches."
                },
                {
                    "company": prev_firm,
                    "title": "Systems Engineer - Machine Learning",
                    "duration_months": 33,
                    "description": "Wrote SQL procedures and mapped candidate JSON models. Maintained legacy Spark data cleansings, occasionally compiling pre-configured text classifier scripts."
                }
            ],
            "skills": skills,
            "education": [{"institution": "Visvesvaraya Technological University", "degree": "B.E.", "field_of_study": "Information Science", "end_year": 2019}],
            "certifications": [{"name": "AWS Certified Machine Learning", "issuer": "Amazon Web Services", "year": 2023}],
            "redrob_signals": {
                "open_to_work_flag": False,
                "last_active_date": "2026-06-05",
                "recruiter_response_rate": 0.42,
                "notice_period_days": 90,
                "github_activity_score": -1,
                "interview_completion_rate": 0.60,
                "skill_assessment_scores": {"Python": 72},
                "willing_to_relocate": True
            }
        })

    # GROUP 4: HONEYPOT TRAPS (12 candidates)
    honey_first = ['CyberTris', 'RoboMatcher', 'QuantumMinds', 'AISeeker_01', 'HyperBot', 'DeepRacerPro', 'AIGuru', 'Samyak_Expert', 'HNSW_Master', 'Mr_RAG', 'VectorBoy', 'TransformerQueen']
    for i in range(12):
        fn = honey_first[i]
        cid = f"CAND_9999{100 + i}"
        h_type = i % 3
        
        if h_type == 0:
            # Style A: Expert proficiency with 0 months duration
            candidates.append({
                "candidate_id": cid,
                "profile": {
                    "name": f"{fn} Tech",
                    "current_title": "Senior AI Engineer",
                    "current_company": "Redrob AI Challenger Mock",
                    "headline": "Expert Founding Engineer specialized in pinecone dense matching and Lambdamart LTR",
                    "summary": "Senior architect holding deep credentials in ranking and neural models. Built massive frameworks.",
                    "years_of_experience": 7,
                    "location": "Pune, India",
                    "country": "India"
                },
                "career_history": [
                    {
                        "company": "Redrob AI Challenger Mock",
                        "title": "Senior AI Engineer",
                        "duration_months": 29,
                        "description": "Supervised neural core. Designed pinecone maps."
                    }
                ],
                "skills": [
                    {"name": "Sentence Transformers", "proficiency": "expert", "endorsements": 1, "duration_months": 0},
                    {"name": "Pinecone", "proficiency": "expert", "endorsements": 0, "duration_months": 0},
                    {"name": "RAG", "proficiency": "expert", "endorsements": 0, "duration_months": 0},
                    {"name": "Python", "proficiency": "expert", "endorsements": 12, "duration_months": 84}
                ],
                "education": [{"institution": "IIT Delhi", "degree": "B.Tech", "field_of_study": "CS", "end_year": 2019}],
                "certifications": [],
                "redrob_signals": {
                    "open_to_work_flag": True,
                    "last_active_date": "2026-06-11",
                    "recruiter_response_rate": 1.0,
                    "notice_period_days": 0,
                    "github_activity_score": 99,
                    "interview_completion_rate": 1.0,
                    "skill_assessment_scores": {"Python": 100}
                }
            })
        elif h_type == 1:
            # Style B: Timeline mismatch (stated 3yrs, combined career adds to 11 yrs)
            candidates.append({
                "candidate_id": cid,
                "profile": {
                    "name": f"FastCareer {fn}",
                    "current_title": "Senior Machine Learning Systems Lead",
                    "current_company": "Apex Solutions",
                    "headline": "Young Leader and ML Engineer",
                    "summary": "Fast progressor through senior technical hierarchies.",
                    "years_of_experience": 3,
                    "location": "Noida, India",
                    "country": "India"
                },
                "career_history": [
                    {
                        "company": "Apex Solutions",
                        "title": "Senior ML Systems Lead",
                        "duration_months": 65,
                        "description": "Leads AI teams. Outperformed goals."
                    },
                    {
                        "company": "Origin Labs",
                        "title": "Founding ML Developer",
                        "duration_months": 72,
                        "description": "Built ranking kernels is Django. Created semantic clusters."
                    }
                ],
                "skills": [
                    {"name": "Python", "proficiency": "advanced", "endorsements": 12, "duration_months": 36},
                    {"name": "Sentence Transformers", "proficiency": "expert", "endorsements": 5, "duration_months": 24}
                ],
                "education": [],
                "certifications": [],
                "redrob_signals": {
                    "open_to_work_flag": True,
                    "last_active_date": "2026-06-11",
                    "recruiter_response_rate": 0.90,
                    "notice_period_days": 15,
                    "github_activity_score": 55,
                    "interview_completion_rate": 0.90,
                    "skill_assessment_scores": {}
                }
            })
        else:
            # Style C: Education end year in the future (2029) or Cert in future (2028)
            candidates.append({
                "candidate_id": cid,
                "profile": {
                    "name": f"TimeTraveler {fn}",
                    "current_title": "Senior AI Research Engineer",
                    "current_company": "Vortex Global",
                    "headline": "Vanguard Artificial Intelligence Engineer",
                    "summary": "Shifting cognitive capabilities ahead of time. Specializing in dense retrieval matrix configurations.",
                    "years_of_experience": 5,
                    "location": "Noida, India",
                    "country": "India"
                },
                "career_history": [
                    {
                        "company": "Vortex Global",
                        "title": "Senior AI Engineer",
                        "duration_months": 53,
                        "description": "Orchestrated dense retrievals."
                    }
                ],
                "skills": [
                    {"name": "Python", "proficiency": "advanced", "endorsements": 10, "duration_months": 60},
                    {"name": "Sentence Transformers", "proficiency": "expert", "endorsements": 8, "duration_months": 30}
                ],
                "education": [{"institution": "VIT University", "degree": "M.Tech", "field_of_study": "AI", "end_year": 2029}],
                "certifications": [{"name": "Redrob Master Certification", "issuer": "Future Labs Org", "year": 2028}],
                "redrob_signals": {
                    "open_to_work_flag": True,
                    "last_active_date": "2026-06-11",
                    "recruiter_response_rate": 0.95,
                    "notice_period_days": 30,
                    "github_activity_score": 80,
                    "interview_completion_rate": 1.0,
                    "skill_assessment_scores": {}
                }
            })

    # GROUP 5: BEHAVIORAL GHOSTS (12 candidates)
    ghost_first = ['Manoj', 'Gayatri', 'Rupesh', 'Anushka', 'Vivek', 'Shruti', 'Animesh', 'Pragati', 'Girish', 'Ridhima', 'Sourav', 'Jyoti']
    for i in range(12):
        fn = ghost_first[i]
        ln = last_names[(i + 9) % len(last_names)]
        cid = f"CAND_8000${100 + i}" # Unique format, let's make it standard CADN format: CAND_8000100 + i
        cid = f"CAND_8000{100 + i}"
        
        skills = [
            {"name": "Python", "proficiency": "expert", "endorsements": 120, "duration_months": 96},
            {"name": "Sentence Transformers", "proficiency": "expert", "endorsements": 95, "duration_months": 48},
            {"name": "Pinecone", "proficiency": "expert", "endorsements": 76, "duration_months": 36},
            {"name": "RAG", "proficiency": "expert", "endorsements": 82, "duration_months": 40},
            {"name": "NDCG", "proficiency": "expert", "endorsements": 62, "duration_months": 44},
            {"name": "FAISS", "proficiency": "expert", "endorsements": 54, "duration_months": 36}
        ]
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": f"{fn} {ln}(Inactive)",
                "current_title": "Staff AI Specialist",
                "current_company": "HyperScale AI Corp",
                "headline": "Staff AI Scientist | ex-Google | ex-Amazon Embedding Team Lead",
                "summary": "Eminent computer scientist with 8 years of pure focus on Dense Retrieval Systems, vector indices, and custom scoring engines. Published 3 semantic search papers. Architected search layers indexing billions of records.",
                "years_of_experience": 8,
                "location": "Bengaluru, India",
                "country": "India"
            },
            "career_history": [
                {
                    "company": "HyperScale AI Corp",
                    "title": "Staff ML Scientist",
                    "duration_months": 44,
                    "description": "Invented localized clustering vector layers mapping dense user queries to index clusters. Programmed distributed Pinecone integrations scaling to 25 million records under sub-20ms latencies. Refined hybrid query builders using Learning-to-Rank algorithms (NDCG, MAP metrics validated)."
                },
                {
                    "company": "Google Bangalore",
                    "title": "Senior ML Software Engineer",
                    "duration_months": 33,
                    "description": "Shipped candidate embeddings indexes targeting content matches. Maintained neural classification parameters and supervised model evaluation grids."
                }
            ],
            "skills": skills,
            "education": [{"institution": "Indian Institute of Science (IISc)", "degree": "M.Tech", "field_of_study": "Computational Science", "end_year": 2019}],
            "certifications": [],
            "redrob_signals": {
                "open_to_work_flag": False,
                "last_active_date": "2025-01-20", # Dead inactive
                "recruiter_response_rate": 0.02,
                "notice_period_days": 90,
                "github_activity_score": 3,
                "interview_completion_rate": 0.05,
                "skill_assessment_scores": {"Python": 99, "Machine Learning": 98}
            }
        })

    # GROUP 6: PLAIN-LANGUAGE SEEKERS (12 candidates)
    plain_first = ['Ketan', 'Bhavna', 'Pranav', 'Uma', 'Akash', 'Shradha', 'Devendra', 'Nisha', 'Mayank', 'Rupa', 'Sachin', 'Leela']
    for i in range(12):
        fn = plain_first[i]
        ln = last_names[(i + 12) % len(last_names)]
        cid = f"CAND_6500{100 + i}"
        yoe = 6 + (i % 2)
        comp = product_companies[(i + 4) % len(product_companies)]
        
        skills = [
            {"name": "Python", "proficiency": "expert", "endorsements": 38, "duration_months": 80},
            {"name": "Java", "proficiency": "advanced", "endorsements": 24, "duration_months": 48},
            {"name": "SQL", "proficiency": "expert", "endorsements": 41, "duration_months": 72},
            {"name": "Elasticsearch", "proficiency": "advanced", "endorsements": 22, "duration_months": 30},
            {"name": "Pinecone", "proficiency": "intermediate", "endorsements": 3, "duration_months": 12},
            {"name": "System Architecture", "proficiency": "advanced", "endorsements": 18, "duration_months": 24}
        ]
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": f"{fn} {ln}",
                "current_title": "Senior Software Engineer",
                "current_company": comp,
                "headline": f"Senior Software Engineer | Backend & Information Retrieval | ex-{comp}",
                "summary": "I build backend search layers and data indices. Strong core programmer with 7 years of engineering focus. Passionate about solving fast query alignments, indexing pipelines, and system latencies. I help products load relevant answers quickly.",
                "years_of_experience": yoe,
                "location": "Pune, India",
                "country": "India"
            },
            "career_history": [
                {
                    "company": comp,
                    "title": "Senior Software Engineer (Backend Systems)",
                    "duration_months": 40,
                    "description": "Designed a system to parse custom human prompts and retrieve high-relevance catalogs. Replaced generic word-matching queries with Dense Vector Similarity layers using pretrained English neural models and local vector database storage (Pinecone). Resulted in search NDCG metrics boosting from 0.62 up to 0.76. Implemented strict automated regression tests and managed rolling A/B tests to monitor daily query conversion ratios."
                },
                {
                    "company": "Nexus Software Tech",
                    "title": "Software Engineer",
                    "duration_months": 34,
                    "description": "Maintained highly responsive REST endpoints. Optimized SQL queries and added elasticsearch query expansions, dropping search response latency below 50ms across half a million daily documents."
                }
            ],
            "skills": skills,
            "education": [{"institution": "Pune Institute of Computer Technology", "degree": "B.E.", "field_of_study": "Computer Engineering", "end_year": 2020}],
            "certifications": [],
            "redrob_signals": {
                "open_to_work_flag": True,
                "last_active_date": "2026-06-09",
                "recruiter_response_rate": 0.85,
                "notice_period_days": 30,
                "github_activity_score": 52,
                "interview_completion_rate": 0.90,
                "skill_assessment_scores": {"Python": 90}
            }
        })

    # GROUP 7: NORMAL DEVELOPERS (30 candidates)
    norm_names = ['Raman', 'Swapan', 'Tarpreet', 'Arvinder', 'Simran', 'Tanmay', 'Siddharth', 'Nayan', 'Varun', 'Ishita', 'Mitali', 'Nupur', 'Harsha', 'Jayesh', 'Lalit', 'Mukund', 'Paresh', 'Naveen', 'Umesh', 'Yogesh', 'Aniket', 'Chaitanya', 'Gaurav', 'Indranil', 'Soumya', 'Prashant', 'Raghav', 'Shreyas', 'Tejas', 'Utkarsh']
    for i in range(30):
        fn = norm_names[i]
        ln = last_names[(i + 4) % len(last_names)]
        cid = f"CAND_5000{100 + i}"
        yoe = 4 + (i % 6)
        loc = locations[(i + 2) % len(locations)]
        
        skills = [
            {"name": "Python", "proficiency": "advanced", "endorsements": 12, "duration_months": yoe * 12},
            {"name": "Pandas", "proficiency": "advanced", "endorsements": 11, "duration_months": 24},
            {"name": "Java", "proficiency": "intermediate", "endorsements": 4, "duration_months": 18},
            {"name": "SQL", "proficiency": "advanced", "endorsements": 15, "duration_months": 36}
        ]
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": f"{fn} {ln}",
                "current_title": "Data Scientist" if i % 2 == 0 else "Software Engineer",
                "current_company": "InnoTech Solutions",
                "headline": "Data Scientist and Python Programmer" if i % 2 == 0 else "Backend developer & API creator",
                "summary": f"Developer with {yoe} years experience creating software services. Experienced with Python, Pandas, data visualizations and simple web applications. Looking to advance into ML/AI roles.",
                "years_of_experience": yoe,
                "location": f"{loc['city']}, India",
                "country": "India"
            },
            "career_history": [
                {
                    "company": "InnoTech Solutions",
                    "title": "Data Scientist" if i % 2 == 0 else "Software Engineer",
                    "duration_months": 29,
                    "description": "Worked on business predictive models for pricing lists. Created regression tables and managed API routes utilizing Flask in Python."
                },
                {
                    "company": "CoreApps Limited",
                    "title": "Junior Developer",
                    "duration_months": 33,
                    "description": "Maintained backend operations, optimized relational databases, configured API payloads and compiled data summaries."
                }
            ],
            "skills": skills,
            "education": [{"institution": "DTU Delhi", "degree": "B.Tech", "field_of_study": "Information Technology", "end_year": 2021}],
            "certifications": [],
            "redrob_signals": {
                "open_to_work_flag": True,
                "last_active_date": "2026-06-08",
                "recruiter_response_rate": 0.70 + (i * 0.005),
                "notice_period_days": 30,
                "github_activity_score": 35,
                "interview_completion_rate": 0.85,
                "skill_assessment_scores": {},
                "willing_to_relocate": i % 2 == 0
            }
        })

    return candidates

if __name__ == "__main__":
    candidates = get_test_candidates()
    print(f"Writing {len(candidates)} candidates to candidates.jsonl")
    with open("candidates.jsonl", "w", encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps(c) + "\n")
    print("Done!")
