import { useAyarlar } from "../api.jsx";
import stil from "./Logo.module.css";

/**
 * Eskilder logosu. Panelden logo yüklenmişse o kullanılır; yoksa repodaki vektör logo.
 * buyuk: açılış ekranı için tam logo (1929 + ESKİLDER yazısıyla).
 */
export default function Logo({ acik = false, buyuk = false }) {
  const ayar = useAyarlar();
  const ad = ayar.kisa_ad || "Eskilder";
  if (ayar.logo) {
    return <img className={`${stil.resim} ${buyuk ? stil.resimBuyuk : ""}`} src={ayar.logo} alt={ad} />;
  }
  if (buyuk) {
    return (
      <span className={stil.tamKutu}>
        <img className={stil.tam} src="/logo.svg" alt={ad} />
      </span>
    );
  }
  return (
    <span className={`${stil.logo} ${acik ? stil.acik : ""}`}>
      <img className={stil.isaret} src="/logo-isaret.svg" alt="" aria-hidden="true" />
      <span className={stil.yazi}>{ad}</span>
    </span>
  );
}
