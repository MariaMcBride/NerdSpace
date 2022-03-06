-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nerdspace_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `nerdspace_schema` ;

-- -----------------------------------------------------
-- Schema nerdspace_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nerdspace_schema` DEFAULT CHARACTER SET utf8 ;
USE `nerdspace_schema` ;

-- -----------------------------------------------------
-- Table `nerdspace_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nerdspace_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` CHAR(60) NULL,
  `confirm_password` CHAR(60) NULL,
  `dob` DATE NULL,
  `avatar` VARCHAR(255) NULL,
  `cover_photo` VARCHAR(255) NULL,
  `bio` VARCHAR(255) NULL,
  `occupation` VARCHAR(60) NULL,
  `company` VARCHAR(60) NULL,
  `location` VARCHAR(60) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nerdspace_schema`.`posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nerdspace_schema`.`posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TINYTEXT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `postuser_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_posts_users_idx` (`postuser_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_users`
    FOREIGN KEY (`postuser_id`)
    REFERENCES `nerdspace_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nerdspace_schema`.`follows`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nerdspace_schema`.`follows` (
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `followeduser_id` INT NOT NULL,
  `follower_id` INT NOT NULL,
  INDEX `fk_followers_users1_idx` (`followeduser_id` ASC) VISIBLE,
  INDEX `fk_followers_users2_idx` (`follower_id` ASC) VISIBLE,
  PRIMARY KEY (`followeduser_id`, `follower_id`),
  CONSTRAINT `fk_followers_users1`
    FOREIGN KEY (`followeduser_id`)
    REFERENCES `nerdspace_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_followers_users2`
    FOREIGN KEY (`follower_id`)
    REFERENCES `nerdspace_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nerdspace_schema`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nerdspace_schema`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TINYTEXT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `commentuser_id` INT NOT NULL,
  `commentpost_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_users1_idx` (`commentuser_id` ASC) VISIBLE,
  INDEX `fk_comments_posts1_idx` (`commentpost_id` ASC) VISIBLE,
  CONSTRAINT `fk_comments_users1`
    FOREIGN KEY (`commentuser_id`)
    REFERENCES `nerdspace_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_posts1`
    FOREIGN KEY (`commentpost_id`)
    REFERENCES `nerdspace_schema`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nerdspace_schema`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nerdspace_schema`.`likes` (
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `likeuser_id` INT NOT NULL,
  `likepost_id` INT NOT NULL,
  INDEX `fk_likes_users1_idx` (`likeuser_id` ASC) VISIBLE,
  INDEX `fk_likes_posts1_idx` (`likepost_id` ASC) VISIBLE,
  PRIMARY KEY (`likeuser_id`, `likepost_id`),
  CONSTRAINT `fk_likes_users1`
    FOREIGN KEY (`likeuser_id`)
    REFERENCES `nerdspace_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_posts1`
    FOREIGN KEY (`likepost_id`)
    REFERENCES `nerdspace_schema`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
