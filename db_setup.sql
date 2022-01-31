SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `js-project`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `accounts`
--

CREATE TABLE `accounts` (
  `login` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `type` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `accounts`
--

INSERT INTO `accounts` (`login`, `password`, `type`) VALUES
('Aaltonen', 'Aaltonen123', 'w'),
('admin', 'admin', 'a'),
('Anson', 'Anson123', 'w'),
('Busto', 'Busto123', 'w'),
('Coutts', 'Coutts123', 'w'),
('Eriksen', 'Eriksen123', 'w'),
('fashinbauer', 'fashinbauer123', 'w'),
('Kayode', 'Kayode123', 'w'),
('Prebensen', 'Prebensen123', 'w'),
('Romanov', 'Romanov123', 'w'),
('Schumacher', 'Schumacher123', 'w'),
('Sousa', 'Sousa123', 'w');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `tasks`
--

CREATE TABLE `tasks` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `deadline` date NOT NULL,
  `exec_day` date NOT NULL,
  `notes` varchar(1024) NOT NULL,
  `exec_notes` varchar(1024) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `tasks`
--

INSERT INTO `tasks` (`id`, `name`, `deadline`, `exec_day`, `notes`, `exec_notes`, `status`) VALUES
(39, 'roof construction', '2021-01-22', '2021-01-18', 'lay down isolation', 'task finished without problems', 1),
(40, 'terrace', '2021-01-20', '2021-01-19', 'grind and oil terrace', '', 0),
(41, 'garage prep', '2021-01-19', '2021-01-18', 'remove all tools from garage', '', 0),
(42, 'order steel rods', '2021-01-20', '2021-01-18', 'order 200 pieces of 15m steel rods for reinforcement', '150 pieces were ordered', 0),
(43, 'settle accounts', '2021-01-21', '2021-01-20', '', '', 0),
(44, 'electronics waste disposal', '2021-01-25', '2021-01-22', 'dispose of electronical waste from building 2', 'already done', 1),
(45, 'transport gravel', '2021-01-28', '2021-01-21', '', '', 0);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `task_assign`
--

CREATE TABLE `task_assign` (
  `task_id` int(11) NOT NULL,
  `worker_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `task_assign`
--

INSERT INTO `task_assign` (`task_id`, `worker_id`) VALUES
(39, 26),
(39, 27),
(39, 30),
(40, 29),
(40, 31),
(41, 31),
(41, 32),
(41, 33),
(42, 25),
(42, 28),
(42, 29),
(42, 31),
(43, 23),
(44, 28),
(44, 29),
(44, 30),
(44, 33),
(45, 24),
(45, 26),
(45, 28),
(45, 30);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `value` decimal(12,2) NOT NULL,
  `date` date NOT NULL,
  `item` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `transactions`
--

INSERT INTO `transactions` (`id`, `value`, `date`, `item`) VALUES
(1, '-10000.00', '2021-01-14', 'steel rods'),
(2, '-3210.00', '2020-12-30', 'roof tiles'),
(3, '-7900.00', '2020-12-26', 'floor tiles'),
(7, '50000.00', '2021-01-18', 'building 1 room 3 advance'),
(8, '-20200.10', '2020-11-23', 'excavator payment');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `workers`
--

CREATE TABLE `workers` (
  `id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `surname` varchar(32) NOT NULL,
  `tel` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `workers`
--

INSERT INTO `workers` (`id`, `name`, `surname`, `tel`) VALUES
(23, 'Lauri', 'Fashinbauer', '123234345'),
(24, 'Bahman', 'Sousa', '109020803'),
(25, 'Luanne', 'Romanov', '857239005'),
(26, 'Jolan', 'Busto', '599925768'),
(27, 'Jirina', 'Anson', '490557223'),
(28, 'Mariyka', 'Coutts', '370965016'),
(29, 'Arijana', 'Schumacher', '465284266'),
(30, 'Ahmed', 'Kayode', '582606181'),
(31, 'Yanick', 'Prebensen', '393473871'),
(32, 'Dominik', 'Aaltonen', '894175721'),
(33, 'Pedrinho', 'Eriksen', '237719801');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `worker_account`
--

CREATE TABLE `worker_account` (
  `worker_id` int(11) NOT NULL,
  `account_login` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `worker_account`
--

INSERT INTO `worker_account` (`worker_id`, `account_login`) VALUES
(23, 'fashinbauer'),
(24, 'Sousa'),
(25, 'Romanov'),
(26, 'Busto'),
(27, 'Anson'),
(28, 'Coutts'),
(29, 'Schumacher'),
(30, 'Kayode'),
(31, 'Prebensen'),
(32, 'Aaltonen'),
(33, 'Eriksen');

--
-- Indeksy dla tabeli `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`login`);

--
-- Indeksy dla tabeli `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `task_assign`
--
ALTER TABLE `task_assign`
  ADD PRIMARY KEY (`task_id`,`worker_id`),
  ADD KEY `task_assign_worker_fk` (`worker_id`);

--
-- Indeksy dla tabeli `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `workers`
--
ALTER TABLE `workers`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `worker_account`
--
ALTER TABLE `worker_account`
  ADD PRIMARY KEY (`worker_id`,`account_login`),
  ADD KEY `worker_account_acc_fk` (`account_login`);

--
-- AUTO_INCREMENT dla tabeli `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT dla tabeli `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT dla tabeli `workers`
--
ALTER TABLE `workers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Ograniczenia dla tabeli `task_assign`
--
ALTER TABLE `task_assign`
  ADD CONSTRAINT `task_assign_task_fk` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  ADD CONSTRAINT `task_assign_worker_fk` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`);

--
-- Ograniczenia dla tabeli `worker_account`
--
ALTER TABLE `worker_account`
  ADD CONSTRAINT `worker_account_acc_fk` FOREIGN KEY (`account_login`) REFERENCES `accounts` (`login`),
  ADD CONSTRAINT `worker_account_worker_fk` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
