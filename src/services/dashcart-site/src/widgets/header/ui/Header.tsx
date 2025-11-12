import React, { useState } from "react"
import styles from "./Header.module.css";
import logo from "@assets/images/icons/dashcart.svg";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@shared/ui/button"


export const Header = () => {
  const [searchValue, setSearchValue] = useState("")
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchValue.trim()) {
      navigate(`/products/search?query=${encodeURIComponent(searchValue)}`);
    }
  };

  const handleSigninClick = () => {
    navigate("/signin");
  }

  return(
    <header className={styles.header}>
      <Link to="/" className={styles.header__logo}>
        <img
          src={logo}
          alt="dashcart логотип"
          loading="lazy"
          className={styles.header__logo_image}
        />
      </Link>
      <form onSubmit={handleSearch} className={styles.header__search_form}>
        <input
          type="search"
          placeholder={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          className={styles.header__searchbar}
        />
      </form>
      <Button
        type="button"
        text="Войти"
        onClick={handleSigninClick}
      />
    </header>
  );
};