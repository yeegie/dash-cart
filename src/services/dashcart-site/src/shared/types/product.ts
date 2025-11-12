export interface Product {
  id: string;
  item_number: string;
  slug: string;
  
  name: string;
  description?: string;
  
  price: number;
  old_price?: number;
  cost_price?: number;
  
  images?: string[];
  
  weight?: number;
  dimensions?: string;
  characteristics?: Record<string, any>;
  
  meta_title?: string;
  meta_description?: string;

  rating?: number;
  review_count?: number;
  purchase_count?: number;
  
  manufacturer?: string;
  category_id: string;

  quantity: number;
  
  passport_check: boolean;
}
