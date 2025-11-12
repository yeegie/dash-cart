import { SkeletonTheme } from "react-loading-skeleton";
import { Outlet } from "react-router-dom";

import { Header } from "@widgets/header";
import { Footer } from "@widgets/footer";

export const Layout = () => {
  return (
    <SkeletonTheme baseColor="#ebebeb" highlightColor="#f5f5f5">
      <div className="page__body">
        <Header />
        <main>
          <Outlet />
        </main>
        <Footer />
      </div>
    </SkeletonTheme>
  );
};