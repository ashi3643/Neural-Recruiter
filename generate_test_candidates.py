#!/usr/bin/env python3
"""
generate_test_candidates.py
Generates a realistic set of candidate profiles representing:
- AI Superstars (Tier A, rich semantic search details)
- Keyword Stuffers (Non-tech HR/Ops with false AI skills)
- Adjacent Tech / Software Engineers (No AI skills, or with AI skills)
- Honeypot/Traps (Impossible timelines, future dates, expert 0 months)
- Consulting firm candidates (TCS, Genpact AI profile, etc.)
- Wrong-domain candidates (Autonomous vehicle, Speech/CV specialists)
"""

import json

def get_test_candidates():
    candidates = []

    # 1. AI Superstars (Should rank #1 to #10)
    superstars = [
        ("Arjun Sharma", "Senior AI Engineer", "Razorpay", 7, ["Sentence Transformers", "Pinecone", "RAG", "NDCG", "PyTorch", "FAISS"]),
        ("Priya Nair", "Machine Learning Engineer", "Flipkart", 6, ["sentence-transformers", "Milvus", "RAG", "MRR", "PyTorch", "BM25"]),
        ("Aditya Mehta", "Senior Machine Learning Engineer", "InMobi", 8, ["embeddings", "Qdrant", "retrieval augmented generation", "learning to rank", "LTR", "XGBoost ranking"]),
        ("Sneha Iyer", "Search Engineer", "PhonePe", 6, ["dense retrieval", "vector search", "BM25", "MAP", "Transformers", "scikit-learn"]),
        ("Rohan Reddy", "Applied Scientist", "Stripe", 7, ["sentence-transformers", "Pinecone", "RAG", "evaluation framework", "Hugging Face", "Elasticsearch"]),
    ]
    for idx, (name, title, company, yoe, skill_names) in enumerate(superstars):
        cid = f"CAND_10000{idx:02d}"
        skills = [{"name": s, "proficiency": "expert" if i % 2 == 0 else "advanced", "duration_months": yoe * 12, "endorsements": 20 + idx} for i, s in enumerate(skill_names)]
        skills.append({"name": "Python", "proficiency": "expert", "duration_months": yoe * 12, "endorsements": 45})
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": name,
                "current_title": title,
                "current_company": company,
                "headline": f"Senior Machine Learning & Retrieval Specialist | ex-{company}",
                "summary": f"SRE or ML practitioner with {yoe}+ years shipping advanced search, multi-stage ranking, and dense recommendation systems in production using embeddings and LTR.",
                "years_of_experience": yoe,
                "location": "Bengaluru, Karnataka",
                "country": "India"
            },
            "career_history": [
                {
                    "company": company,
                    "title": title,
                    "duration_months": int(yoe * 0.6 * 12),
                    "description": "Led search scaling initiative. Implemented multi-stage semantic search index using dense retrieval pipelines, Hugging Face sentence-transformers, and Pinecone vector stores. Optimized search metrics NDCG@10 by 18%."
                },
                {
                    "company": f"Previous tech corp",
                    "title": "Machine Learning Software Engineer",
                    "duration_months": int(yoe * 0.4 * 12),
                    "description": "Constructed text matching pipelines using PyTorch and scikit-learn. Optimized indices using FAISS."
                }
            ],
            "skills": skills,
            "education": [{"institution": "IIT Bombay", "degree": "B.Tech", "field_of_study": "Computer Science", "end_year": 2018}],
            "certifications": [],
            "redrob_signals": {
                "open_to_work_flag": True,
                "last_active_date": "2026-06-10",
                "recruiter_response_rate": 0.95,
                "notice_period_days": 15,
                "github_activity_score": 85,
                "interview_completion_rate": 0.92,
                "skill_assessment_scores": {"Python": 95, "Machine Learning": 92}
            }
        })

    # 2. Keyword Stuffers (Should be hard-blocked or rank near-bottom due to non-AI current titles)
    stuffers = [
        ("Rajesh Verma", "HR Operations Partner", "Global Retail", ["Python", "RAG", "Pinecone", "NDCG", "PyTorch", "Milvus"]),
        ("Sunita Patel", "Talent Scout Coordinator", "Tech Services", ["sentence-transformers", "Milvus", "RAG", "MRR", "FAISS"]),
    ]
    for idx, (name, title, company, skill_names) in enumerate(stuffers):
        cid = f"CAND_10010{idx:02d}"
        yoe = 9
        skills = [{"name": s, "proficiency": "expert", "duration_months": yoe * 12, "endorsements": 1} for s in skill_names]
        skills.append({"name": "Python", "proficiency": "expert", "duration_months": yoe * 12, "endorsements": 0})
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": name,
                "current_title": title,
                "current_company": company,
                "headline": f"Human Resources operations specializing in Python, Pinecone, and RAG architectures",
                "summary": "Administrative generalist with high interest in prompt engineering, embeddings, search pipelines, and vector DB systems.",
                "years_of_experience": yoe,
                "location": "Chandigarh, India",
                "country": "India"
            },
            "career_history": [
                {
                    "company": company,
                    "title": title,
                    "duration_months": yoe * 12,
                    "description": "Coordinated HR interviews and managed payroll operations. Passionate about prompt engineering and langchain scripts."
                }
            ],
            "skills": skills,
            "education": [{"institution": "Panjab University", "degree": "MBA", "field_of_study": "Human Resources", "end_year": 2017}],
            "certifications": [],
            "redrob_signals": {
                "open_to_work_flag": False,
                "last_active_date": "2026-06-05",
                "recruiter_response_rate": 0.90,
                "notice_period_days": 30,
                "github_activity_score": 15,
                "skill_assessment_scores": {"Python": 42}
            }
        })

    # 3. Adjacent Tech - Backend/Frontend Engineers (B-tier. Without AI skills should get score 0.05. With AI skills should score standard)
    techs = [
        ("Kunal Gupta", "Senior Software Engineer (Backend)", "Swiggy", False), # No AI skills
        ("Neha Rao", "Software Engineer", "Zomato", True), # Has AI skills
    ]
    for idx, (name, title, company, has_ai) in enumerate(techs):
        cid = f"CAND_10020{idx:02d}"
        yoe = 7
        skill_names = ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"]
        if has_ai:
            skill_names.extend(["Sentence Transformers", "Pinecone", "vector search"])
            headline = "Backend engineer scaling dense search indexing"
            summary = "Software practitioner who built hybrid retrieval mechanisms for e-commerce catalog search."
        else:
            headline = "Senior Backend engineer"
            summary = "Core platform developer focusing on API microservices, distributed caching, and database replication."

        skills = [{"name": s, "proficiency": "advanced", "duration_months": 36, "endorsements": 15} for s in skill_names]
        
        candidates.append({
            "candidate_id": cid,
            "profile": {
                "name": name,
                "current_title": title,
                "current_company": company,
                "headline": headline,
                "summary": summary,
                "years_of_experience": yoe,
                "location": "Pune, Maharashtra",
                "country": "India"
            },
            "career_history": [
                {
                    "company": company,
                    "title": title,
                    "duration_months": 40,
                    "description": "Built resilient server components and scaled APIs to 10k requests per second."
                }
            ],
            "skills": skills,
            "education": [{"institution": "BITS Pilani", "degree": "B.E.", "field_of_study": "Computer Science", "end_year": 2019}],
            "certifications": [],
            "redrob_signals": {
                "open_to_work_flag": True,
                "last_active_date": "2026-06-09",
                "recruiter_response_rate": 0.85,
                "notice_period_days": 15,
                "github_activity_score": 55,
                "skill_assessment_scores": {"Python": 88}
            }
        })

    # 4. Honeypot/Traps (Timeline Paradox - Stated 3yrs but combined career adds up to 10yrs, or certificate in future. Should rank 0.0)
    candidates.append({
        "candidate_id": "CAND_1003000", # Time traveler / timeline paradox
        "profile": {
            "name": "Ghost Candidate",
            "current_title": "Machine Learning Engineer",
            "current_company": "Startup X",
            "headline": "ML wizard",
            "summary": "Specialist with 3 years of experience.",
            "years_of_experience": 3,
            "location": "Noida, India",
            "country": "India"
        },
        "career_history": [
            {"company": "Startup X", "title": "ML Engineer", "duration_months": 60, "description": "Lived in the future"},
            {"company": "Corp Y", "title": "Developer", "duration_months": 60, "description": "Lived in the past"}
        ],
        "skills": [{"name": "Python", "proficiency": "expert", "duration_months": 12, "endorsements": 1}],
        "education": [],
        "certifications": [],
        "redrob_signals": {
            "last_active_date": "2026-06-11",
            "skill_assessment_scores": {}
        }
    })

    # 5. Consulting Firm Candidate (Should rank lower due to consulting firm filter)
    candidates.append({
        "candidate_id": "CAND_1004000",
        "profile": {
            "name": "Sanjay Dutt",
            "current_title": "Senior AI Architect",
            "current_company": "Genpact",
            "headline": "Consultant specializing in ML",
            "summary": "Assisted clients with migrating cloud platforms and deploying standard PyTorch networks.",
            "years_of_experience": 8,
            "location": "Noida, India",
            "country": "India"
        },
        "career_history": [
            {
                "company": "Genpact",
                "title": "Senior Technical Consultant",
                "duration_months": 96,
                "description": "Facilitated digital transformation workshops. Developed classic neural networks for generic customer support logs."
            }
        ],
        "skills": [
            {"name": "Python", "proficiency": "expert", "duration_months": 96},
            {"name": "Pinecone", "proficiency": "advanced", "duration_months": 24},
            {"name": "RAG", "proficiency": "expert", "duration_months": 24}
        ],
        "education": [],
        "certifications": [],
        "redrob_signals": {
            "last_active_date": "2026-06-11",
            "recruiter_response_rate": 0.85,
            "notice_period_days": 30,
            "github_activity_score": 45,
            "skill_assessment_scores": {"Python": 85}
        }
    })

    # 6. Wrong-Domain ML Engineer (Speech/CV) (Should be penalized 0.5x, ranking below search superstars)
    candidates.append({
        "candidate_id": "CAND_1005000",
        "profile": {
            "name": "Vikram Seth",
            "current_title": "Lead Computer Vision Scientist",
            "current_company": "Autonomous Systems",
            "headline": "Computer Vision & Robotics Guru | ex-Tesla",
            "summary": "Deep specialist in computer vision, autonomous vehicles, lidar sensor fusion, and multi-object tracking.",
            "years_of_experience": 8,
            "location": "Bengaluru, India",
            "country": "India"
        },
        "career_history": [
            {
                "company": "Autonomous Systems",
                "title": "Lead CV Scientist",
                "duration_months": 96,
                "description": "Designed real-time 3D object detection models for lidar point clouds. Trained massive autoencoder vision transformers."
            }
        ],
        "skills": [
            {"name": "Python", "proficiency": "expert", "duration_months": 96},
            {"name": "PyTorch", "proficiency": "expert", "duration_months": 96},
            {"name": "Computer Vision", "proficiency": "expert", "duration_months": 96},
            {"name": "Object Detection", "proficiency": "expert", "duration_months": 96}
        ],
        "education": [],
        "certifications": [],
        "redrob_signals": {
            "last_active_date": "2026-06-10",
            "recruiter_response_rate": 0.90,
            "notice_period_days": 15,
            "github_activity_score": 75,
            "skill_assessment_scores": {"Machine Learning": 98}
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
