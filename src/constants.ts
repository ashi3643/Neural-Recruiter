import { SignalWeights } from './types';

export const REDROB_JD = {
  title: "Senior AI Engineer",
  company: "Redrob AI",
  experience_range: "6–8 years (5–9 acceptable)",
  location: "Pune, Noida, Hyderabad, Bangalore, Mumbai, Delhi NCR (or willing to relocate)",
  description: "Redrob AI is building the future of talent evaluation. We are looking for a Senior AI Engineer to join our founding team. In this role, you will lead the development of our search, ranking, and recommendation engines. The ideal candidate has built and shipped dense-retrieval, hybrid search, or multi-stage semantic ranking systems at a product-centric organization.",
  core_requirements: [
    "Experience shipping end-to-end ranking, search, or recommendation systems to production",
    "Production experience with embeddings, sentence-transformers, BGE, E5, and vector databases",
    "Familiarity with ranking metrics like NDCG, MRR, MAP, and online evaluation (A/B testing)",
    "Strong Python software engineering background (actively writing code today)",
    "6-8 years of experience, preferably at product-centric tech firms rather than offshore consulting bodies"
  ]
};

// Default weights summing to 1.00 per Master Plan
export const DEFAULT_WEIGHTS: SignalWeights = {
  career_quality: 0.20,
  skills_depth: 0.22,
  jd_semantic_fit: 0.15,
  title_alignment: 0.15,
  experience_range: 0.10,
  behavioral_availability: 0.10,
  location_fit: 0.04,
  github_signal: 0.04,
};

export const CONSULTING_FIRMS = [
  'tcs', 'tata consultancy', 'infosys', 'wipro', 'accenture', 'cognizant', 
  'capgemini', 'hcl', 'tech mahindra', 'mphasis', 'ltimindtree', 'mindtree', 
  'genpact', 'deloitte', 'ey', ' Ernst & Young', 'pwc', 'kpmg', 'cognizant technology solutions'
];

export const PREFERRED_CITIES = [
  'pune', 'noida', 'bengaluru', 'bangalore', 'hyderabad', 'mumbai',
  'delhi', 'gurgaon', 'gurugram', 'new delhi', 'ncr', 'faridabad'
];

export const CORE_REQUIRED_SKILLS: Record<string, string[]> = {
  embeddings: ['Sentence Transformers', 'sentence-transformers', 'OpenAI Embeddings', 'BGE', 'E5', 'text embeddings', 'dense retrieval', 'dense vector similarity'],
  vector_dbs: ['Pinecone', 'Weaviate', 'Qdrant', 'Milvus', 'FAISS', 'OpenSearch', 'Elasticsearch', 'Chroma', 'PGVector', 'vector search'],
  python: ['Python', 'Python 3', 'FastAPI', 'Flask', 'Django'],
  eval_metrics: ['NDCG', 'MRR', 'MAP', 'ranking evaluation', 'A/B testing', 'search metrics', 'online evaluation', 'evaluation framework'],
  retrieval_systems: ['RAG', 'hybrid retrieval', 'BM25', 'semantic search', 'information retrieval', 'vector similarity', 'retrieval-augmented generation']
};

export const NICE_TO_HAVE_SKILLS: Record<string, string[]> = {
  llm_finetuning: ['LoRA', 'QLoRA', 'PEFT', 'fine-tuning LLMs', 'fine-tuning', 'parameter efficient fine-tuning'],
  ltr_models: ['LambdaMART', 'XGBoost ranking', 'learning to rank', 'LTR', 'RankNet'],
  ml_frameworks: ['PyTorch', 'TensorFlow', 'Hugging Face', 'Transformers', 'scikit-learn', 'NumPy', 'Pandas'],
  mlops: ['MLflow', 'Weights & Biases', 'BentoML', 'Triton', 'MLOps', 'Docker', 'Kubernetes'],
  distributed: ['Kafka', 'Spark', 'distributed systems', 'Redis', 'AWS', 'GCP']
};

export const DISQUALIFYING_DOMAINS = [
  'computer vision', 'speech recognition', 'robotics', 'image classification', 
  'object detection', 'text-to-speech', 'tts', 'lidar', 'autonomous vehicles'
];
