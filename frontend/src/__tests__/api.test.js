import { describe, expect, it } from "vitest";
import { ApiHatasi, getir, gonder } from "../api.jsx";
import { fetchTaklit } from "./yardimci.jsx";

describe("api", () => {
  it("getir /api önekiyle çağırır ve JSON döner", async () => {
    const f = fetchTaklit({ "/api/duyurular/": { count: 0 } });
    expect(await getir("/duyurular/")).toEqual({ count: 0 });
    expect(f.mock.calls[0][0]).toBe("/api/duyurular/");
  });

  it("getir 404'te ApiHatasi(404) fırlatır", async () => {
    fetchTaklit({ "/api/yok/": 404 });
    await expect(getir("/yok/")).rejects.toMatchObject({ durum: 404 });
    await expect(getir("/yok/")).rejects.toBeInstanceOf(ApiHatasi);
  });

  it("gonder durum ve gövdeyi döner, hata durumunda fırlatmaz", async () => {
    fetchTaklit({ "/api/iletisim/": 429 });
    expect(await gonder("/iletisim/", { a: 1 })).toEqual({ durum: 429, govde: {} });
  });
});
