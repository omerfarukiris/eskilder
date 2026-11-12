import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import Ust from "../bilesenler/Ust.jsx";
import Alt from "../bilesenler/Alt.jsx";
import { Uygulama } from "../App.jsx";
import { ciz, fetchTaklit } from "./yardimci.jsx";

describe("Ust", () => {
  it("menü butonuna tıklayınca bağlantılar açılır, bağlantıya tıklayınca kapanır", async () => {
    ciz(<Ust />);
    const buton = screen.getByRole("button", { name: /menü/i });
    expect(buton).toHaveAttribute("aria-expanded", "false");
    await userEvent.click(buton);
    expect(buton).toHaveAttribute("aria-expanded", "true");
    await userEvent.click(screen.getByRole("link", { name: "Hakkımızda" }));
    expect(buton).toHaveAttribute("aria-expanded", "false");
  });

  it("Destek Ol butonu /destek-ol'a gider", () => {
    ciz(<Ust />);
    expect(screen.getAllByRole("link", { name: "Destek Ol" })[0]).toHaveAttribute("href", "/destek-ol");
  });
});

describe("Alt", () => {
  it("yalnızca dolu sosyal medya bağlantılarını gösterir", () => {
    ciz(<Alt />);
    expect(screen.getByRole("link", { name: "Facebook" })).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Instagram" })).toBeNull();
  });
});

describe("Uygulama", () => {
  it("bilinmeyen rota Bulunamadı sayfasını gösterir", async () => {
    fetchTaklit({});
    ciz(<Uygulama />, { yol: "/boyle-bir-sayfa-yok" });
    expect(await screen.findByRole("heading", { name: /sayfa bulunamadı/i })).toBeInTheDocument();
  });
});
