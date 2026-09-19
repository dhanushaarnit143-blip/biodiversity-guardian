/**
 * cn() — utility for merging Tailwind class names.
 * Uses `clsx` for conditional logic and `tailwind-merge` to deduplicate.
 *
 * Install: npm install clsx tailwind-merge
 *
 * @example
 * cn("glass p-4", isActive && "border-emerald-500", className)
 */

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
