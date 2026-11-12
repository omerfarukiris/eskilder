import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Anasayfa from "../sayfalar/Anasayfa.jsx";
import { ciz, fetchTaklit } from "./yardimci.jsx";

const DUYURULAR = { count: 1, results: [{ baslik: "Burs Başladı", slug: "burs-basladi", ozet: "Ö", kapak: null, yayin_tarihi: "2024-12-23T10:00:00+03:00", one_cikan: false }] };

describe("Anasayfa", () => {
  it("hero, rakamlar, duyurular ve destekçileri gösterir", async () => {
    fetchTaklit({
      "/api/duyurular/": DUYURULAR,
      "/api/etkinlikler/": { count: 1, results: [{ tur: "bulusma", tur_adi: "Buluşma", baslik: "Eskilliler Buluşması", slug: "b", baslangic: "2026-12-12T19:00:00+03:00", yer: "Konya", kapak: null }] },
      "/api/destekciler/": [{ ad: "Örnek Yapı", tur: "firma", logo: null, not_metni: "" }],
    });
    ciz(<Anasayfa />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Eskil'in çocukları için");
    expect(screen.getByText("340+")).toBeInTheDocument();
    expect(await screen.findByText("Burs Başladı")).toBeInTheDocument();
    expect(await screen.findByText("Eskilliler Buluşması")).toBeInTheDocument();
    expect(await screen.findByText("Örnek Yapı")).toBeInTheDocument();
    expect(screen.getAllByRole("link", { name: /destek ol/i })[0]).toHaveAttribute("href", "/destek-ol");
  });

  it("yaklaşan etkinlik ve destekçi yoksa o bölümleri göstermez", async () => {
    fetchTaklit({ "/api/duyurular/": DUYURULAR, "/api/etkinlikler/": { count: 0, results: [] }, "/api/destekciler/": [] });
    ciz(<Anasayfa />);
    await screen.findByText("Burs Başladı");
    expect(screen.queryByRole("heading", { name: /yaklaşan/i })).toBeNull();
    expect(screen.queryByRole("heading", { name: /destekçilerimiz/i })).toBeNull();
  });
});
