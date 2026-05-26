
CREATE TABLE transaction_db.transaction_raw (
    `year` UInt16 ,
    `month` UInt8 ,
    `id` UInt64 ,
    `hospital_id` UInt64 ,
    `hospital_type` LowCardinality(String),
    `ownership` LowCardinality(String),
    `region` LowCardinality(String),
    `urban_rural` LowCardinality(String),
    `service_category` LowCardinality(String),
    `patient_volume` Nullable(Float32) ,
    `avg_daily_visits` Nullable(Float32) ,
    `bed_occupancy_rate` Nullable(Float32),
    `staff_to_patient_ratio` Nullable(Float32),
    `resource_utilization_rate` Nullable(Float32) ,
    `avg_wait_time_minutes` Nullable(Float32) ,
    `service_delay_rate` Nullable(Float32) ,
    `appointment_backlog` Nullable(Float32) ,
    `avg_service_cost` Nullable(Float32) ,
    `cost_per_patient` Nullable(Float32) ,
    `operational_efficiency_index` Nullable(Float32) ,
    `readmission_rate` Nullable(Float32) ,
    `service_completion_rate` Nullable(Float32) ,
    `complaint_rate` Nullable(Float32) ,
    `followup_adherence_rate` Nullable(Float32) ,
    `latent_accessibility_score` Nullable(Float32) ,
    `latent_efficiency_score` Nullable(Float32) ,
    `semantic_cluster_id` UInt32 ,
    `semantic_noise_level` Nullable(Float32) 
) ENGINE=SummingMergeTree()
PRIMARY KEY (id)
PARTITION BY tuple()
ORDER BY (id, year, month, region, ownership, service_category);
