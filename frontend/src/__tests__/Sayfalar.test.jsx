import { act, fireEvent, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import Lightbox from "../bilesenler/Lightbox.jsx";
import DestekOl from "../sayfalar/DestekOl.jsx";
import DuyuruDetay from "../sayfalar/DuyuruDetay.jsx";
import Etkinlikler from "../sayfalar/Etkinlikler.jsx";
import Destekciler from "../sayfalar/Destekciler.jsx";
import { ORNEK_AYARLAR, ciz, fetchTaklit } from "./yardimci.jsx";

describe("DestekOl", () => {
  it("IBAN 4'lü gruplanır, kopyalanınca boşluksuz yazılır ve Kopyalandı görünür", async () => {
    const yaz = vi.fn().mockResolvedValue();
    Object.defineProperty(navigator, "clipboard", { value: { writeText: yaz }, configurable: true });
    ciz(<DestekOl />, { ayarlar: { ...ORNEK_AYARLAR, iban: "TR12 0006 4000 0011 2345 6789 01" } });
    expect(screen.getByText("TR12 0006 4000 0011 2345 6789 01")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /IBAN'ı kopyala/i }));
    expect(yaz).toHaveBeenCalledWith("TR120006400000112345678901");
    expect(await screen.findByText("Kopyalandı")).toBeInTheDocument();
  });

  it("IBAN boşsa yakında mesajı", () => {
    ciz(<DestekOl />, { ayarlar: { ...ORNEK_AYARLAR, iban: "" } });
    expect(screen.getByText("IBAN bilgisi yakında eklenecek.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /kopyala/i })).toBeNull();
  });
});

describe("Lightbox", () => {
  const fotolar = [{ gorsel: "/1.jpg", aciklama: "Bir" }, { gorsel: "/2.jpg", aciklama: "İki" }];

  it("sağ ok sonraki fotoğrafa geçer, Esc ile kapanır", () => {
    const kapat = vi.fn();
    ciz(<Lightbox fotograflar={fotolar} index={0} onKapat={kapat} />);
    expect(screen.getByRole("img")).toHaveAttribute("alt", "Bir");
    fireEvent.keyDown(document, { key: "ArrowRight" });
    expect(screen.getByRole("img")).toHaveAttribute("alt", "İki");
    fireEvent.keyDown(document, { key: "ArrowRight" });
    expect(screen.getByRole("img")).toHaveAttribute("alt", "Bir");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(kapat).toHaveBeenCalled();
  });
});

describe("Detay sayfaları", () => {
  it("DuyuruDetay API 404 → Bulunamadı", async () => {
    fetchTaklit({ "/api/duyurular/yok/": 404 });
    ciz(<Routes><Route path="/duyurular/:slug" element={<DuyuruDetay />} /></Routes>, { yol: "/duyurular/yok" });
    expect(await screen.findByRole("heading", { name: /sayfa bulunamadı/i })).toBeInTheDocument();
  });

  it("DuyuruDetay başlık, içerik ve sekme başlığını gösterir", async () => {
    fetchTaklit({ "/api/duyurular/a/": { baslik: "Burs", slug: "a", ozet: "", kapak: null, yayin_tarihi: "2024-12-23T10:00:00+03:00", one_cikan: false, icerik: "<p>Metin</p>", fotograflar: [] } });
    ciz(<Routes><Route path="/duyurular/:slug" element={<DuyuruDetay />} /></Routes>, { yol: "/duyurular/a" });
    expect(await screen.findByRole("heading", { level: 1, name: "Burs" })).toBeInTheDocument();
    expect(screen.getByText("Metin")).toBeInTheDocument();
    expect(document.title).toBe("Burs | Eskilder");
  });
});

describe("Etkinlikler", () => {
  it("yaklaşan yoksa geçmiş sekmesi açılır", async () => {
    fetchTaklit({
      "zaman=yaklasan": { count: 0, results: [] },
      "zaman=gecmis": { count: 1, results: [{ tur: "bulusma", tur_adi: "Buluşma", baslik: "İftar", slug: "i", baslangic: "2026-04-01T19:00:00+03:00", yer: "Eskil", kapak: null }] },
    });
    ciz(<Etkinlikler />);
    expect(await screen.findByText("İftar")).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "Geçmiş" })).toHaveAttribute("aria-selected", "true");
  });
});

describe("Destekciler", () => {
  it("firmaları ve kişileri ayrı gösterir", async () => {
    fetchTaklit({ "/api/destekciler/": [{ ad: "Yapı A.Ş.", tur: "firma", logo: null, not_metni: "3 öğrenci" }, { ad: "Ahmet Bey", tur: "kisi", logo: null, not_metni: "" }] });
    ciz(<Destekciler />);
    expect(await screen.findByRole("heading", { name: "Firmalar" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Kişiler" })).toBeInTheDocument();
    expect(screen.getByText("Ahmet Bey")).toBeInTheDocument();
    await act(async () => {});
  });
});
