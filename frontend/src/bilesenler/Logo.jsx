import { useAyarlar } from "../api.jsx";
import stil from "./Logo.module.css";

/**
 * Eskilder logosu: yuvarlak beyaz rozet içinde amblem + yanında/altında yazı.
 * Panelden logo yüklenmişse rozetin içinde o gösterilir.
 * buyuk: açılış ekranı (rozet büyük, yazı altta).
 */
export default function Logo({ acik = false, buyuk = false }) {
  const ayar = useAyarlar();
  const ad = ayar.kisa_ad || "Eskilder";
  const gorsel = ayar.logo || "/logo-isaret.svg";
  return (
    <span className={[stil.logo, acik && stil.acik, buyuk && stil.buyuk].filter(Boolean).join(" ")}>
      <span className={stil.rozet}>
        <img src={gorsel} alt="" aria-hidden="true" />
      </span>
      <span className={stil.yazilar}>
        <span className={stil.ad}>{ad}</span>
        <span className={stil.yil}>1929 · Eskil</span>
      </span>
    </span>
  );
}
