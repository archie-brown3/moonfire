"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "The problem" },
  { href: "/data", label: "The data" },
  { href: "/replay", label: "How it learned" },
  { href: "/jumps", label: "Biggest jumps" },
];

export function SiteNav() {
  const pathname = usePathname();
  return (
    <nav aria-label="Pages" className="mx-auto w-full max-w-7xl px-6 pt-6">
      <ul className="flex flex-wrap gap-x-6 gap-y-2 text-sm">
        {LINKS.map((l) => {
          const active = pathname === l.href;
          return (
            <li key={l.href}>
              <Link
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={
                  active
                    ? "text-foreground underline decoration-2 underline-offset-8"
                    : "text-muted-foreground transition-colors hover:text-foreground"
                }
              >
                {l.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
