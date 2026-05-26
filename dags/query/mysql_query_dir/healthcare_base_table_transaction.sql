-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mysql-db:3306
-- Generation Time: May 14, 2026 at 02:55 PM
-- Server version: 8.0.45
-- PHP Version: 8.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `healthcare`
--

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

use `transaction_db`;

DROP TABLE IF EXISTS `transaction`;

CREATE TABLE `transaction` (
  `year` int NOT NULL,
  `month` int NOT NULL,
  `id` bigint NOT NULL,
  `hospital_id` int NOT NULL,
  `hospital_type` enum('Primary','Secondary','Tertiary','') NOT NULL,
  `ownership` enum('Public','NGO','Private','') NOT NULL,
  `region` enum('East','North','West','South','') NOT NULL,
  `urban_rural` enum('Urban','Rural','') NOT NULL,
  `service_category` enum('Outpatient','Diagnostics','Rehabilitation','Emergency','') NOT NULL,
  `patient_volume` float NOT NULL,
  `avg_daily_visits` float NOT NULL,
  `bed_occupancy_rate` float NOT NULL,
  `staff_to_patient_ratio` float NOT NULL,
  `resource_utilization_rate` float NOT NULL,
  `avg_wait_time_minutes` float NOT NULL,
  `service_delay_rate` float NOT NULL,
  `appointment_backlog` float NOT NULL,
  `avg_service_cost` float NOT NULL,
  `cost_per_patient` float NOT NULL,
  `operational_efficiency_index` float NOT NULL,
  `readmission_rate` float NOT NULL,
  `service_completion_rate` float NOT NULL,
  `complaint_rate` float NOT NULL,
  `followup_adherence_rate` float NOT NULL,
  `latent_accessibility_score` float NOT NULL,
  `latent_efficiency_score` float NOT NULL,
  `semantic_cluster_id` int NOT NULL,
  `semantic_noise_level` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;
COMMIT;

ALTER TABLE `transaction` ADD INDEX `idx_transaction_region` (`region`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
