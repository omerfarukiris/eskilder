const SAAT_DILIMI = "Europe/Istanbul";

export function tarihYaz(iso) {
  if (!iso) return "";
  return new Intl.DateTimeFormat("tr-TR", { day: "numeric", month: "long", year: "numeric", timeZone: SAAT_DILIMI }).format(new Date(iso));
}

export function tarihSaatYaz(iso) {
  if (!iso) return "";
  return new Intl.DateTimeFormat("tr-TR", { day: "numeric", month: "long", year: "numeric", weekday: "long", hour: "2-digit", minute: "2-digit", timeZone: SAAT_DILIMI }).format(new Date(iso));
}

export function gunAy(iso) {
  const t = new Date(iso);
  const gun = new Intl.DateTimeFormat("tr-TR", { day: "numeric", timeZone: SAAT_DILIMI }).format(t);
  const ay = new Intl.DateTimeFormat("tr-TR", { month: "short", timeZone: SAAT_DILIMI }).format(t);
  return { gun, ay };
}
