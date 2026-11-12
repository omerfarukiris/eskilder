import { createContext, useContext, useEffect, useState } from "react";

export class ApiHatasi extends Error {
  constructor(durum) {
    super(`API hatası: ${durum}`);
    this.durum = durum;
  }
}

export async function getir(yol) {
  const yanit = await fetch(`/api${yol}`, { headers: { Accept: "application/json" } });
  if (!yanit.ok) throw new ApiHatasi(yanit.status);
  return yanit.json();
}

export async function gonder(yol, veri) {
  const yanit = await fetch(`/api${yol}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(veri),
  });
  const govde = await yanit.json().catch(() => ({}));
  return { durum: yanit.status, govde };
}

/** Bir API yolunu çeker. yol null ise hiçbir şey yapmaz. */
export function useVeri(yol) {
  const [durum, setDurum] = useState({ veri: null, yukleniyor: Boolean(yol), hata: null });
  useEffect(() => {
    if (!yol) return undefined;
    let iptal = false;
    setDurum((onceki) => ({ ...onceki, yukleniyor: true, hata: null }));
    getir(yol)
      .then((veri) => !iptal && setDurum({ veri, yukleniyor: false, hata: null }))
      .catch((hata) => !iptal && setDurum({ veri: null, yukleniyor: false, hata }));
    return () => {
      iptal = true;
    };
  }, [yol]);
  return durum;
}

export const AyarlarContext = createContext({ veri: null, yukleniyor: true, hata: null });

export function AyarlarSaglayici({ children }) {
  const durum = useVeri("/ayarlar/");
  return <AyarlarContext.Provider value={durum}>{children}</AyarlarContext.Provider>;
}

/** Site ayarları; yüklenene kadar boş nesne döner ki bileşenler koşulsuz okuyabilsin. */
export function useAyarlar() {
  return useContext(AyarlarContext).veri || {};
}
