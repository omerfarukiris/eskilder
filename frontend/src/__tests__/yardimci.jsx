import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import { AyarlarContext } from "../api.jsx";

export const ORNEK_AYARLAR = {
  kisa_ad: "Eskilder", resmi_ad: "Eskil Kültür Eğitim ve Dayanışma Derneği", slogan: "Eskil'in çocukları için",
  logo: null, hero_gorsel: null, hero_metin: "Merhaba", telefon: "0332 000", whatsapp: "+90 532 111 22 33",
  eposta: "a@b.com", adres: "Konya", harita_embed_url: "", iban: "TR000000000000000000000000",
  hesap_sahibi: "Dernek", banka: "Banka", destek_ol_metni: "Destek", hakkimizda_metni: "<p>H</p>",
  burs_metni: "<p>B</p>", kvkk_metni: "<p>K</p>", facebook: "https://facebook.com/x", instagram: "", x: "", youtube: "",
  rakamlar: [{ etiket: "öğrenci", deger: "340+" }], kurul: [], dokumanlar: [],
};

export function ciz(oge, { yol = "/", ayarlar = ORNEK_AYARLAR } = {}) {
  return render(
    <AyarlarContext.Provider value={{ veri: ayarlar, yukleniyor: false, hata: null }}>
      <MemoryRouter initialEntries={[yol]}>{oge}</MemoryRouter>
    </AyarlarContext.Provider>,
  );
}

/** fetch'i yol → yanıt eşlemesiyle taklit eder. Değer bir sayıysa o durum koduyla boş yanıt döner. */
export function fetchTaklit(eslesme) {
  const taklit = vi.fn(async (url) => {
    const yol = String(url);
    const anahtar = Object.keys(eslesme).find((k) => yol.includes(k));
    const deger = anahtar === undefined ? 404 : eslesme[anahtar];
    if (typeof deger === "number") return { ok: deger < 400, status: deger, json: async () => ({}) };
    return { ok: true, status: 200, json: async () => deger };
  });
  vi.stubGlobal("fetch", taklit);
  return taklit;
}
