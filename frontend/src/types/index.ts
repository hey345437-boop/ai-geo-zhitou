// Core Types
export interface Brand {
  id: string;
  name: string;
  canonical_name: string;
  category: string;
  aliases: string[];
  website_url?: string;
  created_at: string;
  updated_at: string;
}

export interface VisibilityScore {
  overall: number;
  mention_rate: number;
  position_score: number;
  consistency: number;
  trend: number;
  citation_weighted?: number;
  competitive_ranking?: number;
}

export interface ProbeDataPoint {
  id: string;
  timestamp: string;
  brand: string;
  keyword: string;
  llm_engine: string;
  is_mentioned: boolean;
  position: number;
  response_text: string;
}

export interface VisibilityReport {
  id: string;
  category: string;
  report_date: string;
  maturity: 'low' | 'medium' | 'high';
  brand_shares: Record<string, number>;
  cognitive_gaps: CognitiveGap[];
  strategies: GEOStrategy[];
}

export interface CognitiveGap {
  topic: string;
  opportunity_score: number;
  current_leaders: string[];
  description: string;
}

export interface GEOStrategy {
  type: string;
  priority: 'low' | 'medium' | 'high';
  title: string;
  description: string;
  expected_impact: number;
}

export interface LLMEngine {
  id: string;
  name: string;
  provider: string;
  model: string;
  enabled: boolean;
}

export interface Question {
  id: string;
  text: string;
  intent: string;
  variants: string[];
  category: string;
}

export interface Recommendation {
  id: string;
  type: string;
  priority: 'low' | 'medium' | 'high';
  title: string;
  description: string;
  action: string;
  expected_impact: number;
  status: 'pending' | 'in_progress' | 'completed' | 'dismissed';
}

// API Response Types
export interface APIResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
