-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 01, 2024 at 02:00 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `myportofio_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `event_id` int(11) NOT NULL,
  `category` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `date` varchar(50) NOT NULL,
  `description` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `title` varchar(50) NOT NULL,
  `video_file` varchar(50) NOT NULL,
  `event_date` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`event_id`, `category`, `location`, `date`, `description`, `created_at`, `title`, `video_file`, `event_date`) VALUES
(1, 'male jeans', 'UBUNGO', '2024-08-01', 'mmmmmmmmmmmm', '2024-07-31 22:21:28', 'hhhhhhhhhh', '1a335649d721759bd9f4cf1d6bf46a8c.mp4', '2024-08-01'),
(3, 'LEARNING', 'UBUNGO', '', 'TEST', '2024-07-31 23:43:03', 'PHP DEVELOPER', 'df5974b13c5adbb679fb3953c0bd7f22.mp4', '2024-08-01'),
(4, 'JAVA DEVELOPMENT', 'MBEZI', '', 'TEST', '2024-07-31 23:43:46', 'SPRING BOOT DEVELOPMENT', 'd10df3d74066f96caacf0162d88239a7.mp4', '2024-08-15');

-- --------------------------------------------------------

--
-- Table structure for table `my_gallery`
--

CREATE TABLE `my_gallery` (
  `id` int(11) NOT NULL,
  `upload_photo` varchar(100) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `my_gallery`
--

INSERT INTO `my_gallery` (`id`, `upload_photo`, `description`, `created_at`) VALUES
(2, '3f931fe6d8b88fa5915775eb2d94e3ae.png', 'this is event one ', '2024-07-31 22:41:19'),
(3, '30a244e649924f9506a369f307103cd1.png', 'this s test two', '2024-07-31 23:34:56'),
(4, '4a5e5f8b063121f87eb7b069846074db.png', 'this is test four', '2024-07-31 23:35:11'),
(5, '19bcf36eb1846f4e98353b4fa22205de.png', 'this is test five', '2024-07-31 23:35:24');

-- --------------------------------------------------------

--
-- Table structure for table `my_projects`
--

CREATE TABLE `my_projects` (
  `project_id` int(11) NOT NULL,
  `category` varchar(50) NOT NULL,
  `zipped_file` varchar(50) NOT NULL,
  `technologies` varchar(50) NOT NULL,
  `language` varchar(50) NOT NULL,
  `database_used` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `my_projects`
--

INSERT INTO `my_projects` (`project_id`, `category`, `zipped_file`, `technologies`, `language`, `database_used`, `description`, `created_at`) VALUES
(2, 'Food ordering  system', '375053229c380e5b25aba3fc0d8fe699.zip', 'html5.css with bootstrap and javascript', 'php8.9', 'Mysql', 'for commercal purpose', '2024-07-31 21:30:03');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `uname` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(30) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `uname`, `password`, `role`, `created_at`) VALUES
(1, 'System admin', 'admin123@gmail.com', '3008476a9614994b2538c9faa1b7e808', 'admin', '2024-07-29 20:44:14');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`event_id`);

--
-- Indexes for table `my_gallery`
--
ALTER TABLE `my_gallery`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `my_projects`
--
ALTER TABLE `my_projects`
  ADD PRIMARY KEY (`project_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `my_gallery`
--
ALTER TABLE `my_gallery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `my_projects`
--
ALTER TABLE `my_projects`
  MODIFY `project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
