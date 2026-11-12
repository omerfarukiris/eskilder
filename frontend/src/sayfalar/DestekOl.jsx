import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useAyarlar } from "../api.jsx";
import { SayfaUst, useBaslik } from "../bilesenler/ortak.jsx";
import stil from "./Icerik.module.css";

export function ibanGrupla(iban) {
  return (iban || "").replace(/\s+/g, "").toUpperCase().replace(/(.{4})/g, "$1 ").trim();
}

export default function DestekOl() {
  const a = useAyarlar();
  const [kopyalandi, setKopyalandi] = useState(false);
  const ibanRef = useRef(null);
  useBaslik("Destek Ol");

  const kopyala = async () => {
    const yalin = (a.iban || "").replace(/\s+/g, "");
    try {
      await navigator.clipboard.writeText(yalin);
      setKopyalandi(true);
      setTimeout(() => setKopyalandi(false), 2000);
    } catch {
      const secim = window.getSelection();
      const aralik = document.createRange();
      aralik.selectNodeContents(ibanRef.current);
      secim.removeAllRanges();
      secim.addRange(aralik);
    }
  };

  return (
    <>
      <SayfaUst etiket="Birlikte daha güçlüyüz" baslik="Destek Ol"
        aciklama="Bağışlarınız doğrudan Eskilli öğrencilerimizin burslarına dönüşür." />
      <section className="bolum">
        <div className={`kap ${stil.ikiKolon}`}>
          <div>
            <h2>Bir öğrencinin bursunu üstlenin</h2>
            <p>{a.destek_ol_metni}</p>
            <ol className={stil.adimlar}>
              <li><div><strong>Bağışınızı yapın.</strong><br />Yandaki hesap bilgilerine dilediğiniz tutarda havale/EFT yapabilirsiniz.</div></li>
              <li><div><strong>Açıklamaya adınızı yazın.</strong><br />Böylece size teşekkür edebilir, bağışınızı kayda geçirebiliriz.</div></li>
              <li><div><strong>Bursu birlikte planlayalım.</strong><br />Bir öğrencinin yıllık bursunu üstlenmek isterseniz <Link to="/iletisim">bize yazın</Link>.</div></li>
            </ol>
          </div>
          <aside className={stil.ibanKutu}>
            <h2>Hesap bilgileri</h2>
            {a.iban ? (
              <>
                <span className={stil.iban} ref={ibanRef}>{ibanGrupla(a.iban)}</span>
                {a.hesap_sahibi && <p className={stil.ibanBilgi}>Alıcı: {a.hesap_sahibi}</p>}
                {a.banka && <p className={stil.ibanBilgi}>Banka: {a.banka}</p>}
                <button type="button" className="buton buton-ana" style={{ marginTop: 20, width: "100%" }} onClick={kopyala} aria-live="polite">
                  {kopyalandi ? "Kopyalandı" : "IBAN'ı Kopyala"}
                </button>
              </>
            ) : <p className={stil.ibanBilgi}>IBAN bilgisi yakında eklenecek.</p>}
          </aside>
        </div>
      </section>
    </>
  );
}
