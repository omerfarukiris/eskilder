/* Panelde seçilen görseli göndermeden önce tarayıcıda küçültür (en uzun kenar 1920 px).
   Vercel 4,5 MB istek sınırını aşmamak için. Galeri yükleyicisi de window.eskilderKucult'u kullanır. */
(function () {
  "use strict";
  var EN_UZUN = 1920;
  var UST_SINIR = 4 * 1024 * 1024; // Vercel 4,5 MB istek sınırının altında kal
  var BUYUK_MESAJ = "Bu dosya çok büyük (en fazla 4 MB). Lütfen daha küçük bir dosya seçin; fotoğraflar için JPG veya PNG kullanın.";

  function uyar(girdi, mesaj) {
    var kutu = girdi.parentElement.querySelector("[data-eskilder-uyari]");
    if (!kutu) {
      kutu = document.createElement("p");
      kutu.setAttribute("data-eskilder-uyari", "");
      kutu.setAttribute("role", "alert");
      kutu.style.cssText = "color:#b3261e;font-weight:600;margin:6px 0 0;";
      girdi.parentElement.appendChild(kutu);
    }
    kutu.textContent = mesaj || "";
    kutu.hidden = !mesaj;
  }
  window.eskilderUstSinir = UST_SINIR;
  window.eskilderBuyukMesaj = BUYUK_MESAJ;

  function kucult(dosya) {
    return new Promise(function (coz) {
      if (!dosya.type || dosya.type.indexOf("image/") !== 0 || dosya.type === "image/gif" || dosya.type === "image/svg+xml") {
        return coz(dosya);
      }
      var url = URL.createObjectURL(dosya);
      var img = new Image();
      img.onload = function () {
        URL.revokeObjectURL(url);
        var oran = Math.min(1, EN_UZUN / Math.max(img.naturalWidth, img.naturalHeight));
        if (oran === 1 && dosya.size < 1.5 * 1024 * 1024) return coz(dosya);
        var tuval = document.createElement("canvas");
        tuval.width = Math.round(img.naturalWidth * oran);
        tuval.height = Math.round(img.naturalHeight * oran);
        tuval.getContext("2d").drawImage(img, 0, 0, tuval.width, tuval.height);
        var png = dosya.type === "image/png";
        tuval.toBlob(function (blob) {
          if (!blob) return coz(dosya);
          var ad = dosya.name.replace(/\.[^.]+$/, "") + (png ? ".png" : ".jpg");
          coz(new File([blob], ad, { type: blob.type, lastModified: Date.now() }));
        }, png ? "image/png" : "image/jpeg", 0.85);
      };
      img.onerror = function () { URL.revokeObjectURL(url); coz(dosya); };
      img.src = url;
    });
  }
  window.eskilderKucult = kucult;

  document.addEventListener("change", function (olay) {
    var girdi = olay.target;
    if (!(girdi instanceof HTMLInputElement) || girdi.type !== "file" || girdi.multiple) return;
    if (!girdi.files || !girdi.files.length || girdi.dataset.kucultuldu === "1") return;
    uyar(girdi, "");
    var gorselMi = /image/.test(girdi.accept || "") || /^image\//.test(girdi.files[0].type);
    var islem = gorselMi ? kucult(girdi.files[0]) : Promise.resolve(girdi.files[0]);
    islem.then(function (yeni) {
      if (yeni.size > UST_SINIR) {
        girdi.value = "";
        uyar(girdi, BUYUK_MESAJ);
        return;
      }
      if (yeni === girdi.files[0]) return;
      var aktarim = new DataTransfer();
      aktarim.items.add(yeni);
      girdi.dataset.kucultuldu = "1";
      girdi.files = aktarim.files;
      girdi.dispatchEvent(new Event("change", { bubbles: true }));
      delete girdi.dataset.kucultuldu;
    });
  }, true);
})();
