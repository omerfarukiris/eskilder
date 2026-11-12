import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import Iletisim, { whatsappLinki } from "../sayfalar/Iletisim.jsx";
import { ciz } from "./yardimci.jsx";

function yanit(durum, govde) {
  const f = vi.fn(async () => ({ ok: durum < 400, status: durum, json: async () => govde }));
  vi.stubGlobal("fetch", f);
  return f;
}

async function doldur({ kvkk = true } = {}) {
  const k = userEvent.setup();
  await k.type(screen.getByLabelText(/ad soyad/i), "Ayşe Yılmaz");
  await k.type(screen.getByLabelText(/e-posta/i), "ayse@example.com");
  await k.selectOptions(screen.getByLabelText(/konu/i), "destekci");
  await k.type(screen.getByLabelText(/mesajınız/i), "Destek olmak istiyorum.");
  if (kvkk) await k.click(screen.getByRole("checkbox"));
  return k;
}

describe("Iletisim", () => {
  it("KVKK işaretlenmeden gönderilemez", async () => {
    const f = yanit(201, { tamam: true });
    ciz(<Iletisim />);
    const k = await doldur({ kvkk: false });
    await k.click(screen.getByRole("button", { name: /gönder/i }));
    expect(screen.getByText(/aydınlatma metnini onaylamanız/i)).toBeInTheDocument();
    expect(f).not.toHaveBeenCalled();
  });

  it("geçersiz e-postada istemci hatası gösterir", async () => {
    const f = yanit(201, {});
    ciz(<Iletisim />);
    const k = userEvent.setup();
    await k.type(screen.getByLabelText(/e-posta/i), "yanlis");
    await k.click(screen.getByRole("button", { name: /gönder/i }));
    expect(screen.getByText("Geçerli bir e-posta adresi girin.")).toBeInTheDocument();
    expect(screen.getByText("Ad soyad zorunludur.")).toBeInTheDocument();
    expect(f).not.toHaveBeenCalled();
  });

  it("201 sonrası teşekkür mesajı, gövdede honeypot boş gider", async () => {
    const f = yanit(201, { tamam: true });
    ciz(<Iletisim />);
    const k = await doldur();
    await k.click(screen.getByRole("button", { name: /gönder/i }));
    expect(await screen.findByText(/mesajınız bize ulaştı/i)).toBeInTheDocument();
    const govde = JSON.parse(f.mock.calls[0][1].body);
    expect(govde).toMatchObject({ ad_soyad: "Ayşe Yılmaz", konu: "destekci", kvkk_onay: true, web_sitesi: "" });
  });

  it("400 alan hatası ilgili alanın altında", async () => {
    yanit(400, { eposta: ["Bu e-posta kabul edilmedi."] });
    ciz(<Iletisim />);
    const k = await doldur();
    await k.click(screen.getByRole("button", { name: /gönder/i }));
    expect(await screen.findByText("Bu e-posta kabul edilmedi.")).toBeInTheDocument();
    expect(screen.getByLabelText(/e-posta/i)).toHaveAttribute("aria-invalid", "true");
  });

  it("429'da değerler korunur ve hata görünür", async () => {
    yanit(429, { hata: "Çok fazla mesaj gönderildi. Lütfen bir saat sonra tekrar deneyin." });
    ciz(<Iletisim />);
    const k = await doldur();
    await k.click(screen.getByRole("button", { name: /gönder/i }));
    expect(await screen.findByRole("alert")).toHaveTextContent(/bir saat sonra/);
    expect(screen.getByLabelText(/ad soyad/i)).toHaveValue("Ayşe Yılmaz");
  });

  it("ağ hatasında anlaşılır mesaj", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => { throw new TypeError("ağ"); }));
    ciz(<Iletisim />);
    const k = await doldur();
    await k.click(screen.getByRole("button", { name: /gönder/i }));
    await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent(/bağlantı/i));
  });

  it("WhatsApp linki numaradaki boşluk/+ işaretlerini temizler", () => {
    expect(whatsappLinki("+90 532 111 22 33")).toBe("https://wa.me/905321112233");
    expect(whatsappLinki("0532 111 22 33")).toBe("https://wa.me/905321112233");
    ciz(<Iletisim />);
    expect(screen.getByRole("link", { name: /whatsapp/i })).toHaveAttribute("href", "https://wa.me/905321112233");
  });
});
