import { useState } from "react";
import { Link } from "react-router-dom";
import { gonder, useAyarlar } from "../api.jsx";
import { SayfaUst, useBaslik } from "../bilesenler/ortak.jsx";
import stil from "./Iletisim.module.css";

const KONULAR = [["destekci", "Destekçi olmak istiyorum"], ["burs", "Burs hakkında"], ["diger", "Diğer"]];
const BOS = { ad_soyad: "", eposta: "", telefon: "", konu: "", mesaj: "", kvkk_onay: false, web_sitesi: "" };
const EPOSTA = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/** Türkiye numaralarını wa.me biçimine çevirir: yalnız rakam, başında 90. */
export function whatsappLinki(numara) {
  let rakam = (numara || "").replace(/\D/g, "");
  if (rakam.startsWith("0")) rakam = `90${rakam.slice(1)}`;
  else if (rakam.length === 10 && rakam.startsWith("5")) rakam = `90${rakam}`;
  return rakam ? `https://wa.me/${rakam}` : null;
}

function dogrula(f) {
  const h = {};
  if (!f.ad_soyad.trim()) h.ad_soyad = "Ad soyad zorunludur.";
  if (!f.eposta.trim()) h.eposta = "E-posta zorunludur.";
  else if (!EPOSTA.test(f.eposta.trim())) h.eposta = "Geçerli bir e-posta adresi girin.";
  if (!f.konu) h.konu = "Lütfen bir konu seçin.";
  if (!f.mesaj.trim()) h.mesaj = "Mesaj zorunludur.";
  if (!f.kvkk_onay) h.kvkk_onay = "Devam etmek için KVKK aydınlatma metnini onaylamanız gerekir.";
  return h;
}

function Alan({ ad, etiket, hata, children }) {
  return (
    <div className={stil.alan}>
      <label htmlFor={ad}>{etiket}</label>
      {children}
      {hata && <span id={`${ad}-hata`} className={stil.hata}>{hata}</span>}
    </div>
  );
}

