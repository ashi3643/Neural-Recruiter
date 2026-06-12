import { Candidate } from './types';

// Let's create realistic profiles representing different subgroups
export function generate_candidates(): Candidate[] {
  const candidates: Candidate[] = [];

  // Helper arrays for content generation
  const productCompanies = ['Razorpay', 'Flipkart', 'InMobi', 'PhonePe', 'Dunzo', 'Myntra', 'Ola Cabs', 'Swiggy', 'Zomato', 'Cred', 'Slack', 'Stripe', 'Atlassian'];
  const consultingCompanies = ['Tata Consultancy Services', 'Infosys', 'Wipro Digital', 'Accenture', 'Cognizant Technology Solutions', 'Capgemini India', 'HCL Technologies', 'Tech Mahindra'];
  
  const locationsMap = [
    { city: 'Bengaluru', country: 'India' },
    { city: 'Noida', country: 'India' },
    { city: 'Pune', country: 'India' },
    { city: 'Hyderabad', country: 'India' },
    { city: 'Gurugram', country: 'India' },
    { city: 'Mumbai', country: 'India' },
    { city: 'New Delhi', country: 'India' },
    { city: 'San Francisco', country: 'United States' },
    { city: 'London', country: 'United Kingdom' }
  ];

  // ==========================================
  // GROUP 1: AI SUPERSTARS (15 candidates)
  // Perfectly aligned title, skills, experience, locations & active
  // ==========================================
  const firstNames = ['Arjun', 'Priya', 'Aditya', 'Sneha', 'Rohan', 'Ananya', 'Vikram', 'Divya', 'Sandeep', 'Deepika', 'Kunal', 'Neha', 'Rahul', 'Tanvi', 'Abhishek'];
  const lastNames = ['Sharma', 'Iyer', 'Patel', 'Nair', 'Mehta', 'Reddy', 'Verma', 'Sen', 'Choudhury', 'Joshi', 'Gupta', 'Rao', 'Singh', 'Deshmukh', 'Mishra'];

  for (let i = 0; i < 15; i++) {
    const fn = firstNames[i];
    const ln = lastNames[i];
    const cityObj = locationsMap[i % 5]; // Indian preferred hubs
    const id = `CAND_${1000000 + i}`;
    const years = 6 + (i % 3); // 6, 7, 8 years of experience
    
    candidates.push({
      candidate_id: id,
      tag: 'superstar',
      profile: {
        name: `${fn} ${ln}`,
        headline: `Senior Machine Learning & Search Specialist | ex-${productCompanies[i % 3]}`,
        summary: `Passionate engineer with ${years}+ years shipping information retrieval and recommendation systems at scale. Experienced in neural networks, dense embeddings, hybrid search, and ranking evaluation metrics. Built dense index systems handling millions of daily query hits.`,
        location: `${cityObj.city}, Karnataka`,
        country: cityObj.country,
        years_of_experience: years,
        current_title: i % 2 === 0 ? 'Senior AI Engineer' : 'Machine Learning Engineer',
        current_company: productCompanies[i % productCompanies.length],
        current_company_size: '500-1000',
        current_industry: 'Product Technology & Internet',
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${fn}${ln}`
      },
      career_history: [
        {
          company: productCompanies[i % productCompanies.length],
          title: 'Senior ML Engineer',
          start_date: '2023-01',
          end_date: 'Present',
          duration_months: 41,
          is_current: true,
          industry: 'Internet / SaaS',
          company_size: '500-1000',
          description: `Designed and deployed end-to-end multi-stage hybrid ranking system. Integrated dense vector similarity (Sentence-Transformers + Pinecone) alongside classical hybrid sparse models. Leveraged Learning-to-Rank (LTR LambdaMART) resulting in a 14% lift in Search NDCG@10 metrics. Monitored online production performance through continuous split A/B testing.`
        },
        {
          company: productCompanies[(i + 1) % productCompanies.length],
          title: 'Machine Learning Engineer',
          start_date: '2020-03',
          end_date: '2022-12',
          duration_months: 33,
          is_current: false,
          industry: 'E-Commerce',
          company_size: '1000-5000',
          description: `Built candidate text embedding pipelines to parse, match and rank semantic compatibility scores. Optimized search latency below 45ms. Deployed real-time query vector index caches based on FAISS library.`
        }
      ],
      education: [
        {
          institution: 'Indian Institute of Technology (IIT), Bombay',
          degree: 'B.Tech',
          field_of_study: 'Computer Science and Engineering',
          start_year: 2014,
          end_year: 2018,
          grade: '9.2 CGPA',
          tier: 'tier_1'
        }
      ],
      skills: [
        { name: 'Python', proficiency: 'expert', endorsements: 44, duration_months: years * 12 },
        { name: 'Sentence Transformers', proficiency: 'expert', endorsements: 32, duration_months: 36 },
        { name: 'Pinecone', proficiency: 'advanced', endorsements: 28, duration_months: 30 },
        { name: 'RAG', proficiency: 'expert', endorsements: 35, duration_months: 32 },
        { name: 'NDCG', proficiency: 'expert', endorsements: 21, duration_months: 28 },
        { name: 'PyTorch', proficiency: 'advanced', endorsements: 41, duration_months: 48 },
        { name: 'FAISS', proficiency: 'advanced', endorsements: 18, duration_months: 24 }
      ],
      certifications: [
        { name: 'TensorFlow Developer Certificate', issuer: 'Google', year: 2021 }
      ],
      redrob_signals: {
        open_to_work_flag: i % 2 === 0,
        last_active_date: '2026-06-10', // fully active yesterday
        recruiter_response_rate: 0.88 + (i * 0.008),
        avg_response_time_hours: 1.5,
        notice_period_days: 15 + (i * 2), // nice short notice
        github_activity_score: 82 + i,
        interview_completion_rate: 0.95,
        offer_acceptance_rate: 0.85,
        skill_assessment_scores: { 'Python': 98, 'Machine Learning': 95 },
        profile_completeness_score: 95,
        applications_submitted_30d: 6,
        saved_by_recruiters_30d: 8,
        willing_to_relocate: true,
        preferred_work_mode: 'flexible',
        expected_salary_range_inr_lpa: { min: 28, max: 40 },
        verified_email: true,
        verified_phone: true,
        linkedin_connected: true
      }
    });
  }

  // ==========================================
  // GROUP 2: KEYWORD STUFFERS (15 candidates)
  // Non-tech titles (HR/Ops/Accountant) stuffing AI terms
  // ==========================================
  const stufferFirstNames = ['Rajesh', 'Sunita', 'Anil', 'Kiran', 'Manish', 'Kavita', 'Sanjay', 'Alok', 'Amit', 'Pooja', 'Suresh', 'Geeta', 'Ramesh', 'Harish', 'Ritu'];
  const stufferTitles = ['HR Operations Partner', 'Senior Operations Manager', 'Finance Lead', 'Customer Success Associate', 'Logistics Analyst', 'Talent Scout Coordinator', 'Sales Specialist'];
  
  for (let i = 0; i < 15; i++) {
    const fn = stufferFirstNames[i];
    const ln = lastNames[(i + 3) % lastNames.length];
    const id = `CAND_${1000100 + i}`;
    const years = 8 + (i % 4);
    
    candidates.push({
      candidate_id: id,
      tag: 'keyword_stuffer',
      profile: {
        name: `${fn} ${ln}`,
        headline: `Supercharged Operations & Tech Enthusiast | Python | RAG | Pinecone | OpenAI embeddings | Generative AI expert`,
        summary: `Results-driven operations professional now specializing in AI capabilities. Expertise in Python scripts, RAG pipelines, Prompt engineering, embeddings matching, and LLM orchestration. Levering neural net embeddings for workflow efficiency.`,
        location: 'Chandigarh, Punjab',
        country: 'India',
        years_of_experience: years,
        current_title: stufferTitles[i % stufferTitles.length],
        current_company: 'Global Retail Corp',
        current_company_size: '10000+',
        current_industry: 'Retail & Service Management',
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${fn}${ln}`
      },
      career_history: [
        {
          company: 'Global Retail Corp',
          title: stufferTitles[i % stufferTitles.length],
          start_date: '2021-02',
          end_date: 'Present',
          duration_months: 64,
          is_current: true,
          industry: 'Logistics / Retail',
          company_size: '10000+',
          description: `Coordinates logistics workflows, managing a team of 15 logistics associates. Integrated tiny Python scripts and OpenAI API ChatGPT tokens to draft automated email responses, enhancing office throughput metrics. Explored vector storage conceptually.`
        },
        {
          company: 'Pinnacle Services',
          title: 'Operations Assistant',
          start_date: '2018-05',
          end_date: '2021-01',
          duration_months: 32,
          is_current: false,
          industry: 'Business Consulting',
          company_size: '1000-5000',
          description: `Maintained file organization databases. Conducted simple spreadsheet queries and managed regional operational reports.`
        }
      ],
      education: [
        {
          institution: 'Kurukshetra University',
          degree: 'B.Com',
          field_of_study: 'Business Commerce',
          start_year: 2014,
          end_year: 2017,
          grade: 'B+',
          tier: 'tier_4'
        }
      ],
      skills: [
        { name: 'Python', proficiency: 'expert', endorsements: 1, duration_months: 6 },
        { name: 'Sentence Transformers', proficiency: 'expert', endorsements: 0, duration_months: 3 },
        { name: 'Pinecone', proficiency: 'expert', endorsements: 0, duration_months: 3 },
        { name: 'RAG', proficiency: 'expert', endorsements: 1, duration_months: 4 },
        { name: 'NDCG', proficiency: 'advanced', endorsements: 0, duration_months: 2 },
        { name: 'Operations Management', proficiency: 'expert', endorsements: 45, duration_months: 120 }
      ],
      certifications: [
        { name: 'Prompt Engineering Bootcamp Certificate', issuer: 'Online Academy', year: 2025 }
      ],
      redrob_signals: {
        open_to_work_flag: true,
        last_active_date: '2026-06-11',
        recruiter_response_rate: 0.95,
        avg_response_time_hours: 0.5,
        notice_period_days: 0,
        github_activity_score: 12, // extremely low active code
        interview_completion_rate: 1.0,
        offer_acceptance_rate: 0.90,
        skill_assessment_scores: { 'Python': 35 }, // platform verify reveals low actual capacity
        profile_completeness_score: 88,
        applications_submitted_30d: 42,
        saved_by_recruiters_30d: 1,
        willing_to_relocate: true,
        preferred_work_mode: 'remote',
        expected_salary_range_inr_lpa: { min: 6, max: 9 },
        verified_email: true,
        verified_phone: true,
        linkedin_connected: true
      }
    });
  }

  // ==========================================
  // GROUP 3: CONSULTING TRAP (15 candidates)
  // 100% career in IT outsourcing service giants
  // ==========================================
  const consultFirstNames = ['Vikash', 'Aishwarya', 'Karthik', 'Swati', 'Hari', 'Pallavi', 'Vijay', 'Sumit', 'Jaya', 'Shankar', 'Nidhi', 'Madhuri', 'Tarun', 'Shalini', 'Nikhil'];
  for (let i = 0; i < 15; i++) {
    const fn = consultFirstNames[i];
    const ln = lastNames[(i + 6) % lastNames.length];
    const id = `CAND_${1000200 + i}`;
    const years = 7 + (i % 3);
    const firm = consultingCompanies[i % consultingCompanies.length];
    
    candidates.push({
      candidate_id: id,
      tag: 'normal', // treated as normal but fails product company check/scores low on career quality
      profile: {
        name: `${fn} ${ln}`,
        headline: `Lead Consultant | AI-ML Delivery Lead at ${firm}`,
        summary: `Accomplished AI Solutions Consultant with ${years} years delivery management expertise in banking, healthcare and insurance clients. Implemented diverse enterprise RAG databases using out-of-the-box pipeline connectors. Skilled Scrum Master and customer stakeholder catalyst.`,
        location: 'Hyderabad, Telangana',
        country: 'India',
        years_of_experience: years,
        current_title: 'AI Architect & Delivery Lead',
        current_company: firm,
        current_company_size: '10000+',
        current_industry: 'IT Services & Consulting',
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${fn}${ln}`
      },
      career_history: [
        {
          company: firm,
          title: 'Lead AI Engineer',
          start_date: '2022-04',
          end_date: 'Present',
          duration_months: 50,
          is_current: true,
          industry: 'IT Outsourcing',
          company_size: '10000+',
          description: `Supervises client delivery architectures on cloud. Orchestrates vendor AI frameworks. Implemented LangChain connectors to feed knowledge documents into default third-party vector databases. Supported client demo pitches.`
        },
        {
          company: consultingCompanies[(i + 2) % consultingCompanies.length],
          title: 'Systems Engineer - Machine Learning',
          start_date: '2019-06',
          end_date: '2022-03',
          duration_months: 33,
          is_current: false,
          industry: 'IT Services',
          company_size: '10000+',
          description: `Wrote SQL procedures and mapped candidate JSON models. Maintained legacy Spark data cleansings, occasionally compiling pre-configured text classifier scripts.`
        }
      ],
      education: [
        {
          institution: 'Visvesvaraya Technological University',
          degree: 'B.E.',
          field_of_study: 'Information Science',
          start_year: 2015,
          end_year: 2019,
          grade: '8.1 CGPA',
          tier: 'tier_3'
        }
      ],
      skills: [
        { name: 'Python', proficiency: 'advanced', endorsements: 18, duration_months: 48 },
        { name: 'RAG', proficiency: 'advanced', endorsements: 12, duration_months: 24 },
        { name: 'Pinecone', proficiency: 'intermediate', endorsements: 5, duration_months: 18 },
        { name: 'Sentence Transformers', proficiency: 'intermediate', endorsements: 3, duration_months: 12 },
        { name: 'Project Management', proficiency: 'expert', endorsements: 85, duration_months: 80 }
      ],
      certifications: [
        { name: 'AWS Certified Machine Learning', issuer: 'Amazon Web Services', year: 2023 }
      ],
      redrob_signals: {
        open_to_work_flag: false,
        last_active_date: '2026-06-05',
        recruiter_response_rate: 0.42,
        avg_response_time_hours: 12.0,
        notice_period_days: 90, // terrible long 90-day consulting notice period!
        github_activity_score: -1, // No real github history (private consulting client networks)
        interview_completion_rate: 0.60,
        offer_acceptance_rate: 0.50,
        skill_assessment_scores: { 'Python': 72 },
        profile_completeness_score: 92,
        applications_submitted_30d: 2,
        saved_by_recruiters_30d: 2,
        willing_to_relocate: true,
        preferred_work_mode: 'hybrid',
        expected_salary_range_inr_lpa: { min: 20, max: 26 },
        verified_email: true,
        verified_phone: true,
        linkedin_connected: true
      }
    });
  }

  // ==========================================
  // GROUP 4: HONEYPOT TRAPS (12 candidates)
  // Impossible profiles (Trap 2: faked data, future dates)
  // ==========================================
  const honeyFirstNames = ['CyberTris', 'RoboMatcher', 'QuantumMinds', 'AISeeker_01', 'HyperBot', 'DeepRacerPro', 'AIGuru', 'Samyak_Expert', 'HNSW_Master', 'Mr_RAG', 'VectorBoy', 'TransformerQueen'];
  for (let i = 0; i < 12; i++) {
    const fn = honeyFirstNames[i];
    const ln = 'Honeypot';
    const id = `CAND_9999${100 + i}`; // noticeable IDs
    
    // Choose one specific honeypot style
    const hType = i % 3;
    let candidateEntry: Candidate;
    
    if (hType === 0) {
      // Style A: Expert proficiency with 0 months duration
      candidateEntry = {
        candidate_id: id,
        tag: 'honeypot',
        profile: {
          name: `${fn} Tech`,
          headline: `Expert Founding Engineer specialized in pinecone dense matching and Lambdamart LTR`,
          summary: `Senior architect holding deep credentials in ranking and neural models. Built massive frameworks.`,
          location: 'Pune, Maharashtra',
          country: 'India',
          years_of_experience: 7,
          current_title: 'Senior AI Engineer',
          current_company: 'Redrob AI Challenger Mock',
          current_company_size: '10-50',
          current_industry: 'Information Technology',
          avatar_url: `https://api.dicebear.com/7.x/identicon/svg?seed=${fn}`
        },
        career_history: [
          {
            company: 'Redrob AI Challenger Mock',
            title: 'Senior AI Engineer',
            start_date: '2024-01',
            end_date: 'Present',
            duration_months: 29,
            is_current: true,
            industry: 'IT',
            company_size: '10-50',
            description: `Supervised neural core. Designed pinecone maps.`
          }
        ],
        education: [
          {
            institution: 'IIT Delhi',
            degree: 'B.Tech',
            field_of_study: 'CS',
            start_year: 2015,
            end_year: 2019,
            grade: '10.0',
            tier: 'tier_1'
          }
        ],
        skills: [
          { name: 'Sentence Transformers', proficiency: 'expert', endorsements: 1, duration_months: 0 }, // 0 months
          { name: 'Pinecone', proficiency: 'expert', endorsements: 0, duration_months: 0 }, // 0 months
          { name: 'RAG', proficiency: 'expert', endorsements: 0, duration_months: 0 }, // 0 months
          { name: 'Python', proficiency: 'expert', endorsements: 12, duration_months: 84 }
        ],
        certifications: [],
        redrob_signals: {
          open_to_work_flag: true,
          last_active_date: '2026-06-11',
          recruiter_response_rate: 1.0,
          avg_response_time_hours: 0.1,
          notice_period_days: 0,
          github_activity_score: 99,
          interview_completion_rate: 1.0,
          offer_acceptance_rate: 1.0,
          skill_assessment_scores: { 'Python': 100 },
          profile_completeness_score: 100,
          applications_submitted_30d: 50,
          saved_by_recruiters_30d: 20,
          willing_to_relocate: true,
          preferred_work_mode: 'remote',
          expected_salary_range_inr_lpa: { min: 25, max: 45 },
          verified_email: true,
          verified_phone: true,
          linkedin_connected: true
        }
      };
    } else if (hType === 1) {
      // Style B: Timeline mismatch (e.g. stated YoE=3 years, but career roles sum to 12 years)
      candidateEntry = {
        candidate_id: id,
        tag: 'honeypot',
        profile: {
          name: `FastCareer ${fn}`,
          headline: `Young Leader and ML Engineer`,
          summary: `Fast progressor through senior technical hierarchies.`,
          location: 'Pune, Maharashtra',
          country: 'India',
          years_of_experience: 3, // Claims 3 years YoE
          current_title: 'Senior Machine Learning Systems Lead',
          current_company: 'Apex Solutions',
          current_company_size: '50-100',
          current_industry: 'IT',
          avatar_url: `https://api.dicebear.com/7.x/identicon/svg?seed=${fn}`
        },
        career_history: [
          {
            company: 'Apex Solutions',
            title: 'Senior ML Systems Lead',
            start_date: '2021-01',
            end_date: 'Present',
            duration_months: 65, // > 5 years current role
            is_current: true,
            industry: 'IT',
            company_size: '50-100',
            description: `Leads AI teams. Outperformed goals.`
          },
          {
            company: 'Origin Labs',
            title: 'Founding ML Developer',
            start_date: '2015-01',
            end_date: '2020-12',
            duration_months: 72, // 6 years previous role
            is_current: false,
            industry: 'IT',
            company_size: '10-25',
            description: `Built ranking kernels is Django. Created semantic clusters.`
          }
        ], // Combined months: 137 (~11 years) vs Stated YoE: 3 years
        education: [],
        skills: [
          { name: 'Python', proficiency: 'advanced', endorsements: 12, duration_months: 36 },
          { name: 'Sentence Transformers', proficiency: 'expert', endorsements: 5, duration_months: 24 }
        ],
        certifications: [],
        redrob_signals: {
          open_to_work_flag: true,
          last_active_date: '2026-06-11',
          recruiter_response_rate: 0.90,
          avg_response_time_hours: 1.0,
          notice_period_days: 15,
          github_activity_score: 55,
          interview_completion_rate: 0.90,
          offer_acceptance_rate: 0.80,
          skill_assessment_scores: {},
          profile_completeness_score: 80,
          applications_submitted_30d: 4,
          saved_by_recruiters_30d: 2,
          willing_to_relocate: true,
          preferred_work_mode: 'remote',
          expected_salary_range_inr_lpa: { min: 40, max: 50 },
          verified_email: true,
          verified_phone: true,
          linkedin_connected: true
        }
      };
    } else {
      // Style C: Certification date in the future (e.g. 2029) or Education in future (2031)
      candidateEntry = {
        candidate_id: id,
        tag: 'honeypot',
        profile: {
          name: `TimeTraveler ${fn}`,
          headline: `Vanguard Artificial Intelligence Engineer`,
          summary: `Shifting cognitive capabilities ahead of time. Specializing in dense retrieval matrix configurations.`,
          location: 'Noida, Uttar Pradesh',
          country: 'India',
          years_of_experience: 5,
          current_title: 'Senior AI Research Engineer',
          current_company: 'Vortex Global',
          current_company_size: '100-200',
          current_industry: 'IT',
          avatar_url: `https://api.dicebear.com/7.x/identicon/svg?seed=${fn}`
        },
        career_history: [
          {
            company: 'Vortex Global',
            title: 'Senior AI Engineer',
            start_date: '2022-01',
            end_date: 'Present',
            duration_months: 53,
            is_current: true,
            industry: 'IT',
            company_size: '100-200',
            description: `Orchestrated dense retrievals.`
          }
        ],
        education: [
          {
            institution: 'VIT University',
            degree: 'M.Tech',
            field_of_study: 'AI',
            start_year: 2019,
            end_year: 2029, // Future education end! (2029 > 2026)
            grade: '9.0',
            tier: 'tier_2'
          }
        ],
        skills: [
          { name: 'Python', proficiency: 'advanced', endorsements: 10, duration_months: 60 },
          { name: 'Sentence Transformers', proficiency: 'expert', endorsements: 8, duration_months: 30 }
        ],
        certifications: [
          { name: 'Redrob Master Certification', issuer: 'Future Labs Org', year: 2028 } // Future certification (2028 > 2026)
        ],
        redrob_signals: {
          open_to_work_flag: true,
          last_active_date: '2026-06-11',
          recruiter_response_rate: 0.95,
          avg_response_time_hours: 0.5,
          notice_period_days: 30,
          github_activity_score: 80,
          interview_completion_rate: 1.0,
          offer_acceptance_rate: 0.85,
          skill_assessment_scores: {},
          profile_completeness_score: 95,
          applications_submitted_30d: 3,
          saved_by_recruiters_30d: 3,
          willing_to_relocate: true,
          preferred_work_mode: 'remote',
          expected_salary_range_inr_lpa: { min: 20, max: 30 },
          verified_email: true,
          verified_phone: true,
          linkedin_connected: true
        }
      };
    }
    candidates.push(candidateEntry);
  }

  // ==========================================
  // GROUP 5: BEHAVIORAL GHOSTS (12 candidates)
  // Perfect skills on paper, but completely inactive/unreachable
  // ==========================================
  const ghostFirstNames = ['Manoj', 'Gayatri', 'Rupesh', 'Anushka', 'Vivek', 'Shruti', 'Animesh', 'Pragati', 'Girish', 'Ridhima', 'Sourav', 'Jyoti'];
  for (let i = 0; i < 12; i++) {
    const fn = ghostFirstNames[i];
    const ln = lastNames[(i + 9) % lastNames.length];
    const id = `CAND_8000${100 + i}`;
    
    candidates.push({
      candidate_id: id,
      tag: 'ghost',
      profile: {
        name: `${fn} ${ln} (Inactive)`,
        headline: `Staff AI Scientist | ex-Google | ex-Amazon Embedding Team Lead`,
        summary: `Eminent computer scientist with 8 years of pure focus on Dense Retrieval Systems, vector indices, and custom scoring engines. Published 3 semantic search papers. Architected search layers indexing billions of records.`,
        location: 'Bengaluru, Karnataka',
        country: 'India',
        years_of_experience: 8,
        current_title: 'Staff AI Specialist',
        current_company: 'HyperScale AI Corp',
        current_company_size: '1000-5000',
        current_industry: 'Big Tech',
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${fn}${ln}`
      },
      career_history: [
        {
          company: 'HyperScale AI Corp',
          title: 'Staff ML Scientist',
          start_date: '2022-10',
          end_date: 'Present',
          duration_months: 44,
          is_current: true,
          industry: 'Search Technology',
          company_size: '1000-5000',
          description: `Invented localized clustering vector layers mapping dense user queries to index clusters. Programmed distributed Pinecone integrations scaling to 25 million records under sub-20ms latencies. Refined hybrid query builders using Learning-to-Rank algorithms (NDCG, MAP metrics validated).`
        },
        {
          company: 'Google Bangalore',
          title: 'Senior ML Software Engineer',
          start_date: '2019-12',
          end_date: '2022-09',
          duration_months: 33,
          is_current: false,
          industry: 'Search Solutions',
          company_size: '10000+',
          description: `Shipped candidate embeddings indexes targeting content matches. Maintained neural classification parameters and supervised model evaluation grids.`
        }
      ],
      education: [
        {
          institution: 'Indian Institute of Science (IISc), Bangalore',
          degree: 'M.Tech',
          field_of_study: 'Computational Science',
          start_year: 2017,
          end_year: 2019,
          grade: '9.8 GPA',
          tier: 'tier_1'
        }
      ],
      skills: [
        { name: 'Python', proficiency: 'expert', endorsements: 120, duration_months: 96 },
        { name: 'Sentence Transformers', proficiency: 'expert', endorsements: 95, duration_months: 48 },
        { name: 'Pinecone', proficiency: 'expert', endorsements: 76, duration_months: 36 },
        { name: 'RAG', proficiency: 'expert', endorsements: 82, duration_months: 40 },
        { name: 'NDCG', proficiency: 'expert', endorsements: 62, duration_months: 44 },
        { name: 'FAISS', proficiency: 'expert', endorsements: 54, duration_months: 36 }
      ],
      certifications: [],
      // Secret killer: Dead recruiter signals (unreachable candidate)
      redrob_signals: {
        open_to_work_flag: false,
        last_active_date: '2025-01-20', // Inactive for almost 1.5 years (current date 2026-06)
        recruiter_response_rate: 0.02, // Will absolutely ghost any recruiter (response rate 2%)
        avg_response_time_hours: 144.0, // takes 6 days to response (if ever)
        notice_period_days: 90,
        github_activity_score: 3, // abandoned public coding
        interview_completion_rate: 0.05, // Ghosts interview calls
        offer_acceptance_rate: -1, // no history
        skill_assessment_scores: { 'Python': 99, 'Machine Learning': 98 },
        profile_completeness_score: 98,
        applications_submitted_30d: 0,
        saved_by_recruiters_30d: 12,
        willing_to_relocate: false,
        preferred_work_mode: 'remote',
        expected_salary_range_inr_lpa: { min: 55, max: 70 },
        verified_email: true,
        verified_phone: false,
        linkedin_connected: true
      }
    });
  }

  // ==========================================
  // GROUP 6: PLAIN-LANGUAGE TIER-5s (12 candidates)
  // Software engineers with AMAZING production IR skills, but no active buzzword skills list
  // ==========================================
  const plainFirstNames = ['Ketan', 'Bhavna', 'Pranav', 'Uma', 'Akash', 'Shradha', 'Devendra', 'Nisha', 'Mayank', 'Rupa', 'Sachin', 'Leela'];
  for (let i = 0; i < 12; i++) {
    const fn = plainFirstNames[i];
    const ln = lastNames[(i + 12) % lastNames.length];
    const id = `CAND_6500${100 + i}`;
    const years = 6 + (i % 2);
    
    candidates.push({
      candidate_id: id,
      tag: 'plain_language',
      profile: {
        name: `${fn} ${ln}`,
        headline: `Senior Software Engineer | Backend & Information Retrieval | ex-${productCompanies[(i + 4) % productCompanies.length]}`,
        summary: `I build backend search layers and data indices. Strong core programmer with 7 years of engineering focus. Passionate about solving fast query alignments, indexing pipelines, and system latencies. I help products load relevant answers quickly.`,
        location: 'Pune, Maharashtra',
        country: 'India',
        years_of_experience: years,
        current_title: 'Senior Software Engineer',
        current_company: productCompanies[(i + 4) % productCompanies.length],
        current_company_size: '200-500',
        current_industry: 'Product Software',
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${fn}${ln}`
      },
      // Brilliant career history with production semantic search details written in plain language
      career_history: [
        {
          company: productCompanies[(i + 4) % productCompanies.length],
          title: 'Senior Software Engineer (Backend Systems)',
          start_date: '2023-02',
          end_date: 'Present',
          duration_months: 40,
          is_current: true,
          industry: 'Product SaaS',
          company_size: '200-500',
          description: `Designed a system to parse custom human prompts and retrieve high-relevance catalogs. Replaced generic word-matching queries with Dense Vector Similarity layers using pretrained English neural models and local vector database storage (Pinecone). Resulted in search NDCG metrics boosting from 0.62 up to 0.76. Implemented strict automated regression tests and managed rolling A/B tests to monitor daily query conversion ratios.`
        },
        {
          company: 'Nexus Software Tech',
          title: 'Software Engineer',
          start_date: '2020-03',
          end_date: '2023-01',
          duration_months: 34,
          is_current: false,
          industry: 'Internet Technology',
          company_size: '50-100',
          description: `Maintained highly responsive REST endpoints. Optimized SQL queries and added elasticsearch query expansions, dropping search response latency below 50ms across half a million daily documents.`
        }
      ],
      education: [
        {
          institution: 'Pune Institute of Computer Technology (PICT)',
          degree: 'B.E.',
          field_of_study: 'Computer Engineering',
          start_year: 2016,
          end_year: 2020,
          grade: '9.0 GPA',
          tier: 'tier_2'
        }
      ],
      // No buzzword AI/NLP skills explicitly configured! (This is what makes them Trap 4 Plain-Language targets)
      skills: [
        { name: 'Python', proficiency: 'expert', endorsements: 38, duration_months: 80 },
        { name: 'Java', proficiency: 'advanced', endorsements: 24, duration_months: 48 },
        { name: 'SQL', proficiency: 'expert', endorsements: 41, duration_months: 72 },
        { name: 'Elasticsearch', proficiency: 'advanced', endorsements: 22, duration_months: 30 },
        { name: 'Pinecone', proficiency: 'intermediate', endorsements: 3, duration_months: 12 },
        { name: 'System Architecture', proficiency: 'advanced', endorsements: 18, duration_months: 24 }
      ],
      certifications: [],
      redrob_signals: {
        open_to_work_flag: true,
        last_active_date: '2026-06-09',
        recruiter_response_rate: 0.85,
        avg_response_time_hours: 2.0,
        notice_period_days: 30, // great sweet spot
        github_activity_score: 52,
        interview_completion_rate: 0.90,
        offer_acceptance_rate: 0.80,
        skill_assessment_scores: { 'Python': 90 },
        profile_completeness_score: 90,
        applications_submitted_30d: 5,
        saved_by_recruiters_30d: 4,
        willing_to_relocate: true,
        preferred_work_mode: 'flexible',
        expected_salary_range_inr_lpa: { min: 22, max: 32 },
        verified_email: true,
        verified_phone: true,
        linkedin_connected: true
      }
    });
  }

  // ==========================================
  // GROUP 7: NORMAL TECH CANDIDATES (30 candidates)
  // Average Python devs & generic Data Scientists
  // ==========================================
  const normNames = ['Raman', 'Swapan', 'Tarpreet', 'Arvinder', 'Simran', 'Tanmay', 'Siddharth', 'Nayan', 'Varun', 'Ishita', 'Mitali', 'Nupur', 'Harsha', 'Jayesh', 'Lalit', 'Mukund', 'Paresh', 'Naveen', 'Umesh', 'Yogesh', 'Aniket', 'Chaitanya', 'Gaurav', 'Indranil', 'Soumya', 'Prashant', 'Raghav', 'Shreyas', 'Tejas', 'Utkarsh'];
  for (let i = 0; i < 30; i++) {
    const fn = normNames[i];
    const ln = lastNames[(i + 4) % lastNames.length];
    const id = `CAND_5000${100 + i}`;
    const years = 4 + (i % 6); // 4-9 years of experience
    const cityObj = locationsMap[(i + 2) % locationsMap.length];
    
    candidates.push({
      candidate_id: id,
      tag: 'normal',
      profile: {
        name: `${fn} ${ln}`,
        headline: i % 2 === 0 ? 'Data Scientist and Python Programmer' : 'Backend developer & API creator',
        summary: `Developer with ${years} years experience creating software services. Experienced with Python, Pandas, data visualizations and simple web applications. Looking to advance into ML/AI roles.`,
        location: `${cityObj.city}, ${cityObj.country === 'India' ? 'India' : 'Abroad'}`,
        country: cityObj.country,
        years_of_experience: years,
        current_title: i % 2 === 0 ? 'Data Scientist' : 'Software Engineer',
        current_company: 'InnoTech Solutions',
        current_company_size: '100-200',
        current_industry: 'IT Services',
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${fn}${ln}`
      },
      career_history: [
        {
          company: 'InnoTech Solutions',
          title: i % 2 === 0 ? 'Data Scientist' : 'Software Engineer',
          start_date: '2024-01',
          end_date: 'Present',
          duration_months: 29,
          is_current: true,
          industry: 'Consulting services',
          company_size: '100-200',
          description: `Worked on business predictive models for pricing lists. Created regression tables and managed API routes utilizing Flask in Python.`
        },
        {
          company: 'CoreApps Limited',
          title: 'Junior Developer',
          start_date: '2021-03',
          end_date: '2023-12',
          duration_months: 33,
          is_current: false,
          industry: 'IT Service Provider',
          company_size: '50-100',
          description: `Maintained backend operations, optimized relational databases, configured API payloads and compiled data summaries.`
        }
      ],
      education: [
        {
          institution: 'Delhi Technological University (DTU)',
          degree: 'B.Tech',
          field_of_study: 'Information Technology',
          start_year: 2017,
          end_year: 2021,
          grade: '8.2 CGPA',
          tier: 'tier_2'
        }
      ],
      skills: [
        { name: 'Python', proficiency: 'advanced', endorsements: 12, duration_months: years * 12 },
        { name: 'Pandas', proficiency: 'advanced', endorsements: 11, duration_months: 24 },
        { name: 'Java', proficiency: 'intermediate', endorsements: 4, duration_months: 18 },
        { name: 'SQL', proficiency: 'advanced', endorsements: 15, duration_months: 36 }
      ],
      certifications: [],
      redrob_signals: {
        open_to_work_flag: true,
        last_active_date: '2026-06-08',
        recruiter_response_rate: 0.70 + (i * 0.005),
        avg_response_time_hours: 3.5,
        notice_period_days: 30,
        github_activity_score: 35,
        interview_completion_rate: 0.85,
        offer_acceptance_rate: 0.75,
        skill_assessment_scores: {},
        profile_completeness_score: 85,
        applications_submitted_30d: 4,
        saved_by_recruiters_30d: 2,
        willing_to_relocate: i % 2 === 0,
        preferred_work_mode: 'flexible',
        expected_salary_range_inr_lpa: { min: 14, max: 20 },
        verified_email: true,
        verified_phone: true,
        linkedin_connected: false
      }
    });
  }

  // Double check IDs are completely unique
  return candidates;
}
