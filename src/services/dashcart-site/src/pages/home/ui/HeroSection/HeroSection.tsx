import React from 'react';
import styles from './HeroSection.module.css';

export const HeroSection: React.FC = () => {
  return (
    <section className={styles.hero}>
      <div className={styles.container}>
        <div className={styles.content}>
          <h1 className={styles.title}>
            Доставка продуктов
            <span className={styles.highlight}> за 2 часа</span>
          </h1>
          <p className={styles.subtitle}>
            Свежие продукты от проверенных поставщиков с быстрой доставкой до двери
          </p>
          <div className={styles.features}>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>🚚</span>
              <span>Бесплатная доставка от 100₽</span>
            </div>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>🌱</span>
              <span>Свежие продукты каждый день</span>
            </div>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>⭐</span>
              <span>Только качественные товары</span>
            </div>
          </div>
          <button className={styles.ctaButton}>
            Сделать заказ
          </button>
        </div>
        <div className={styles.image}>
          <div className={styles.foodImage}></div>
        </div>
      </div>
    </section>
  );
};