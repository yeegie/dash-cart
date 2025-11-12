import React from 'react';
import type { Product } from "@shared/types/product";
import styles from './ProductCard.module.css';

interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  onQuickView?: (product: Product) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onAddToCart,
  onQuickView
}) => {
  const {
    id,
    name,
    description,
    price,
    old_price,
    images,
    rating = 0,
    review_count = 0,
    purchase_count = 0,
    manufacturer,
    quantity,
    passport_check
  } = product;

  const mainImage = images?.[0] || '/placeholder-image.jpg';
  const hasDiscount = old_price && old_price > price;
  const discountPercent = hasDiscount 
    ? Math.round(((old_price - price) / old_price) * 100)
    : 0;

  const handleAddToCart = () => {
    onAddToCart?.(product);
  };

  const handleQuickView = () => {
    onQuickView?.(product);
  };

  return (
    <div className={styles.card}>
      {/* Product Image */}
      <div className={styles.imageContainer}>
        <img 
          src={mainImage} 
          alt={name}
          className={styles.image}
          loading="lazy"
        />
        
        {/* Discount Badge */}
        {hasDiscount && (
          <div className={styles.discountBadge}>
            -{discountPercent}%
          </div>
        )}

        {/* Passport Check Badge */}
        {passport_check && (
          <div className={styles.passportBadge}>
            📋 Паспорт
          </div>
        )}

        {/* Quick View Button */}
        <button 
          className={styles.quickViewBtn}
          onClick={handleQuickView}
          aria-label="Быстрый просмотр"
        >
          👁️
        </button>
      </div>

      {/* Product Info */}
      <div className={styles.content}>
        {/* Manufacturer */}
        {manufacturer && (
          <div className={styles.manufacturer}>
            {manufacturer}
          </div>
        )}

        {/* Product Name */}
        <h3 className={styles.name} title={name}>
          {name}
        </h3>

        {/* Description */}
        {description && (
          <p className={styles.description}>
            {description}
          </p>
        )}

        {/* Rating */}
        <div className={styles.rating}>
          <div className={styles.stars}>
            {'★'.repeat(Math.floor(rating))}
            {'☆'.repeat(5 - Math.floor(rating))}
          </div>
          <span className={styles.reviewCount}>({review_count})</span>
        </div>

        {/* Purchase Count */}
        {purchase_count > 0 && (
          <div className={styles.purchaseCount}>
            Купили: {purchase_count} раз
          </div>
        )}

        {/* Price Section */}
        <div className={styles.priceSection}>
          <div className={styles.currentPrice}>
            {price.toLocaleString('ru-RU')} ₽
          </div>
          
          {hasDiscount && (
            <div className={styles.oldPrice}>
              {old_price.toLocaleString('ru-RU')} ₽
            </div>
          )}
        </div>

        {/* Stock Status */}
        <div className={styles.stock}>
          {quantity > 0 ? (
            <span className={styles.inStock}>✓ В наличии</span>
          ) : (
            <span className={styles.outOfStock}>✗ Нет в наличии</span>
          )}
        </div>

        {/* Add to Cart Button */}
        <button
          className={styles.addToCartBtn}
          onClick={handleAddToCart}
          disabled={quantity === 0}
        >
          {quantity > 0 ? 'В корзину' : 'Нет в наличии'}
        </button>
      </div>
    </div>
  );
};