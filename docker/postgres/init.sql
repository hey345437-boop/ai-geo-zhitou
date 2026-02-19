-- GEO Optimizer Database Initialization

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Brands table
CREATE TABLE IF NOT EXISTS brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    canonical_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    aliases TEXT[],
    website_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Probe jobs table
CREATE TABLE IF NOT EXISTS probe_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id),
    keywords TEXT[],
    frequency VARCHAR(20),
    status VARCHAR(20),
    last_run_at TIMESTAMP,
    next_run_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Probe data points table
CREATE TABLE IF NOT EXISTS probe_data_points (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID REFERENCES probe_jobs(id),
    brand_id UUID REFERENCES brands(id),
    keyword TEXT,
    llm_engine VARCHAR(50),
    is_mentioned BOOLEAN,
    position INTEGER,
    response_text TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_brand_timestamp ON probe_data_points(brand_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_llm_engine ON probe_data_points(llm_engine);
CREATE INDEX IF NOT EXISTS idx_probe_job ON probe_data_points(job_id);

-- Experiments table
CREATE TABLE IF NOT EXISTS experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    hypothesis TEXT,
    treatment_variant_id UUID,
    control_variant_id UUID,
    status VARCHAR(20),
    start_date DATE,
    end_date DATE,
    sample_size INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content variants table
CREATE TABLE IF NOT EXISTS content_variants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID REFERENCES experiments(id),
    content TEXT,
    variant_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Visibility reports table
CREATE TABLE IF NOT EXISTS visibility_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(100),
    report_date DATE,
    maturity_level VARCHAR(20),
    brand_shares JSONB,
    cognitive_gaps JSONB,
    strategies JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id),
    type VARCHAR(50),
    priority VARCHAR(20),
    title TEXT,
    description TEXT,
    action TEXT,
    expected_impact FLOAT,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert sample data
INSERT INTO brands (name, canonical_name, category, aliases) VALUES
    ('Sample Brand', 'Sample Brand', 'Technology', ARRAY['SampleBrand', 'Sample'])
ON CONFLICT DO NOTHING;
