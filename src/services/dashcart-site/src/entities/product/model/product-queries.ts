// entities/product/model/use-products.ts
import { useState, useEffect } from 'react';
import { productApi } from '../api/product-api';
import type { Product } from '@/shared/types/product';

export const useProducts = () => {
  const [data, setData] = useState<{ products: Product[] } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setIsLoading(true);
        console.log('🔄 Начинаем загрузку продуктов...');
        const response = await productApi.getProducts();
        console.log('✅ Продукты загружены:', response);
        setData(response);
      } catch (err) {
        console.error('❌ Ошибка загрузки:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return { data, isLoading, error };
};