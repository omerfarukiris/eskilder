import { useAyarlar } from "../api.jsx";
import stil from "./Logo.module.css";

/**
 * Eskilder logosu (orijinal logodan sadeleştirilmiş amblem + "ESKİLDER" + 1929).
 * Panelden logo yüklenmişse amblemin yerine o gösterilir.
 * acik: koyu zemin (alt bilgi); buyuk: açılış ekranı.
 */
export default function Logo({ acik = false, buyuk = false }) {
  const ayar = useAyarlar();
  const ad = (ayar.kisa_ad || "Eskilder").toLocaleUpperCase("tr-TR");
  return (
    <span className={[stil.logo, acik && stil.acik, buyuk && stil.buyuk].filter(Boolean).join(" ")}>
      <span className={stil.amblem}>
        <img src={ayar.logo || "/logo-sade.svg"} alt="" aria-hidden="true" />
      </span>
      <span className={stil.yazilar}>
        <span className={stil.ad}>{ad}</span>
        <span className={stil.yil}>1929</span>
      </span>
    </span>
  );
}
