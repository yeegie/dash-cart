import React from 'react';
import { useNavigate } from 'react-router-dom';
import { HeroSection } from '../HeroSection/HeroSection';
import { ProductGrid } from "@features/product-grid"
import { useProducts } from "@entities/product";
import styles from './home.module.css';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { data, isLoading, error } = useProducts();

  // ДЕБАГ - что приходит в данные
  console.log('🏠 HomePage данные:', {
    isLoading,
    error,
    data,
    hasData: !!data,
    productsCount: data?.products?.length,
    products: data?.products
  });

  const handleCatalogClick = () => {
    navigate('/products');
  };

  if (isLoading) {
    console.log('🔄 Показываем загрузку...');
    return (
      <div className={styles.homePage}>
        <HeroSection />
        <div className={styles.loading}>
          <h3>Загружаем товары...</h3>
          <div className={styles.skeletonGrid}>
            {[...Array(8)].map((_, i) => (
              <div key={i} className={styles.skeletonCard}></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    console.log('❌ Показываем ошибку:', error);
    return (
      <div className={styles.homePage}>
        <HeroSection />
        <div className={styles.error}>
          <h3>Ошибка загрузки товаров</h3>
          <p>{error.message}</p>
        </div>
      </div>
    );
  }

  console.log('🎯 Рендерим товары:', {
    data,
    products: data?.products,
    productsLength: data?.products?.length
  });

  const products = data?.products || [];

  console.log('📦 Финальные продукты:', products);

  return (
    <div className={styles.homePage}>
      <HeroSection />

      <section className={styles.productsSection}>
        <div className={styles.container}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              {products.length > 0 ? `Найдено ${products.length} товаров` : 'Товаров нет'}
            </h2>
            <p className={styles.sectionSubtitle}>
              {products.length > 0 ? 'Самые востребованные товары' : 'Попробуйте зайти позже'}
            </p>
          </div>

          {/* ДЕБАГ перед ProductGrid */}
          {console.log('🎨 Передаем в ProductGrid:', products)}

          <ProductGrid
            products={products}
            loading={false}
            columns={4}
          />

          {products.length > 0 && (
            <div className={styles.ctaSection}>
              <h3>Не нашли что искали?</h3>
              <p>В нашем каталоге еще больше товаров</p>
              <button
                className={styles.catalogButton}
                onClick={handleCatalogClick}
              >
                Перейти в полный каталог
              </button>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};