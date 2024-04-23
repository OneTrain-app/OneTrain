-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: MACCAUD_OLIVIER_INFO1X_FILMS_164_2023

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS Gomes_Jose_DEVA1A_OneTrain_2024;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS Gomes_Jose_DEVA1A_OneTrain_2024;

-- Utilisation de cette base de donnée

USE Gomes_Jose_DEVA1A_OneTrain_2024;
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : mar. 23 avr. 2024 à 08:35
-- Version du serveur : 10.6.17-MariaDB-1:10.6.17+maria~ubu2004
-- Version de PHP : 8.2.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `OneTrain`
--

-- --------------------------------------------------------

--
-- Structure de la table `T_Alertes`
--

DROP TABLE IF EXISTS `T_Alertes`;
CREATE TABLE `T_Alertes` (
  `ID_Alertes` int(11) NOT NULL,
  `Nom` varchar(255) NOT NULL,
  `ID_Evenements` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `T_Alertes`
--

INSERT INTO `T_Alertes` (`ID_Alertes`, `Nom`, `ID_Evenements`) VALUES
(1, 'Match contre payerne', 1);

-- --------------------------------------------------------

--
-- Structure de la table `T_Alertes_Evenements`
--

DROP TABLE IF EXISTS `T_Alertes_Evenements`;
CREATE TABLE `T_Alertes_Evenements` (
  `ID_Alertes_Evenements` int(11) NOT NULL,
  `FK_Alertes` int(11) DEFAULT NULL,
  `FK_Evenements` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `T_Commandes`
--

DROP TABLE IF EXISTS `T_Commandes`;
CREATE TABLE `T_Commandes` (
  `ID_Commandes` int(11) NOT NULL,
  `Date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Quantité` int(255) NOT NULL,
  `Nom_Acheteur` varchar(255) NOT NULL,
  `ID_Materiel` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `T_Commandes`
--

INSERT INTO `T_Commandes` (`ID_Commandes`, `Date`, `Quantité`, `Nom_Acheteur`, `ID_Materiel`) VALUES
(1, '2024-03-14 09:55:38', 21, 'André', 1);

-- --------------------------------------------------------

--
-- Structure de la table `T_Credentials`
--

DROP TABLE IF EXISTS `T_Credentials`;
CREATE TABLE `T_Credentials` (
  `ID_Credentials` int(11) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `T_Credentials`
--

INSERT INTO `T_Credentials` (`ID_Credentials`, `Email`, `Password`) VALUES
(1, 'gsdo@gmail.com', 'fsdfdfds');

-- --------------------------------------------------------

--
-- Structure de la table `T_Evenements`
--

DROP TABLE IF EXISTS `T_Evenements`;
CREATE TABLE `T_Evenements` (
  `ID_Evenements` int(255) NOT NULL,
  `Type_Evenements` varchar(255) NOT NULL,
  `Date` date NOT NULL,
  `Couleur` varchar(255) NOT NULL,
  `Endroit` varchar(255) NOT NULL,
  `Description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `T_Evenements`
--

INSERT INTO `T_Evenements` (`ID_Evenements`, `Type_Evenements`, `Date`, `Couleur`, `Endroit`, `Description`) VALUES
(1, 'Match', '2024-03-16', 'Rouge', 'Lucens', 'Match contre Payerne'),
(2, 'Entrainement', '2024-03-21', 'Bleu', 'Moudon', 'Entrainement 19h à Moudon'),
(3, 'Reunion', '2024-03-23', 'Vert', 'Lucens', 'Reunion avec le president');

-- --------------------------------------------------------

--
-- Structure de la table `T_Materiel`
--

DROP TABLE IF EXISTS `T_Materiel`;
CREATE TABLE `T_Materiel` (
  `ID_Materiel` int(255) NOT NULL,
  `Nom` varchar(255) NOT NULL,
  `Quantite` int(255) NOT NULL,
  `Description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `T_Materiel`
--

INSERT INTO `T_Materiel` (`ID_Materiel`, `Nom`, `Quantite`, `Description`) VALUES
(1, 'Ballon', 12, 'Ballon de football');

-- --------------------------------------------------------

--
-- Structure de la table `T_Personne`
--

DROP TABLE IF EXISTS `T_Personne`;
CREATE TABLE `T_Personne` (
  `ID_Personne` int(255) NOT NULL,
  `Nom` varchar(255) DEFAULT NULL,
  `Prenom` varchar(255) DEFAULT NULL,
  `ID_Role` int(3) DEFAULT NULL,
  `ID_Credentials` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `T_Personne_Credentials`
--

DROP TABLE IF EXISTS `T_Personne_Credentials`;
CREATE TABLE `T_Personne_Credentials` (
  `ID_Personne_Credentials` int(11) NOT NULL,
  `FK_Personne` int(11) DEFAULT NULL,
  `FK_Credentials` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `T_Personne_Role`
--

DROP TABLE IF EXISTS `T_Personne_Role`;
CREATE TABLE `T_Personne_Role` (
  `ID_Personne_Role` int(11) NOT NULL,
  `FK_Personne` int(11) DEFAULT NULL,
  `FK_Role` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `T_Role`
--

DROP TABLE IF EXISTS `T_Role`;
CREATE TABLE `T_Role` (
  `ID_Role` int(11) NOT NULL,
  `Permission` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Déchargement des données de la table `T_Role`
--

INSERT INTO `T_Role` (`ID_Role`, `Permission`) VALUES
(1, 'all'),
(2, 'View');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `T_Alertes`
--
ALTER TABLE `T_Alertes`
  ADD PRIMARY KEY (`ID_Alertes`),
  ADD KEY `ID_Evenements` (`ID_Evenements`);

--
-- Index pour la table `T_Alertes_Evenements`
--
ALTER TABLE `T_Alertes_Evenements`
  ADD PRIMARY KEY (`ID_Alertes_Evenements`),
  ADD KEY `FK_Alertes` (`FK_Alertes`),
  ADD KEY `FK_Evenements` (`FK_Evenements`);

--
-- Index pour la table `T_Commandes`
--
ALTER TABLE `T_Commandes`
  ADD PRIMARY KEY (`ID_Commandes`),
  ADD KEY `ID_Materiel` (`ID_Materiel`);

--
-- Index pour la table `T_Credentials`
--
ALTER TABLE `T_Credentials`
  ADD PRIMARY KEY (`ID_Credentials`);

--
-- Index pour la table `T_Evenements`
--
ALTER TABLE `T_Evenements`
  ADD PRIMARY KEY (`ID_Evenements`);

--
-- Index pour la table `T_Materiel`
--
ALTER TABLE `T_Materiel`
  ADD PRIMARY KEY (`ID_Materiel`);

--
-- Index pour la table `T_Personne`
--
ALTER TABLE `T_Personne`
  ADD PRIMARY KEY (`ID_Personne`),
  ADD KEY `T_Personne_ibfk_1` (`ID_Credentials`),
  ADD KEY `ID_Role` (`ID_Role`);

--
-- Index pour la table `T_Personne_Credentials`
--
ALTER TABLE `T_Personne_Credentials`
  ADD PRIMARY KEY (`ID_Personne_Credentials`),
  ADD KEY `FK_Credentials` (`FK_Credentials`),
  ADD KEY `FK_Personne` (`FK_Personne`);

--
-- Index pour la table `T_Personne_Role`
--
ALTER TABLE `T_Personne_Role`
  ADD PRIMARY KEY (`ID_Personne_Role`),
  ADD KEY `FK_Personne` (`FK_Personne`),
  ADD KEY `FK_Role` (`FK_Role`);

--
-- Index pour la table `T_Role`
--
ALTER TABLE `T_Role`
  ADD PRIMARY KEY (`ID_Role`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `T_Alertes`
--
ALTER TABLE `T_Alertes`
  MODIFY `ID_Alertes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `T_Alertes_Evenements`
--
ALTER TABLE `T_Alertes_Evenements`
  MODIFY `ID_Alertes_Evenements` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `T_Commandes`
--
ALTER TABLE `T_Commandes`
  MODIFY `ID_Commandes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `T_Credentials`
--
ALTER TABLE `T_Credentials`
  MODIFY `ID_Credentials` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `T_Evenements`
--
ALTER TABLE `T_Evenements`
  MODIFY `ID_Evenements` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `T_Materiel`
--
ALTER TABLE `T_Materiel`
  MODIFY `ID_Materiel` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `T_Personne`
--
ALTER TABLE `T_Personne`
  MODIFY `ID_Personne` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `T_Personne_Credentials`
--
ALTER TABLE `T_Personne_Credentials`
  MODIFY `ID_Personne_Credentials` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `T_Personne_Role`
--
ALTER TABLE `T_Personne_Role`
  MODIFY `ID_Personne_Role` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `T_Role`
--
ALTER TABLE `T_Role`
  MODIFY `ID_Role` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `T_Alertes`
--
ALTER TABLE `T_Alertes`
  ADD CONSTRAINT `T_Alertes_ibfk_1` FOREIGN KEY (`ID_Evenements`) REFERENCES `T_Evenements` (`ID_Evenements`);

--
-- Contraintes pour la table `T_Alertes_Evenements`
--
ALTER TABLE `T_Alertes_Evenements`
  ADD CONSTRAINT `T_Alertes_Evenements_ibfk_1` FOREIGN KEY (`FK_Alertes`) REFERENCES `T_Alertes` (`ID_Alertes`),
  ADD CONSTRAINT `T_Alertes_Evenements_ibfk_2` FOREIGN KEY (`FK_Evenements`) REFERENCES `T_Evenements` (`ID_Evenements`);

--
-- Contraintes pour la table `T_Commandes`
--
ALTER TABLE `T_Commandes`
  ADD CONSTRAINT `T_Commandes_ibfk_1` FOREIGN KEY (`ID_Materiel`) REFERENCES `T_Materiel` (`ID_Materiel`);

--
-- Contraintes pour la table `T_Personne`
--
ALTER TABLE `T_Personne`
  ADD CONSTRAINT `T_Personne_ibfk_1` FOREIGN KEY (`ID_Credentials`) REFERENCES `T_Credentials` (`ID_Credentials`),
  ADD CONSTRAINT `T_Personne_ibfk_2` FOREIGN KEY (`ID_Role`) REFERENCES `T_Role` (`ID_Role`);

--
-- Contraintes pour la table `T_Personne_Credentials`
--
ALTER TABLE `T_Personne_Credentials`
  ADD CONSTRAINT `T_Personne_Credentials_ibfk_1` FOREIGN KEY (`FK_Credentials`) REFERENCES `T_Credentials` (`ID_Credentials`),
  ADD CONSTRAINT `T_Personne_Credentials_ibfk_2` FOREIGN KEY (`FK_Personne`) REFERENCES `T_Personne` (`ID_Personne`);

--
-- Contraintes pour la table `T_Personne_Role`
--
ALTER TABLE `T_Personne_Role`
  ADD CONSTRAINT `T_Personne_Role_ibfk_1` FOREIGN KEY (`FK_Personne`) REFERENCES `T_Personne` (`ID_Personne`),
  ADD CONSTRAINT `T_Personne_Role_ibfk_2` FOREIGN KEY (`FK_Role`) REFERENCES `T_Role` (`ID_Role`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
