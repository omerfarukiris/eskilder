import { useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import { AyarlarSaglayici } from "./api.jsx";
import Alt from "./bilesenler/Alt.jsx";
import Ust from "./bilesenler/Ust.jsx";
import Anasayfa from "./sayfalar/Anasayfa.jsx";
import Bulunamadi from "./sayfalar/Bulunamadi.jsx";
import Burs from "./sayfalar/Burs.jsx";
import Destekciler from "./sayfalar/Destekciler.jsx";
import DestekOl from "./sayfalar/DestekOl.jsx";
import DuyuruDetay from "./sayfalar/DuyuruDetay.jsx";
import Duyurular from "./sayfalar/Duyurular.jsx";
import EtkinlikDetay from "./sayfalar/EtkinlikDetay.jsx";
import Etkinlikler from "./sayfalar/Etkinlikler.jsx";
import Hakkimizda from "./sayfalar/Hakkimizda.jsx";
import Iletisim from "./sayfalar/Iletisim.jsx";
import Kvkk from "./sayfalar/Kvkk.jsx";

function SayfaBasinaKaydir() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo?.(0, 0); }, [pathname]);
  return null;
}

/** Router içinde çalışan uygulama gövdesi (testlerde MemoryRouter ile sarılır). */
export function Uygulama() {
  return (
    <div className="sayfa-cerceve">
      <a href="#icerik" className="atla">İçeriğe geç</a>
      <SayfaBasinaKaydir />
      <Ust />
      <main id="icerik">
        <Routes>
          <Route path="/" element={<Anasayfa />} />
          <Route path="/hakkimizda" element={<Hakkimizda />} />
          <Route path="/burs" element={<Burs />} />
          <Route path="/duyurular" element={<Duyurular />} />
          <Route path="/duyurular/:slug" element={<DuyuruDetay />} />
          <Route path="/etkinlikler" element={<Etkinlikler />} />
          <Route path="/etkinlikler/:slug" element={<EtkinlikDetay />} />
          <Route path="/destekcilerimiz" element={<Destekciler />} />
          <Route path="/destek-ol" element={<DestekOl />} />
          <Route path="/iletisim" element={<Iletisim />} />
          <Route path="/kvkk" element={<Kvkk />} />
          <Route path="*" element={<Bulunamadi />} />
        </Routes>
      </main>
      <Alt />
    </div>
  );
}

export default function App() {
  return (
    <AyarlarSaglayici>
      <Uygulama />
    </AyarlarSaglayici>
  );
}
