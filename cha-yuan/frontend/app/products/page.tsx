/**
 * Products Page - Tea Catalog
 * Server Component for server-side data fetching
 * Singapore context: GST 9%, SGD currency
 */

import { Suspense } from "react";
import { Metadata } from "next";
import { getProducts, getCategories, getOrigins } from "@/lib/api/products";
import { ProductCatalog } from "./components/product-catalog";
import { ProductGridSkeleton } from "@/components/product-grid";
import { Leaf } from "lucide-react";

// Metadata for SEO
export const metadata: Metadata = {
  title: "Shop Premium Teas | CHA YUAN (茶源)",
  description:
    "Discover our curated collection of premium teas from China, Taiwan, Japan, and India. " +
    "Sourced directly from heritage tea gardens. Free delivery in Singapore.",
  keywords: [
    "premium tea",
    "singapore tea shop",
    "green tea",
    "oolong",
    "black tea",
    "white tea",
    "puerh",
    "tea subscription",
  ],
  openGraph: {
    title: "Shop Premium Teas | CHA YUAN",
    description: "Discover our curated collection of premium teas from Asia's finest gardens.",
    type: "website",
  },
};

interface ProductsPageProps {
  searchParams: {
    category?: string;
    origin?: string;
    season?: string;
    page?: string;
  };
}

/**
 * Products Page
 * Main catalog with filtering and pagination
 */
export default async function ProductsPage({ searchParams }: ProductsPageProps) {
  // Fetch data server-side
  const [productsResponse, categories, origins] = await Promise.all([
    getProducts({
      category: searchParams.category,
      origin: searchParams.origin,
      season: searchParams.season,
      page: searchParams.page ? parseInt(searchParams.page) : undefined,
    }),
    getCategories(),
    getOrigins(),
  ]);

  const products = productsResponse.items;

  return (
    <main className="min-h-screen bg-ivory-50">
      {/* Hero Header */}
      <div className="bg-gradient-to-b from-tea-50/50 to-ivory-50 py-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <Leaf className="w-8 h-8 text-tea-600 mx-auto mb-4" />
          <h1 className="font-serif text-4xl md:text-5xl text-bark-900 mb-4">
            Our Tea Collection
          </h1>
          <p className="text-bark-700/70 max-w-2xl mx-auto text-lg leading-relaxed">
            Discover premium teas sourced directly from heritage gardens across 
            China, Taiwan, Japan, and India. Each tea selected for its distinctive 
            character and exceptional quality.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Product Catalog Client Component */}
        <Suspense fallback={<ProductGridSkeleton columns={3} count={6} />}>
          <ProductCatalog
            products={products}
            categories={categories}
            origins={origins}
          />
        </Suspense>
      </div>

      {/* Newsletter / CTA */}
      <section className="bg-bark-900 text-ivory-50 py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="font-serif text-3xl mb-4">
            Curated for Your Palate
          </h2>
          <p className="text-ivory-100/80 mb-8 max-w-xl mx-auto">
            Not sure where to start? Take our preference quiz and receive 
            personalized tea recommendations tailored to your taste.
          </p>
          <a
            href="/quiz"
            className="inline-flex items-center px-6 py-3 bg-gold-500 
                     text-bark-900 font-medium rounded-lg
                     hover:bg-gold-400 transition-colors"
          >
            Take the Quiz
          </a>
        </div>
      </section>
    </main>
  );
}
