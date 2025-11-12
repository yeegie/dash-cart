// entities/product/api/product-api.ts
import { apiClient } from '@/shared/api/api-client';
import type { Product } from '@/shared/types/product';

export interface GetProductsParams {
  page?: number;
  limit?: number;
  category_id?: string;
  search?: string;
}

export interface ProductsResponse {
  products: Product[];
  total: number;
  page: number;
  limit: number;
}

export const productApi = {
  async getProducts(params?: GetProductsParams): Promise<ProductsResponse> {
    console.log('🔄 Запрос продуктов...');
    try {
      const response = await apiClient.get<ProductsResponse>('/products', { params });
      console.log('✅ Данные получены:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Ошибка запроса:', error);
      throw error;
    }
  },
};