-- PostgreSQL Migration Script
-- Generated from phpMyAdmin MySQL Dump Conversion

-- --------------------------------------------------------
-- 1. Create Custom ENUM Types
-- --------------------------------------------------------
-- Note: PostgreSQL enums cannot contain empty strings '' directly as an identifier 
-- without quotes, so they are wrapped in standard single quotes.

DROP TABLE IF EXISTS "transaction";
DROP TABLE IF EXISTS "transaction_east";
DROP TABLE IF EXISTS "transaction_north";
DROP TABLE IF EXISTS "transaction_west";
DROP TABLE IF EXISTS "transaction_south";

DROP TYPE IF EXISTS hospital_type_enum;
DROP TYPE IF EXISTS ownership_enum;
DROP TYPE IF EXISTS region_enum;
DROP TYPE IF EXISTS urban_rural_enum;
DROP TYPE IF EXISTS service_category_enum;

CREATE TYPE hospital_type_enum AS ENUM ('Primary', 'Secondary', 'Tertiary', '');
CREATE TYPE ownership_enum AS ENUM ('Public', 'NGO', 'Private', '');
CREATE TYPE region_enum AS ENUM ('East', 'North', 'West', 'South', '');
CREATE TYPE urban_rural_enum AS ENUM ('Urban', 'Rural', '');
CREATE TYPE service_category_enum AS ENUM ('Outpatient', 'Diagnostics', 'Rehabilitation', 'Emergency', '');

-- --------------------------------------------------------
-- 2. Table structure for table "transaction"
-- --------------------------------------------------------

CREATE TABLE "transaction" (
  -- BIGSERIAL handles both the bigint type and the AUTO_INCREMENT functionality automatically
  "year" INT NOT NULL,
  "month" INT NOT NULL,
  "id" BIGSERIAL PRIMARY KEY,
  "hospital_id" INT NOT NULL,
  "hospital_type" hospital_type_enum NOT NULL,
  "ownership" ownership_enum NOT NULL,
  "region" region_enum NOT NULL,
  "urban_rural" urban_rural_enum NOT NULL,
  "service_category" service_category_enum NOT NULL,
  -- MySQL 'float' maps to 'real' (single precision) or 'double precision' in Postgres
  "patient_volume" REAL NOT NULL,
  "avg_daily_visits" REAL NOT NULL,
  "bed_occupancy_rate" REAL NOT NULL,
  "staff_to_patient_ratio" REAL NOT NULL,
  "resource_utilization_rate" REAL NOT NULL,
  "avg_wait_time_minutes" REAL NOT NULL,
  "service_delay_rate" REAL NOT NULL,
  "appointment_backlog" REAL NOT NULL,
  "avg_service_cost" REAL NOT NULL,
  "cost_per_patient" REAL NOT NULL,
  "operational_efficiency_index" REAL NOT NULL,
  "readmission_rate" REAL NOT NULL,
  "service_completion_rate" REAL NOT NULL,
  "complaint_rate" REAL NOT NULL,
  "followup_adherence_rate" REAL NOT NULL,
  "latent_accessibility_score" REAL NOT NULL,
  "latent_efficiency_score" REAL NOT NULL,
  "semantic_cluster_id" INT NOT NULL,
  "semantic_noise_level" REAL NOT NULL
);