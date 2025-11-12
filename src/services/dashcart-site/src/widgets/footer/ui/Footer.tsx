// widgets/footer/ui/Footer.tsx
import { Link } from "react-router-dom";
import styles from "./Footer.module.css";

export const Footer = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.footer__container}>
        
        {/* Лого и описание */}
        <div className={styles.footer__brand}>
          <Link to="/" className={styles.footer__logo}>
            DashCart
          </Link>
          <p className={styles.footer__description}>
            Ваш надежный помощник в мире покупок. 
            Быстро, удобно, выгодно.
          </p>
        </div>

        {/* Навигация */}
        <nav className={styles.footer__nav}>
          <div className={styles.footer__column}>
            <h4 className={styles.footer__title}>Магазин</h4>
            <ul className={styles.footer__list}>
              <li><Link to="/products">Все товары</Link></li>
              <li><Link to="/categories">Категории</Link></li>
              <li><Link to="/sales">Акции</Link></li>
              <li><Link to="/new">Новинки</Link></li>
            </ul>
          </div>

          <div className={styles.footer__column}>
            <h4 className={styles.footer__title}>Помощь</h4>
            <ul className={styles.footer__list}>
              <li><Link to="/faq">Доставка</Link></li>
              <li><Link to="/faq">Оплата</Link></li>
              <li><Link to="/faq">Возврат</Link></li>
              <li><Link to="/faq">FAQ</Link></li>
            </ul>
          </div>

          <div className={styles.footer__column}>
            <h4 className={styles.footer__title}>О нас</h4>
            <ul className={styles.footer__list}>
              <li><Link to="/about">О компании</Link></li>
              <li><Link to="/contacts">Контакты</Link></li>
              <li><Link to="/career">Вакансии</Link></li>
              <li><Link to="/blog">Блог</Link></li>
            </ul>
          </div>
        </nav>

        {/* Контакты и соцсети */}
        <div className={styles.footer__contacts}>
          <h4 className={styles.footer__title}>Свяжитесь с нами</h4>
          <div className={styles.footer__social}>
            <a href="#" className={styles.social__link}>Telegram</a>
            <a href="#" className={styles.social__link}>VK</a>
            <a href="#" className={styles.social__link}>Instagram</a>
          </div>
          <div className={styles.footer__info}>
            <p>📞 +7 (999) 123-45-67</p>
            <p>✉️ hello@dashcart.ru</p>
          </div>
        </div>
      </div>

      {/* Копирайт */}
      <div className={styles.footer__bottom}>
        <p>&copy; 2025 DashCart. Все права защищены.</p>
        <div className={styles.footer__legal}>
          <Link to="/privacy">Политика конфиденциальности</Link>
          <Link to="/terms">Условия использования</Link>
        </div>
      </div>
    </footer>
  );
};