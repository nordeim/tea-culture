"use client";

import { cn } from "@/lib/utils";

/* ============================================
   GST BADGE COMPONENT
   Display SGD price with GST indicator
   Singapore-compliant pricing display
   ============================================ */

interface GstBadgeProps {
  price: number;
  priceWithGst: number;
  gstAmount: number;
  currency: string;
  gstInclusive?: boolean;
  size?: "sm" | "md" | "lg";
  className?: string;
}

/**
 * GST Badge Component
 * 
 * Displays Singapore Dollar price with optional GST indicator.
 * Formats according to Singapore conventions.
 * 
 * @example
 * <GstBadge price={48} priceWithGst={52.32} gstAmount={4.32} currency="SGD" />
 * // Displays: $52.32 incl. GST
 */
export function GstBadge({
  price,
  priceWithGst,
  gstAmount,
  currency,
  gstInclusive = true,
  size = "md",
  className,
}: GstBadgeProps) {
  const formatter = new Intl.NumberFormat("en-SG", {
    style: "currency",
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const sizeClasses = {
    sm: {
      price: "text-base",
      gst: "text-[10px]",
    },
    md: {
      price: "text-xl",
      gst: "text-xs",
    },
    lg: {
      price: "text-2xl",
      gst: "text-sm",
    },
  };

  return (
    <div className={cn("flex flex-col", className)}>
      <div className="flex items-baseline gap-2">
        <span
          className={cn(
            "font-display font-semibold text-gold-600",
            sizeClasses[size].price
          )}
        >
          {formatter.format(gstInclusive ? priceWithGst : price)}
        </span>
        {gstInclusive && (
          <span
            className={cn(
              "text-bark-700/60 font-medium",
              sizeClasses[size].gst
            )}
          >
            incl. GST
          </span>
        )}
      </div>
      {gstInclusive && (
        <span className="text-[10px] text-bark-700/40">
          GST: {formatter.format(gstAmount)}
        </span>
      )}
    </div>
  );
}

export default GstBadge;
