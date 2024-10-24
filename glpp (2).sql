-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 22, 2024 at 10:28 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `glpp`
--

-- --------------------------------------------------------

--
-- Table structure for table `achats`
--

CREATE TABLE `achats` (
  `id_achat` int(11) NOT NULL,
  `code_demande` int(11) NOT NULL,
  `code_article` varchar(20) NOT NULL,
  `libelle_article` varchar(255) NOT NULL,
  `quantite` int(11) NOT NULL,
  `prix_achat` decimal(6,0) NOT NULL,
  `emplacement` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `fournisseur` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `achats`
--

INSERT INTO `achats` (`id_achat`, `code_demande`, `code_article`, `libelle_article`, `quantite`, `prix_achat`, `emplacement`, `date`, `fournisseur`) VALUES
(1, 1, '0', 'Adhésif', 1, 0, 'sahel', '2024-10-21 14:13:10', 'x'),
(2, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:16:29', 'xxvsd'),
(3, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:21:57', 'xxvsd'),
(4, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:22:06', 'xxvsd'),
(5, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:23:16', 'xxvsd'),
(6, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:23:44', 'xxvsd'),
(7, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:26:48', 'xxvsd'),
(8, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:26:53', 'xxvsd'),
(9, 2, 'ADF001', 'Adhésif', 5, 0, 'sahel', '2024-10-22 15:26:57', ''),
(10, 1, 'test', 'Article 1', 10, 1, 'sahel', '2024-10-22 15:30:34', 'xxvsd');

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id_article` int(11) NOT NULL,
  `code_article` varchar(11) NOT NULL,
  `libelle_article` varchar(255) NOT NULL,
  `prix_achat` double NOT NULL,
  `emplacement` varchar(255) NOT NULL,
  `quantite` int(11) NOT NULL,
  `fournisseur` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `quantite_min` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id_article`, `code_article`, `libelle_article`, `prix_achat`, `emplacement`, `quantite`, `fournisseur`, `date`, `quantite_min`) VALUES
(5, 'SCHTLA', 'Sachet de caisse laser', 2, 'Sahel', 1, '', '2024-10-15 15:08:43', 10),
(6, 'FICR01', 'Fiche Identification Caisse Rose', 7, 'Sahel', 3, '', '2024-10-15 15:08:43', 10),
(7, 'SSMRM', 'Sachet SM & RM', 1, 'Sahel', 5, '', '2024-10-15 15:08:43', 10),
(8, 'ADF001', 'Adhésif', 3, 'Sahel', 2, '', '2024-10-15 15:08:43', 10),
(9, 'RIDMAX', 'Ruban Impression Datamax', 4, 'Sahel', 10, '', '2024-10-15 15:08:43', 10),
(10, 'PLMBJN', 'Plombs jaune', 6, 'Sahel', 8, '', '2024-10-15 15:08:43', 10),
(11, 'PLMBBL', 'Plombs bleu', 2, 'Sahel', 21, '', '2024-10-15 15:08:43', 10),
(12, 'SCHTNR', 'Sachet noir', 1, 'Sahel', 30, '', '2024-10-15 15:08:43', 10),
(13, 'SCOTTR', 'Scotch transparent', 1, 'Sahel', 20, 'Sahel', '2024-10-15 15:08:43', 10),
(14, 'SCOTJN', 'Scotch jaune', 1, 'Sahel', 20, '', '2024-10-15 15:08:43', 10),
(15, 'SCOTMR', 'Scotch marron', 1, 'Sahel', 20, '', '2024-10-15 15:08:43', 10),
(16, 'SCOTRG', 'Scotch rouge', 1, 'Sahel', 20, '', '2024-10-15 15:08:43', 10),
(17, 'SCHTSM', 'Sachet stampa', 2, 'Sahel', 10, '', '2024-10-15 15:08:43', 10),
(18, 'FILRET', 'Fil retirable', 1, 'Sahel', 3, '', '2024-10-15 15:08:43', 10),
(19, 'ETQDFC', 'Étiquette défective', 1, 'Sahel', 20, '', '2024-10-15 15:08:43', 10),
(20, 'ETQSTK', 'Étiquettes stock', 1, 'Sahel', 15, '', '2024-10-15 15:08:43', 10),
(21, 'RLRMPK', 'Roulo stampa piking', 1, 'Sahel', 10, '', '2024-10-15 15:08:43', 10),
(22, 'RURMPK', 'Ruban stampa piking', 1, 'Sahel', 20, '', '2024-10-18 07:44:30', 10),
(23, 'SCHTPB', 'Sachet poubelle', 1, 'Sahel', 25, '', '2024-10-15 15:08:43', 10),
(24, 'PLB001', 'Plomb Blanc', 5, 'Sahel', 10, '', '2024-10-15 15:08:43', 10),
(26, 'FICB01', 'Fiche Identification Caisse Bleu', 2, 'Sahel', 4, '', '2024-10-15 15:08:43', 10),
(27, 'PALETB', 'Palette Bois', 8, 'Sahel', 5, '', '2024-10-15 15:08:43', 10);

-- --------------------------------------------------------

--
-- Table structure for table `counter_demande_vente`
--

CREATE TABLE `counter_demande_vente` (
  `id` int(11) NOT NULL,
  `total_count` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `counter_table`
--

CREATE TABLE `counter_table` (
  `count_value` int(11) DEFAULT 0,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `counter_table`
--

INSERT INTO `counter_table` (`count_value`, `id`) VALUES
(2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `demande_d_achat`
--

CREATE TABLE `demande_d_achat` (
  `code_demande` int(11) NOT NULL,
  `code_article` varchar(11) NOT NULL,
  `libelle_article` varchar(255) NOT NULL,
  `quantite` int(11) NOT NULL,
  `emplacement` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `demandeur` varchar(255) NOT NULL,
  `etat` int(11) DEFAULT NULL,
  `reception` int(11) NOT NULL,
  `fournisseur` varchar(50) DEFAULT NULL,
  `prix_achat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `demande_d_achat`
--

INSERT INTO `demande_d_achat` (`code_demande`, `code_article`, `libelle_article`, `quantite`, `emplacement`, `date`, `demandeur`, `etat`, `reception`, `fournisseur`, `prix_achat`) VALUES
(1, 'test', 'Article 1', 10, 'sahel', '2024-10-22 14:23:46', 'User1', 0, 0, 'xxvsd', 1),
(2, 'ADF001', 'Adhésif', 5, 'sahel', '2024-10-22 19:18:27', 'User2', 1, 0, '', 0),
(3, 'ADF001', 'Adhésif', 20, 'gafsa', '2024-10-22 15:08:10', 'user', 0, 1, NULL, 100),
(28, '0', 'test', 4, 'sahel', '2024-10-22 14:57:24', 'user', 0, 1, NULL, 2),
(38, 'SCHTLA', 'Sachet de caisse laser	', 5, 'sahel', '2024-10-22 14:57:24', 'user', 0, 1, NULL, 2),
(39, 'ADF001', 'Adhesif', 100, 'sahel', '2024-10-22 15:06:49', 'user', 0, 1, NULL, 1),
(40, 'PLMBBL', 'Plombs bleu', 10, 'sahel', '2024-10-22 18:20:29', 'user', 1, 0, NULL, NULL);

--
-- Triggers `demande_d_achat`
--
DELIMITER $$
CREATE TRIGGER `after_demande_d_achat_insert` AFTER INSERT ON `demande_d_achat` FOR EACH ROW BEGIN
    IF NEW.etat = 1 THEN
        UPDATE counter_table SET count_value = count_value + 1;
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_demande_d_achat_update` AFTER UPDATE ON `demande_d_achat` FOR EACH ROW BEGIN
    -- Increment the count if etat changes to 1
    IF NEW.etat = 1 AND OLD.etat <> 1 THEN
        UPDATE counter_table SET count_value = count_value + 1;
    -- Decrement the count if etat changes from 1 to something else
    ELSEIF OLD.etat = 1 AND NEW.etat <> 1 THEN
        UPDATE counter_table SET count_value = count_value - 1;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `demande_vente`
--

CREATE TABLE `demande_vente` (
  `code_demande` int(11) NOT NULL,
  `code_article` varchar(50) NOT NULL,
  `libelle_article` varchar(20) NOT NULL,
  `quantite` int(11) NOT NULL,
  `prix_vente` decimal(6,3) DEFAULT NULL,
  `emplacement` varchar(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `demandeur` varchar(20) NOT NULL,
  `vers` varchar(20) NOT NULL,
  `commande` varchar(20) NOT NULL,
  `etat` int(11) NOT NULL,
  `reception` int(11) NOT NULL,
  `Commentaire` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `demande_vente`
--

INSERT INTO `demande_vente` (`code_demande`, `code_article`, `libelle_article`, `quantite`, `prix_vente`, `emplacement`, `date`, `demandeur`, `vers`, `commande`, `etat`, `reception`, `Commentaire`) VALUES
(1, 'ADF001', 'Adesive', 2, 1.200, 'sahel', '2024-10-22 15:29:48', 'zina', '[value-8]', 'sqdvsdv10', 0, 0, ''),
(2, 'SCHTNR', 'Sachet noir', 5, 0.000, 'sahel', '2024-10-22 19:18:52', 'user1', 'bsp', '', 1, 0, ''),
(3, 'ART123', 'Adhésif', 10, 0.000, 'sahel', '2024-10-22 20:25:21', 'user', 'atelier1', 'CMD001', 0, 1, ''),
(4, 'ADF001', 'Adhésif', 10, 0.000, '', '2024-10-22 16:07:10', 'user', 'bsp', 'x', 0, 1, '');

-- --------------------------------------------------------

--
-- Table structure for table `fournisseur`
--

CREATE TABLE `fournisseur` (
  `id_fournisseur` int(11) NOT NULL,
  `nom_fournisseur` varchar(20) NOT NULL,
  `matricule_fiscale` varchar(50) DEFAULT NULL,
  `addresse` varchar(20) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fournisseur`
--

INSERT INTO `fournisseur` (`id_fournisseur`, `nom_fournisseur`, `matricule_fiscale`, `addresse`, `telephone`) VALUES
(1, 'x', 'xxxxx', 'xx', 'xx'),
(2, 'a', '12345', 'aaaa', '12345678');

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `id_history` int(11) NOT NULL,
  `code_demande` int(11) DEFAULT NULL,
  `code_article` varchar(50) DEFAULT NULL,
  `libelle_article` varchar(255) DEFAULT NULL,
  `quantite` int(11) DEFAULT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `fournisseur` varchar(20) DEFAULT NULL,
  `emplacement` varchar(20) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  `usine` varchar(20) DEFAULT NULL,
  `date_action` timestamp NULL DEFAULT current_timestamp(),
  `date_approuver_demande` timestamp NULL DEFAULT current_timestamp(),
  `date_reception` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`id_history`, `code_demande`, `code_article`, `libelle_article`, `quantite`, `prix`, `fournisseur`, `emplacement`, `action`, `user`, `details`, `usine`, `date_action`, `date_approuver_demande`, `date_reception`) VALUES
(18, 3, NULL, NULL, NULL, 5.00, 'test', NULL, 'Demande d\'achat approuvée', 'administrateur', NULL, NULL, NULL, '2024-10-18 14:33:06', NULL),
(21, 38, 'SCHTLA', 'Sachet de caisse laser	', 5, NULL, NULL, 'sahel', 'Création de demande d\'achat', 'user', 'Demande créée', 'sahel', '2024-10-19 07:46:07', '2024-10-19 07:46:07', '2024-10-19 07:46:07'),
(22, 39, 'ADF001', 'Adhesif', 100, NULL, NULL, 'sahel', 'Création de demande d\'achat', 'user', 'Demande créée', 'sahel', '2024-10-19 10:12:36', '2024-10-19 10:12:36', '2024-10-19 10:12:36'),
(23, 39, NULL, NULL, NULL, 1.00, 'x', NULL, 'Demande d\'achat approuvée', 'achat', NULL, NULL, NULL, '2024-10-19 11:13:20', NULL),
(24, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Article Vendue', 'usersahel', 'L\'article correspondant à la demande a été vendue', NULL, NULL, NULL, '2024-10-22 12:41:22'),
(25, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Article Vendue', 'usersahel', 'L\'article correspondant à la demande a été vendue', NULL, NULL, NULL, '2024-10-22 15:16:29'),
(26, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Article reçu', 'usersahel', 'L\'article correspondant à la demande a été reçu en magasin', NULL, NULL, NULL, '2024-10-22 15:21:57'),
(27, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Article reçu', 'usersahel', 'L\'article correspondant à la demande a été reçu en magasin', NULL, NULL, NULL, '2024-10-22 15:22:06'),
(28, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Article reçu', 'usersahel', 'L\'article correspondant à la demande a été reçu en magasin', NULL, NULL, NULL, '2024-10-22 15:23:16'),
(29, 1, NULL, NULL, NULL, NULL, NULL, NULL, 'Article Vendue', 'usersahel', 'L\'article correspondant à la demande a été vendue', NULL, NULL, NULL, '2024-10-22 15:29:48'),
(30, 28, NULL, NULL, NULL, 2.00, 'aa', NULL, 'Demande d\'achat approuvée', 'achat', NULL, NULL, NULL, '2024-10-22 15:58:13', NULL),
(31, 38, NULL, NULL, NULL, 2.00, 'zrbebre', NULL, 'Demande d\'achat approuvée', 'achat', NULL, NULL, NULL, '2024-10-22 15:58:22', NULL),
(32, 39, NULL, NULL, NULL, 1.00, 'x', NULL, 'Demande d\'achat approuvée', 'achat', NULL, NULL, NULL, '2024-10-22 16:07:22', NULL),
(33, 40, 'PLMBBL', 'Plombs bleu', 10, NULL, NULL, 'sahel', 'Création de demande d\'achat', 'user', 'Demande créée', 'sahel', '2024-10-22 18:20:29', '2024-10-22 18:20:29', '2024-10-22 18:20:29');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `emplacement` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `emplacement`, `role`) VALUES
(3, 'administrateur', 'pbkdf2:sha256:600000$LCbgBPjqsqUEIJ9R$4831c81f21d20aa4a6d3480e81b2d86601af90acadd6d83c5cc25d4f474ffb1f', 'sahel', 'admin'),
(5, 'achat', 'pbkdf2:sha256:600000$m6IcEbYakPC0QC81$0735bfe44dcf4374d8bd185a6ede49dd01219be98a0063ef9010d111f4031a17', 'sahel', 'achat'),
(10, 'responsablesahel', 'pbkdf2:sha256:600000$rYAlohhAFzQVB5eP$41f2b16a06b72dc3fd62890c2bf98157c9327bbffa0a494d72a44bb92f0ded84', 'sahel', 'responsablesahel'),
(11, 'responsablegafsa', 'pbkdf2:sha256:600000$OIG1GsbXQv3xWSgn$b90b4fb52f34f33d4356c4a66fcb1e616b8d64849beccd85786b224819d376b4', 'gafsa', 'responsablegafsa'),
(12, 'responsablekasserine', 'pbkdf2:sha256:600000$6rBYHyE3LqdDcNaV$6b58024c16355333bc08264d7e686bca82e350030ce82220c75906c01e895e0e', 'kasserine', 'responsablekasserine'),
(13, 'manager', 'pbkdf2:sha256:600000$guZlEx09zwqqg8B7$d6a3b8fc6d1083a26f773e11b2b3cb78cceab8c831073f1ba3cf78f75aa81425', 'sahel', 'manager'),
(14, 'usergafsa', 'pbkdf2:sha256:600000$M4p0B5W10ptDdVEw$4ff62e6f5fe4e3aba3c40188588d9cf8db84fc9ba8dbc4674d264f2bd6415582', 'gafsa', 'user'),
(15, 'userkasserine', 'pbkdf2:sha256:600000$XXIzLYCqf4jDzd0Y$34ed05e664ceb2beb7bbb2cee4e3e723c8ef736951937e88e45a1d7b0d7cc3d2', 'kasserine', 'user'),
(16, 'usersahel', 'pbkdf2:sha256:600000$1L91f6UreBt4q265$6fb16b3d6c814d4375d746e531db8de30920454c333bc88bc38ba95c0bc9bcc1', 'sahel', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `usine`
--

CREATE TABLE `usine` (
  `id_usine` int(11) NOT NULL,
  `nom_usine` varchar(20) NOT NULL,
  `region` varchar(20) NOT NULL,
  `addresse` varchar(20) DEFAULT NULL,
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `etat` varchar(20) NOT NULL,
  `role` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usine`
--

INSERT INTO `usine` (`id_usine`, `nom_usine`, `region`, `addresse`, `latitude`, `longitude`, `telephone`, `etat`, `role`) VALUES
(2, 'sperenza', '', '', '', '', NULL, 'externe', ''),
(4, 'Mahdco', '', '', '', '', NULL, 'externe', ''),
(5, 'fethi comptage', '', '', '', '', NULL, 'interne', ''),
(6, 'borouz', '', '', '', '', NULL, 'externe', ''),
(7, 'chaine confection', '', '', '', '', NULL, 'interne', ''),
(10, 'EAS', '', '', '', '', NULL, 'externe', ''),
(12, 'brodland', '', '', '', '', NULL, 'externe', ''),
(14, 'starlette', '', '', '', '', NULL, 'externe', ''),
(15, 'export', '', '', '', '', NULL, 'interne', ''),
(17, 'trc', '', '', '', '', NULL, 'externe', ''),
(18, 'royaume', '', '', '', '', NULL, 'externe', ''),
(20, 'hamadi', '', '', '', '', NULL, 'interne', ''),
(23, 'dymtex', '', '', '', '', NULL, 'externe', ''),
(24, 'abasi', '', '', '', '', NULL, 'externe', ''),
(25, 'linatex', '', '', '', '', NULL, 'externe', ''),
(27, 'bha', '', '', '', '', NULL, 'externe', ''),
(28, 'defi', '', '', '', '', NULL, 'externe', ''),
(29, 'hamza comptage', '', '', '', '', NULL, 'interne', ''),
(30, 'primatex', '', '', '', '', NULL, 'externe', ''),
(31, 'teinture', '', '', '', '', NULL, '', ''),
(32, 'magasin tissu', '', '', '', '', NULL, '', ''),
(33, 'new baby', '', '', '', '', NULL, 'externe', ''),
(35, 'creation', '', '', '', '', NULL, 'externe', ''),
(36, 'racine', '', '', '', '', NULL, 'externe', ''),
(39, 'zina coupe', '', '', '', '', NULL, 'externe', ''),
(42, 'lobna stampa', '', '', '', '', NULL, '', ''),
(43, 'benetton Gafsa', '', '', '', '', NULL, '', ''),
(44, 'rayen', '', '', '', '', NULL, 'externe', ''),
(45, 'qualite stampa', '', '', '', '', NULL, '', ''),
(46, 'AFROTEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(49, 'A-TEX', 'gafsa', '', '34.4292', '8.7641', NULL, 'externe', ''),
(50, 'BIGATEX', 'gafsa', '', '34.4252', '8.7639', NULL, 'externe', ''),
(51, 'CREATEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(52, 'GSC', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(53, 'HAYTEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(54, 'IBCS RM', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(55, 'KHCF', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(56, 'MARNATEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(57, 'NEJIATEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(58, 'OLFATEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(59, 'benetton kasserine', 'kasserine', NULL, NULL, NULL, NULL, 'externe', NULL),
(60, 'STARTEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(61, 'WAJIHTEX', 'gafsa', '', '34.4230', '8.7753', NULL, 'externe', ''),
(63, 'AMISTEK', 'kasserine', '', '35.1472', '8.6543', NULL, '', ''),
(64, 'AZIZ', 'kasserine', '', '35.2012', '8.8394', NULL, '', ''),
(65, 'BAHA', 'kasserine', '', '35.2051', '8.5499', NULL, '', ''),
(66, 'BENATEX', 'kasserine', '', '35.2034', '8.7796', NULL, '', ''),
(67, 'BIS BRODLAND', 'kasserine', '', '35.2005', '8.8355', NULL, '', ''),
(68, 'CESAR', 'kasserine', '', '35.2060', '8.8684', NULL, '', ''),
(69, 'CHAHDTEXCF', 'kasserine', '', '35.2012', '8.8368', NULL, '', ''),
(70, 'CMKA', 'kasserine', '', '35.2004', '8.8586', NULL, '', ''),
(71, 'DHAHRI A', 'kasserine', '', '35.2010', '8.8294', NULL, '', ''),
(72, 'FERTEX', 'kasserine', '', '35.2211', '8.6548', NULL, '', ''),
(73, 'ISOMERAZE', 'kasserine', '', '35.2220', '8.6420', NULL, '', ''),
(74, 'LAAYOUNTEA', 'kasserine', '', '35.1540', '8.6263', NULL, '', ''),
(75, 'SUFFEITULA', 'kasserine', '', '35.1502', '8.6601', NULL, '', ''),
(76, 'TEX PRINT SM', 'kasserine', '', '35.2036', '8.7797', NULL, '', ''),
(77, 'VISCOSA CF', 'kasserine', '', '35.2034', '8.8660', NULL, '', ''),
(78, 'AH', 'sahel', '', '35.6823', '10.0495', NULL, '', ''),
(79, 'BABY', 'sahel', '', '35.6830', '10.0505', NULL, '', ''),
(80, 'BENTEX', 'sahel', '', '35.6753', '10.0768', NULL, '', ''),
(81, 'BHA', 'sahel', '', '35.6820', '10.0480', NULL, '', ''),
(82, 'BIT', 'sahel', '', '35.6758', '10.0713', NULL, '', ''),
(83, 'BRODLAND', 'sahel', '', '35.6742', '10.0915', NULL, '', ''),
(84, 'BSP', 'sahel', '', '35.7572', '10.9118', NULL, '', ''),
(86, 'CREATIONCF', 'sahel', '', '35.4235', '10.0672', NULL, '', ''),
(87, 'cyc', 'sahel', '', '35.6751', '10.0788', '', 'externe', ''),
(88, 'DEFI', 'sahel', '', '35.6867', '10.0492', NULL, '', ''),
(89, 'ENFAVETCF1', 'sahel', '', '35.4235', '10.0672', NULL, '', ''),
(90, 'ESCONFINT', 'sahel', '', '35.6750', '10.0910', NULL, '', ''),
(91, 'GNC', 'sahel', '', '35.6838', '10.0454', NULL, '', ''),
(92, 'IAS', 'sahel', '', '35.7724', '10.8322', NULL, '', ''),
(93, 'Lareine', 'sahel', '', '35.6822', '10.0468', NULL, '', ''),
(94, 'LEOMINORCF', 'sahel', '', '35.4120', '10.0824', NULL, '', ''),
(95, 'MARMA', 'sahel', '', '35.7594', '10.8144', NULL, '', ''),
(96, 'MENGIATEX', 'sahel', '', '35.6750', '10.0918', NULL, '', ''),
(97, 'NATEX', 'sahel', '', '35.6838', '10.0462', NULL, '', ''),
(98, 'SAGHATEX', 'sahel', '', '35.7750', '10.8200', NULL, '', ''),
(99, 'SIME', 'sahel', '', '35.4260', '10.0767', NULL, '', ''),
(100, 'SOREN', 'sahel', '', '35.6823', '10.0495', NULL, '', ''),
(101, 'TAROM', 'sahel', '', '35.6753', '10.0768', NULL, '', ''),
(102, 'TEXDRILL', 'sahel', '', '35.6750', '10.0910', NULL, '', ''),
(103, 'TG-BE', 'sahel', '', '35.6755', '10.0920', NULL, '', ''),
(104, 'VESTEX', 'sahel', '', '35.6750', '10.0918', NULL, '', ''),
(105, 'ZECE', 'sahel', '', '35.6823', '10.0495', NULL, '', ''),
(106, 'socaf', 'sahel', 'Ksour Essef', '35.661', '10.898', NULL, '', ''),
(107, 'sperenza', 'sahel', 'Ksour Essef', '35.661', '10.898', NULL, '', ''),
(108, 'cyc', 'sahel', 'Ksour Essef', '35.661', '10.898', NULL, '', ''),
(109, 'mahdco', 'sahel', 'Mahdia', '35.5045', '11.0602', NULL, '', ''),
(110, 'starlette', 'sahel', 'Sayada', '35.6785', '10.8838', NULL, '', ''),
(111, 'trc', 'sahel', 'El Masdour 5032', '35.6315', '10.8938', NULL, '', ''),
(112, 'AFROTEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, 'externe', ''),
(115, 'A-TEX', 'gafsa', NULL, '34.4292', '8.7641', NULL, 'externe', ''),
(116, 'BIGATEX', 'gafsa', NULL, '34.4252', '8.7639', NULL, 'externe', ''),
(117, 'CREATEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, 'externe', ''),
(119, 'HAYTEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, 'externe', ''),
(120, 'IBCS RM', 'gafsa', NULL, '34.4230', '8.7753', NULL, 'externe', ''),
(121, 'KHCF', 'gafsa', NULL, '34.4230', '8.7753', NULL, 'externe', ''),
(122, 'MARNATEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, '', ''),
(123, 'NEJIATEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, '', ''),
(124, 'OLFATEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, '', ''),
(125, 'STAR12 SM', 'gafsa', NULL, '34.4230', '8.7753', NULL, '', ''),
(126, 'STARTEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, '', ''),
(127, 'WAJIHTEX', 'gafsa', NULL, '34.4230', '8.7753', NULL, '', ''),
(128, 'AMEN', 'kasserine', NULL, '35.1650', '8.8693', NULL, '', ''),
(129, 'AMISTEK', 'kasserine', NULL, '35.1472', '8.6543', NULL, '', ''),
(130, 'AZIZ', 'kasserine', NULL, '35.2012', '8.8394', NULL, '', ''),
(131, 'BAHA', 'kasserine', NULL, '35.2051', '8.5499', NULL, '', ''),
(132, 'BENATEX', 'kasserine', NULL, '35.2034', '8.7796', NULL, '', ''),
(133, 'BIS BRODLAND', 'kasserine', NULL, '35.2005', '8.8355', NULL, '', ''),
(134, 'CESAR', 'kasserine', NULL, '35.2060', '8.8684', NULL, '', ''),
(135, 'CHAHDTEXCF', 'kasserine', NULL, '35.2012', '8.8368', NULL, '', ''),
(136, 'CMKA', 'kasserine', NULL, '35.2004', '8.8586', NULL, '', ''),
(137, 'DHAHRI A', 'kasserine', NULL, '35.2010', '8.8294', NULL, '', ''),
(138, 'FERTEX', 'kasserine', NULL, '35.2211', '8.6548', NULL, '', ''),
(139, 'ISOMERAZE', 'kasserine', NULL, '35.2220', '8.6420', NULL, '', ''),
(140, 'LAAYOUNTEA', 'kasserine', NULL, '35.1540', '8.6263', NULL, '', ''),
(141, 'SUFFEITULA', 'kasserine', NULL, '35.1502', '8.6601', NULL, '', ''),
(142, 'TEX PRINT SM', 'kasserine', NULL, '35.2036', '8.7797', NULL, '', ''),
(143, 'VISCOSA CF', 'kasserine', NULL, '35.2034', '8.8660', NULL, '', ''),
(144, 'AH', 'sahel', NULL, '35.6823', '10.0495', NULL, '', ''),
(145, 'BABY', 'sahel', NULL, '35.6830', '10.0505', NULL, '', ''),
(146, 'BENTEXA', 'sahel', NULL, '35.6753', '10.0768', NULL, '', ''),
(147, 'BHA', 'sahel', NULL, '35.6820', '10.0480', NULL, '', ''),
(148, 'BIT', 'sahel', NULL, '35.6758', '10.0713', NULL, '', ''),
(149, 'BRODLAND', 'sahel', NULL, '35.6742', '10.0915', NULL, '', ''),
(150, 'BSP RM', 'sahel', NULL, '35.7572', '10.9118', NULL, '', ''),
(151, 'BSP SM', 'sahel', NULL, '35.7572', '10.9118', NULL, '', ''),
(152, 'CREATIONCF', 'sahel', NULL, '35.4235', '10.0672', NULL, '', ''),
(153, 'CYC', 'sahel', NULL, '35.6751', '10.0788', NULL, '', ''),
(154, 'DEFI', 'sahel', NULL, '35.6867', '10.0492', NULL, '', ''),
(155, 'ENFAVETCF1', 'sahel', NULL, '35.4235', '10.0672', NULL, '', ''),
(156, 'ESCONFINT', 'sahel', NULL, '35.6750', '10.0910', NULL, '', ''),
(157, 'GNC-EXPORT', 'sahel', NULL, '35.6838', '10.0454', NULL, '', ''),
(158, 'IAS SM', 'sahel', NULL, '35.7724', '10.8322', NULL, '', ''),
(159, 'L’areine', 'sahel', NULL, '35.6822', '10.0468', NULL, '', ''),
(160, 'LEOMINORCF', 'sahel', NULL, '35.4120', '10.0824', NULL, '', ''),
(161, 'MARMA', 'sahel', NULL, '35.7594', '10.8144', NULL, '', ''),
(162, 'MENGIATEX', 'sahel', NULL, '35.6750', '10.0918', NULL, '', ''),
(163, 'NATEX', 'sahel', NULL, '35.6838', '10.0462', NULL, '', ''),
(164, 'SAGHATEX', 'sahel', NULL, '35.7750', '10.8200', NULL, '', ''),
(165, 'SIME', 'sahel', NULL, '35.4260', '10.0767', NULL, '', ''),
(166, 'SOREN', 'sahel', NULL, '35.6823', '10.0495', NULL, '', ''),
(167, 'TAROM', 'sahel', NULL, '35.6753', '10.0768', NULL, '', ''),
(168, 'TEXDRILL', 'sahel', NULL, '35.6750', '10.0910', NULL, '', ''),
(169, 'TG-BE', 'sahel', NULL, '35.6755', '10.0920', NULL, '', ''),
(170, 'VESTEX', 'sahel', NULL, '35.6750', '10.0918', NULL, '', ''),
(171, 'ZECE', 'sahel', NULL, '35.6823', '10.0495', NULL, '', ''),
(172, 'socaf', 'sahel', 'Ksour Essef', '35.661', '10.898', NULL, '', ''),
(173, 'sperenza', 'sahel', 'Ksour Essef', '35.661', '10.898', NULL, '', ''),
(174, 'cyc', 'sahel', 'Ksour Essef', '35.661', '10.898', NULL, '', ''),
(175, 'mahdco', 'sahel', 'Mahdia', '35.5045', '11.0602', NULL, '', ''),
(176, 'starlette', 'sahel', 'Sayada', '35.6785', '10.8838', NULL, '', ''),
(177, 'trc', 'sahel', 'El Masdour 5032', '35.6315', '10.8938', NULL, '', ''),
(178, 'benetton kasserine', 'kasserine', '', '', '', '', 'interne', '');

-- --------------------------------------------------------

--
-- Table structure for table `ventes`
--

CREATE TABLE `ventes` (
  `id_vente` int(11) NOT NULL,
  `code_demande` int(11) DEFAULT NULL,
  `code_article` varchar(20) DEFAULT NULL,
  `libelle_article` varchar(20) DEFAULT NULL,
  `quantite` int(11) DEFAULT NULL,
  `prix_vente` decimal(6,3) DEFAULT NULL,
  `emplacement` varchar(20) DEFAULT NULL,
  `vers` varchar(20) DEFAULT NULL,
  `demandeur` varchar(20) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ventes`
--

INSERT INTO `ventes` (`id_vente`, `code_demande`, `code_article`, `libelle_article`, `quantite`, `prix_vente`, `emplacement`, `vers`, `demandeur`, `date`) VALUES
(1, 1, '1', 'test', 1, 1.000, 'test', 'x', NULL, '2024-10-16 15:40:52'),
(3, 1, 'ADF001', 'Adesive', 2, 0.000, 'sahel', '[value-8]', 'zina', '2024-10-22 12:41:22'),
(4, 1, 'ADF001', 'Adesive', 2, 1.200, 'sahel', '[value-8]', 'zina', '2024-10-22 15:29:48');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `achats`
--
ALTER TABLE `achats`
  ADD PRIMARY KEY (`id_achat`);

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id_article`);

--
-- Indexes for table `counter_demande_vente`
--
ALTER TABLE `counter_demande_vente`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `counter_table`
--
ALTER TABLE `counter_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `demande_d_achat`
--
ALTER TABLE `demande_d_achat`
  ADD PRIMARY KEY (`code_demande`);

--
-- Indexes for table `demande_vente`
--
ALTER TABLE `demande_vente`
  ADD PRIMARY KEY (`code_demande`);

--
-- Indexes for table `fournisseur`
--
ALTER TABLE `fournisseur`
  ADD PRIMARY KEY (`id_fournisseur`);

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id_history`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `usine`
--
ALTER TABLE `usine`
  ADD PRIMARY KEY (`id_usine`);

--
-- Indexes for table `ventes`
--
ALTER TABLE `ventes`
  ADD PRIMARY KEY (`id_vente`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `achats`
--
ALTER TABLE `achats`
  MODIFY `id_achat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id_article` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `counter_demande_vente`
--
ALTER TABLE `counter_demande_vente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `counter_table`
--
ALTER TABLE `counter_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `demande_d_achat`
--
ALTER TABLE `demande_d_achat`
  MODIFY `code_demande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `demande_vente`
--
ALTER TABLE `demande_vente`
  MODIFY `code_demande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `fournisseur`
--
ALTER TABLE `fournisseur`
  MODIFY `id_fournisseur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id_history` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `usine`
--
ALTER TABLE `usine`
  MODIFY `id_usine` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=189;

--
-- AUTO_INCREMENT for table `ventes`
--
ALTER TABLE `ventes`
  MODIFY `id_vente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
