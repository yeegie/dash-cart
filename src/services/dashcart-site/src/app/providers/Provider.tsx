import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Layout } from "@app/layouts";

import { HomePage } from "@pages/home";
import { CatalogPage } from "@pages/catalog";
import { CartPage } from "@pages/cart";
import { NotFoundPage } from "@pages/not-found";

import { FaqPage } from "@pages/faq"

export default function Provider() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="/catalog" element={<CatalogPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="*" element={<NotFoundPage />} />
          <Route path="/faq" element={<FaqPage />} />
        </Route>
      </Routes>
    </Router>
  );
};