export default function Iletisim() {
  const a = useAyarlar();
  const [form, setForm] = useState(BOS);
  const [hatalar, setHatalar] = useState({});
  const [genelHata, setGenelHata] = useState("");
  const [gonderiliyor, setGonderiliyor] = useState(false);
  const [tamam, setTamam] = useState(false);
  useBaslik("İletişim");

  const degistir = (olay) => {
    const { name, type, checked, value } = olay.target;
    setForm((f) => ({ ...f, [name]: type === "checkbox" ? checked : value }));
    setHatalar((h) => ({ ...h, [name]: undefined }));
  };

  const girdi = (ad) => ({
    id: ad, name: ad, value: form[ad], onChange: degistir,
    "aria-invalid": hatalar[ad] ? "true" : undefined,
    "aria-describedby": hatalar[ad] ? `${ad}-hata` : undefined,
  });

  const gonderForm = async (olay) => {
    olay.preventDefault();
    setGenelHata("");
    const istemci = dogrula(form);
    setHatalar(istemci);
    if (Object.keys(istemci).length) return;
    setGonderiliyor(true);
    try {
      const { durum, govde } = await gonder("/iletisim/", form);
      if (durum === 201) {
        setTamam(true);
        setForm(BOS);
      } else if (durum === 400) {
        setHatalar(Object.fromEntries(Object.entries(govde).map(([k, v]) => [k, Array.isArray(v) ? v[0] : String(v)])));
      } else {
        setGenelHata(govde?.hata || "Mesajınız gönderilemedi. Lütfen biraz sonra tekrar deneyin.");
      }
    } catch {
      setGenelHata("Bağlantı kurulamadı. İnternet bağlantınızı kontrol edip tekrar deneyin.");
    } finally {
      setGonderiliyor(false);
    }
  };

  const wa = whatsappLinki(a.whatsapp);

  return (
    <>
      <SayfaUst etiket="Bize ulaşın" baslik="İletişim"
        aciklama="Destekçimiz olmak, burs hakkında bilgi almak ya da sadece merhaba demek için yazın." />
      <section className="bolum">
        <div className={`kap ${stil.izgara}`}>
          <div className={stil.kart}>
            {tamam ? (
              <div className={stil.basari} role="status">
                <span aria-hidden="true">✓</span>
                <h2>Teşekkürler!</h2>
                <p>Mesajınız bize ulaştı. En kısa sürede dönüş yapacağız.</p>
                <button type="button" className="buton buton-cizgi" onClick={() => setTamam(false)}>Yeni mesaj yaz</button>
              </div>
            ) : (
              <form onSubmit={gonderForm} noValidate>
                <h2>Mesaj gönderin</h2>
                {genelHata && <p className={stil.genelHata} role="alert">{genelHata}</p>}
                <div className={stil.ikili}>
                  <Alan ad="ad_soyad" etiket="Ad Soyad" hata={hatalar.ad_soyad}>
                    <input type="text" autoComplete="name" {...girdi("ad_soyad")} />
                  </Alan>
                  <Alan ad="eposta" etiket="E-posta" hata={hatalar.eposta}>
                    <input type="email" autoComplete="email" inputMode="email" {...girdi("eposta")} />
                  </Alan>
                </div>
                <div className={stil.ikili}>
                  <Alan ad="telefon" etiket="Telefon (isteğe bağlı)" hata={hatalar.telefon}>
                    <input type="tel" autoComplete="tel" inputMode="tel" {...girdi("telefon")} />
                  </Alan>
                  <Alan ad="konu" etiket="Konu" hata={hatalar.konu}>
                    <select {...girdi("konu")}>
                      <option value="" disabled>Seçin…</option>
                      {KONULAR.map(([deger, ad]) => <option key={deger} value={deger}>{ad}</option>)}
                    </select>
                  </Alan>
                </div>
                <Alan ad="mesaj" etiket="Mesajınız" hata={hatalar.mesaj}>
                  <textarea rows={6} maxLength={5000} {...girdi("mesaj")} />
                </Alan>
                <div className={stil.tuzak} aria-hidden="true">
                  <label htmlFor="web_sitesi">Web siteniz</label>
                  <input id="web_sitesi" name="web_sitesi" type="text" tabIndex={-1} autoComplete="off" value={form.web_sitesi} onChange={degistir} />
                </div>
                <div className={stil.onay}>
                  <label>
                    <input type="checkbox" name="kvkk_onay" checked={form.kvkk_onay} onChange={degistir}
                      aria-invalid={hatalar.kvkk_onay ? "true" : undefined} aria-describedby={hatalar.kvkk_onay ? "kvkk_onay-hata" : undefined} />
                    <span><Link to="/kvkk" target="_blank">KVKK aydınlatma metnini</Link> okudum, kişisel verilerimin talebime dönüş yapılması amacıyla işlenmesini kabul ediyorum.</span>
                  </label>
                  {hatalar.kvkk_onay && <span id="kvkk_onay-hata" className={stil.hata}>{hatalar.kvkk_onay}</span>}
                </div>
                <button type="submit" className="buton buton-koyu" disabled={gonderiliyor}>
                  {gonderiliyor ? "Gönderiliyor…" : "Mesajı Gönder"}
                </button>
              </form>
            )}
          </div>
          <aside className={stil.yan}>
            <h2>İletişim bilgileri</h2>
            <ul className={stil.bilgiler}>
              {a.telefon && <li><span>Telefon</span><a href={`tel:${a.telefon.replace(/[^\d+]/g, "")}`}>{a.telefon}</a></li>}
              {wa && <li><span>WhatsApp</span><a href={wa} target="_blank" rel="noopener noreferrer" aria-label="WhatsApp ile yazın">WhatsApp ile yazın</a></li>}
              {a.eposta && <li><span>E-posta</span><a href={`mailto:${a.eposta}`}>{a.eposta}</a></li>}
              {a.adres && <li><span>Adres</span>{a.adres}</li>}
            </ul>
            {a.harita_embed_url && (
              <iframe className={stil.harita} src={a.harita_embed_url} title="Dernek konumu" loading="lazy" referrerPolicy="no-referrer-when-downgrade" />
            )}
          </aside>
        </div>
      </section>
    </>
  );
}
