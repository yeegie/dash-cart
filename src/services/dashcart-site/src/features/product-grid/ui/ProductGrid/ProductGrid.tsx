import React from 'react';
import { ProductCard } from '../ProductCard/ProductCard';
import styles from './ProductGrid.module.css';
import type { Product } from "@shared/types/product"

export interface ProductGridProps {
  products: Product[];
  loading?: boolean;
  columns?: number;
  className?: string;
}

export const ProductGrid: React.FC<ProductGridProps> = ({
  products,
  loading = false,
  columns = 4,
  className = ''
}) => {
  if (loading) {
    return (
      <div className={`${styles.grid} ${className}`} style={{ '--columns': columns } as React.CSSProperties}>
        {Array.from({ length: 8 }).map((_, index) => (
          <div key={index} className={styles.skeletonCard}>
            <div className={styles.skeletonImage}></div>
            <div className={styles.skeletonContent}>
              <div className={styles.skeletonLine}></div>
              <div className={styles.skeletonLine}></div>
              <div className={styles.skeletonLine}></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (!products.length) {
    return (
      <div className={styles.empty}>
        <h3>Товары не найдены</h3>
        <p>Попробуйте изменить параметры поиска</p>
      </div>
    );
  }

  const handleAddToCart = (product: any) => {
    console.log('Add to cart:', product);
    // Здесь будет логика добавления в корзину
  };

  const handleQuickView = (product: any) => {
    console.log('Quick view:', product);
    // Здесь будет логика быстрого просмотра
  };

  return (
    <div 
      className={`${styles.grid} ${className}`}
      style={{ '--columns': columns } as React.CSSProperties}
    >
      {products.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={handleAddToCart}
          onQuickView={handleQuickView}
        />
      ))}
    </div>
  );
};