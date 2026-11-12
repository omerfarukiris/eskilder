import { act, fireEvent, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Acilis, { acilisGosterilsinMi } from "../bilesenler/Acilis.jsx";
import { ciz } from "./yardimci.jsx";

const medya = (eslesir) => () => ({ matches: eslesir });

describe("acilisGosterilsinMi", () => {
  it("ilk ziyarette true", () => expect(acilisGosterilsinMi(sessionStorage, medya(false))).toBe(true));
  it("acilis_goruldu=1 ise false", () => {
    sessionStorage.setItem("acilis_goruldu", "1");
    expect(acilisGosterilsinMi(sessionStorage, medya(false))).toBe(false);
  });
  it("reduced-motion açıksa false", () => expect(acilisGosterilsinMi(sessionStorage, medya(true))).toBe(false));
  it("storage hata verirse true döner ve fırlatmaz", () => {
    const bozuk = { getItem: () => { throw new Error("gizli mod"); } };
    expect(acilisGosterilsinMi(bozuk, medya(false))).toBe(true);
  });
});

describe("Acilis", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal("matchMedia", medya(false));
  });
  afterEach(() => vi.useRealTimers());

  it("1200 ms sonra kaldırılır ve oturuma işlenir", () => {
    ciz(<Acilis />);
    expect(screen.getByTestId("acilis")).toBeInTheDocument();
    act(() => vi.advanceTimersByTime(1200));
    expect(screen.queryByTestId("acilis")).toBeNull();
    expect(sessionStorage.getItem("acilis_goruldu")).toBe("1");
  });

  it("tıklayınca hemen kapanır", () => {
    ciz(<Acilis />);
    fireEvent.click(screen.getByTestId("acilis"));
    expect(screen.queryByTestId("acilis")).toBeNull();
  });

  it("Esc ile kapanır", () => {
    ciz(<Acilis />);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByTestId("acilis")).toBeNull();
  });

  it("aynı oturumda ikinci kez gösterilmez", () => {
    sessionStorage.setItem("acilis_goruldu", "1");
    ciz(<Acilis />);
    expect(screen.queryByTestId("acilis")).toBeNull();
  });
});
